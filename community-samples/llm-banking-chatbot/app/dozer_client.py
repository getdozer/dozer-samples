"""HTTP client for querying Dozer REST API endpoints."""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional
import requests


class DozerClientError(RuntimeError):
    """Raised when a Dozer REST endpoint request fails."""


class DozerClient:
    """Thin HTTP client for Dozer's auto-generated REST endpoints."""

    def __init__(self, base_url: Optional[str] = None, timeout: float = 5.0) -> None:
        self.base_url = (base_url or os.getenv("DOZER_BASE_URL", "http://localhost:8080")).rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()

    def health(self) -> Dict[str, Any]:
        """Check Dozer API health."""
        return self._get("/health")

    def list_customer_profiles(self) -> List[Dict[str, Any]]:
        """Fetch all unified customer profiles from Dozer."""
        data = self._get("/customer_profiles")
        if isinstance(data, list):
            return data
        return data.get("records", [])

    def get_customer_profile(self, customer_id: str) -> Optional[Dict[str, Any]]:
        """Fetch a single unified customer profile by customer_id."""
        url = f"{self.base_url}/customer_profiles/{customer_id}"
        try:
            resp = self._session.get(url, timeout=self.timeout)
        except requests.RequestException as exc:
            raise DozerClientError(f"Failed to reach Dozer at {url}: {exc}") from exc

        if resp.status_code == 404:
            return None
        if not resp.ok:
            raise DozerClientError(f"Dozer returned {resp.status_code} for {url}: {resp.text}")
        return resp.json()

    def query_customer_profiles(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Query customer profiles using Dozer's POST /query filter contract."""
        url = f"{self.base_url}/customer_profiles/query"
        try:
            resp = self._session.post(url, json={"$filter": filters}, timeout=self.timeout)
        except requests.RequestException as exc:
            raise DozerClientError(f"Failed to query Dozer at {url}: {exc}") from exc

        if not resp.ok:
            raise DozerClientError(f"Dozer query returned {resp.status_code}: {resp.text}")
        data = resp.json()
        return data if isinstance(data, list) else data.get("records", [])

    def list_credit_cards(self) -> List[Dict[str, Any]]:
        """Fetch the credit card product catalog from Dozer."""
        data = self._get("/credit_cards")
        if isinstance(data, list):
            return data
        return data.get("records", [])

    def _get(self, path: str) -> Any:
        url = f"{self.base_url}{path}"
        try:
            resp = self._session.get(url, timeout=self.timeout)
        except requests.RequestException as exc:
            raise DozerClientError(f"Failed to reach Dozer at {url}: {exc}") from exc

        if not resp.ok:
            raise DozerClientError(f"Dozer returned {resp.status_code} for {url}: {resp.text}")
        return resp.json()
