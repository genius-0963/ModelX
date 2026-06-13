"""
FastAPI Application Entry Point.

Configures the FastAPI application, lifespan events, middleware,
and mounts all route routers.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.api.middleware import setup_middleware
from src.api.routes import health, goals, tasks, memory, knowledge, reflections
from src.config.logging import get_logger
from src.config.settings import get_settings

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Manage application lifecycle.
    Initializes database connections, cache, and vector store on startup,
    and cleans them up on shutdown.
    """
    settings = get_settings()
    logger.info("Starting up autonomous agent platform", env=settings.environment)
    
    # Initialization logic would go here (e.g., connect to DBs)
    # This is handled mostly by dependency injection in routes, 
    # but global singletons could be initialized here.
    
    yield
    
    logger.info("Shutting down autonomous agent platform")
    # Cleanup logic goes here


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    settings = get_settings()
    
    app = FastAPI(
        title=settings.project_name,
        description="Phase 1 AGI-Inspired Autonomous Agent Platform",
        version=settings.version,
        lifespan=lifespan,
        docs_url="/docs" if settings.environment != "production" else None,
        redoc_url="/redoc" if settings.environment != "production" else None,
    )
    
    # Setup middleware (CORS, logging, error handling)
    setup_middleware(app, settings)
    
    # Include routers
    app.include_router(health.router)
    app.include_router(goals.router, prefix="/api/v1/goals", tags=["Goals"])
    app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["Tasks"])
    app.include_router(memory.router, prefix="/api/v1/memory", tags=["Memory"])
    app.include_router(knowledge.router, prefix="/api/v1/knowledge", tags=["Knowledge"])
    app.include_router(reflections.router, prefix="/api/v1/reflections", tags=["Reflections"])
    
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        """Catch-all exception handler to prevent leaking sensitive info."""
        logger.error("Unhandled exception", path=request.url.path, error=str(exc))
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error. Please try again later."},
        )

    return app


app = create_app()
