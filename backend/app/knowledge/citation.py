"""Citation generation, conflict detection, and evidence formatting."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from .official_sources import OFFICIAL_SOURCE_REGISTRY, check_source_freshness
from .verified_data import RegulatoryRecord


class FormattedCitation(BaseModel):
    """Evidence citation block for agent responses."""
    citation_id: str
    authority_name: str
    statutory_law: str
    official_source_url: str
    authority_weight: float
    freshness_status: str
    excerpt: str


def generate_citations(records: List[RegulatoryRecord]) -> List[FormattedCitation]:
    """Generates structured, verified citation blocks for agent output."""
    citations: List[FormattedCitation] = []
    seen = set()

    for idx, rec in enumerate(records, 1):
        if rec.record_id in seen:
            continue
        seen.add(rec.record_id)

        freshness_info = check_source_freshness(rec.source_id)
        source_meta = OFFICIAL_SOURCE_REGISTRY.get(rec.source_id)
        weight = source_meta.authority_weight if source_meta else 0.8

        citations.append(FormattedCitation(
            citation_id=f"CIT-{idx:02d}",
            authority_name=rec.issuing_authority,
            statutory_law=rec.statutory_law,
            official_source_url=rec.official_source_url,
            authority_weight=weight,
            freshness_status=freshness_info.get("status", "VERIFIED"),
            excerpt=rec.summary
        ))

    return citations


def detect_regulatory_conflicts(citations: List[FormattedCitation]) -> List[Dict[str, Any]]:
    """Detects potential discrepancies between federal and local regulations."""
    conflicts = []
    # E.g., check if a local decree has precedence over general commercial rules
    # Here we enforce that authoritative Federal Decree-Law No. (32) supersedes prior local 51% restrictions
    has_federal_llc = any("32 of 2021" in c.statutory_law for c in citations)
    has_local_pre_2021 = any("prior local sponsorship" in c.excerpt.lower() for c in citations)

    if has_federal_llc and has_local_pre_2021:
        conflicts.append({
            "conflict_type": "STATUTORY_PREEMPTION",
            "resolution": "Federal Decree-Law No. 32 of 2021 supersedes prior 51% local sponsorship requirements, permitting 100% foreign ownership."
        })

    return conflicts
