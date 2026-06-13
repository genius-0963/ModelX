"""
API Dependencies.

Provides dependency injection for database sessions, vector stores,
and agent instances required by the API routes.
"""

from typing import AsyncGenerator, Annotated
from fastapi import Depends

from src.api.auth import get_current_user, User
from src.config.settings import get_settings, Settings
from src.db.session import get_session
from src.db.repositories.session_repo import SessionRepository
from src.db.repositories.task_repo import TaskRepository
from src.db.repositories.memory_repo import MemoryRepository
from src.db.repositories.reflection_repo import ReflectionRepository
from src.rag.vector_store import VectorStoreManager
from src.rag.embeddings import EmbeddingService
from src.rag.retriever import Retriever
from src.rag.ingestion import IngestionPipeline

# Agent instances (acting as singletons for the application)
# In a real app, these might be initialized in the lifespan and stored in app.state
_vector_store = None
_embedding_service = None

async def get_vector_store() -> VectorStoreManager:
    """Get the VectorStoreManager singleton."""
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStoreManager()
    return _vector_store

async def get_embedding_service() -> EmbeddingService:
    """Get the EmbeddingService singleton."""
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service

async def get_retriever(
    vector_store: Annotated[VectorStoreManager, Depends(get_vector_store)],
    embedding_service: Annotated[EmbeddingService, Depends(get_embedding_service)],
) -> Retriever:
    """Get an initialized Retriever."""
    return Retriever(vector_store, embedding_service)

async def get_session_repo(db_session=Depends(get_session)) -> SessionRepository:
    """Get the SessionRepository bound to the current DB session."""
    return SessionRepository(db_session)

async def get_task_repo(db_session=Depends(get_session)) -> TaskRepository:
    """Get the TaskRepository bound to the current DB session."""
    return TaskRepository(db_session)

async def get_memory_repo(db_session=Depends(get_session)) -> MemoryRepository:
    """Get the MemoryRepository bound to the current DB session."""
    return MemoryRepository(db_session)

async def get_reflection_repo(db_session=Depends(get_session)) -> ReflectionRepository:
    """Get the ReflectionRepository bound to the current DB session."""
    return ReflectionRepository(db_session)

# Export standard dependency types for routes
CurrentUser = Annotated[User, Depends(get_current_user)]
DB_SessionRepo = Annotated[SessionRepository, Depends(get_session_repo)]
DB_TaskRepo = Annotated[TaskRepository, Depends(get_task_repo)]
DB_MemoryRepo = Annotated[MemoryRepository, Depends(get_memory_repo)]
DB_ReflectionRepo = Annotated[ReflectionRepository, Depends(get_reflection_repo)]
RAG_Retriever = Annotated[Retriever, Depends(get_retriever)]
