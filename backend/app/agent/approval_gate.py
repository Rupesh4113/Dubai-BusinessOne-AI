"""Human-in-the-Loop Approval Gatekeeper."""

import secrets
import time
from typing import Dict, Any, Optional, Tuple, List
from ..memory import layer4_history, ExecutionRecord


class ApprovalGate:
    """Coordinates risk mitigation and supervisor sign-offs for High-Risk tasks."""

    @staticmethod
    def generate_approval_request(task_id: str, summary: str, parameters: Dict[str, Any]) -> str:
        """Generates a cryptographically secure one-time token and marks task pending."""
        token = f"AUTH-TOKEN-{secrets.token_hex(8).upper()}"
        layer4_history.set_pending_approval(task_id, token)
        return token

    @staticmethod
    def verify_and_grant_approval(task_id: str, approval_token: str, supervisor_id: str) -> Tuple[bool, str]:
        """Validates supervisor token and transitions task state to APPROVED."""
        task: Optional[ExecutionRecord] = layer4_history.get_task(task_id)
        
        # If task_id not directly matched, check pending tasks for matching token
        if not task or task.approval_token != approval_token:
            for pending_task in layer4_history.list_pending_approvals():
                if pending_task.approval_token == approval_token:
                    task = pending_task
                    task_id = pending_task.task_id
                    break

        if not task:
            return False, "Task ID or token not found in execution history."

        if task.status != "PENDING_APPROVAL":
            return False, f"Task is not awaiting approval. Current status: '{task.status}'."

        if task.approval_token != approval_token:
            return False, "Invalid or expired human approval token."

        layer4_history.approve_task(task_id, supervisor_id)
        return True, "Approval verified. Task authorized for execution."

    @staticmethod
    def list_pending() -> List[ExecutionRecord]:
        """Returns all actions currently awaiting human review."""
        return layer4_history.list_pending_approvals()

    @staticmethod
    def record_decision(approval_token: str, decision: str, reviewer_id: str, reviewer_notes: str = "") -> Tuple[bool, str]:
        """Convenience dispatcher to record an approval or rejection."""
        matched_task: Optional[ExecutionRecord] = None
        for p in layer4_history.list_pending_approvals():
            if p.approval_token == approval_token:
                matched_task = p
                break

        if not matched_task:
            return False, "Token not found among pending approvals."

        if decision.upper() == "APPROVED":
            return ApprovalGate.verify_and_grant_approval(matched_task.task_id, approval_token, reviewer_id)
        else:
            matched_task.status = "REJECTED"
            matched_task.audit_notes.append(f"Rejected by {reviewer_id}. Notes: {reviewer_notes}")
            return True, "Action has been rejected and cancelled."


approval_gate = ApprovalGate()
