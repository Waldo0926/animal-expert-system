"""Animal identification expert system."""

from .engine import ForwardChainingEngine
from .knowledge_base import KnowledgeBase, load_knowledge_base

__all__ = ["ForwardChainingEngine", "KnowledgeBase", "load_knowledge_base"]
__version__ = "2.0.0"
