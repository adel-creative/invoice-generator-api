"""
Configuration Management
Handles all environment variables and application settings
"""

from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database
    DATABASE_URL: str = "sqlite:///./invoices.db"
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Email
    EMAIL_HOST: str
    EMAIL_PORT: int = 587
    EMAIL_USE_TLS: bool = True
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    EMAIL_FROM: str
    EMAIL_FROM_NAME: str = "Invoice Generator"
    
    # App
    APP_NAME: str = "Arabic Invoice Generator API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ALLOWED_ORIGINS: str = "http://localhost:3000"
    
    # File Storage
    UPLOAD_DIR: str = "./static/invoices"
    QR_DIR: str = "./static/qr_codes"
    MAX_FILE_SIZE: int = 5242880  # 5MB
    
    # Rate Limiting
    EMAIL_RATE_LIMIT: int = 5  # emails per hour per user
    
    # Payment
    PAYMENT_BASE_URL: str = "https://pay.yourdomain.com"
    
    # Timezone
    TIMEZONE: str = "Africa/Casablanca"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance
    Using lru_cache to avoid reading .env multiple times
    """
    return Settings()


# Quick access to settings
settings = get_settings()