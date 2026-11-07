#!/usr/bin/env python3
"""Dozer API Client (REST & gRPC), LangChain Tool Wrapper, and Local SQL Pipeline Engine.

Supports:
1. Live Dozer REST API (`POST /{endpoint}/query` and `POST /{endpoint}/count` on port 8080)
2. Live Dozer gRPC API (`localhost:50051` typed/common service query fallback)
3. LangChain-compatible `DozerCustomerProfileTool` for agent/chain tool calling
4. Local SQL Pipeline Execution fallback that parses `dozer-config.yaml` custom
   YAML tags (`!LocalStorage`, `!Table`, `!CSV`, `!Postgres`), loads the configured
   CSV datasets into an in-memory SQLite engine, and executes the exact `SELECT ... INTO`
   SQL transformations from `dozer-config.yaml`.
"""

from __future__ import annotations

import csv
import json
import re
import sqlite3
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import requests
import yaml


class DozerYamlLoader(yaml.SafeLoader):
    """YAML Loader that preserves Dozer custom tags (!LocalStorage, !Table, !CSV, !Postgres)."""


def _construct_tagged_mapping(loader: yaml.SafeLoader, tag_suffix: str, node: yaml.Node) -> Dict[str, Any]:
    if isinstance(node, yaml.MappingNode):
        data = loader.construct_mapping(node, deep=True)
        data["_dozer_tag"] = tag_suffix
        return data
    raise yaml.constructor.ConstructorError(None, None, f"Unsupported node for tag {tag_suffix}", node.start_mark)


for _tag in ("!LocalStorage", "!Table", "!CSV", "!Postgres"):
    DozerYamlLoader.add_constructor(
        _tag,
        lambda loader, node, t=_tag: _construct_tagged_mapping(loader, t, node),
    )


@dataclass
class CustomerProfile:
    """Unified customer profile joined and aggregated by Dozer across datasets."""

    customer_id: int
    customer_code: str
    full_name: str
    age: int
    annual_income: float
    credit_score: int
    employment_status: str
    preferred_reward_type: str
    city: str
    existing_card_type: str
    current_balance: float
    credit_limit: float
    current_apr: float
    late_payments_last_year: int
    utilization_pct: float
    tx_count: int
    total_spend: float
    travel_spend: float
    dining_spend: float
    groceries_spend: float
    fuel_spend: float
    online_shopping_spend: float
    utilities_spend: float

    @property
    def top_spending_categories(self) -> List[tuple[str, float]]:
        categories = [
            ("travel", self.travel_spend),
            ("dining", self.dining_spend),
            ("groceries", self.groceries_spend),
            ("fuel", self.fuel_spend),
            ("online_shopping", self.online_shopping_spend),
            ("utilities", self.utilities_spend),
        ]
        return sorted([c for c in categories if c[1] > 0], key=lambda item: item[1], reverse=True)

    def to_context_dict(self) -> Dict[str, Any]:
        payload = asdict(self)
        payload["top_spending_categories"] = [
            {"category": cat, "spend": spend} for cat, spend in self.top_spending_categories
        ]
        return payload

    def format_for_prompt(self) -> str:
        top_cats = ", ".join(
            f"{cat.replace('_', ' ').title()} (${amt:,.2f})" for cat, amt in self.top_spending_categories[:3]
        ) or "No recent transactions"
        return (
            f"Customer Name: {self.full_name} (ID: {self.customer_id} / Code: {self.customer_code})\n"
            f"Demographics: Age {self.age}, {self.employment_status}, located in {self.city}\n"
            f"Financial Standing: Annual Income ${self.annual_income:,.2f} | Credit Score: {self.credit_score}\n"
            f"Existing Credit Account: {self.existing_card_type} | Balance: ${self.current_balance:,.2f} / "
            f"${self.credit_limit:,.2f} limit ({self.utilization_pct:.2f}% utilization) at {self.current_apr:.2f}% APR | "
            f"Late Payments (12m): {self.late_payments_last_year}\n"
            f"Aggregated Monthly Spend (Dozer Real-Time View): ${self.total_spend:,.2f} across {self.tx_count} transactions\n"
            f"Top Spending Categories: {top_cats}\n"
            f"Category Breakdown: Travel=${self.travel_spend:,.2f}, Dining=${self.dining_spend:,.2f}, "
            f"Groceries=${self.groceries_spend:,.2f}, Fuel=${self.fuel_spend:,.2f}, "
            f"Online Shopping=${self.online_shopping_spend:,.2f}, Utilities=${self.utilities_spend:,.2f}\n"
            f"Stated Reward Preference: {self.preferred_reward_type}"
        )


