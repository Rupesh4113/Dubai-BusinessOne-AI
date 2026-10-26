"""API Routers Package."""

from .agent_router import router as agent_router
from .approval_router import router as approval_router
from .calculator_router import router as calculator_router
from .knowledge_router import router as knowledge_router
from .health_router import router as health_router

__all__ = [
    "agent_router",
    "approval_router",
    "calculator_router",
    "knowledge_router",
    "health_router"
]
