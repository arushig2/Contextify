"""
Application configuration.

This module centralizes all environment-based configuration
using Pydantic Settings.

Every module in the application should import the shared
`settings` instance instead of reading environment variables
directly.

Responsibilities:
- Load environment variables
- Validate configuration
- Provide application settings
"""
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )
    # -------------------------
    # Application
    # -------------------------
    app_name: str = "Contextify"
    app_env: Literal["local", "development", "production"] = "local"
    log_level: str = "INFO"

    # -------------------------
    # Gemini
    # -------------------------
    gemini_api_key: str | None = None
    gemini_model: str | None = None

    # -------------------------
    # Embeddings
    # -------------------------
    embedding_model: str | None = None
    hf_api_key: str | None = None

    # -------------------------
    # Qdrant
    # -------------------------
    qdrant_url: str | None = None
    qdrant_api_key: str | None = None
    qdrant_collection: str | None = None

settings = Settings()