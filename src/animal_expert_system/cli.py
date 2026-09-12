"""Command-line interface for the expert system."""

from __future__ import annotations

import argparse
from typing import Sequence

from .engine import ForwardChainingEngine
from .knowledge_base import load_knowledge_base


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="animal-expert-system",
        description="Rule-based animal identification using forward chaining.",
    )
    parser.add_argument(
        "--features",
        nargs="*",
        type=int,
        default=[],
        help="Observable feature IDs, e.g. --features 1 6 12 13",
    )
    parser.add_argument(
        "--list-features",
        action="store_true",
        help="List observable feature IDs and exit.",
    )
    parser.add_argument(
        "--language",
        choices=("en", "zh", "bilingual"),
        default="bilingual",
        help="Output language.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    kb = load_knowledge_base()

    if args.list_features:
        for concept in kb.observable:
            print(f"{concept.id:>2}: {kb.format_concept(concept.id, args.language)}")
        return 0

    if not args.features:
        _parser().print_help()
        return 0

    try:
        result = ForwardChainingEngine(kb).infer(args.features)
    except ValueError as exc:
        print(f"Error: {exc}")
        return 2

    print("Initial facts:")
    for fact in sorted(result.initial_facts):
        print(f"  - {fact}: {kb.format_concept(fact, args.language)}")

    print("\nInference trace:")
    if not result.steps:
        print("  (no rule fired)")
    for step in result.steps:
        premises = ", ".join(kb.format_concept(x, args.language) for x in step.premises)
        conclusion = kb.format_concept(step.conclusion, args.language)
        print(f"  {step.rule_id}: IF {premises} THEN {conclusion}")

    print("\nResult:")
    if result.animals:
        for animal in result.animals:
            print(f"  -> {kb.format_concept(animal, args.language)}")
    else:
        print("  -> No animal can be identified from the supplied facts.")
    return 0
