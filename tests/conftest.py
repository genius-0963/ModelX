"""Shared pytest fixtures for the autonomous agent platform test suite."""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pydantic import SecretStr


# ---------------------------------------------------------------------------
# Dummy settings values
# ---------------------------------------------------------------------------
_DUMMY_SETTINGS = {
    "anthropic_api_key": SecretStr("sk-ant-test-dummy-key-000"),
    "openai_api_key": SecretStr("sk-test-dummy-openai-key-000"),
    "anthropic_model": "claude-sonnet-4-20250514",
    "embedding_model": "text-embedding-3-large",
    "embedding_dimensions": 3072,
    "llm_temperature": 0.1,
    "llm_max_tokens": 8192,
    "postgres_host": "localhost",
    "postgres_port": 5432,
    "postgres_db": "test_agent_platform",
    "postgres_user": "test_agent",
    "postgres_password": SecretStr("test_password"),
    "qdrant_url": "http://localhost:6333",
    "qdrant_api_key": None,
    "redis_url": "redis://localhost:6379/0",
    "tavily_api_key": None,
    "jwt_secret_key": SecretStr("test-jwt-secret"),
    "jwt_algorithm": "HS256",
    "jwt_expiration_minutes": 60,
    "max_execution_time_seconds": 300,
    "max_memory_tokens": 128000,
    "sandbox_enabled": True,
    "max_iterations": 50,
    "max_task_retries": 3,
    "log_level": "DEBUG",
    "log_format": "console",
    "project_name": "Test Agent Platform",
    "version": "0.1.0-test",
    "environment": "development",
    "host": "0.0.0.0",
    "port": 8000,
    "debug": True,
    "cors_origins": ["http://localhost:3000"],
}


def _make_mock_settings() -> MagicMock:
    """Build a MagicMock that behaves like a Settings instance."""
    mock = MagicMock()
    for key, value in _DUMMY_SETTINGS.items():
        setattr(mock, key, value)
    # Computed properties
    mock.database_url = (
        "postgresql+asyncpg://test_agent:test_password@localhost:5432/test_agent_platform"
    )
    mock.database_url_sync = (
        "postgresql+psycopg://test_agent:test_password@localhost:5432/test_agent_platform"
    )
    mock.database_url_psycopg = (
        "postgresql://test_agent:test_password@localhost:5432/test_agent_platform"
    )
    return mock


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def mock_settings():
    """Patch get_settings to return deterministic test settings."""
    settings = _make_mock_settings()
    with patch("src.config.settings.get_settings", return_value=settings):
        yield settings


@pytest.fixture()
def mock_llm():
    """Patch ChatAnthropic to return a mock LLM that produces valid JSON."""
    llm_instance = AsyncMock()
    default_response = MagicMock()
    default_response.content = json.dumps({
        "intent": "Test goal intent",
        "scope": "small",
        "domain": "testing",
        "constraints": [],
        "success_criteria": ["Tests pass"],
        "required_capabilities": ["research"],
        "estimated_complexity": 2,
        "risks": [],
    })
    llm_instance.ainvoke = AsyncMock(return_value=default_response)

    with patch("langchain_anthropic.ChatAnthropic", return_value=llm_instance) as mock_cls:
        mock_cls.return_value = llm_instance
        yield llm_instance


@pytest.fixture()
def mock_db_session():
    """Provide an AsyncMock database session."""
    session = AsyncMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.close = AsyncMock()
    session.execute = AsyncMock()
    session.flush = AsyncMock()
    session.refresh = AsyncMock()
    return session


@pytest.fixture()
def mock_vector_store():
    """Provide a mocked VectorStoreManager."""
    store = AsyncMock()
    store.initialize = AsyncMock()
    store.upsert = AsyncMock()
    store.upsert_batch = AsyncMock()
    store.search = AsyncMock(return_value=[])
    store.delete = AsyncMock()
    store.get = AsyncMock(return_value=None)
    store.count = AsyncMock(return_value=0)
    store.close = AsyncMock()
    return store


@pytest.fixture()
def mock_embedding_service():
    """Provide a mocked EmbeddingService returning deterministic 3072-dim vectors."""
    service = AsyncMock()
    dummy_vector = [0.1] * 3072
    service.embed_text = AsyncMock(return_value=dummy_vector)
    service.embed_batch = AsyncMock(
        side_effect=lambda texts, **kw: [dummy_vector] * len(texts)
    )
    service.model = "text-embedding-3-large"
    service.dimensions = 3072
    service.clear_cache = MagicMock()
    service.cache_size = 0
    return service
