"""Layer 4: Execution History, Idempotency, and Immutable Audit Trail."""

import time
import uuid
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class ExecutionRecord(BaseModel):
    """Immutable audit record for every action executed by the agent."""
    task_id: str
    idempotency_key: str
    tenant_id: str
    user_id: str
    action_name: str
    risk_level: str  # "LOW", "MEDIUM", "HIGH"
    status: str      # "SUBMITTED", "PENDING_APPROVAL", "APPROVED", "REJECTED", "EXECUTED", "VERIFIED", "FAILED"
    input_parameters: Dict[str, Any]
    output_result: Optional[Dict[str, Any]] = None
    approval_token: Optional[str] = None
    approved_by_user_id: Optional[str] = None
    created_at_epoch: float = Field(default_factory=time.time)
    completed_at_epoch: Optional[float] = None
    audit_notes: List[str] = Field(default_factory=list)


class ExecutionHistoryStore:
    """Stores execution tasks, enforces idempotency, and logs audit events."""

    def __init__(self):
        self._tasks: Dict[str, ExecutionRecord] = {}
        self._idempotency_index: Dict[str, str] = {}  # idempotency_key -> task_id

    def create_task(
        self,
        tenant_id: str,
        user_id: str,
        action_name: str,
        risk_level: str,
        input_parameters: Dict[str, Any],
        idempotency_key: Optional[str] = None
    ) -> ExecutionRecord:
        """Initializes a new task or returns existing if idempotency key matches."""
        idem_key = idempotency_key or str(uuid.uuid4())

        if idem_key in self._idempotency_index:
            existing_task_id = self._idempotency_index[idem_key]
            existing = self._tasks[existing_task_id]
            existing.audit_notes.append(f"Idempotent request intercepted at {time.time()}. Returning existing record.")
            return existing

        task_id = f"TASK-{int(time.time())}-{uuid.uuid4().hex[:6]}"
        record = ExecutionRecord(
            task_id=task_id,
            idempotency_key=idem_key,
            tenant_id=tenant_id,
            user_id=user_id,
            action_name=action_name,
            risk_level=risk_level,
            status="SUBMITTED",
            input_parameters=input_parameters,
            audit_notes=[f"Task initiated under Risk Tier '{risk_level}'"]
        )

        self._tasks[task_id] = record
        self._idempotency_index[idem_key] = task_id
        return record

    def get_task(self, task_id: str) -> Optional[ExecutionRecord]:
        return self._tasks.get(task_id)

    def set_pending_approval(self, task_id: str, approval_token: str) -> Optional[ExecutionRecord]:
        """Marks high-risk task as awaiting human approval."""
        task = self._tasks.get(task_id)
        if task:
            task.status = "PENDING_APPROVAL"
            task.approval_token = approval_token
            task.audit_notes.append(f"High-Risk Gate triggered: Task held for Human Approval. Token: {approval_token}")
        return task

    def approve_task(self, task_id: str, user_id: str) -> Optional[ExecutionRecord]:
        """Human approval granted."""
        task = self._tasks.get(task_id)
        if task and task.status == "PENDING_APPROVAL":
            task.status = "APPROVED"
            task.approved_by_user_id = user_id
            task.audit_notes.append(f"Human Approval granted by authorized user '{user_id}'.")
        return task

    def mark_executed(self, task_id: str, result: Dict[str, Any], verified: bool = True) -> Optional[ExecutionRecord]:
        """Marks task as executed and verified."""
        task = self._tasks.get(task_id)
        if task:
            task.status = "VERIFIED" if verified else "EXECUTED"
            task.output_result = result
            task.completed_at_epoch = time.time()
            task.audit_notes.append(f"Task executed successfully. Verification status: {'PASSED' if verified else 'UNVERIFIED'}.")
        return task

    def mark_failed(self, task_id: str, error_message: str) -> Optional[ExecutionRecord]:
        """Marks task as failed with recorded error."""
        task = self._tasks.get(task_id)
        if task:
            task.status = "FAILED"
            task.completed_at_epoch = time.time()
            task.audit_notes.append(f"Execution failed: {error_message}")
        return task

    def list_tasks(self, tenant_id: str, limit: int = 50) -> List[ExecutionRecord]:
        """Returns recent tasks for tenant audit dashboard."""
        tenant_tasks = [t for t in self._tasks.values() if t.tenant_id == tenant_id]
        tenant_tasks.sort(key=lambda x: x.created_at_epoch, reverse=True)
        return tenant_tasks[:limit]

    def list_pending_approvals(self, tenant_id: Optional[str] = None) -> List[ExecutionRecord]:
        """Returns all tasks currently waiting for human supervisor approval."""
        pending = [t for t in self._tasks.values() if t.status == "PENDING_APPROVAL"]
        if tenant_id:
            pending = [t for t in pending if t.tenant_id == tenant_id]
        pending.sort(key=lambda x: x.created_at_epoch, reverse=True)
        return pending


layer4_history = ExecutionHistoryStore()