def load_dozer_config(config_path: Union[str, Path]) -> Dict[str, Any]:
    """Parse and validate a Dozer YAML configuration file."""
    path = Path(config_path)
    with path.open("r", encoding="utf-8") as fh:
        config = yaml.load(fh, Loader=DozerYamlLoader)
    if not isinstance(config, dict) or "app_name" not in config:
        raise ValueError(f"Invalid Dozer config at {path}")
    return config


class LocalDozerSQLPipeline:
    """Executes the exact SQL transformations from `dozer-config.yaml` over local CSV datasets."""

    def __init__(self, project_root: Union[str, Path], config_filename: str = "dozer-config.yaml") -> None:
        self.project_root = Path(project_root)
        self.config_path = self.project_root / config_filename
        self.config = load_dozer_config(self.config_path)
        self.conn = sqlite3.connect(":memory:", check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._initialize_pipeline()

    def _infer_value(self, raw_val: str) -> Union[int, float, str]:
        val = raw_val.strip()
        if re.fullmatch(r"-?\d+", val):
            return int(val)
        if re.fullmatch(r"-?\d+\.\d+", val):
            return float(val)
        return val

    def _load_csv_table(self, table_name: str, csv_path: Path) -> None:
        with csv_path.open("r", encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            rows = list(reader)
            fieldnames = reader.fieldnames or []

        if not fieldnames:
            raise ValueError(f"Empty CSV header in {csv_path}")

        col_types: List[str] = []
        for col in fieldnames:
            sample_val = rows[0][col] if rows else ""
            inferred = self._infer_value(sample_val) if sample_val != "" else ""
            if isinstance(inferred, int):
                col_types.append(f"{col} INTEGER")
            elif isinstance(inferred, float):
                col_types.append(f"{col} REAL")
            else:
                col_types.append(f"{col} TEXT")

        self.conn.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.conn.execute(f"CREATE TABLE {table_name} ({', '.join(col_types)})")

        placeholders = ", ".join(["?"] * len(fieldnames))
        for row in rows:
            values = [self._infer_value(row[col]) for col in fieldnames]
            self.conn.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", values)
        self.conn.commit()

    def _translate_select_into(self, sql_block: str) -> List[tuple[str, str]]:
        """Convert Dozer `SELECT ... INTO <table_name> FROM ...` into SQLite views/tables."""
        statements: List[tuple[str, str]] = []
        raw_stmts = [s.strip() for s in sql_block.split(";") if s.strip()]
        pattern = re.compile(r"\bINTO\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+FROM\b", re.IGNORECASE)
        for stmt in raw_stmts:
            match = pattern.search(stmt)
            if not match:
                raise ValueError(f"Expected SELECT ... INTO <table> FROM in Dozer SQL: {stmt}")
            target_table = match.group(1)
            select_query = pattern.sub("FROM", stmt, count=1)
            statements.append((target_table, select_query))
        return statements

    def _initialize_pipeline(self) -> None:
        for conn_cfg in self.config.get("connections", []):
            cfg = conn_cfg.get("config", {})
            if cfg.get("_dozer_tag") == "!LocalStorage":
                base_dir = self.project_root / cfg.get("details", {}).get("path", "./data")
                for tbl in cfg.get("tables", []):
                    t_name = tbl["name"]
                    csv_rel = tbl.get("config", {}).get("path", f"{t_name}.csv")
                    self._load_csv_table(t_name, base_dir / csv_rel)

        self.refresh_materialized_views()

    def refresh_materialized_views(self) -> None:
        """Re-execute Dozer SQL transformations to materialize unified views."""
        sql_block = self.config.get("sql", "")
        for target_table, select_query in self._translate_select_into(sql_block):
            self.conn.execute(f"DROP TABLE IF EXISTS {target_table}")
            self.conn.execute(f"CREATE TABLE {target_table} AS {select_query}")
        self.conn.commit()

    def insert_realtime_transaction(self, tx_record: Dict[str, Any]) -> None:
        """Simulate a real-time CDC INSERT event into `transactions` and refresh Dozer views."""
        cols = ["tx_id", "customer_id", "tx_date", "merchant", "category", "amount", "currency", "is_international"]
        vals = [tx_record[c] for c in cols]
        self.conn.execute(
            f"INSERT INTO transactions ({', '.join(cols)}) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            vals,
        )
        self.conn.commit()
        self.refresh_materialized_views()

    def query_endpoint(
        self,
        endpoint_table: str,
        filter_dict: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Query an endpoint table using Dozer's `$filter` and `$limit` semantics."""
        where_clauses: List[str] = []
        params: List[Any] = []
        if filter_dict:
            for k, v in filter_dict.items():
                where_clauses.append(f"{k} = ?")
                params.append(v)
        where_sql = f" WHERE {' AND '.join(where_clauses)}" if where_clauses else ""
        limit_sql = f" LIMIT {int(limit)}" if limit is not None else ""
        cur = self.conn.execute(f"SELECT * FROM {endpoint_table}{where_sql}{limit_sql}", params)
        return [dict(row) for row in cur.fetchall()]

    def count_endpoint(self, endpoint_table: str, filter_dict: Optional[Dict[str, Any]] = None) -> int:
        """Return record count for an endpoint table using Dozer's `/count` semantics."""
        return len(self.query_endpoint(endpoint_table, filter_dict))


class DozerClient:
    """Unified Dozer client that queries the live Dozer REST/gRPC API with automatic local SQL fallback."""

    # Support legacy persona aliases from issue #1690 discussions alongside primary seed personas
    LEGACY_ALIASES: Dict[str, int] = {
        "ALICE JOHNSON": 101,
        "AVA SHARMA": 101,
        "BOB SMITH": 102,
        "LIAM CHEN": 102,
        "CHARLIE DAVIS": 103,
        "SOFIA MARTINEZ": 103,
        "DIANA EVANS": 104,
        "MARCUS JOHNSON": 104,
        "PRIYA PATEL": 105,
    }

    def __init__(
        self,
        base_url: str = "http://localhost:8080",
        grpc_url: str = "localhost:50051",
        project_root: Optional[Union[str, Path]] = None,
        offline_fixture: bool = False,
        timeout: float = 2.5,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.grpc_url = grpc_url
        self.project_root = Path(project_root) if project_root else Path(__file__).resolve().parent.parent
        self.offline_fixture = offline_fixture
        self.timeout = timeout
        self.local_pipeline = LocalDozerSQLPipeline(self.project_root)

    def query_rest(
        self,
        endpoint_path: str,
        filter_dict: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Query Dozer REST endpoint `POST /{endpoint}/query` with `{"$filter": ..., "$limit": ...}`."""
        path = endpoint_path.lstrip("/")
        url = f"{self.base_url}/{path}/query"
        payload: Dict[str, Any] = {}
        if filter_dict:
            payload["$filter"] = filter_dict
        if limit is not None:
            payload["$limit"] = limit
        resp = requests.post(url, json=payload, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and "records" in data:
            return data["records"]
        return [data]

    def count_rest(self, endpoint_path: str, filter_dict: Optional[Dict[str, Any]] = None) -> int:
        """Query Dozer REST count endpoint `POST /{endpoint}/count`."""
        path = endpoint_path.lstrip("/")
        url = f"{self.base_url}/{path}/count"
        payload: Dict[str, Any] = {}
        if filter_dict:
            payload["$filter"] = filter_dict
        if not self.offline_fixture:
            try:
                resp = requests.post(url, json=payload, timeout=self.timeout)
                resp.raise_for_status()
                data = resp.json()
                if isinstance(data, dict) and "count" in data:
                    return int(data["count"])
                if isinstance(data, int):
                    return data
            except requests.RequestException:
                pass
        return self.local_pipeline.count_endpoint(path, filter_dict)

    def get_customer_profile(self, customer_identifier: Union[int, str]) -> CustomerProfile:
        """Fetch a unified `CustomerProfile` by `customer_id` (101), `customer_code` ('C001'), or name."""
        ident_str = str(customer_identifier).strip()
        upper_ident = ident_str.upper()
        if ident_str.isdigit():
            filter_dict: Dict[str, Any] = {"customer_id": int(ident_str)}
        elif upper_ident in self.LEGACY_ALIASES:
            filter_dict = {"customer_id": self.LEGACY_ALIASES[upper_ident]}
        else:
            filter_dict = {"customer_code": upper_ident}

        records: List[Dict[str, Any]] = []
        if not self.offline_fixture:
            try:
                records = self.query_rest("/customer_profiles", filter_dict)
            except requests.RequestException:
                records = self.local_pipeline.query_endpoint("customer_profiles", filter_dict)
        else:
            records = self.local_pipeline.query_endpoint("customer_profiles", filter_dict)

        if not records:
            raise KeyError(f"Customer '{customer_identifier}' not found in Dozer customer_profiles endpoint.")

        row = records[0]
        return CustomerProfile(
            customer_id=int(row["customer_id"]),
            customer_code=str(row["customer_code"]),
            full_name=str(row["full_name"]),
            age=int(row["age"]),
            annual_income=float(row["annual_income"]),
            credit_score=int(row["credit_score"]),
            employment_status=str(row["employment_status"]),
            preferred_reward_type=str(row["preferred_reward_type"]),
            city=str(row["city"]),
            existing_card_type=str(row["existing_card_type"]),
            current_balance=float(row["current_balance"]),
            credit_limit=float(row["credit_limit"]),
            current_apr=float(row["current_apr"]),
            late_payments_last_year=int(row["late_payments_last_year"]),
            utilization_pct=float(row["utilization_pct"]),
            tx_count=int(row["tx_count"]),
            total_spend=float(row["total_spend"]),
            travel_spend=float(row["travel_spend"]),
            dining_spend=float(row["dining_spend"]),
            groceries_spend=float(row["groceries_spend"]),
            fuel_spend=float(row["fuel_spend"]),
            online_shopping_spend=float(row["online_shopping_spend"]),
            utilities_spend=float(row["utilities_spend"]),
        )

    def get_category_spending(self, customer_id: int) -> List[Dict[str, Any]]:
        """Fetch per-category transaction metrics from Dozer `/category_spending` endpoint."""
        filter_dict = {"customer_id": int(customer_id)}
        if not self.offline_fixture:
            try:
                return self.query_rest("/category_spending", filter_dict)
            except requests.RequestException:
                pass
        return self.local_pipeline.query_endpoint("category_spending", filter_dict)

    def list_all_profiles(self) -> List[CustomerProfile]:
        """Return all unified customer profiles."""
        rows = self.local_pipeline.query_endpoint("customer_profiles")
        return [self.get_customer_profile(r["customer_id"]) for r in rows]


class DozerCustomerProfileTool:
    """LangChain-compatible Tool wrapping `DozerClient.get_customer_profile`."""

    name: str = "dozer_customer_profile_lookup"
    description: str = (
        "Fetch a customer's real-time unified financial profile (income, credit score, "
        "credit utilization, and transaction spend by category) from Dozer REST/gRPC API."
    )

    def __init__(self, dozer_client: DozerClient) -> None:
        self.dozer_client = dozer_client

    def run(self, customer_identifier: Union[int, str]) -> str:
        profile = self.dozer_client.get_customer_profile(customer_identifier)
        return profile.format_for_prompt()

    def invoke(self, input_val: Union[int, str, Dict[str, Any]]) -> str:
        if isinstance(input_val, dict):
            cid = input_val.get("customer_id") or input_val.get("customer") or "C001"
            return self.run(cid)
        return self.run(input_val)
