"""Official Source & Verified Knowledge Package."""

from .official_sources import OFFICIAL_SOURCE_REGISTRY, check_source_freshness, OfficialSourceMetadata
from .verified_data import VERIFIED_REGULATORY_RECORDS, search_verified_knowledge, RegulatoryRecord, search_verified_regulations
from .citation import generate_citations, detect_regulatory_conflicts, FormattedCitation

# Aliases for convenience
OFFICIAL_SOURCES = OFFICIAL_SOURCE_REGISTRY

__all__ = [
    "OFFICIAL_SOURCE_REGISTRY",
    "OFFICIAL_SOURCES",
    "check_source_freshness",
    "OfficialSourceMetadata",
    "VERIFIED_REGULATORY_RECORDS",
    "search_verified_knowledge",
    "search_verified_regulations",
    "RegulatoryRecord",
    "generate_citations",
    "detect_regulatory_conflicts",
    "FormattedCitation"
]
