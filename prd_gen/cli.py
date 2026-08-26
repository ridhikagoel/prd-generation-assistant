import argparse
import sys
from pathlib import Path

from prd_gen.pipeline import MODEL, check_gaps, draft_prd

UNANSWERED = "(not answered — proceed with your best-supported assumption and flag it explicitly)"


def run(idea: str, model: str, auto: bool, output: str | None):
    print("--- Step 1: checking for blocking gaps ---", file=sys.stderr)
    gaps = check_gaps(idea, model)

    qa_pairs = []
    if gaps["questions"]:
        print(f"\n{len(gaps['questions'])} clarifying question(s) before drafting:\n", file=sys.stderr)
        for q in gaps["questions"]:
            print(f"  - {q}", file=sys.stderr)
        print(file=sys.stderr)

        if auto:
            print("(--auto set: proceeding without answers, will be flagged as assumptions)\n", file=sys.stderr)
            qa_pairs = [(q, UNANSWERED) for q in gaps["questions"]]
        else:
            for q in gaps["questions"]:
                answer = input(f"{q}\n> ").strip()
                qa_pairs.append((q, answer if answer else UNANSWERED))
    else:
        print("No blocking gaps found — drafting directly.\n", file=sys.stderr)

    print("--- Step 2: drafting PRD ---", file=sys.stderr)
    prd = draft_prd(idea, qa_pairs, model)

    if output:
        Path(output).write_text(prd)
        print(f"\nWrote PRD to {output}", file=sys.stderr)
    else:
        print(prd)

    return prd


def main():
    parser = argparse.ArgumentParser(description="PRD generation assistant")
    sub = parser.add_subparsers(dest="command", required=True)

    p_gen = sub.add_parser("generate", help="Generate a PRD from a feature idea")
    src = p_gen.add_mutually_exclusive_group(required=True)
    src.add_argument("--idea", help="Feature idea as a string")
    src.add_argument("--idea-file", help="Path to a file containing the feature idea")
    p_gen.add_argument("--model", default=MODEL)
    p_gen.add_argument("--auto", action="store_true", help="Don't prompt interactively for answers")
    p_gen.add_argument("--output", help="Write the PRD to this file instead of stdout")

    args = parser.parse_args()

    if args.command == "generate":
        idea = args.idea if args.idea else Path(args.idea_file).read_text()
        run(idea, args.model, args.auto, args.output)


if __name__ == "__main__":
    main()
