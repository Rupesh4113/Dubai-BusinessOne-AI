"""Automated tests for 4-Tier Memory and Zero-Inference Cache."""

import pytest
import time
from backend.app.memory import (
    ExactAnswerCache,
    UserOrganizationMemory,
    ExecutionHistoryStore,
    memory_manager
)


def test_layer1_cache_hit_and_telemetry():
    cache = ExactAnswerCache(default_ttl_seconds=3600)
    tenant = "tenant_dubai_1"
    query = "What is the UAE Corporate Tax rate for 2026?"
    key = cache.generate_fingerprint(tenant, query, language="en")

    # Miss initially
    assert cache.get(key) is None
    assert cache.total_misses == 1

    # Set cache
    response_payload = {
        "answer": "UAE Corporate Tax is 0% up to AED 375,000 and 9% above AED 375,000.",
        "statutory_reference": "Federal Decree-Law No. 47 of 2022"
    }
    cache.set(key, tenant, query, response_payload)

    # Hit
    cached_entry = cache.get(key)
    assert cached_entry is not None
    assert cached_entry.response_data["answer"] == response_payload["answer"]
    assert cached_entry.hit_count == 1
    assert cached_entry.estimated_tokens_saved == 800
    assert cache.total_hits == 1

    stats = cache.get_stats()
    assert stats["hit_ratio_percent"] == 50.0  # 1 hit, 1 miss


def test_layer1_time_sensitive_veto():
    cache = ExactAnswerCache()
    tenant = "tenant_fx"
    query = "Get current exchange rate"
    key = cache.generate_fingerprint(tenant, query)

    # Set with is_time_sensitive=True
    cache.set(key, tenant, query, {"rate": 3.6725}, is_time_sensitive=True)
    # Immediately accessible
    assert cache.get(key) is not None

    # Simulate stale time-sensitive entry (> 60 seconds)
    entry = cache._store[key]
    entry.created_at_epoch = time.time() - 65

    # Should be rejected as stale and removed
    assert cache.get(key) is None


def test_layer3_tenant_isolation():
    mem = UserOrganizationMemory()
    mem.update_profile("tenant_A", {"company_name": "Al Wasl Trading LLC", "trn": "100111111111111"})
    mem.update_profile("tenant_B", {"company_name": "Jumeirah Tech FZCO", "trn": "100222222222222"})

    profile_a = mem.get_profile("tenant_A")
    profile_b = mem.get_profile("tenant_B")

    assert profile_a.company_name == "Al Wasl Trading LLC"
    assert profile_b.company_name == "Jumeirah Tech FZCO"
    assert profile_a.trn != profile_b.trn


def test_layer4_idempotency_prevention():
    history = ExecutionHistoryStore()
    idem_key = "IDEMPOTENT-PAYMENT-UUID-999"

    task1 = history.create_task(
        tenant_id="tenant_main",
        user_id="user_admin",
        action_name="trade_license_renewal",
        risk_level="HIGH",
        input_parameters={"license_no": "109283", "amount": 6000},
        idempotency_key=idem_key
    )
    assert task1.status == "SUBMITTED"

    # Second call with identical idempotency key
    task2 = history.create_task(
        tenant_id="tenant_main",
        user_id="user_admin",
        action_name="trade_license_renewal",
        risk_level="HIGH",
        input_parameters={"license_no": "109283", "amount": 6000},
        idempotency_key=idem_key
    )

    # Must be the exact same task, preventing duplicate submission
    assert task1.task_id == task2.task_id
    assert any("Idempotent request intercepted" in note for note in task2.audit_notes)
