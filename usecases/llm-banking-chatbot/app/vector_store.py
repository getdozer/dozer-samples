#!/usr/bin/env python3
"""Vector Database Indexer and Semantic Retriever for Credit Card Products.

Supports:
1. ChromaDB (`chromadb` / `langchain_community.vectorstores.Chroma`) when installed.
2. Built-in deterministic semantic concept + character n-gram embedding engine
   (`DeterministicBankingEmbeddings` + `CardProductVectorStore`) that executes cosine
   similarity search without requiring external API keys or network calls.
"""

from __future__ import annotations

import csv
import math
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union


@dataclass
class CardProductDocument:
    """Credit card product brochure document stored in the Vector Database."""

    product_id: str
    card_name: str
    target_segment: str
    min_credit_score: int
    min_annual_income: float
    annual_fee: float
    apr_range: str
    signup_bonus: str
    primary_rewards: str
    foreign_tx_fee_pct: float
    description: str

    @property
    def page_content(self) -> str:
        return (
            f"{self.card_name} ({self.product_id}) - Segment: {self.target_segment}. "
            f"Primary Rewards: {self.primary_rewards}. "
            f"Sign-up Bonus: {self.signup_bonus}. "
            f"Annual Fee: ${self.annual_fee:.0f}, APR: {self.apr_range}, "
            f"Foreign Transaction Fee: {self.foreign_tx_fee_pct}%. "
            f"Eligibility: Min Credit Score {self.min_credit_score}, Min Income ${self.min_annual_income:,.0f}. "
            f"Details: {self.description}"
        )

    @property
    def metadata(self) -> Dict[str, Any]:
        return asdict(self)


class DeterministicBankingEmbeddings:
    """Deterministic domain-aware semantic embedding function compatible with LangChain & ChromaDB."""

    DOMAIN_CONCEPTS: List[Tuple[str, List[str], float]] = [
        ("travel_airlines_hotels", ["travel", "flight", "airline", "hotel", "lounge", "airport", "international", "miles", "foreign", "trip", "vacation", "flyer"], 3.2),
        ("dining_restaurants", ["dining", "restaurant", "food", "eat", "dinner", "cafe", "culinary"], 2.8),
        ("groceries_supermarket_fuel", ["grocery", "groceries", "supermarket", "wholesale", "costco", "kroger", "fuel", "gas", "station", "household", "family", "everyday"], 3.2),
        ("cashback_rewards", ["cashback", "cash", "back", "percent", "savings", "no annual fee", "$0 annual fee"], 2.4),
        ("student_starter_credit", ["student", "campus", "college", "starter", "build credit", "fico", "young", "bookstore", "streaming"], 3.2),
        ("balance_transfer_low_apr", ["balance", "transfer", "apr", "interest", "debt", "consolidation", "utilization", "payoff", "0%", "shield", "high balance"], 3.4),
        ("business_cloud_founder", ["business", "founder", "self-employed", "cloud", "aws", "saas", "software", "coworking", "online_shopping", "online shopping", "consultant"], 3.2),
    ]

    def __init__(self, ngram_buckets: int = 64) -> None:
        self.ngram_buckets = ngram_buckets

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"[a-z0-9%_]+", text.lower())

    def embed_query(self, text: str) -> List[float]:
        lower_text = text.lower()
        tokens = set(self._tokenize(lower_text))
        vec: List[float] = []

        # 1. Domain semantic concept dimensions
        for _, keywords, weight in self.DOMAIN_CONCEPTS:
            hits = 0.0
            for kw in keywords:
                if " " in kw:
                    if kw in lower_text:
                        hits += 1.5
                elif kw in tokens or any(tok.startswith(kw[:5]) for tok in tokens if len(kw) >= 5):
                    hits += 1.0
            vec.append(hits * weight)

        # 2. Hashed character 3-gram dimensions for lexical nuance
        buckets = [0.0] * self.ngram_buckets
        cleaned = re.sub(r"\s+", " ", lower_text)
        for i in range(max(0, len(cleaned) - 2)):
            trigram = cleaned[i : i + 3]
            h = sum((idx + 1) * ord(ch) for idx, ch in enumerate(trigram)) % self.ngram_buckets
            buckets[h] += 0.15
        vec.extend(buckets)

        # L2 normalize
        norm = math.sqrt(sum(x * x for x in vec)) or 1.0
        return [x / norm for x in vec]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_query(t) for t in texts]

    def __call__(self, input: List[str]) -> List[List[float]]:
        """ChromaDB EmbeddingFunction protocol compatibility."""
        return self.embed_documents(input)


