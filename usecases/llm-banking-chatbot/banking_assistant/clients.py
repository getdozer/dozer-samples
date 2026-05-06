from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Protocol

import requests


class BankingDataClient(Protocol):
    def customer_profiles(self) -> list[dict[str, Any]]:
        ...

    def transactions(self) -> list[dict[str, Any]]:
        ...

    def card_products(self) -> list[dict[str, Any]]:
        ...

    def faq_documents(self) -> list[dict[str, Any]]:
        ...


class DozerRestClient:
    """Small resilient reader for Dozer REST endpoints."""

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def customer_profiles(self) -> list[dict[str, Any]]:
        return self._get_records("/customer-profiles")

    def transactions(self) -> list[dict[str, Any]]:
        return self._get_records("/transactions")

    def card_products(self) -> list[dict[str, Any]]:
        return self._get_records("/card-products")

    def faq_documents(self) -> list[dict[str, Any]]:
        return self._get_records("/faq-documents")

    def _get_records(self, path: str) -> list[dict[str, Any]]:
        response = requests.get(f"{self.base_url}{path}", timeout=15)
        response.raise_for_status()
        return normalize_dozer_response(response.json())


class FixtureClient:
    """Offline client for tests and first-run demos."""

    def __init__(self, data_dir: Path) -> None:
        self.data_dir = data_dir

    @classmethod
    def from_default_data_dir(cls) -> "FixtureClient":
        return cls(Path(__file__).resolve().parents[1] / "data")

    def customer_profiles(self) -> list[dict[str, Any]]:
        customers = read_csv(self.data_dir / "customer_profiles" / "customers.csv")
        transactions = self.transactions()
        profiles: list[dict[str, Any]] = []
        for customer in customers:
            customer_tx = [tx for tx in transactions if tx["customer_id"] == customer["customer_id"]]
            amounts = [float(tx["amount_eur"]) for tx in customer_tx]
            profile = dict(customer)
            profile["transaction_count"] = len(customer_tx)
            profile["total_spend_eur"] = round(sum(amounts), 2)
            profile["average_transaction_eur"] = round(sum(amounts) / len(amounts), 2) if amounts else 0
            profile["largest_transaction_eur"] = max(amounts) if amounts else 0
            profiles.append(profile)
        return profiles

    def transactions(self) -> list[dict[str, Any]]:
        return read_csv(self.data_dir / "transactions" / "transactions.csv")

    def card_products(self) -> list[dict[str, Any]]:
        return read_csv(self.data_dir / "card_products" / "card_products.csv")

    def faq_documents(self) -> list[dict[str, Any]]:
        return read_csv(self.data_dir / "support_docs" / "faqs.csv")


def normalize_dozer_response(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [normalize_record(item) for item in payload]
    if isinstance(payload, dict):
        records = payload.get("records") or payload.get("data") or payload.get("items")
        if isinstance(records, list):
            return [normalize_record(item) for item in records]
        return [normalize_record(payload)]
    return []


def normalize_record(item: Any) -> dict[str, Any]:
    if not isinstance(item, dict):
        return {"value": item}
    record = item.get("record", item)
    if isinstance(record, dict):
        return dict(record)
    return dict(item)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

