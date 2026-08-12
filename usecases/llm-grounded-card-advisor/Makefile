.PHONY: demo test eval

demo:
	python -m app.cli --customer-id C001 --query "travel rewards with useful grocery cashback" --json

test:
	python -m unittest discover -s tests -v

eval:
	python -m tests.eval_retrieval
