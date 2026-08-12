import unittest

from app.models import CardProduct
from app.vector_search import DeterministicVectorSearch


def product(product_id, name, description):
    return CardProduct(
        product_id, name, description, 0, 0, 0, 18, 90, ("low",), .01, 1, 1
    )


class VectorSearchTests(unittest.TestCase):
    def setUp(self):
        self.search = DeterministicVectorSearch(256)
        self.products = [
            product("TRAVEL", "Travel Explorer", "airport flights hotels travel"),
            product("GROCERY", "Grocery Cash", "supermarket grocery cashback"),
        ]

    def test_exact_semantics_rank_first(self):
        self.assertEqual(self.search.rank("airport travel", self.products)[0].product.product_id, "TRAVEL")

    def test_results_are_deterministic(self):
        first = self.search.rank("cashback groceries", self.products)
        second = self.search.rank("cashback groceries", self.products)
        self.assertEqual(first, second)

    def test_ties_use_stable_product_id(self):
        products = [product("B", "Same", "same"), product("A", "Same", "same")]
        self.assertEqual([hit.product.product_id for hit in self.search.rank("same", products)], ["A", "B"])

    def test_rejects_tiny_embedding(self):
        with self.assertRaises(ValueError):
            DeterministicVectorSearch(4)


if __name__ == "__main__":
    unittest.main()
