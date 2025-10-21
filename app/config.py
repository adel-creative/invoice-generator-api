"""
Application Configuration
"""

import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application Info
    APP_NAME: str = "Invoice Generator API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Base URL - Auto-detect from environment
    BASE_URL: str = os.getenv(
        "BASE_URL",
        # HF auto-provides SPACE_HOST
        os.getenv("SPACE_HOST", "http://localhost:7860")
    )

    # Database - IMPORTANT: Use external PostgreSQL (Supabase)
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./invoices.db"  # Fallback for local dev only
    )

    # JWT Settings
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "your-secret-key-change-in-production-min-32-chars"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # Email Settings (SMTP)
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM_EMAIL: str = os.getenv(
        "SMTP_FROM_EMAIL", "noreply@yourdomain.com")
    SMTP_FROM_NAME: str = os.getenv("SMTP_FROM_NAME", "Invoice Generator")

    # File Storage
    UPLOAD_DIR: str = "static/invoices"
    QR_DIR: str = "static/qr_codes"

    # CORS
    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "*")

    # Rate Limiting
    EMAIL_RATE_LIMIT: int = int(os.getenv("EMAIL_RATE_LIMIT", "5"))

    # Payment (for future use)
    PAYMENT_GATEWAY_URL: Optional[str] = os.getenv("PAYMENT_GATEWAY_URL")
    STRIPE_SECRET_KEY: Optional[str] = os.getenv("STRIPE_SECRET_KEY")
    STRIPE_PUBLISHABLE_KEY: Optional[str] = os.getenv("STRIPE_PUBLISHABLE_KEY")

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
