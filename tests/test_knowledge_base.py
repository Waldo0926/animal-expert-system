import unittest

from animal_expert_system.knowledge_base import load_knowledge_base


class KnowledgeBaseTests(unittest.TestCase):
    def test_expected_counts(self):
        kb = load_knowledge_base()
        self.assertEqual(len(kb.concepts), 31)
        self.assertEqual(len(kb.observable), 20)
        self.assertEqual(len(kb.animals), 7)
        self.assertEqual(len(kb.rules), 15)

    def test_all_rule_references_are_valid(self):
        kb = load_knowledge_base()
        ids = set(kb.concepts)
        for rule in kb.rules:
            self.assertTrue(rule.premises.issubset(ids))
            self.assertIn(rule.conclusion, ids)


if __name__ == "__main__":
    unittest.main()
