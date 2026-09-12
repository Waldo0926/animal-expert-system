import unittest

from animal_expert_system.engine import ForwardChainingEngine
from animal_expert_system.knowledge_base import load_knowledge_base


class ForwardChainingEngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kb = load_knowledge_base()
        cls.engine = ForwardChainingEngine(cls.kb)

    def assert_identifies(self, facts, animal_id):
        result = self.engine.infer(facts)
        self.assertIn(animal_id, result.animals)
        return result

    def test_leopard_requires_multi_hop_reasoning(self):
        result = self.assert_identifies([1, 6, 12, 13], 25)
        self.assertIn(21, result.final_facts)  # mammal
        self.assertIn(23, result.final_facts)  # carnivore
        self.assertGreaterEqual(len(result.steps), 3)

    def test_tiger(self):
        self.assert_identifies([1, 6, 12, 14], 26)

    def test_giraffe(self):
        self.assert_identifies([2, 10, 13, 15, 16], 27)

    def test_zebra(self):
        self.assert_identifies([1, 10, 14], 28)

    def test_ostrich(self):
        self.assert_identifies([3, 15, 16, 17, 18], 29)

    def test_penguin(self):
        self.assert_identifies([3, 17, 18, 19], 30)

    def test_albatross(self):
        self.assert_identifies([3, 20], 31)

    def test_insufficient_facts_returns_no_animal(self):
        result = self.engine.infer([1])
        self.assertEqual(result.animals, ())
        self.assertIn(21, result.final_facts)

    def test_rejects_derived_fact_as_user_input(self):
        with self.assertRaises(ValueError):
            self.engine.infer([21])


if __name__ == "__main__":
    unittest.main()
