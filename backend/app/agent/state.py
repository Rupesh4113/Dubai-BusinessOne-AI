"""Agent State definitions for the Dubai BusinessOne Operations State Machine."""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class AgentTaskState(BaseModel):
    """Complete state snapshot of an agent operation workflow."""
    task_id: str
    tenant_id: str
    user_id: str
    raw_prompt: str
    sanitized_prompt: str = ""
    language: str = "en"
    current_step: str = "INITIALIZED"  # INITIALIZED, SANITIZED, CACHE_CHECKED, INTENT_EXTRACTED, KNOWLEDGE_RETRIEVED, CALCULATED, RISK_EVALUATED, PENDING_APPROVAL, EXECUTED, VERIFIED, COMPLETED, FAILED

    intent: str = "UNKNOWN"
    extracted_entities: Dict[str, Any] = Field(default_factory=dict)
    risk_level: str = "LOW"            # LOW, MEDIUM, HIGH
    requires_human_approval: bool = False
    approval_token: Optional[str] = None
    is_approved_by_human: bool = False
    approved_by: Optional[str] = None

    is_cached_zero_inference: bool = False
    retrieved_knowledge: List[Dict[str, Any]] = Field(default_factory=list)
    citations: List[Dict[str, Any]] = Field(default_factory=list)
    intermediate_calculations: Dict[str, Any] = Field(default_factory=dict)

    planned_tools: List[Dict[str, Any]] = Field(default_factory=list)
    executed_tools: List[Dict[str, Any]] = Field(default_factory=list)

    final_response_text: str = ""
    structured_output: Dict[str, Any] = Field(default_factory=dict)
    audit_trail: List[str] = Field(default_factory=list)
    error_message: Optional[str] = None
