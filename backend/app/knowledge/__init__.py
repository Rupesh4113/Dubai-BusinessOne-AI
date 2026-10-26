"""Official Source & Verified Knowledge Package."""

from .official_sources import OFFICIAL_SOURCE_REGISTRY, check_source_freshness, OfficialSourceMetadata
from .verified_data import VERIFIED_REGULATORY_RECORDS, search_verified_knowledge, RegulatoryRecord
from .citation import generate_citations, detect_regulatory_conflicts, FormattedCitation

__all__ = [
    "OFFICIAL_SOURCE_REGISTRY",
    "check_source_freshness",
    "OfficialSourceMetadata",
    "VERIFIED_REGULATORY_RECORDS",
    "search_verified_knowledge",
    "RegulatoryRecord",
    "generate_citations",
    "detect_regulatory_conflicts",
    "FormattedCitation"
]
