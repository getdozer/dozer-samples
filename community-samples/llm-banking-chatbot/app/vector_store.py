"""Local cosine similarity vector store for credit card product matching."""

from __future__ import annotations

import hashlib
import math
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple
import numpy as np


_TOKEN_RE = re.compile(r"[a-z0-9]+")

# Domain synonym clusters so semantically related banking terms align in local embeddings.
_DOMAIN_CLUSTERS: Dict[str, Tuple[str, ...]] = {
    "travel": ("travel", "airline", "airlines", "flight", "flights", "hotel", "hotels", "lounge", "miles", "international", "airport", "flyer", "trip"),
    "groceries": ("grocery", "groceries", "supermarket", "supermarkets", "household", "cashback", "everyday", "fuel", "utilities", "family", "families"),
    "online_shopping": ("online", "shopping", "ecommerce", "digital", "warranty", "purchase", "protection", "amazon", "retail"),
    "dining": ("dining", "restaurant", "restaurants", "cafe", "cafes", "food", "foodie", "foodies", "gourmet", "grill"),
    "starter": ("starter", "secured", "student", "students", "newcomer", "newcomers", "building", "credit", "entertainment", "streaming", "spotify", "steam"),
    "fee_sensitive": ("zero", "free", "no", "low", "fee", "cashback"),
}


def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """Compute cosine similarity between two 1-D NumPy vectors."""
    norm_a = float(np.linalg.norm(vec_a))
    norm_b = float(np.linalg.norm(vec_b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    score = float(np.dot(vec_a, vec_b) / (norm_a * norm_b))
    return max(-1.0, min(1.0, score))


class LocalTextEmbedder:
    """Deterministic, zero-dependency local text embedder with banking domain features."""

    def __init__(self, dimensions: int = 128) -> None:
        if dimensions < 16:
            raise ValueError("dimensions must be at least 16")
        self.dimensions = dimensions
        self._cluster_names = list(_DOMAIN_CLUSTERS.keys())

    def embed(self, text: str) -> np.ndarray:
        """Convert text into an L2-normalized dense vector."""
        vec = np.zeros(self.dimensions, dtype=np.float32)
        tokens = _TOKEN_RE.findall(text.lower())
        if not tokens:
            return vec

        # Reserve first len(_cluster_names) slots for domain-semantic clusters (high weight).
        cluster_offset = len(self._cluster_names)
        hash_dims = self.dimensions - cluster_offset

        for idx, cluster_name in enumerate(self._cluster_names):
            keywords = _DOMAIN_CLUSTERS[cluster_name]
            hits = sum(1 for tok in tokens if tok in keywords)
            if hits > 0:
                vec[idx] += 2.0 * math.sqrt(hits)

        # Add unigram + bigram hashed features in the remaining dimensions.
        ngrams = list(tokens) + [f"{tokens[i]}_{tokens[i + 1]}" for i in range(len(tokens) - 1)]
        for gram in ngrams:
            digest = hashlib.blake2b(gram.encode("utf-8"), digest_size=8).digest()
            raw = int.from_bytes(digest, "little")
            bucket = cluster_offset + (raw % hash_dims)
            sign = 1.0 if ((raw >> 63) & 1) == 0 else -1.0
            vec[bucket] += sign

        norm = float(np.linalg.norm(vec))
        if norm > 0.0:
            vec /= norm
        return vec


@dataclass(frozen=True)
class CardMatch:
    """Ranked credit card recommendation with similarity score and eligibility info."""

    card: Dict[str, Any]
    similarity_score: float
    eligible: bool
    eligibility_reasons: List[str]


class CreditCardVectorStore:
    """In-memory vector store indexing credit card products for cosine-similarity search."""

    def __init__(self, embedder: Optional[LocalTextEmbedder] = None) -> None:
        self.embedder = embedder or LocalTextEmbedder()
        self._cards: List[Dict[str, Any]] = []
        self._vectors: List[np.ndarray] = []

    @property
    def size(self) -> int:
        return len(self._cards)

    def index_cards(self, cards: List[Dict[str, Any]]) -> None:
        """Index a list of credit card records into the local vector store."""
        self._cards = [dict(card) for card in cards]
        self._vectors = [self.embedder.embed(self._card_to_document(card)) for card in self._cards]

    def search(
        self,
        query_text: str,
        customer_profile: Optional[Dict[str, Any]] = None,
        top_k: int = 3,
        enforce_eligibility: bool = True,
    ) -> List[CardMatch]:
        """Find top-k matching credit cards using cosine similarity and optional eligibility filtering."""
        if not self._cards:
            return []

        enriched_query = self._build_enriched_query(query_text, customer_profile)
        query_vec = self.embedder.embed(enriched_query)

        matches: List[CardMatch] = []
        for card, card_vec in zip(self._cards, self._vectors):
            sim = cosine_similarity(query_vec, card_vec)
            eligible, reasons = self._check_eligibility(card, customer_profile)
            if enforce_eligibility and not eligible:
                continue
            matches.append(
                CardMatch(
                    card=card,
                    similarity_score=round(sim, 4),
                    eligible=eligible,
                    eligibility_reasons=reasons,
                )
            )

        matches.sort(key=lambda m: m.similarity_score, reverse=True)
        return matches[:top_k]

    @staticmethod
    def _card_to_document(card: Dict[str, Any]) -> str:
        fee = float(card.get("annual_fee", 0))
        fee_phrase = "no annual fee zero fee free" if fee == 0 else f"annual fee {fee}"
        return " ".join(
            [
                str(card.get("card_name", "")),
                str(card.get("primary_category", "")),
                str(card.get("benefits_summary", "")),
                str(card.get("target_persona", "")),
                fee_phrase,
            ]
        )

    @staticmethod
    def _build_enriched_query(query_text: str, customer_profile: Optional[Dict[str, Any]]) -> str:
        if not customer_profile:
            return query_text
        top_cat = customer_profile.get("top_category", "")
        segment = customer_profile.get("segment", "")
        return f"{query_text} {top_cat} {segment}".strip()

    @staticmethod
    def _check_eligibility(
        card: Dict[str, Any],
        customer_profile: Optional[Dict[str, Any]],
    ) -> Tuple[bool, List[str]]:
        if not customer_profile:
            return True, ["No customer profile provided; eligibility not restricted."]

        reasons: List[str] = []
        credit_score = int(customer_profile.get("credit_score", 0))
        annual_income = float(customer_profile.get("annual_income", 0.0))
        min_score = int(card.get("min_credit_score", 0))
        min_income = float(card.get("min_income", 0.0))

        if credit_score < min_score:
            reasons.append(f"Credit score {credit_score} is below minimum {min_score}.")
        if annual_income < min_income:
            reasons.append(f"Annual income {annual_income:.0f} is below minimum {min_income:.0f}.")

        if not reasons:
            return True, ["Meets credit score and income requirements."]
        return False, reasons
