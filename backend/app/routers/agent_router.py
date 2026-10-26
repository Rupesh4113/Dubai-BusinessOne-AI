"""Agent Execution and Chat API Router."""

from typing import Dict, Any, Optional, List
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from ..agent import orchestrator, AgentTaskState
from ..auth import get_current_user
from ..memory import memory_manager, layer4_history

router = APIRouter(prefix="/agent", tags=["Agent Operations & Chat"])


class AgentChatRequest(BaseModel):
    prompt: str = Field(..., description="Natural language prompt / business instruction")
    language: str = Field(default="en", description="User language: en, ar, hi, ur, fil, ml")
    idempotency_key: Optional[str] = Field(default=None, description="Optional key to prevent duplicate execution")
    approval_token: Optional[str] = Field(default=None, description="One-time human approval token to resume a pending high-risk action")


@router.post("/chat", response_model=AgentTaskState)
def agent_chat(payload: AgentChatRequest, current_user: Dict = Depends(get_current_user)):
    """Primary conversational operations endpoint.

    Evaluates instructions, consults 4-tier memory, runs deterministic math,
    enforces risk policies, invokes tools, and generates evidence-grounded responses.
    """
    state = orchestrator.process_request(
        prompt=payload.prompt,
        tenant_id=current_user["tenant_id"],
        user_id=current_user["user_id"],
        language=payload.language,
        idempotency_key=payload.idempotency_key,
        approval_token=payload.approval_token
    )
    return state


@router.get("/tasks")
def list_tasks(limit: int = 50, current_user: Dict = Depends(get_current_user)):
    """Returns immutable execution history and audit records for tenant."""
    tasks = layer4_history.list_tasks(current_user["tenant_id"], limit=limit)
    return {"tasks": [t.model_dump() for t in tasks], "count": len(tasks)}


@router.get("/telemetry")
def get_telemetry():
    """System-wide performance, token-saving, and zero-inference reuse telemetry."""
    return memory_manager.get_telemetry()
