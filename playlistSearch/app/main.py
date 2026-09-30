import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.clients import qdrant_client, groq_client
from app.db.base import Base
from app.db.session import engine
from app.db.vector_store import get_or_create_collection


# Setup logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Handles startup and shutdown logic for the FastAPI application.
    Application lifespan context manager: handles startup and shutdown logic.
    Creates database tables automatically if they don't already exist.
    """
    logger.info("Initializing database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized successfully.")
    except Exception as e:
        logger.error(f"Error during database initialization: {e}", exc_info=True)
    
    
    # Create the Qdrant collection if it doesn't exist
    logger.info("Initializing Qdrant collection...")
    try:
        await get_or_create_collection(qdrant_client)
        logger.info("Qdrant collection initialized successfully.")
    except Exception as e:
        logger.error(f"Error during Qdrant collection initialization: {e}", exc_info=True)
    yield
    logger.info("Application shutdown completed.")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include API v1 router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get(
    "/",
    status_code=status.HTTP_200_OK,
    tags=["root"],
    summary="Root API info",
)
def root():
    """
    Welcome endpoint providing API status and documentation links.
    """
    return {
        "title": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "online",
        "docs": "/docs",
        "api_v1": settings.API_V1_STR,
    }


@app.get(
    "/health",
    status_code=status.HTTP_200_OK,
    tags=["health"],
    summary="Health check endpoint",
)
def health_check():
    """
    Liveness and health check endpoint for monitoring/load balancers.
    """
    return {"status": "healthy", "database": "connected"}
