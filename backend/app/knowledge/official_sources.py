"""Official UAE and Dubai Government Source Registry and Freshness Validator."""

from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, HttpUrl


class OfficialSourceMetadata(BaseModel):
    """Metadata for an authoritative regulatory source."""
    source_id: str
    authority_name: str
    authority_level: str  # "FEDERAL_MINISTRY", "EMIRATE_DEPARTMENT", "CHAMBER_COMMERCE", "TAX_AUTHORITY"
    jurisdiction: str     # "UAE_FEDERAL", "DUBAI_EMIRATE"
    official_portal_url: str
    authority_weight: float  # 0.0 to 1.0
    last_verified_timestamp: str
    cache_ttl_days: int = 30
    is_active: bool = True
    contact_channels: List[str] = []


OFFICIAL_SOURCE_REGISTRY: Dict[str, OfficialSourceMetadata] = {
    "DUBAI_CHAMBER": OfficialSourceMetadata(
        source_id="DUBAI_CHAMBER",
        authority_name="Dubai Chamber of Commerce",
        authority_level="CHAMBER_COMMERCE",
        jurisdiction="DUBAI_EMIRATE",
        official_portal_url="https://www.dubaichamber.com/en/home/",
        authority_weight=0.95,
        last_verified_timestamp="2026-03-01T00:00:00Z",
        cache_ttl_days=30,
        contact_channels=["customercare@dubaichamber.com", "+971-4-2280000"]
    ),
    "DUBAI_DET": OfficialSourceMetadata(
        source_id="DUBAI_DET",
        authority_name="Dubai Department of Economy and Tourism (DET / DED)",
        authority_level="EMIRATE_DEPARTMENT",
        jurisdiction="DUBAI_EMIRATE",
        official_portal_url="https://www.ded.ae",
        authority_weight=0.98,
        last_verified_timestamp="2026-03-01T00:00:00Z",
        cache_ttl_days=30,
        contact_channels=["info@dubaidet.ae", "+971-4-4455555"]
    ),
    "UAE_FTA": OfficialSourceMetadata(
        source_id="UAE_FTA",
        authority_name="UAE Federal Tax Authority (FTA)",
        authority_level="TAX_AUTHORITY",
        jurisdiction="UAE_FEDERAL",
        official_portal_url="https://tax.gov.ae",
        authority_weight=1.00,
        last_verified_timestamp="2026-03-01T00:00:00Z",
        cache_ttl_days=14,  # Tax rulings require shorter TTL
        contact_channels=["info@tax.gov.ae", "800829"]
    ),
    "UAE_MOE": OfficialSourceMetadata(
        source_id="UAE_MOE",
        authority_name="UAE Ministry of Economy (MoE)",
        authority_level="FEDERAL_MINISTRY",
        jurisdiction="UAE_FEDERAL",
        official_portal_url="https://www.moec.gov.ae",
        authority_weight=1.00,
        last_verified_timestamp="2026-03-01T00:00:00Z",
        cache_ttl_days=30,
        contact_channels=["info@economy.ae", "8001222"]
    ),
    "CBUAE": OfficialSourceMetadata(
        source_id="CBUAE",
        authority_name="Central Bank of the United Arab Emirates",
        authority_level="FEDERAL_MINISTRY",
        jurisdiction="UAE_FEDERAL",
        official_portal_url="https://www.centralbank.ae",
        authority_weight=1.00,
        last_verified_timestamp="2026-03-01T00:00:00Z",
        cache_ttl_days=1,  # FX requires daily verification
        contact_channels=["info@cbuae.gov.ae", "80022823"]
    )
}


def check_source_freshness(source_id: str, max_age_days: Optional[int] = None) -> Dict[str, Any]:
    """Evaluates whether an official source verification is fresh or needs re-checking."""
    if source_id not in OFFICIAL_SOURCE_REGISTRY:
        return {
            "is_fresh": False,
            "status": "UNKNOWN_SOURCE",
            "age_days": None,
            "recommendation": "Reject unallowlisted source or verify manually."
        }

    source = OFFICIAL_SOURCE_REGISTRY[source_id]
    max_days = max_age_days if max_age_days is not None else source.cache_ttl_days

    try:
        last_dt = datetime.fromisoformat(source.last_verified_timestamp.replace("Z", "+00:00"))
        now_dt = datetime.now(timezone.utc)
        age_days = (now_dt - last_dt).days

        is_fresh = age_days <= max_days
        return {
            "source_id": source_id,
            "authority_name": source.authority_name,
            "is_fresh": is_fresh,
            "age_days": age_days,
            "max_allowed_age_days": max_days,
            "status": "FRESH" if is_fresh else "STALE_REVERIFICATION_REQUIRED",
            "authority_weight": source.authority_weight,
            "official_url": source.official_portal_url
        }
    except Exception as e:
        return {
            "source_id": source_id,
            "is_fresh": False,
            "status": f"ERROR_PARSING_DATE: {str(e)}",
            "age_days": None
        }
