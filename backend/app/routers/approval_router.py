"""Human-in-the-Loop Supervisor Approval Router."""

from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from ..auth import get_current_user, require_role, UserRole, ApprovalDecision
from ..memory import layer4_history
from ..agent import approval_gate, orchestrator

router = APIRouter(prefix="/approvals", tags=["Human Approval & Supervision"])


@router.get("/pending")
def list_pending_approvals(current_user: Dict = Depends(get_current_user)):
    """Lists all tasks currently paused at the High-Risk Human Approval Gate."""
    pending = layer4_history.list_pending_approvals(current_user["tenant_id"])
    return {
        "pending_tasks": [t.model_dump() for t in pending],
        "total_pending": len(pending)
    }


@router.post("/decision")
def submit_approval_decision(
    decision: ApprovalDecision,
    current_user: Dict = Depends(require_role([UserRole.ADMIN, UserRole.SUPERVISOR]))
):
    """Supervisor grants or rejects authorization for a High-Risk operation."""
    task = layer4_history.get_task(decision.task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")

    if decision.decision.upper() == "REJECT":
        task.status = "REJECTED"
        task.audit_notes.append(f"Rejected by supervisor {current_user['email']}: {decision.comments or 'No reason specified'}")
        return {
            "task_id": task.task_id,
            "status": "REJECTED",
            "message": "Task has been officially rejected by human supervisor."
        }

    # Verify token
    valid, msg = approval_gate.verify_and_grant_approval(
        decision.task_id,
        decision.approval_token,
        current_user["user_id"]
    )
    if not valid:
        raise HTTPException(status_code=400, detail=msg)

    # Resume task execution with verified approval
    resumed_state = orchestrator.process_request(
        prompt=task.input_parameters.get("prompt", ""),
        tenant_id=task.tenant_id,
        user_id=current_user["user_id"],
        approval_token=decision.approval_token
    )

    return {
        "task_id": task.task_id,
        "status": "APPROVED_AND_EXECUTED",
        "resumed_state": resumed_state.model_dump()
    }
