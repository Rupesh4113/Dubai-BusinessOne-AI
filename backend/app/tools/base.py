"""Base Tool Interface and Execution Policy."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel


class ToolResult(BaseModel):
    """Structured result returned by every tool execution."""
    tool_name: str
    success: bool
    data: Dict[str, Any]
    error_message: Optional[str] = None
    verification_passed: bool = True
    audit_trail: List[str] = []


class BaseTool(ABC):
    """Abstract base class for all authorized agent tools."""

    name: str
    description: str
    risk_level: str  # "LOW", "MEDIUM", "HIGH"
    requires_approval: bool = False
    required_role: str = "OPERATOR"

    @abstractmethod
    def run(self, params: Dict[str, Any], context: Dict[str, Any]) -> ToolResult:
        """Executes the tool with parameter validation and postcondition verification."""
        pass

    def verify_postcondition(self, result_data: Dict[str, Any]) -> bool:
        """Independent verification of tool side-effects or calculation integrity."""
        return True
