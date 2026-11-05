# Dozer + LLM + Vector Search + LangChain Credit Card Advisor Sample

This sample implements the hyper-personalized banking chatbot architecture described in [Dozer's LLM Chatbot article](https://getdozer.io/blog/llm-chatbot) for [getdozer/dozer#1690](https://github.com/getdozer/dozer/issues/1690).

## Architecture
1. **Multi-Dataset Ingestion (`dozer-config.yaml`)**: Joins `customers.csv` and `transactions.csv` into a real-time `customer_360_profile` materialization alongside `credit_cards.csv`.
2. **Real-Time Context Retrieval (`advisor.py`)**: Queries the Dozer `/customer_profile` REST endpoint, filters eligible credit card embeddings/products by live credit score and top spend category, and constructs the grounded LangChain prompt.
3. **Automated Tests (`test_advisor.py`)**: Verified with `pytest`.
