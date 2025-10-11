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
    DEBUG: bool = False

    # Base URL (auto-detect or set manually)
    BASE_URL: str = os.getenv(
        "BASE_URL",
        "https://screeching-tildi-adelzidoune-ca9a7151.koyeb.app"
    )

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./invoices.db"
    )

    # JWT Settings
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "your-secret-key-change-in-production-min-32-chars"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

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
    ALLOWED_ORIGINS: str = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:3000,http://localhost:8000,https://screeching-tildi-adelzidoune-ca9a7151.koyeb.app"
    )

    # Rate Limiting
    EMAIL_RATE_LIMIT: int = 5  # emails per hour per user

    # Payment (for future use)
    PAYMENT_GATEWAY_URL: Optional[str] = None
    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_PUBLISHABLE_KEY: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
