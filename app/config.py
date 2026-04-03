from functools import lru_cache
from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # App
    app_env: Literal["development", "staging", "production"] = "development"
    debug: bool = False
    secret_key: str = "dev-secret-key"

    # Database
    database_url: str = "postgresql+asyncpg://postgres:password@localhost:5432/call_analyzer"
    db_pool_size: int = 10
    db_max_overflow: int = 20

    # Anthropic
    anthropic_api_key: str = ""
    default_llm_model: str = "claude-sonnet-4-6"
    llm_max_tokens: int = 4096

    # CORS
    cors_origins: list[str] = ["http://localhost:3000"]

    # Analysis
    analysis_chunk_size: int = 8000

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str):
            import json
            return json.loads(v)
        return v


@lru_cache
def get_settings() -> Settings:
    return Settings()
