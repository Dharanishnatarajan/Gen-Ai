import argparse
import os
from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


DEFAULT_COLLECTION = "product_manual"
DEFAULT_PERSIST_DIR = "day2_lab1/chroma_store"


def build_embeddings(model: str) -> OpenAIEmbeddings:
    return OpenAIEmbeddings(
        model=model,
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Index a PDF product manual into ChromaDB using LangChain."
    )
    parser.add_argument(
        "--pdf",
        required=True,
        help="Path to the product manual PDF.",
    )
    parser.add_argument(
        "--persist-dir",
        default=DEFAULT_PERSIST_DIR,
        help=f"Directory where the ChromaDB index will be stored (default: {DEFAULT_PERSIST_DIR}).",
    )
    parser.add_argument(
        "--collection",
        default=DEFAULT_COLLECTION,
        help=f"Chroma collection name (default: {DEFAULT_COLLECTION}).",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=1000,
        help="Chunk size for recursive text splitting (default: 1000).",
    )
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=200,
        help="Chunk overlap for recursive text splitting (default: 200).",
    )
    parser.add_argument(
        "--embedding-model",
        default=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
        help="Embedding model to use (default: OPENAI_EMBEDDING_MODEL or text-embedding-3-small).",
    )
    args = parser.parse_args()

    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    loader = PyPDFLoader(str(pdf_path))
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
    )
    chunks = splitter.split_documents(documents)
    if not chunks:
        raise ValueError("No chunks were created from the PDF.")

    persist_dir = Path(args.persist_dir)
    persist_dir.mkdir(parents=True, exist_ok=True)

    vector_store = Chroma(
        collection_name=args.collection,
        persist_directory=str(persist_dir),
        embedding_function=build_embeddings(args.embedding_model),
    )
    vector_store.add_documents(chunks)

    print(f"Indexed {len(documents)} pages into {len(chunks)} chunks.")
    print(f"Collection: {args.collection}")
    print(f"Persisted to: {persist_dir.resolve()}")


if __name__ == "__main__":
    main()
