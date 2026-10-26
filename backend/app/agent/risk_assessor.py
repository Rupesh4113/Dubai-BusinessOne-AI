"""Risk Assessment and Authorization Policy Engine."""

from typing import Dict, Any, Tuple


def evaluate_action_risk(intent: str, entities: Dict[str, Any], requested_tools: list[str]) -> Tuple[str, bool, str]:
    """Assesses the risk level of the planned operation.

    Returns:
        (risk_level: "LOW"|"MEDIUM"|"HIGH", requires_human_approval: bool, rationale: str)
    """
    # High-Risk Operations: Real official submissions, legal commitments, financial charges
    if intent in ["TRADE_NAME_RESERVATION"] or "trade_license_reservation" in requested_tools:
        return (
            "HIGH",
            True,
            "Trade name reservation and commercial license filing create legal and financial commitments with the Dubai Department of Economy and Tourism (DET). Requires human supervisor sign-off."
        )

    # Medium-Risk Operations: Reconciliation discrepancy flags, profile modifications
    if intent in ["INVOICE_RECONCILIATION"] or "invoice_reconciler" in requested_tools:
        return (
            "MEDIUM",
            False,
            "Invoice verification and auditing. Reversible, audited operational check."
        )

    # Low-Risk Operations: Information retrieval, deterministic calculations, document generation
    return (
        "LOW",
        False,
        "Read-only official knowledge retrieval, deterministic math calculation, and operational report synthesis. Safe for autonomous execution."
    )
