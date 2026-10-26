"""Automated integration tests for FastAPI REST Endpoints."""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_health_endpoint():
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert "uptime_seconds" in data
    assert "zero_inference_cache" in data


def test_vat_endpoint():
    payload = {
        "amount": 1000.0,
        "is_tax_inclusive": False,
        "vat_category": "standard"
    }
    res = client.post("/api/v1/calculate/vat", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["base_amount"] == "1000.00"
    assert data["vat_amount"] == "50.00"
    assert data["total_amount"] == "1050.00"


def test_corporate_tax_endpoint():
    payload = {
        "taxable_net_profit": 500000.0
    }
    res = client.post("/api/v1/calculate/corporate-tax", json=payload)
    assert res.status_code == 200
    data = res.json()
    # 500,000 - 375,000 = 125,000 * 9% = 11,250.00
    assert data["tier1_exempt_amount"] == "375000.00"
    assert data["tier2_taxable_amount"] == "125000.00"
    assert data["total_tax_payable_aed"] == "11250.00"


def test_knowledge_search_endpoint():
    res = client.get("/api/v1/knowledge/search?q=foreign+ownership+llc")
    assert res.status_code == 200
    data = res.json()
    assert len(data) > 0
    assert any("Foreign Ownership" in d["title"] for d in data)


def test_agent_chat_endpoint():
    payload = {
        "prompt": "What are the Dubai Chamber annual fees for a commercial LLC?",
        "language": "en"
    }
    res = client.post("/api/v1/agent/chat", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["current_step"] in ["COMPLETED", "PENDING_APPROVAL"]
    assert "Dubai BusinessOne AI" in data["final_response_text"] or len(data["intermediate_calculations"]) > 0
