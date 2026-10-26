"""Configuration settings for Dubai BusinessOne AI."""

from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable overrides."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    APP_NAME: str = "Dubai BusinessOne AI"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "production"
    DEBUG: bool = False

    # Security & Authentication
    SECRET_KEY: str = "dubai-businessone-production-secret-key-change-in-production-2026"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    ADMIN_DEFAULT_EMAIL: str = "admin@businessone.dubai.ae"
    ADMIN_DEFAULT_PASSWORD: str = "DubaiBizOne2026!Secure"

    # Database & Persistence
    DATABASE_URL: str = "sqlite+aiosqlite:///./dubai_businessone.db"
    REDIS_URL: Optional[str] = None  # Falls back to Layer 1 memory cache

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://businessone.dubai.ae"
    ]

    # Model Routing & LLM Provider Settings
    DEFAULT_LLM_PROVIDER: str = "hybrid"  # "local_openweight", "gemini", "vllm", "rule_deterministic"
    OPEN_WEIGHT_MODEL_NAME: str = "Qwen/Qwen2.5-7B-Instruct"
    VLLM_ENDPOINT: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    OPENAI_COMPATIBLE_ENDPOINT: Optional[str] = None
    MAX_TOKENS_PER_TASK: int = 2048

    # Calculation Rules & Regulatory Constants
    UAE_VAT_RATE: float = 0.05
    UAE_CORP_TAX_EXEMPT_THRESHOLD_AED: float = 375000.00
    UAE_CORP_TAX_STANDARD_RATE: float = 0.09
    USD_AED_PEG_RATE: float = 3.6725

    # Memory & Caching
    L1_CACHE_TTL_SECONDS: int = 86400  # 24 hours for verified static regulatory responses
    FRESHNESS_MAX_AGE_DAYS: int = 30  # Max age before requiring official re-verification

    # Notification Endpoints
    ENABLE_NOTIFICATIONS: bool = True
    WHATSAPP_SANDBOX: bool = True
    TEAMS_WEBHOOK_URL: Optional[str] = None
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None


settings = Settings()
