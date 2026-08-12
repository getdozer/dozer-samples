"""Command-line entry point for deterministic and Dozer-backed runs."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from .advisor import GroundedCardAdvisor
from .explainer import LangChainCardExplainer
from .gateway import DozerGateway, FixtureGateway
from .vector_search import ChromaLangChainSearch, DeterministicVectorSearch


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Grounded card-product advisor")
    parser.add_argument("--customer-id", required=True)
    parser.add_argument("--query")
    parser.add_argument("--gateway", choices=("fixture", "dozer"), default="fixture")
    parser.add_argument("--search", choices=("local", "chroma"), default="local")
    parser.add_argument("--dozer-url", default="http://localhost:8080")
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--chat", action="store_true", help="read queries until 'quit' or EOF")
    parser.add_argument(
        "--llm",
        action="store_true",
        help="use LangChain for a top-result explanation when OPENAI_API_KEY is set",
    )
    parser.add_argument("--llm-model", default="gpt-4o-mini")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    return parser


def _build_advisor(args: argparse.Namespace) -> GroundedCardAdvisor:
    root = Path(__file__).resolve().parents[1]
    gateway = (
        FixtureGateway(root / "data")
        if args.gateway == "fixture"
        else DozerGateway(args.dozer_url)
    )
    search = DeterministicVectorSearch() if args.search == "local" else ChromaLangChainSearch()
    explainer = None
    if args.llm and os.environ.get("OPENAI_API_KEY"):
        explainer = LangChainCardExplainer(args.llm_model)
    return GroundedCardAdvisor(gateway, search, explainer)


def _emit(advisor: GroundedCardAdvisor, args: argparse.Namespace, query: str) -> int:
    try:
        result = advisor.recommend(args.customer_id, query, limit=args.limit)
    except (ValueError, LookupError, RuntimeError) as exc:
        error = {"error": type(exc).__name__, "message": str(exc)}
        print(json.dumps(error, sort_keys=True) if args.json else f"Error: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"Recommendations for {result['customer_id']}:")
        for index, item in enumerate(result["recommendations"], start=1):
            print(f"{index}. {item['product_name']}: {item['reason']}")
            if "llm_explanation" in item:
                print(f"   LLM explanation: {item['llm_explanation']}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.chat and not args.query:
        parser.error("--query is required unless --chat is used")
    try:
        advisor = _build_advisor(args)
    except (ValueError, LookupError, RuntimeError) as exc:
        error = {"error": type(exc).__name__, "message": str(exc)}
        print(json.dumps(error, sort_keys=True) if args.json else f"Error: {exc}", file=sys.stderr)
        return 2
    if not args.chat:
        return _emit(advisor, args, args.query)

    if args.query and _emit(advisor, args, args.query) != 0:
        return 2
    while True:
        try:
            query = input("card-advisor> ").strip()
        except EOFError:
            return 0
        if query.lower() in {"quit", "exit"}:
            return 0
        if query and _emit(advisor, args, query) != 0:
            continue


if __name__ == "__main__":
    raise SystemExit(main())
