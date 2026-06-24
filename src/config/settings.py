"""
Application settings using Pydantic Settings.

All configuration is loaded from environment variables or .env files.
Uses a cached singleton pattern via get_settings() for efficient access.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr, computed_field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration for the Autonomous Agent Platform."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # -------------------------------------------------------------------------
    # LLM Configuration
    # -------------------------------------------------------------------------
    anthropic_api_key: SecretStr = Field(
        ..., description="Anthropic API key for Claude access"
    )
    anthropic_base_url: str | None = Field(
        default=None,
        description="Custom base URL for Anthropic API (e.g., OpenRouter)",
    )
    anthropic_model: str = Field(
        default="claude-sonnet-4-20250514",
        description="Claude model identifier",
    )
    llm_temperature: float = Field(
        default=0.1,
        ge=0.0,
        le=2.0,
        description="LLM temperature for generation",
    )
    llm_max_tokens: int = Field(
        default=8192,
        ge=1,
        le=200000,
        description="Maximum tokens for LLM responses",
    )

    # -------------------------------------------------------------------------
    # Embedding Configuration
    # -------------------------------------------------------------------------
    openai_api_key: SecretStr = Field(
        ..., description="OpenAI API key for embeddings"
    )
    openai_base_url: str | None = Field(
        default=None,
        description="Custom base URL for OpenAI API (e.g., Pekpik)",
    )
    embedding_model: str = Field(
        default="text-embedding-3-large",
        description="OpenAI embedding model name",
    )
    embedding_dimensions: int = Field(
        default=3072,
        description="Embedding vector dimensions",
    )

    # -------------------------------------------------------------------------
    # Alternative LLM Providers (Pekpik API)
    # -------------------------------------------------------------------------
    deepseek_api_key: str | None = Field(
        default=None,
        description="DeepSeek API key",
    )
    deepseek_base_url: str = Field(
        default="https://aiapiv2.pekpik.com/v1",
        description="DeepSeek base URL",
    )
    deepseek_model: str = Field(
        default="deepseek-chat",
        description="DeepSeek model name",
    )

    gemini_api_key: str | None = Field(
        default=None,
        description="Gemini API key",
    )
    gemini_base_url: str = Field(
        default="https://aiapiv2.pekpik.com/v1",
        description="Gemini base URL",
    )
    gemini_model: str = Field(
        default="gemini-2.5-flash",
        description="Gemini model name",
    )

    kimi_api_key: str | None = Field(
        default=None,
        description="Kimi API key",
    )
    kimi_base_url: str = Field(
        default="https://aiapiv2.pekpik.com/v1",
        description="Kimi base URL",
    )
    kimi_model: str = Field(
        default="kimi-k2.5",
        description="Kimi model name",
    )

    qwen_api_key: str | None = Field(
        default=None,
        description="Qwen API key",
    )
    qwen_base_url: str = Field(
        default="https://aiapiv2.pekpik.com/v1",
        description="Qwen base URL",
    )
    qwen_model: str = Field(
        default="qwen/qwen3.6-27b",
        description="Qwen model name",
    )

    nvidia_api_key: str | None = Field(
        default=None,
        description="NVIDIA API key",
    )
    nvidia_base_url: str = Field(
        default="https://aiapiv2.pekpik.com/v1",
        description="NVIDIA base URL",
    )
    nvidia_model: str = Field(
        default="nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
        description="NVIDIA model name",
    )

    # -------------------------------------------------------------------------
    # PostgreSQL Database
    # -------------------------------------------------------------------------
    postgres_host: str = Field(default="localhost")
    postgres_port: int = Field(default=5432)
    postgres_db: str = Field(default="agent_platform")
    postgres_user: str = Field(default="agent")
    postgres_password: SecretStr = Field(default=SecretStr("agent_password"))

    @computed_field  # type: ignore[prop-decorator]
    @property
    def database_url(self) -> str:
        """Async SQLAlchemy database URL."""
        pwd = self.postgres_password.get_secret_value()
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{pwd}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def database_url_sync(self) -> str:
        """Sync database URL for Alembic migrations."""
        pwd = self.postgres_password.get_secret_value()
        return (
            f"postgresql+psycopg://{self.postgres_user}:{pwd}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def database_url_psycopg(self) -> str:
        """Raw psycopg URL for LangGraph checkpointer."""
        pwd = self.postgres_password.get_secret_value()
        return (
            f"postgresql://{self.postgres_user}:{pwd}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    # -------------------------------------------------------------------------
    # Qdrant Vector Database
    # -------------------------------------------------------------------------
    qdrant_url: str = Field(
        default="http://localhost:6333",
        description="Qdrant server URL",
    )
    qdrant_api_key: str | None = Field(
        default=None,
        description="Qdrant API key (optional for local)",
    )

    # -------------------------------------------------------------------------
    # Neo4j Knowledge Graph
    # -------------------------------------------------------------------------
    neo4j_uri: str = Field(
        default="bolt://localhost:7687",
        description="Neo4j connection URI",
    )
    neo4j_user: str = Field(
        default="neo4j",
        description="Neo4j username",
    )
    neo4j_password: SecretStr = Field(
        default=SecretStr("neo4j_password"),
        description="Neo4j password",
    )

    # -------------------------------------------------------------------------
    # Redis Cache
    # -------------------------------------------------------------------------
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL",
    )

    # -------------------------------------------------------------------------
    # Web Search
    # -------------------------------------------------------------------------
    tavily_api_key: str | None = Field(
        default=None,
        description="Tavily API key for web search",
    )

    # -------------------------------------------------------------------------
    # API Security
    # -------------------------------------------------------------------------
    jwt_secret_key: SecretStr = Field(
        default=SecretStr("dev-secret-change-in-production"),
        description="JWT signing secret",
    )
    jwt_algorithm: str = Field(default="HS256")
    jwt_expiration_minutes: int = Field(default=60)

    # -------------------------------------------------------------------------
    # Safety & Limits
    # -------------------------------------------------------------------------
    max_execution_time_seconds: int = Field(
        default=300,
        description="Maximum execution time for sandboxed code",
    )
    max_memory_tokens: int = Field(
        default=128000,
        description="Maximum tokens for memory context",
    )
    sandbox_enabled: bool = Field(
        default=True,
        description="Enable Docker sandbox for code execution",
    )
    max_iterations: int = Field(
        default=50,
        ge=1,
        le=200,
        description="Maximum agent loop iterations per goal",
    )
    max_task_retries: int = Field(
        default=3,
        ge=0,
        le=10,
        description="Maximum retries for failed tasks",
    )

    # -------------------------------------------------------------------------
    # Logging
    # -------------------------------------------------------------------------
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO"
    )
    log_format: Literal["json", "console"] = Field(
        default="json",
        description="Log output format (json for production, console for dev)",
    )

    # -------------------------------------------------------------------------
    # Application
    # -------------------------------------------------------------------------
    project_name: str = Field(
        default="Autonomous Agent Platform",
        description="Application display name",
    )
    version: str = Field(default="0.1.0")
    environment: Literal["development", "staging", "production"] = Field(
        default="development",
        description="Deployment environment",
    )

    # -------------------------------------------------------------------------
    # Server
    # -------------------------------------------------------------------------
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)
    debug: bool = Field(default=False)
    cors_origins: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="Allowed CORS origins",
    )

    @field_validator("anthropic_base_url")
    @classmethod
    def normalize_anthropic_base_url(cls, value: str | None) -> str | None:
        """Normalize Anthropic-compatible provider URLs."""
        if value is None:
            return None

        normalized = value.strip().rstrip("/")
        if not normalized:
            return None

        if normalized == "https://openrouter.ai/api/v1":
            return "https://openrouter.ai/api"

        return normalized


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get cached application settings singleton."""
    return Settings()
