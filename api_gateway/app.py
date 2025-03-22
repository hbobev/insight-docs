import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.router import api_router
from core.config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Asynchronous context manager for managing the lifespan of the FastAPI application.

    This context manager logs messages when the API Gateway Service starts up and shuts down.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None
    """
    logger.info("Starting up API Gateway Service")
    yield
    logger.info("Shutting down API Gateway Service")


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application instance
    """
    application = FastAPI(
        title=settings.API_GATEWAY_PROJECT_NAME,
        description="API Gateway for Document Processing Pipeline",
        version=settings.API_GATEWAY_VERSION,
        # docs_url=f"{settings.API_GATEWAY_HOST}:{settings.API_GATEWAY_PORT}/docs",
        # openapi_url=f"{settings.API_GATEWAY_HOST}:{settings.API_GATEWAY_PORT}/openapi.json",
        lifespan=lifespan,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.API_GATEWAY_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(api_router, prefix=f"{settings.API_GATEWAY_API_PREFIX}")

    return application


app = create_application()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host=settings.API_GATEWAY_HOST,
        port=settings.API_GATEWAY_PORT,
        reload=settings.DEBUG,
    )
