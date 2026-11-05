import csv
import json
import os
import urllib.request
from typing import Dict, List, Any

DOZER_REST_URL = os.environ.get("DOZER_REST_URL", "http://127.0.0.1:8080")


class DozerProfileClient:
    """Queries real-time unified customer profiles from Dozer REST endpoints with local CSV fallback."""

    def __init__(self, base_url: str = DOZER_REST_URL, data_dir: str = None):
        self.base_url = base_url.rstrip("/")
        self.data_dir = data_dir or os.path.join(os.path.dirname(__file__), "data")

    def get_customer_profile(self, customer_id: int) -> Dict[str, Any]:
        try:
            req = urllib.request.Request(
                f"{self.base_url}/customer_profile/query",
                data=json.dumps({"$filter": {"customer_id": int(customer_id)}}).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=2) as resp:
                rows = json.loads(resp.read().decode("utf-8"))
                if rows:
                    return rows[0]
        except Exception:
            pass
        return self._local_fallback_profile(customer_id)

    def _local_fallback_profile(self, customer_id: int) -> Dict[str, Any]:
        cid = str(customer_id)
        customer = None
        with open(os.path.join(self.data_dir, "customers.csv"), encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row["customer_id"] == cid:
                    customer = row
                    break
        if not customer:
            raise ValueError(f"Customer {customer_id} not found")

        txs = []
        with open(os.path.join(self.data_dir, "transactions.csv"), encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row["customer_id"] == cid:
                    txs.append(row)

        total_spend = sum(float(t["amount_usd"]) for t in txs)
        top_cat = max((t["merchant_category"] for t in txs), default="General")
        return {
            "customer_id": int(cid),
            "full_name": customer["full_name"],
            "income_tier": customer["income_tier"],
            "credit_score": int(customer["credit_score"]),
            "tx_count": len(txs),
            "total_spend_usd": round(total_spend, 2),
            "top_category": top_cat,
        }

    def list_credit_cards(self) -> List[Dict[str, Any]]:
        cards = []
        with open(os.path.join(self.data_dir, "credit_cards.csv"), encoding="utf-8") as f:
            for row in csv.DictReader(f):
                row["min_credit_score"] = int(row["min_credit_score"])
                row["annual_fee_usd"] = float(row["annual_fee_usd"])
                cards.append(row)
        return cards


def build_hyper_personalized_prompt(profile: Dict[str, Any], matched_cards: List[Dict[str, Any]], user_query: str) -> str:
    cards_txt = "\n".join(
        f"- {c['card_name']} (Min Score: {c['min_credit_score']}, Fee: ${c['annual_fee_usd']}): {c['rewards_summary']}"
        for c in matched_cards
    )
    return (
        f"System: You are a hyper-personalized banking AI assistant powered by Dozer real-time customer profiles.\n"
        f"Customer Profile: {profile['full_name']} | Credit Score: {profile['credit_score']} | "
        f"Total Spend: ${profile['total_spend_usd']} | Top Category: {profile['top_category']}\n"
        f"Eligible Card Products:\n{cards_txt}\n"
        f"Customer Question: {user_query}"
    )


def recommend_credit_card(customer_id: int, user_query: str, client: DozerProfileClient = None) -> Dict[str, Any]:
    client = client or DozerProfileClient()
    profile = client.get_customer_profile(customer_id)
    all_cards = client.list_credit_cards()
    eligible = [c for c in all_cards if profile["credit_score"] >= c["min_credit_score"]]
    eligible.sort(key=lambda c: (0 if c["target_category"] == profile["top_category"] else 1, -c["min_credit_score"]))
    prompt = build_hyper_personalized_prompt(profile, eligible, user_query)
    best = eligible[0] if eligible else None
    recommendation = (
        f"Hi {profile['full_name']}, based on your Dozer real-time profile (Credit Score {profile['credit_score']} "
        f"and ${profile['total_spend_usd']} recent spend primarily in {profile['top_category']}), "
        f"we recommend the {best['card_name']}: {best['rewards_summary']}."
        if best else "No matching card products found."
    )
    return {
        "customer_profile": profile,
        "eligible_cards": eligible,
        "langchain_context_prompt": prompt,
        "advisor_response": recommendation,
    }


if __name__ == "__main__":
    out = recommend_credit_card(101, "Which credit card maximizes rewards for my upcoming international flights?")
    print(json.dumps(out, indent=2))
