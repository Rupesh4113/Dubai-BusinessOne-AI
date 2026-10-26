"""Verified Official Knowledge and Source Ingestion Router."""

from typing import Optional, List
from fastapi import APIRouter, Query
from ..knowledge import (
    OFFICIAL_SOURCE_REGISTRY,
    check_source_freshness,
    search_verified_knowledge,
    generate_citations,
    RegulatoryRecord
)

router = APIRouter(prefix="/knowledge", tags=["Official Sources & Regulatory Knowledge"])


@router.get("/sources")
def list_sources():
    """Returns official allowable source registry and authority weights."""
    return [s.model_dump() for s in OFFICIAL_SOURCE_REGISTRY.values()]


@router.get("/sources/{source_id}/freshness")
def check_freshness(source_id: str):
    """Checks whether an official source verification is current or requires re-checking."""
    return check_source_freshness(source_id)


@router.get("/search", response_model=List[RegulatoryRecord])
def search_regulations(
    q: str = Query(..., description="Regulatory search query"),
    category: Optional[str] = Query(None, description="Category filter (e.g. BUSINESS_SETUP, CORPORATE_TAX, VAT, CHAMBER_MEMBERSHIP)")
):
    """Searches verified UAE legal articles and executive regulations."""
    return search_verified_knowledge(q, category=category)
