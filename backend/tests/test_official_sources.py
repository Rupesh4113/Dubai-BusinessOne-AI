"""Automated tests for Official Source Integration and Citation Generator."""

import pytest
from backend.app.knowledge import (
    OFFICIAL_SOURCE_REGISTRY,
    check_source_freshness,
    search_verified_knowledge,
    generate_citations,
    detect_regulatory_conflicts
)


def test_official_source_registry_integrity():
    assert "DUBAI_CHAMBER" in OFFICIAL_SOURCE_REGISTRY
    assert "DUBAI_DET" in OFFICIAL_SOURCE_REGISTRY
    assert "UAE_FTA" in OFFICIAL_SOURCE_REGISTRY

    chamber = OFFICIAL_SOURCE_REGISTRY["DUBAI_CHAMBER"]
    assert chamber.authority_weight >= 0.90
    assert "dubaichamber.com" in chamber.official_portal_url


def test_source_freshness_check():
    freshness = check_source_freshness("DUBAI_DET")
    assert freshness["source_id"] == "DUBAI_DET"
    assert freshness["authority_name"] == "Dubai Department of Economy and Tourism (DET / DED)"
    assert "status" in freshness

    unknown = check_source_freshness("UNOFFICIAL_BLOG_SOURCE")
    assert unknown["is_fresh"] is False
    assert unknown["status"] == "UNKNOWN_SOURCE"


def test_verified_knowledge_search():
    # Search for Corporate Tax
    results = search_verified_knowledge("corporate tax small business relief 375000")
    assert len(results) > 0
    top = results[0]
    assert "Corporate Tax" in top.topic or "Taxation" in top.statutory_law
    assert "UAE Federal Tax Authority" in top.issuing_authority

    # Search for Chamber membership
    chamber_results = search_verified_knowledge("dubai chamber membership fees tier")
    assert len(chamber_results) > 0
    top_chamber = chamber_results[0]
    assert "Dubai Chamber" in top_chamber.topic or "Chamber" in top_chamber.issuing_authority


def test_citation_generation():
    results = search_verified_knowledge("mainland llc 100% foreign ownership")
    citations = generate_citations(results)
    assert len(citations) > 0
    c = citations[0]
    assert c.citation_id.startswith("CIT-")
    assert c.official_source_url.startswith("https://")
    assert c.authority_weight >= 0.8
