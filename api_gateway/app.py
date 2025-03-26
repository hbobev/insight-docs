import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from api.v1.api_routes import api_router
from core.config import settings
from core.exceptions import register_exception_handlers

logging.basicConfig(
    level=settings.LOG_LEVEL.upper(),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logging.getLogger().handlers[0].formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - [%(request_id)s] - %(message)s",
    defaults={"request_id": "no-request-id"},
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
        docs_url=f"{settings.API_GATEWAY_API_PREFIX}/docs",
        openapi_url=f"{settings.API_GATEWAY_API_PREFIX}/openapi.json",
        lifespan=lifespan,
    )

    register_exception_handlers(application)

    if settings.ENABLE_RATE_LIMIT:
        application.state.limiter = Limiter(
            key_func=get_remote_address,
            default_limits=[
                f"{settings.RATE_LIMIT_MAX_REQUESTS}/{settings.RATE_LIMIT_WINDOW_SECONDS} second"
            ],
        )
        application.add_middleware(SlowAPIMiddleware)
        logger.info(
            f"Rate limiting enabled: {settings.RATE_LIMIT_MAX_REQUESTS} "
            f"requests per {settings.RATE_LIMIT_WINDOW_SECONDS} seconds"
        )

    if settings.APP_ENV == "development":
        logger.info(f"CORS enabled for origins: {settings.API_GATEWAY_CORS_ORIGINS}")

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.API_GATEWAY_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(api_router, prefix=settings.API_GATEWAY_API_PREFIX)

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
