"""Knowledge-base loading and validation."""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional

from .models import Concept, Rule


@dataclass(frozen=True)
class KnowledgeBase:
    concepts: Mapping[int, Concept]
    rules: tuple[Rule, ...]

    @property
    def observable(self) -> tuple[Concept, ...]:
        return tuple(c for c in self.concepts.values() if c.kind == "observable")

    @property
    def animals(self) -> tuple[Concept, ...]:
        return tuple(c for c in self.concepts.values() if c.kind == "animal")

    def concept(self, concept_id: int) -> Concept:
        try:
            return self.concepts[concept_id]
        except KeyError as exc:
            raise ValueError(f"Unknown concept id: {concept_id}") from exc

    def format_concept(self, concept_id: int, language: str = "en") -> str:
        concept = self.concept(concept_id)
        if language == "zh":
            return concept.zh
        if language == "bilingual":
            return f"{concept.en} / {concept.zh}"
        return concept.en


def _default_path() -> Path:
    return Path(files("animal_expert_system.data").joinpath("knowledge_base.json"))


def load_knowledge_base(path: Optional[Path | str] = None) -> KnowledgeBase:
    source = Path(path) if path is not None else _default_path()
    raw = json.loads(source.read_text(encoding="utf-8"))

    concepts: Dict[int, Concept] = {}
    for item in raw["concepts"]:
        concept = Concept(
            id=int(item["id"]),
            key=str(item["key"]),
            en=str(item["en"]),
            zh=str(item["zh"]),
            kind=str(item["kind"]),
        )
        if concept.id in concepts:
            raise ValueError(f"Duplicate concept id: {concept.id}")
        if concept.kind not in {"observable", "derived", "animal"}:
            raise ValueError(f"Unsupported concept kind: {concept.kind}")
        concepts[concept.id] = concept

    rules: List[Rule] = []
    seen_rule_ids: set[str] = set()
    for item in raw["rules"]:
        rule = Rule(
            id=str(item["id"]),
            premises=frozenset(int(x) for x in item["if"]),
            conclusion=int(item["then"]),
        )
        if rule.id in seen_rule_ids:
            raise ValueError(f"Duplicate rule id: {rule.id}")
        seen_rule_ids.add(rule.id)

        referenced = set(rule.premises) | {rule.conclusion}
        missing = referenced.difference(concepts)
        if missing:
            raise ValueError(f"Rule {rule.id} references unknown concepts: {sorted(missing)}")
        if not rule.premises:
            raise ValueError(f"Rule {rule.id} has no premises")
        rules.append(rule)

    return KnowledgeBase(concepts=concepts, rules=tuple(rules))


def validate_initial_facts(kb: KnowledgeBase, facts: Iterable[int]) -> frozenset[int]:
    normalized = frozenset(int(x) for x in facts)
    unknown = normalized.difference(kb.concepts)
    if unknown:
        raise ValueError(f"Unknown fact ids: {sorted(unknown)}")

    non_observable = [fact for fact in normalized if kb.concept(fact).kind != "observable"]
    if non_observable:
        raise ValueError(
            "Initial facts must be observable features only; received: "
            + ", ".join(str(x) for x in sorted(non_observable))
        )
    return normalized
