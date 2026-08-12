import unittest

from tests.eval_retrieval import evaluate


class RetrievalEvaluationTests(unittest.TestCase):
    def test_retrieval_quality_regression_gate(self):
        metrics = evaluate()
        self.assertEqual(metrics["cases"], 5)
        self.assertGreaterEqual(metrics["hit_rate_at_3"], 1.0)
        self.assertGreaterEqual(metrics["mean_reciprocal_rank"], 0.85)


if __name__ == "__main__":
    unittest.main()
