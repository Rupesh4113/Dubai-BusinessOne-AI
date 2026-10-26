"""Primary FastAPI Application for Dubai BusinessOne AI."""

import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .config import settings
from .auth.router import router as auth_router
from .routers import (
    agent_router,
    approval_router,
    calculator_router,
    knowledge_router,
    health_router
)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Intelligent Digital Operations Agent for the Dubai Chamber Digital AI Agent Competition. Features 4-Tier Zero-Inference Memory, Deterministic Financial Calculations, Official UAE Source Verification, and Risk-Tiered Human Approvals.",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production config can restrict via settings.CORS_ORIGINS
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Measures latency and attaches timing header to all API responses."""
    start_time = time.time()
    response = await call_next(request)
    process_time_ms = round((time.time() - start_time) * 1000, 2)
    response.headers["X-Process-Time-Ms"] = str(process_time_ms)
    response.headers["X-Agent-Engine"] = "DubaiBusinessOne-v1"
    return response


# Include Routers
app.include_router(health_router)
app.include_router(auth_router, prefix="/api/v1")
app.include_router(agent_router, prefix="/api/v1")
app.include_router(approval_router, prefix="/api/v1")
app.include_router(calculator_router, prefix="/api/v1")
app.include_router(knowledge_router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "OPERATIONAL",
        "jurisdiction": "Dubai, United Arab Emirates",
        "documentation": "/docs",
        "api_v1_prefix": "/api/v1",
        "features": [
            "4-Tier Zero-Inference Memory System",
            "Deterministic UAE Financial & Tax Calculation Engines",
            "Official Source Citations (Dubai DET, Dubai Chamber, UAE FTA)",
            "Risk-Tiered Human Supervisor Approval Gates",
            "Multilingual Support (EN, AR, HI, UR, FIL, ML)"
        ]
    }
