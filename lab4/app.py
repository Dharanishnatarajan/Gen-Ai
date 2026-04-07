import argparse

from customer_support_prompts import (
    build_react_support_prompt,
    build_self_reflection_support_prompt,
    build_structured_output_support_prompt,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Print production-ready customer support chatbot prompts."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--react",
        action="store_true",
        help="Print the ReAct customer support prompt.",
    )
    group.add_argument(
        "--self-reflection",
        action="store_true",
        help="Print the self-reflection customer support prompt.",
    )
    group.add_argument(
        "--structured-output",
        action="store_true",
        help="Print the structured-output customer support prompt.",
    )
    args = parser.parse_args()

    if args.self_reflection:
        prompt = build_self_reflection_support_prompt()
    elif args.structured_output:
        prompt = build_structured_output_support_prompt()
    else:
        prompt = build_react_support_prompt()

    print(prompt)


if __name__ == "__main__":
    main()
