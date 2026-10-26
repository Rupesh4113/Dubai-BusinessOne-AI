"""Automated tests for Risk Tiering and Human Approval Gate."""

import pytest
from backend.app.agent import orchestrator, AgentTaskState
from backend.app.memory import layer4_history


def test_high_risk_trade_name_reservation_requires_approval():
    prompt = "Please reserve trade name 'Falcon Tech Solutions LLC' in Dubai DET"
    tenant = "tenant_risk_1"

    # Turn 1: Initial request
    state1: AgentTaskState = orchestrator.process_request(prompt, tenant_id=tenant, language="en")

    # Must be held at approval gate
    assert state1.current_step == "PENDING_APPROVAL"
    assert state1.risk_level == "HIGH"
    assert state1.requires_human_approval is True
    assert state1.approval_token is not None
    assert state1.approval_token.startswith("AUTH-TOKEN-")
    assert state1.is_approved_by_human is False

    # Verify no tool was executed yet without supervisor approval
    assert len(state1.executed_tools) == 0

    token = state1.approval_token

    # Turn 2: Unauthorized or wrong token rejection
    state_invalid: AgentTaskState = orchestrator.process_request(
        prompt,
        tenant_id=tenant,
        language="en",
        approval_token="WRONG-TOKEN-999"
    )
    assert state_invalid.current_step == "PENDING_APPROVAL"
    assert state_invalid.is_approved_by_human is False

    # Turn 3: Authorized supervisor provides valid one-time token
    state_approved: AgentTaskState = orchestrator.process_request(
        prompt,
        tenant_id=tenant,
        user_id="user_supervisor_99",
        language="en",
        approval_token=token
    )
    assert state_approved.current_step == "COMPLETED"
    assert state_approved.is_approved_by_human is True
    assert len(state_approved.executed_tools) >= 1

    # Check reservation output
    res_tool = [t for t in state_approved.executed_tools if t["tool_name"] == "trade_license_reservation"][0]
    assert res_tool["data"]["status"] == "OFFICIALLY_RESERVED"
    assert "voucher_number" in res_tool["data"]
