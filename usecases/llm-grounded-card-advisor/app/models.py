"""Domain models with strict parsing at the data boundary."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from typing import Any, Mapping


class DataContractError(ValueError):
    """Raised when data is incomplete or malformed."""


def _required(row: Mapping[str, Any], key: str) -> str:
    value = row.get(key)
    if value is None or str(value).strip() == "":
        raise DataContractError(f"missing required field: {key}")
    return str(value).strip()


def _integer(row: Mapping[str, Any], key: str) -> int:
    try:
        return int(_required(row, key))
    except ValueError as exc:
        raise DataContractError(f"invalid integer field: {key}") from exc


def _decimal(row: Mapping[str, Any], key: str) -> float:
    try:
        return float(_required(row, key))
    except ValueError as exc:
        raise DataContractError(f"invalid decimal field: {key}") from exc


def _bounded_number(name: str, value: int | float, minimum: float, maximum: float) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise DataContractError(f"invalid numeric field: {name}")
    if not math.isfinite(value) or value < minimum or value > maximum:
        raise DataContractError(f"numeric field out of range: {name}")


@dataclass(frozen=True)
class CustomerFeatures:
    customer_id: str
    age: int
    annual_income: float
    credit_score: int
    risk_band: str
    monthly_spend: float
    travel_spend: float
    grocery_spend: float
    active_account: bool

    def __post_init__(self) -> None:
        _bounded_number("age", self.age, 0, 130)
        _bounded_number("annual_income", self.annual_income, 0, 1_000_000_000)
        _bounded_number("credit_score", self.credit_score, 300, 850)
        _bounded_number("monthly_spend", self.monthly_spend, 0, 1_000_000_000)
        _bounded_number("travel_spend", self.travel_spend, 0, 1_000_000_000)
        _bounded_number("grocery_spend", self.grocery_spend, 0, 1_000_000_000)
        if self.travel_spend + self.grocery_spend > self.monthly_spend:
            raise DataContractError("category spend exceeds monthly_spend")
        if not isinstance(self.active_account, bool):
            raise DataContractError("invalid boolean field: active_account")

    @classmethod
    def from_mapping(cls, row: Mapping[str, Any]) -> "CustomerFeatures":
        active = _required(row, "active_account").lower()
        if active not in {"true", "false", "1", "0"}:
            raise DataContractError("invalid boolean field: active_account")
        return cls(
            customer_id=_required(row, "customer_id"),
            age=_integer(row, "age"),
            annual_income=_decimal(row, "annual_income"),
            credit_score=_integer(row, "credit_score"),
            risk_band=_required(row, "risk_band").lower(),
            monthly_spend=_decimal(row, "monthly_spend"),
            travel_spend=_decimal(row, "travel_spend"),
            grocery_spend=_decimal(row, "grocery_spend"),
            active_account=active in {"true", "1"},
        )


@dataclass(frozen=True)
class CardProduct:
    product_id: str
    name: str
    description: str
    annual_fee: float
    min_income: float
    min_credit_score: int
    min_age: int
    max_age: int
    allowed_risk_bands: tuple[str, ...]
    reward_rate: float
    travel_multiplier: float
    grocery_multiplier: float

    def __post_init__(self) -> None:
        _bounded_number("annual_fee", self.annual_fee, 0, 1_000_000_000)
        _bounded_number("min_income", self.min_income, 0, 1_000_000_000)
        # Zero is a valid sentinel for products that impose no score minimum.
        _bounded_number("min_credit_score", self.min_credit_score, 0, 850)
        _bounded_number("min_age", self.min_age, 0, 130)
        _bounded_number("max_age", self.max_age, 0, 130)
        _bounded_number("reward_rate", self.reward_rate, 0, 1)
        _bounded_number("travel_multiplier", self.travel_multiplier, 0, 100)
        _bounded_number("grocery_multiplier", self.grocery_multiplier, 0, 100)
        if self.min_age > self.max_age:
            raise DataContractError("min_age exceeds max_age")

    @classmethod
    def from_mapping(cls, row: Mapping[str, Any]) -> "CardProduct":
        bands = tuple(
            band.strip().lower()
            for band in _required(row, "allowed_risk_bands").split("|")
            if band.strip()
        )
        if not bands:
            raise DataContractError("allowed_risk_bands must not be empty")
        return cls(
            product_id=_required(row, "product_id"),
            name=_required(row, "name"),
            description=_required(row, "description"),
            annual_fee=_decimal(row, "annual_fee"),
            min_income=_decimal(row, "min_income"),
            min_credit_score=_integer(row, "min_credit_score"),
            min_age=_integer(row, "min_age"),
            max_age=_integer(row, "max_age"),
            allowed_risk_bands=bands,
            reward_rate=_decimal(row, "reward_rate"),
            travel_multiplier=_decimal(row, "travel_multiplier"),
            grocery_multiplier=_decimal(row, "grocery_multiplier"),
        )

    def search_text(self) -> str:
        return (
            f"{self.name} {self.description} annual fee {self.annual_fee:.0f} "
            f"reward rate {self.reward_rate:.2f} travel {self.travel_multiplier:.2f} "
            f"grocery {self.grocery_multiplier:.2f}"
        )


@dataclass(frozen=True)
class Provenance:
    source: str
    endpoint: str
    record_id: str
    fields: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["fields"] = list(self.fields)
        return value


@dataclass(frozen=True)
class Recommendation:
    product_id: str
    product_name: str
    score: float
    reason: str
    estimated_annual_value: float
    provenance: tuple[Provenance, ...]

    def __post_init__(self) -> None:
        _bounded_number("score", self.score, -1, 1)
        _bounded_number(
            "estimated_annual_value", self.estimated_annual_value, -1_000_000_000, 1_000_000_000
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "score": round(self.score, 6),
            "reason": self.reason,
            "estimated_annual_value": round(self.estimated_annual_value, 2),
            "provenance": [item.to_dict() for item in self.provenance],
        }
