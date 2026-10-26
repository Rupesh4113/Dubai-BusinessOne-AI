"""Human-in-the-Loop Approval Gatekeeper."""

import secrets
import time
from typing import Dict, Any, Optional, Tuple
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


approval_gate = ApprovalGate()
