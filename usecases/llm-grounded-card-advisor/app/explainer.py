"""Optional LangChain explanation of a deterministically selected product."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ExplanationContext:
    """Minimal, immutable context; eligibility and product selection stay upstream."""

    query: str
    product_id: str
    product_name: str
    deterministic_reason: str
    estimated_annual_value: float
    monthly_spend: float
    travel_spend: float
    grocery_spend: float


class CardExplainer(Protocol):
    def explain(self, context: ExplanationContext) -> str: ...


class LangChainCardExplainer:
    """Lazy OpenAI/LangChain adapter that can explain, but cannot select, a card."""

    def __init__(self, model: str = "gpt-4o-mini") -> None:
        try:
            from langchain_core.messages import HumanMessage, SystemMessage
            from langchain_openai import ChatOpenAI
        except ImportError as exc:
            raise RuntimeError(
                "LLM explanations require optional packages from requirements-chroma.txt"
            ) from exc
        self._human_message = HumanMessage
        self._system_message = SystemMessage
        self._chat = ChatOpenAI(model=model, temperature=0)

    def explain(self, context: ExplanationContext) -> str:
        prompt = (
            "User intent: " + context.query + "\n"
            "Selected product: " + context.product_name + " (" + context.product_id + ")\n"
            "Verified calculation: " + context.deterministic_reason + "\n"
            f"Estimated annual value: {context.estimated_annual_value:.2f}\n"
            f"Spend context: monthly={context.monthly_spend:.2f}, "
            f"travel={context.travel_spend:.2f}, grocery={context.grocery_spend:.2f}"
        )
        response = self._chat.invoke(
            [
                self._system_message(
                    content=(
                        "Explain only the already selected product using the supplied facts. "
                        "Do not assess eligibility, suggest another product, alter any value, "
                        "or claim this is financial advice. Use at most three short sentences."
                    )
                ),
                self._human_message(content=prompt),
            ]
        )
        content = response.content
        if not isinstance(content, str) or not content.strip():
            raise RuntimeError("LLM returned an empty explanation")
        return content.strip()[:1200]
