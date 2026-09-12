"""Forward-chaining inference engine."""

from __future__ import annotations

from typing import Iterable

from .knowledge_base import KnowledgeBase, validate_initial_facts
from .models import InferenceResult, InferenceStep


class ForwardChainingEngine:
    """Infer new facts until the rule set reaches a fixed point.

    A rule fires when all of its premises are known and its conclusion is not.
    Newly inferred conclusions are inserted into working memory immediately,
    enabling multi-hop reasoning in later passes.
    """

    def __init__(self, knowledge_base: KnowledgeBase) -> None:
        self.kb = knowledge_base

    def infer(self, initial_facts: Iterable[int]) -> InferenceResult:
        initial = validate_initial_facts(self.kb, initial_facts)
        working_memory = set(initial)
        steps: list[InferenceStep] = []

        changed = True
        while changed:
            changed = False
            for rule in self.kb.rules:
                if rule.conclusion in working_memory:
                    continue
                if rule.premises.issubset(working_memory):
                    working_memory.add(rule.conclusion)
                    steps.append(
                        InferenceStep(
                            rule_id=rule.id,
                            premises=tuple(sorted(rule.premises)),
                            conclusion=rule.conclusion,
                        )
                    )
                    changed = True

        animal_ids = tuple(
            concept.id
            for concept in self.kb.animals
            if concept.id in working_memory
        )

        return InferenceResult(
            initial_facts=initial,
            final_facts=frozenset(working_memory),
            steps=tuple(steps),
            animals=animal_ids,
        )
