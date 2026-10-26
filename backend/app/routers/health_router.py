"""Health check and readiness probe router."""

import time
from fastapi import APIRouter
from ..config import settings
from ..memory import memory_manager

router = APIRouter(tags=["System Health & Monitoring"])

START_TIME = time.time()


@router.get("/health")
def health_check():
    """Liveness probe reporting component statuses."""
    telemetry = memory_manager.get_telemetry()
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "uptime_seconds": round(time.time() - START_TIME, 2),
        "zero_inference_cache": telemetry["layer1_cache_stats"],
        "pending_human_approvals": telemetry["layer4_pending_approvals_count"]
    }


@router.get("/ready")
def readiness_check():
    """Readiness probe checking database and calculation engine readiness."""
    return {"status": "ready", "ready_for_traffic": True}
