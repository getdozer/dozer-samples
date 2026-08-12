"""Deterministic local vector search with an opt-in Chroma adapter."""

from __future__ import annotations

import hashlib
import math
import re
from dataclasses import dataclass
from typing import Iterable, Protocol

from .models import CardProduct


@dataclass(frozen=True)
class SearchHit:
    product: CardProduct
    score: float


class ProductSearch(Protocol):
    def rank(self, query: str, products: Iterable[CardProduct]) -> list[SearchHit]: ...


class DeterministicVectorSearch:
    """Dependency-free feature hashing and cosine similarity."""

    def __init__(self, dimensions: int = 256) -> None:
        if dimensions < 8:
            raise ValueError("dimensions must be at least 8")
        self.dimensions = dimensions

    def _vector(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions
        for token in re.findall(r"[a-z0-9]+", text.lower()):
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % self.dimensions
            sign = 1.0 if digest[4] & 1 else -1.0
            vector[index] += sign
        norm = math.sqrt(sum(value * value for value in vector))
        return [value / norm for value in vector] if norm else vector

    def rank(self, query: str, products: Iterable[CardProduct]) -> list[SearchHit]:
        query_vector = self._vector(query)
        hits = []
        for product in products:
            product_vector = self._vector(product.search_text())
            similarity = sum(a * b for a, b in zip(query_vector, product_vector))
            hits.append(SearchHit(product, similarity))
        return sorted(hits, key=lambda hit: (-hit.score, hit.product.product_id))


class ChromaLangChainSearch:
    """Optional in-memory LangChain/Chroma path; imports only when selected."""

    def __init__(self) -> None:
        try:
            from langchain_chroma import Chroma
        except ImportError as exc:
            raise RuntimeError(
                "Chroma search requires optional packages from requirements-chroma.txt"
            ) from exc
        self._chroma_type = Chroma
        self._embeddings = _FeatureHashEmbeddings()

    def rank(self, query: str, products: Iterable[CardProduct]) -> list[SearchHit]:
        materialized = list(products)
        if not materialized:
            return []
        store = self._chroma_type.from_texts(
            [product.search_text() for product in materialized],
            embedding=self._embeddings,
            metadatas=[{"index": index} for index in range(len(materialized))],
        )
        results = store.similarity_search_with_relevance_scores(query, k=len(materialized))
        return [
            SearchHit(materialized[int(document.metadata["index"])], float(score))
            for document, score in results
        ]


class _FeatureHashEmbeddings:
    """LangChain embedding contract backed by the reproducible local encoder."""

    def __init__(self, dimensions: int = 256) -> None:
        self._search = DeterministicVectorSearch(dimensions)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._search._vector(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._search._vector(text)
