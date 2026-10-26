"""Layer 2: Verified Knowledge Base with Version Tracking and Fast Retrieval."""

from typing import List, Optional, Dict, Any
from ..knowledge.verified_data import VERIFIED_REGULATORY_RECORDS, search_verified_knowledge, RegulatoryRecord
from ..knowledge.official_sources import check_source_freshness


class VerifiedKnowledgeBase:
    """Manages Layer 2 authoritative procedures, rules, and freshness."""

    def __init__(self):
        self._records = VERIFIED_REGULATORY_RECORDS

    def retrieve(self, query: str, category: Optional[str] = None, max_results: int = 5) -> List[Dict[str, Any]]:
        """Retrieves verified knowledge records with freshness metadata."""
        matches: List[RegulatoryRecord] = search_verified_knowledge(query, category=category, max_results=max_results)
        results = []

        for m in matches:
            freshness = check_source_freshness(m.source_id)
            results.append({
                "record_id": m.record_id,
                "category": m.category,
                "topic": m.topic,
                "title": m.title,
                "summary": m.summary,
                "detailed_rules": m.detailed_rules,
                "statutory_law": m.statutory_law,
                "issuing_authority": m.issuing_authority,
                "official_source_url": m.official_source_url,
                "effective_date": m.effective_date,
                "freshness": freshness
            })
        return results

    def get_by_id(self, record_id: str) -> Optional[RegulatoryRecord]:
        for r in self._records:
            if r.record_id == record_id:
                return r
        return None


layer2_kb = VerifiedKnowledgeBase()
