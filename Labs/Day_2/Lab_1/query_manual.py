import argparse
import os

from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


DEFAULT_COLLECTION = "product_manual"
DEFAULT_PERSIST_DIR = "day2_lab1/chroma_store"
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def build_embeddings(model: str) -> OpenAIEmbeddings:
    return OpenAIEmbeddings(
        model=model,
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Query a ChromaDB product manual index and answer with grounded context."
    )
    parser.add_argument(
        "--question",
        "-q",
        required=True,
        help="Question to ask about the indexed manual.",
    )
    parser.add_argument(
        "--persist-dir",
        default=DEFAULT_PERSIST_DIR,
        help=f"Directory where the ChromaDB index is stored (default: {DEFAULT_PERSIST_DIR}).",
    )
    parser.add_argument(
        "--collection",
        default=DEFAULT_COLLECTION,
        help=f"Chroma collection name (default: {DEFAULT_COLLECTION}).",
    )
    parser.add_argument(
        "--embedding-model",
        default=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
        help="Embedding model to use for retrieval.",
    )
    parser.add_argument(
        "--model",
        "-m",
        default=DEFAULT_MODEL,
        help=f"Chat model to use (default: OPENAI_MODEL or {DEFAULT_MODEL}).",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=4,
        help="Number of retrieved chunks to use (default: 4).",
    )
    args = parser.parse_args()

    vector_store = Chroma(
        collection_name=args.collection,
        persist_directory=args.persist_dir,
        embedding_function=build_embeddings(args.embedding_model),
    )
    docs = vector_store.similarity_search(args.question, k=args.top_k)
    if not docs:
        raise ValueError("No relevant documents were found in the index.")

    context = "\n\n".join(
        [
            f"Source chunk {index + 1} (page {doc.metadata.get('page', 'unknown')}):\n{doc.page_content}"
            for index, doc in enumerate(docs)
        ]
    )

    prompt = (
        "You are a careful product support assistant. Answer the user's question using only the "
        "retrieved manual context. If the context is insufficient, say that clearly instead of guessing.\n\n"
        f"Question: {args.question}\n\n"
        f"Context:\n{context}\n\n"
        "Answer with:\n"
        "1. A concise answer\n"
        "2. Supporting evidence from the manual\n"
        "3. Any uncertainty or missing context"
    )

    llm = ChatOpenAI(
        model=args.model,
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )
    response = llm.invoke(prompt)
    print(response.content)


if __name__ == "__main__":
    main()
