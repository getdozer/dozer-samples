from __future__ import annotations

import math
import re
from collections import Counter
from typing import Iterable


def retrieve_relevant_documents(question: str, documents: list[str], top_k: int = 3) -> list[str]:
    try:
        return retrieve_with_langchain_chroma(question, documents, top_k)
    except Exception:
        return lexical_retrieve(question, documents, top_k)


def retrieve_with_langchain_chroma(question: str, documents: list[str], top_k: int) -> list[str]:
    from langchain_community.vectorstores import Chroma
    from langchain_core.documents import Document
    from langchain_core.embeddings import Embeddings

    class HashEmbeddings(Embeddings):
        def embed_documents(self, texts: list[str]) -> list[list[float]]:
            return [hash_embedding(text) for text in texts]

        def embed_query(self, text: str) -> list[float]:
            return hash_embedding(text)

    vector_store = Chroma.from_documents(
        [Document(page_content=document) for document in documents],
        embedding=HashEmbeddings(),
        collection_name="banking_chatbot_sample",
    )
    return [doc.page_content for doc in vector_store.similarity_search(question, k=top_k)]


def lexical_retrieve(question: str, documents: list[str], top_k: int) -> list[str]:
    query = token_counts(question)
    ranked = sorted(
        documents,
        key=lambda document: cosine_similarity(query, token_counts(document)),
        reverse=True,
    )
    return ranked[:top_k]


def hash_embedding(text: str, dimensions: int = 128) -> list[float]:
    vector = [0.0] * dimensions
    for token, count in token_counts(text).items():
        vector[hash(token) % dimensions] += float(count)
    magnitude = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [value / magnitude for value in vector]


def token_counts(text: str) -> Counter[str]:
    return Counter(tokens(text))


def tokens(text: str) -> Iterable[str]:
    stopwords = {
        "a",
        "an",
        "and",
        "card",
        "credit",
        "for",
        "i",
        "is",
        "of",
        "on",
        "or",
        "should",
        "the",
        "to",
        "use",
        "which",
        "with",
    }
    return (token for token in re.findall(r"[a-z0-9]+", text.lower()) if token not in stopwords)


def cosine_similarity(left: Counter[str], right: Counter[str]) -> float:
    if not left or not right:
        return 0.0
    shared = set(left) & set(right)
    numerator = sum(left[token] * right[token] for token in shared)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    return numerator / ((left_norm * right_norm) or 1.0)
