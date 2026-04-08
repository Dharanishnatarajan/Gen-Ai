import argparse
import os

from openai import OpenAI
from cot_math_template import build_cot_math_prompt


def main():
    parser = argparse.ArgumentParser(
        description="Solve multi-step math problems using a Chain-of-Thought prompt via the OpenAI API."
    )
    parser.add_argument(
        "--problem",
        "-p",
        default="If a train travels 180 miles in 3 hours, what is its average speed in miles per hour?",
        help="The math problem to solve.",
    )
    parser.add_argument(
        "--model",
        "-m",
        default=os.getenv("OPENAI_MODEL", "gpt-4.1"),
        help="OpenAI model to use (default: OPENAI_MODEL env var or gpt-4.1).",
    )
    args = parser.parse_args()

    client = OpenAI()
    prompt = build_cot_math_prompt()

    response = client.responses.create(
        model=args.model,
        input=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": args.problem},
        ],
    )

    print(response.output_text)


if __name__ == "__main__":
    main()
