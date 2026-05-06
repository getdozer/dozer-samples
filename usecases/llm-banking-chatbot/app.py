from __future__ import annotations

import argparse
import os

from banking_assistant.clients import DozerRestClient, FixtureClient
from banking_assistant.recommender import build_grounded_answer


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Dozer + LangChain banking assistant sample")
    parser.add_argument("--customer-id", default="1001", help="Customer id to personalize against")
    parser.add_argument("--question", required=True, help="Question to answer")
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Use local CSV fixtures instead of the Dozer REST API",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    client = FixtureClient.from_default_data_dir() if args.offline else DozerRestClient(
        os.environ.get("DOZER_REST_URL", "http://localhost:8080"),
    )
    answer = build_grounded_answer(client, customer_id=args.customer_id, question=args.question)
    print(answer)


if __name__ == "__main__":
    main()

