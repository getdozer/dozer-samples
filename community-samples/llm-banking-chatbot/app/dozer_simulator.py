"""Local HTTP Dozer endpoint simulator for development and integration testing.

Reads CSV sources (customers, transactions, credit_cards), executes the same
SQL join/aggregation semantics defined in dozer-config.yaml, and serves real
HTTP JSON endpoints over ThreadingHTTPServer.
"""

from __future__ import annotations

import csv
import json
import threading
from collections import defaultdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse


def _load_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def build_in_memory_views(data_dir: Path) -> Tuple[Dict[str, Dict[str, Any]], Dict[str, Dict[str, Any]]]:
    """Build customer_profiles and credit_cards views from CSV files."""
    customers_raw = _load_csv(data_dir / "customers.csv")
    transactions_raw = _load_csv(data_dir / "transactions.csv")
    cards_raw = _load_csv(data_dir / "credit_cards.csv")

    tx_by_customer: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for row in transactions_raw:
        tx_by_customer[row["customer_id"]].append(
            {
                "transaction_id": row["transaction_id"],
                "customer_id": row["customer_id"],
                "merchant": row["merchant"],
                "category": row["category"],
                "amount": float(row["amount"]),
                "currency": row["currency"],
                "transaction_date": row["transaction_date"],
                "channel": row["channel"],
            }
        )

    profiles: Dict[str, Dict[str, Any]] = {}
    for cust in customers_raw:
        cid = cust["customer_id"]
        txs = tx_by_customer.get(cid, [])
        amounts = [t["amount"] for t in txs]
        total_spend = round(sum(amounts), 2)
        tx_count = len(txs)
        avg_spend = round(total_spend / tx_count, 2) if tx_count > 0 else 0.0
        max_spend = round(max(amounts), 2) if tx_count > 0 else 0.0

        category_totals: Dict[str, float] = defaultdict(float)
        for t in txs:
            category_totals[t["category"]] += t["amount"]
        top_category = max(category_totals.items(), key=lambda kv: kv[1])[0] if category_totals else "general"

        profiles[cid] = {
            "customer_id": cid,
            "full_name": cust["full_name"],
            "email": cust["email"],
            "age": int(cust["age"]),
            "annual_income": float(cust["annual_income"]),
            "credit_score": int(cust["credit_score"]),
            "city": cust["city"],
            "segment": cust["segment"],
            "account_opened_at": cust["account_opened_at"],
            "transaction_count": tx_count,
            "total_spend": total_spend,
            "avg_transaction_amount": avg_spend,
            "max_transaction_amount": max_spend,
            "top_category": top_category,
            "category_spend": {k: round(v, 2) for k, v in sorted(category_totals.items())},
        }

    cards: Dict[str, Dict[str, Any]] = {}
    for card in cards_raw:
        card_id = card["card_id"]
        cards[card_id] = {
            "card_id": card_id,
            "card_name": card["card_name"],
            "issuer": card["issuer"],
            "annual_fee": float(card["annual_fee"]),
            "min_credit_score": int(card["min_credit_score"]),
            "min_income": float(card["min_income"]),
            "primary_category": card["primary_category"],
            "cashback_rate": float(card["cashback_rate"]),
            "travel_miles_multiplier": float(card["travel_miles_multiplier"]),
            "benefits_summary": card["benefits_summary"],
            "target_persona": card["target_persona"],
        }

    return profiles, cards


class DozerSimulatorServer:
    """Real local HTTP server simulating Dozer REST endpoints."""

    def __init__(self, data_dir: Path, host: str = "127.0.0.1", port: int = 0) -> None:
        self.data_dir = Path(data_dir)
        self.profiles, self.cards = build_in_memory_views(self.data_dir)
        self._httpd = self._create_server(host, port)
        self._thread: Optional[threading.Thread] = None

    @property
    def base_url(self) -> str:
        host, port = self._httpd.server_address[:2]
        return f"http://{host}:{port}"

    def start(self) -> str:
        """Start the HTTP server in a daemon background thread and return base_url."""
        if self._thread is None:
            self._thread = threading.Thread(target=self._httpd.serve_forever, daemon=True)
            self._thread.start()
        return self.base_url

    def stop(self) -> None:
        """Shut down the HTTP server cleanly."""
        self._httpd.shutdown()
        self._httpd.server_close()
        if self._thread is not None:
            self._thread.join(timeout=2.0)
            self._thread = None

    def __enter__(self) -> "DozerSimulatorServer":
        self.start()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.stop()

    def _create_server(self, host: str, port: int) -> ThreadingHTTPServer:
        profiles = self.profiles
        cards = self.cards

        class _Handler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:  # noqa: N802
                path = urlparse(self.path).path.rstrip("/") or "/"
                if path == "/health":
                    self._send_json(200, {"status": "SERVING", "service": "dozer-simulator"})
                    return
                if path == "/customer_profiles":
                    self._send_json(200, list(profiles.values()))
                    return
                if path.startswith("/customer_profiles/"):
                    cid = path.split("/", 2)[2]
                    record = profiles.get(cid)
                    if record is None:
                        self._send_json(404, {"error": f"Customer '{cid}' not found"})
                        return
                    self._send_json(200, record)
                    return
                if path == "/credit_cards":
                    self._send_json(200, list(cards.values()))
                    return
                if path.startswith("/credit_cards/"):
                    card_id = path.split("/", 2)[2]
                    record = cards.get(card_id)
                    if record is None:
                        self._send_json(404, {"error": f"Credit card '{card_id}' not found"})
                        return
                    self._send_json(200, record)
                    return
                self._send_json(404, {"error": f"Unknown endpoint: {path}"})

            def do_POST(self) -> None:  # noqa: N802
                path = urlparse(self.path).path.rstrip("/")
                if path != "/customer_profiles/query":
                    self._send_json(404, {"error": f"Unknown endpoint: {path}"})
                    return

                length = int(self.headers.get("Content-Length", "0"))
                raw_body = self.rfile.read(length) if length > 0 else b"{}"
                try:
                    payload = json.loads(raw_body.decode("utf-8"))
                except json.JSONDecodeError:
                    self._send_json(400, {"error": "Invalid JSON body"})
                    return

                flt = payload.get("$filter", {})
                results = [
                    rec
                    for rec in profiles.values()
                    if all(rec.get(k) == v for k, v in flt.items())
                ]
                self._send_json(200, results)

            def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
                return

            def _send_json(self, status_code: int, body: Any) -> None:
                encoded = json.dumps(body).encode("utf-8")
                self.send_response(status_code)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(encoded)))
                self.end_headers()
                self.wfile.write(encoded)

        return ThreadingHTTPServer((host, port), _Handler)
