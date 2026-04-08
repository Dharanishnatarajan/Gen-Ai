import argparse
import sys
from pathlib import Path

from prompt_template import build_react_agent_prompt

sys.path.append(str(Path(__file__).resolve().parents[1] / "lab2"))
from cot_math_template import build_cot_math_prompt


def main():
    parser = argparse.ArgumentParser(
        description="Generate agent prompts for grounded reasoning and math Chain-of-Thought."
    )
    template_group = parser.add_mutually_exclusive_group()
    template_group.add_argument(
        "--react",
        action="store_true",
        help="Generate the ReAct-style prompt (default).",
    )
    template_group.add_argument(
        "--cot-math",
        action="store_true",
        help="Generate the Chain-of-Thought math prompt.",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Write the generated prompt to a file instead of printing it.",
    )
    args = parser.parse_args()

    if args.cot_math:
        prompt = build_cot_math_prompt()
    else:
        prompt = build_react_agent_prompt()

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(prompt)
        print(f"Prompt saved to {args.output}")
    else:
        print(prompt)


if __name__ == "__main__":
    main()
