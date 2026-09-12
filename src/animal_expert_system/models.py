"""Domain models for the expert system."""

from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet, Tuple


@dataclass(frozen=True)
class Concept:
    id: int
    key: str
    en: str
    zh: str
    kind: str


@dataclass(frozen=True)
class Rule:
    id: str
    premises: FrozenSet[int]
    conclusion: int


@dataclass(frozen=True)
class InferenceStep:
    rule_id: str
    premises: Tuple[int, ...]
    conclusion: int


@dataclass(frozen=True)
class InferenceResult:
    initial_facts: FrozenSet[int]
    final_facts: FrozenSet[int]
    steps: Tuple[InferenceStep, ...]
    animals: Tuple[int, ...]
