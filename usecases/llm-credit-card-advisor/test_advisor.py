from advisor import DozerProfileClient, recommend_credit_card


def test_high_tier_travel_customer_recommendation():
    result = recommend_credit_card(101, "Which card is best for my travel spend?")
    assert result["customer_profile"]["full_name"] == "Alice Vance"
    assert result["customer_profile"]["top_category"] == "Travel"
    assert result["eligible_cards"][0]["card_id"] == "cc_sapphire"
    assert "Apex Travel Reserve" in result["advisor_response"]


def test_medium_tier_groceries_customer_recommendation():
    result = recommend_credit_card(102, "I want a zero-fee card for groceries.")
    assert result["customer_profile"]["full_name"] == "Marco Silva"
    assert len(result["eligible_cards"]) == 1
    assert result["eligible_cards"][0]["card_id"] == "cc_cashback"
