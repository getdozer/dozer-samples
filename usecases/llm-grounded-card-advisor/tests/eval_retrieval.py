"""Small deterministic ranking evaluation with explicit expected products."""

from __future__ import annotations

import json
from pathlib import Path

from app.gateway import FixtureGateway
from app.vector_search import DeterministicVectorSearch


CASES = (
    ("airport flights hotels travel", "CARD-TRAVEL"),
    ("Everyday Cash groceries daily purchases", "CARD-CASH"),
    ("Premium Reserve premium travel", "CARD-PREMIUM"),
    ("Credit Builder credit history", "CARD-BUILDER"),
    ("Select Cashback flexible cashback", "CARD-SELECT"),
)


def evaluate() -> dict[str, float | int]:
    root = Path(__file__).resolve().parents[1]
    products = FixtureGateway(root / "data").list_card_products()
    search = DeterministicVectorSearch()
    reciprocal_ranks = []
    hits_at_three = 0
    for query, expected in CASES:
        ranking = [hit.product.product_id for hit in search.rank(query, products)]
        rank = ranking.index(expected) + 1
        reciprocal_ranks.append(1 / rank)
        hits_at_three += int(rank <= 3)
    return {
        "cases": len(CASES),
        "hit_rate_at_3": hits_at_three / len(CASES),
        "mean_reciprocal_rank": sum(reciprocal_ranks) / len(CASES),
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
