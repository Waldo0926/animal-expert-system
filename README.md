# Animal Identification Expert System

[![Type](https://img.shields.io/badge/Type-AI_Coursework-2563eb?style=for-the-badge)](#)
[![Tech](https://img.shields.io/badge/Tech-Python_%C2%B7_PyQt5-7c3aed?style=for-the-badge)](#)
[![License](https://img.shields.io/badge/License-MIT-16a34a?style=for-the-badge)](LICENSE)


**English** · [中文](README.zh-CN.md)

A small **symbolic AI / expert-system** project that identifies animals from observable features using a production-rule knowledge base and a genuine **forward-chaining inference engine**.

> This repository is a 2026 independent refactor of the idea behind a 2022 team coursework project for an Introduction to Artificial Intelligence practice week. The original team submission is not published here; see [Coursework origin and attribution](docs/coursework-origin.md).

## Why this project exists

Modern AI is often associated with machine learning, but classical AI also studies explicit knowledge representation and logical reasoning. This project demonstrates that side of AI with a compact, inspectable inference engine.

The knowledge base contains:

- **20 observable features**
- **4 derived categories**: mammal, bird, carnivore, ungulate
- **7 identifiable animals**: leopard, tiger, giraffe, zebra, ostrich, penguin, albatross
- **15 production rules**

## Key features

- True fixed-point **forward chaining** with multi-hop inference
- Structured JSON knowledge base instead of positional text parsing
- Clear separation of knowledge, inference, CLI, and GUI layers
- Bilingual English / Simplified Chinese labels
- Optional PyQt5 desktop GUI
- Dependency-free inference engine and CLI
- Automated unit tests for all seven animal classifications
- GitHub Actions CI across multiple Python versions

## How forward chaining works

Suppose the user provides these facts:

```text
has hair, eats meat, tawny, dark spots
```

The engine can derive:

```text
R01: has hair -> mammal
R05: eats meat -> carnivore
R09: mammal + carnivore + tawny + dark spots -> leopard
```

The important part is that **new conclusions are inserted back into working memory**. This allows later rules to use earlier conclusions, rather than checking every rule only against the user's original input.

See [Architecture](docs/architecture.md) for the full design.

## Project structure

```text
animal-expert-system/
├── src/animal_expert_system/
│   ├── data/knowledge_base.json
│   ├── engine.py
│   ├── knowledge_base.py
│   ├── models.py
│   ├── cli.py
│   └── gui.py
├── tests/
├── docs/
├── .github/workflows/test.yml
├── pyproject.toml
└── README.zh-CN.md
```

## Quick start

### 1. Clone and install

```bash
git clone https://github.com/<your-username>/animal-expert-system.git
cd animal-expert-system
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e .
```

### 2. List observable features

```bash
animal-expert-system --list-features
```

### 3. Run an inference

```bash
animal-expert-system --features 1 6 12 13
```

Expected final result:

```text
leopard / 金钱豹
```

You can also run it without installing the console command:

```bash
PYTHONPATH=src python -m animal_expert_system --features 1 6 12 13
```

## Desktop GUI

Install the optional GUI dependency:

```bash
pip install -e '.[gui]'
animal-expert-gui
```

The GUI lets the user select observable features, run inference, inspect the fired rules, and reset the working state.

## Tests

```bash
python -m unittest discover -s tests -v
```

The test suite verifies all seven target animals and checks that multi-hop inference really occurs.

## Knowledge-base format

Rules live in [`knowledge_base.json`](src/animal_expert_system/data/knowledge_base.json). A rule is represented explicitly:

```json
{
  "id": "R09",
  "if": [21, 23, 12, 13],
  "then": 25
}
```

where each numeric ID references a concept defined in the same file. Keeping the data outside the inference engine makes the reasoning code reusable and the knowledge base easy to extend.

## What changed from the coursework prototype

The public version is not a dump of the old assignment folder. It was rebuilt to remove bundled environments, executables, IDE metadata, personal/student information, and generated prototype code. More importantly, the reasoning engine now iterates until no new fact can be inferred, enabling genuine multi-stage reasoning.

See [Coursework origin and attribution](docs/coursework-origin.md) for details.

## Tech stack

Python 3.10+ · Symbolic AI · Expert Systems · Production Rules · Forward Chaining · JSON · PyQt5 · unittest · GitHub Actions

## License

MIT License. See [LICENSE](LICENSE).
