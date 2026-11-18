"""LangChain-based personalized banking chatbot powered by Dozer & local vector search."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.prompts import ChatPromptTemplate

from app.dozer_client import DozerClient
from app.vector_store import CardMatch, CreditCardVectorStore


class LocalBankingChatModel(BaseChatModel):
    """Deterministic LangChain BaseChatModel for offline/local banking synthesis."""

    @property
    def _llm_type(self) -> str:
        return "local-banking-chat-model"

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Any = None,
        **kwargs: Any,
    ) -> ChatResult:
        human_content = messages[-1].content if messages else ""
        context = self._extract_context(str(human_content))
        profile = context.get("profile", {})
        matches = context.get("matches", [])
        question = context.get("question", "")

        name = profile.get("full_name", "Valued Customer")
        segment = profile.get("segment", "standard")
        total_spend = profile.get("total_spend", 0.0)
        tx_count = profile.get("transaction_count", 0)
        top_cat = profile.get("top_category", "general")
        credit_score = profile.get("credit_score", "N/A")
        annual_income = profile.get("annual_income", 0.0)

        if not matches:
            reply = (
                f"Hello {name}, based on your Dozer profile (credit score: {credit_score}, "
                f"annual income: ${annual_income:,.0f}, recent spend: ${total_spend:,.2f} across "
                f"{tx_count} transactions), no eligible credit card products matched your query "
                f"'{question}'. Please check with an advisor for tailored options."
            )
        else:
            top = matches[0]
            lines = [
                f"Hello {name}! Based on your unified Dozer banking profile "
                f"(segment: {segment}, credit score: {credit_score}, annual income: ${annual_income:,.0f}, "
                f"recent spend: ${total_spend:,.2f} across {tx_count} transactions, top category: {top_cat}):",
                "",
                f"Top Recommendation: **{top['card_name']}** ({top['card_id']}) "
                f"[similarity: {top['similarity_score']:.2f}, annual fee: ${top['annual_fee']:.0f}]",
                f"- Why it fits: {top['benefits_summary']}",
                f"- Target persona: {top['target_persona']}",
            ]
            if len(matches) > 1:
                lines.append("")
                lines.append("Other eligible matches:")
                for alt in matches[1:]:
                    lines.append(
                        f"- {alt['card_name']} (similarity: {alt['similarity_score']:.2f}, "
                        f"annual fee: ${alt['annual_fee']:.0f}, primary category: {alt['primary_category']})"
                    )
            reply = "\n".join(lines)

        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=reply))])

    @staticmethod
    def _extract_context(text: str) -> Dict[str, Any]:
        marker = "CONTEXT_JSON:"
        if marker not in text:
            return {}
        raw = text.split(marker, 1)[1].strip()
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {}


@dataclass
class ChatResponse:
    """Structured response returned by BankingChatbot."""

    customer_id: str
    answer: str
    recommended_cards: List[CardMatch]
    profile: Optional[Dict[str, Any]]
    used_live_llm: bool


class BankingChatbot:
    """End-to-end LangChain banking assistant backed by Dozer and local vector search."""

    def __init__(
        self,
        dozer_client: Optional[DozerClient] = None,
        vector_store: Optional[CreditCardVectorStore] = None,
        chat_model: Optional[BaseChatModel] = None,
    ) -> None:
        self.dozer_client = dozer_client or DozerClient()
        self.vector_store = vector_store or CreditCardVectorStore()
        self.used_live_llm = False
        self.chat_model = chat_model or self._build_chat_model()

        self._prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a personalized banking advisor. Use only the verified Dozer "
                    "customer profile and eligible credit card matches provided in CONTEXT_JSON.",
                ),
                (
                    "human",
                    "Customer Question: {question}\n\nCONTEXT_JSON:\n{context_json}",
                ),
            ]
        )
        self._chain = self._prompt | self.chat_model

    def _build_chat_model(self) -> BaseChatModel:
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if api_key:
            try:
                from langchain_openai import ChatOpenAI  # type: ignore

                self.used_live_llm = True
                return ChatOpenAI(model="gpt-4o-mini", temperature=0.2, api_key=api_key)
            except ImportError:
                pass
        return LocalBankingChatModel()

    def refresh_catalog(self) -> int:
        """Fetch credit card catalog from Dozer and index it in the vector store."""
        cards = self.dozer_client.list_credit_cards()
        self.vector_store.index_cards(cards)
        return self.vector_store.size

    def ask(self, customer_id: str, question: str, top_k: int = 3) -> ChatResponse:
        """Answer a customer's question using Dozer profile + vector search + LangChain."""
        profile = self.dozer_client.get_customer_profile(customer_id)
        if profile is None:
            return ChatResponse(
                customer_id=customer_id,
                answer=f"Customer '{customer_id}' was not found in Dozer.",
                recommended_cards=[],
                profile=None,
                used_live_llm=self.used_live_llm,
            )

        if self.vector_store.size == 0:
            self.refresh_catalog()

        matches = self.vector_store.search(
            query_text=question,
            customer_profile=profile,
            top_k=top_k,
            enforce_eligibility=True,
        )

        context_payload = {
            "question": question,
            "profile": profile,
            "matches": [
                {
                    "card_id": m.card["card_id"],
                    "card_name": m.card["card_name"],
                    "annual_fee": m.card["annual_fee"],
                    "primary_category": m.card["primary_category"],
                    "benefits_summary": m.card["benefits_summary"],
                    "target_persona": m.card["target_persona"],
                    "similarity_score": m.similarity_score,
                }
                for m in matches
            ],
        }

        ai_msg = self._chain.invoke(
            {
                "question": question,
                "context_json": json.dumps(context_payload),
            }
        )
        return ChatResponse(
            customer_id=customer_id,
            answer=str(ai_msg.content),
            recommended_cards=matches,
            profile=profile,
            used_live_llm=self.used_live_llm,
        )
