"""FastAPI HTTP server exposing the personalized banking chatbot."""

from __future__ import annotations

from typing import Any, Dict, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.chatbot import BankingChatbot


class ChatRequest(BaseModel):
    customer_id: str = Field(..., description="Customer ID from Dozer customer_profiles")
    question: str = Field(..., min_length=1, description="User banking or card recommendation question")
    top_k: int = Field(default=3, ge=1, le=10)


class CardRecommendationOut(BaseModel):
    card_id: str
    card_name: str
    annual_fee: float
    primary_category: str
    similarity_score: float
    benefits_summary: str


class ChatResponseOut(BaseModel):
    customer_id: str
    answer: str
    recommended_cards: List[CardRecommendationOut]
    used_live_llm: bool


def create_app(chatbot: BankingChatbot | None = None) -> FastAPI:
    """Create a FastAPI app wired to a BankingChatbot instance."""
    bot = chatbot or BankingChatbot()
    application = FastAPI(title="Dozer Personalized Banking Chatbot", version="1.0.0")

    @application.get("/health")
    def health() -> Dict[str, Any]:
        return {"status": "ok", "dozer_base_url": bot.dozer_client.base_url}

    @application.get("/recommendations/{customer_id}")
    def recommendations(customer_id: str, query: str = "best credit card for my spending", top_k: int = 3) -> Dict[str, Any]:
        res = bot.ask(customer_id=customer_id, question=query, top_k=top_k)
        if res.profile is None:
            raise HTTPException(status_code=404, detail=res.answer)
        return {
            "customer_id": res.customer_id,
            "profile": res.profile,
            "recommended_cards": [
                {
                    "card_id": m.card["card_id"],
                    "card_name": m.card["card_name"],
                    "annual_fee": m.card["annual_fee"],
                    "primary_category": m.card["primary_category"],
                    "similarity_score": m.similarity_score,
                    "benefits_summary": m.card["benefits_summary"],
                }
                for m in res.recommended_cards
            ],
        }

    @application.post("/chat", response_model=ChatResponseOut)
    def chat(req: ChatRequest) -> ChatResponseOut:
        res = bot.ask(customer_id=req.customer_id, question=req.question, top_k=req.top_k)
        if res.profile is None:
            raise HTTPException(status_code=404, detail=res.answer)
        return ChatResponseOut(
            customer_id=res.customer_id,
            answer=res.answer,
            recommended_cards=[
                CardRecommendationOut(
                    card_id=m.card["card_id"],
                    card_name=m.card["card_name"],
                    annual_fee=m.card["annual_fee"],
                    primary_category=m.card["primary_category"],
                    similarity_score=m.similarity_score,
                    benefits_summary=m.card["benefits_summary"],
                )
                for m in res.recommended_cards
            ],
            used_live_llm=res.used_live_llm,
        )

    return application


app = create_app()
