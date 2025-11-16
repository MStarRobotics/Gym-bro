"""Application configuration using Pydantic settings."""
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # AI Providers
    OPENAI_API_KEY: str | None = None
    GOOGLE_API_KEY: str | None = None
    AI_PROVIDER: Literal["openai", "google"] = "openai"

    # Razorpay
    RAZORPAY_KEY_ID: str
    RAZORPAY_KEY_SECRET: str

    # Firebase
    FIREBASE_SERVICE_ACCOUNT_PATH: str

    # Socket.io
    SOCKETIO_PORT: int = 3001
    SOCKETIO_CORS_ORIGINS: str = "http://localhost:3000"

    # Environment
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    DEBUG: bool = False

    @property
    def socketio_cors_origins_list(self) -> list[str]:
        """Parse CORS origins into a list."""
        return [origin.strip() for origin in self.SOCKETIO_CORS_ORIGINS.split(",")]


settings = Settings()
