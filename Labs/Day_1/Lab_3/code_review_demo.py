import argparse
import os
from pathlib import Path

from openai import OpenAI

from code_review_template import build_code_review_prompt


DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1")


def load_code(file_path: str | None, inline_code: str | None) -> str:
    if file_path:
        return Path(file_path).read_text(encoding="utf-8")
    if inline_code:
        return inline_code
    raise ValueError("Provide either --file or --code.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Review Python code using a self-reflecting code review prompt via the OpenAI-compatible API."
        )
    )
    parser.add_argument(
        "--file",
        "-f",
        help="Path to the Python file to review.",
    )
    parser.add_argument(
        "--code",
        "-c",
        help="Inline Python code to review.",
    )
    parser.add_argument(
        "--model",
        "-m",
        default=DEFAULT_MODEL,
        help="Model to use (default: OPENAI_MODEL env var or gpt-4.1).",
    )
    args = parser.parse_args()

    if bool(args.file) == bool(args.code):
        parser.error("Provide exactly one of --file or --code.")

    code = load_code(args.file, args.code)
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )

    user_input = (
        "Review the following Python code.\n\n"
        "Assumptions:\n"
        "- The code should be treated as a standalone Python snippet unless the code itself implies otherwise.\n"
        "- If a fix depends on missing requirements, state that explicitly.\n\n"
        "Python code:\n"
        "```python\n"
        f"{code}\n"
        "```"
    )

    response = client.responses.create(
        model=args.model,
        max_output_tokens=2200,
        input=[
            {"role": "system", "content": build_code_review_prompt()},
            {"role": "user", "content": user_input},
        ],
    )

    print(response.output_text)


if __name__ == "__main__":
    main()
