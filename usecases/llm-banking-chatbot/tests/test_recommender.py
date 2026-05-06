from banking_assistant.clients import FixtureClient
from banking_assistant.recommender import build_grounded_answer, rank_products


def test_rank_products_prefers_customer_spend_focus():
    client = FixtureClient.from_default_data_dir()
    customer = client.customer_profiles()[0]
    transactions = [tx for tx in client.transactions() if tx["customer_id"] == customer["customer_id"]]

    ranked = rank_products(customer, transactions, client.card_products())

    assert ranked[0].product["name"] == "Horizon Travel Rewards"
    assert ranked[0].score > ranked[-1].score


def test_build_grounded_answer_includes_dozer_context_and_retrieved_knowledge():
    client = FixtureClient.from_default_data_dir()

    answer = build_grounded_answer(
        client,
        customer_id="1001",
        question="Which card should I use for travel and groceries?",
    )

    assert "Ana Silva" in answer
    assert "Top recommendation" in answer
    assert "Retrieved knowledge" in answer

