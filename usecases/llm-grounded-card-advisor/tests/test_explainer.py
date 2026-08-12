import unittest
from pathlib import Path
from unittest.mock import patch

from app.advisor import GroundedCardAdvisor
from app.cli import _build_advisor, build_parser
from app.explainer import ExplanationContext, LangChainCardExplainer
from app.gateway import FixtureGateway


ROOT = Path(__file__).resolve().parents[1]


class CapturingExplainer:
    def __init__(self):
        self.context = None

    def explain(self, context):
        self.context = context
        return "A concise explanation."


class Message:
    def __init__(self, content):
        self.content = content


class Response:
    content = "The selected card matches the verified travel calculation."


class Chat:
    def __init__(self):
        self.messages = None

    def invoke(self, messages):
        self.messages = messages
        return Response()


class ExplainerTests(unittest.TestCase):
    def test_llm_flag_without_api_key_keeps_deterministic_path(self):
        args = build_parser().parse_args(
            ["--customer-id", "C001", "--query", "travel", "--llm"]
        )
        with patch.dict("os.environ", {}, clear=True):
            advisor = _build_advisor(args)
        self.assertIsNone(advisor.explainer)

    def test_advisor_selects_before_explainer_and_exposes_minimal_context(self):
        explainer = CapturingExplainer()
        result = GroundedCardAdvisor(
            FixtureGateway(ROOT / "data"), explainer=explainer
        ).recommend("C001", "airport travel rewards", limit=2)

        selected = result["recommendations"][0]
        self.assertEqual(selected["llm_explanation"], "A concise explanation.")
        self.assertEqual(explainer.context.product_id, selected["product_id"])
        self.assertIsInstance(explainer.context, ExplanationContext)
        self.assertFalse(hasattr(explainer.context, "credit_score"))
        self.assertFalse(hasattr(explainer.context, "annual_income"))
        self.assertEqual(len(result["recommendations"]), 2)

    def test_langchain_contract_only_prompts_for_selected_product(self):
        explainer = LangChainCardExplainer.__new__(LangChainCardExplainer)
        explainer._human_message = Message
        explainer._system_message = Message
        explainer._chat = Chat()
        context = ExplanationContext(
            query="airport travel", product_id="CARD-TRAVEL", product_name="Travel Plus",
            deterministic_reason="Eligible; computed value 100/year.",
            estimated_annual_value=100, monthly_spend=2000,
            travel_spend=900, grocery_spend=480,
        )

        text = explainer.explain(context)

        self.assertIn("selected card", text)
        prompt = "\n".join(message.content for message in explainer._chat.messages)
        self.assertIn("CARD-TRAVEL", prompt)
        self.assertIn("Do not assess eligibility", prompt)
        self.assertNotIn("credit_score", prompt)
        self.assertNotIn("annual_income", prompt)


if __name__ == "__main__":
    unittest.main()
