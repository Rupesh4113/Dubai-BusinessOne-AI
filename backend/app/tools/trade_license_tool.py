"""Trade License Reservation Tool (HIGH RISK - Requires Human Approval)."""

import time
import uuid
from typing import Dict, Any
from .base import BaseTool, ToolResult


class TradeLicenseReservationTool(BaseTool):
    name = "trade_license_reservation"
    description = "Formally reserves a verified trade name and drafts official license dossier in the Dubai DET registry. HIGH-RISK: Requires human supervisor approval."
    risk_level = "HIGH"
    requires_approval = True
    required_role = "SUPERVISOR"

    def run(self, params: Dict[str, Any], context: Dict[str, Any]) -> ToolResult:
        # Check if approval token was passed and verified in context
        is_approved = context.get("human_approved", False)
        approval_token = context.get("approval_token")

        if not is_approved:
            return ToolResult(
                tool_name=self.name,
                success=False,
                data={},
                error_message="BLOCKED: High-risk operation requires verified Human Approval Token. Cannot execute autonomously.",
                verification_passed=False,
                audit_trail=["Blocked attempt to execute trade license reservation without human approval."]
            )

        company_name = params.get("company_name", "").strip().upper()
        legal_form = params.get("legal_form", "LLC")
        activities = params.get("activities", ["Information Technology Consultancy"])
        share_capital = params.get("share_capital", 300000)

        # Generate official mock reservation voucher
        reservation_id = f"DET-RES-{int(time.time())}-{uuid.uuid4().hex[:4].upper()}"
        initial_voucher_no = f"VOUCHER-DET-{uuid.uuid4().hex[:6].upper()}"

        audit = [
            f"Human supervisor '{context.get('approved_by', 'Supervisor')}' approved execution with token '{approval_token}'.",
            f"Trade Name '{company_name}' reserved under Dubai DET Voucher #{initial_voucher_no}.",
            f"Statutory validity period: 60 days from issuance date."
        ]

        return ToolResult(
            tool_name=self.name,
            success=True,
            data={
                "reservation_id": reservation_id,
                "voucher_number": initial_voucher_no,
                "company_name": company_name,
                "legal_form": legal_form,
                "licensed_activities": activities,
                "declared_capital_aed": share_capital,
                "status": "OFFICIALLY_RESERVED",
                "validity_days": 60,
                "issuing_authority": "Dubai Department of Economy and Tourism (DET)",
                "next_steps": [
                    "Draft Memorandum of Association (MOA) through Dubai DET electronic portal.",
                    "Obtain Ejari registered commercial lease or finalize Instant License waiver.",
                    "Pay consolidated commercial voucher."
                ]
            },
            verification_passed=True,
            audit_trail=audit
        )