def _cosine_similarity(v1: List[float], v2: List[float]) -> float:
    return sum(a * b for a, b in zip(v1, v2))


class CardProductVectorStore:
    """Vector Database indexing credit card brochures with ChromaDB & deterministic cosine retrieval."""

    def __init__(
        self,
        csv_path: Union[str, Path],
        embedding_fn: Optional[DeterministicBankingEmbeddings] = None,
        use_chroma_if_available: bool = True,
    ) -> None:
        self.csv_path = Path(csv_path)
        self.embedding_fn = embedding_fn or DeterministicBankingEmbeddings()
        self.documents: List[CardProductDocument] = self._load_catalog()
        self.vectors: List[List[float]] = self.embedding_fn.embed_documents(
            [doc.page_content for doc in self.documents]
        )
        self.backend_name = "deterministic_in_memory_vector_store"
        self._chroma_collection = None

        if use_chroma_if_available:
            try:
                import chromadb

                client = chromadb.EphemeralClient()
                collection = client.get_or_create_collection(name="dozer_credit_cards")
                collection.upsert(
                    ids=[d.product_id for d in self.documents],
                    embeddings=self.vectors,
                    documents=[d.page_content for d in self.documents],
                    metadatas=[d.metadata for d in self.documents],
                )
                self._chroma_collection = collection
                self.backend_name = "chromadb_ephemeral"
            except Exception:
                self._chroma_collection = None

    def _load_catalog(self) -> List[CardProductDocument]:
        docs: List[CardProductDocument] = []
        with self.csv_path.open("r", encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                docs.append(
                    CardProductDocument(
                        product_id=row["product_id"].strip(),
                        card_name=row["card_name"].strip(),
                        target_segment=row["target_segment"].strip(),
                        min_credit_score=int(row["min_credit_score"]),
                        min_annual_income=float(row["min_annual_income"]),
                        annual_fee=float(row["annual_fee"]),
                        apr_range=row["apr_range"].strip(),
                        signup_bonus=row["signup_bonus"].strip(),
                        primary_rewards=row["primary_rewards"].strip(),
                        foreign_tx_fee_pct=float(row["foreign_tx_fee_pct"]),
                        description=row["description"].strip(),
                    )
                )
        return docs

    def similarity_search_with_score(
        self,
        query: str,
        k: int = 3,
        customer_profile: Optional[Any] = None,
    ) -> List[Tuple[CardProductDocument, float]]:
        """Retrieve top-k credit card products ranked by semantic similarity and profile context."""
        augmented_query = query
        if customer_profile is not None:
            top_list = customer_profile.top_spending_categories
            primary_cat = (top_list[0][0] + " " + top_list[0][0]) if top_list else ""
            secondary_cat = top_list[1][0] if len(top_list) > 1 else ""
            util_hint = (
                "balance transfer low apr debt consolidation high utilization"
                if customer_profile.utilization_pct >= 50.0
                else ""
            )
            emp_hint = customer_profile.employment_status.lower()
            pref_hint = customer_profile.preferred_reward_type.replace("_", " ")
            augmented_query = f"{query} {primary_cat} {secondary_cat} {pref_hint} {emp_hint} {util_hint}".strip()

        q_vec = self.embedding_fn.embed_query(augmented_query)
        scored: List[Tuple[CardProductDocument, float]] = []
        for doc, d_vec in zip(self.documents, self.vectors):
            sim = _cosine_similarity(q_vec, d_vec)
            if customer_profile is not None:
                eligible = (
                    customer_profile.credit_score >= doc.min_credit_score
                    and customer_profile.annual_income >= doc.min_annual_income
                )
                if eligible:
                    sim += 0.12
                else:
                    sim -= 0.25
            scored.append((doc, round(sim, 4)))

        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[:k]

    def as_retriever(self, search_kwargs: Optional[Dict[str, Any]] = None) -> "CardProductRetriever":
        """Return a LangChain-compatible Retriever object."""
        k = (search_kwargs or {}).get("k", 3)
        return CardProductRetriever(vector_store=self, k=k)


class CardProductRetriever:
    """LangChain-compatible retriever interface (`invoke` / `get_relevant_documents`)."""

    def __init__(self, vector_store: CardProductVectorStore, k: int = 3) -> None:
        self.vector_store = vector_store
        self.k = k

    def get_relevant_documents(
        self, query: str, customer_profile: Optional[Any] = None
    ) -> List[CardProductDocument]:
        hits = self.vector_store.similarity_search_with_score(
            query=query, k=self.k, customer_profile=customer_profile
        )
        return [doc for doc, _ in hits]

    def invoke(self, query: str) -> List[CardProductDocument]:
        return self.get_relevant_documents(query)
