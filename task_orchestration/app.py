import logging
from contextlib import asynccontextmanager

# Initialize Celery
from celery import Celery
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.api_routes import api_router
from core.config import settings

logging.basicConfig(
    level=settings.LOG_LEVEL.upper(),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Asynchronous context manager for managing the lifespan of the FastAPI application.

    This context manager logs messages when the Task Orchestration Service starts up and shuts down.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None
    """
    logger.info("Starting up Task Orchestration Service")
    yield
    logger.info("Shutting down Task Orchestration Service")


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application instance
    """
    application = FastAPI(
        title=settings.PROJECT_NAME,
        description="Task Orchestration Service for InsightDocs Pipeline",
        version="0.1.0",
        docs_url=f"{settings.API_V1_PREFIX}/docs",
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
        lifespan=lifespan,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(
        api_router,
        prefix=settings.API_V1_PREFIX,
        tags=["task_orchestration"],
    )

    return application


app = create_application()


celery_app = Celery(
    "task_orchestration",
    broker="amqp://rabbitmq:5672",
    backend="redis://redis:6379/0",
)


celery_app.conf.task_routes = {
    "tasks.document_processing.*": {"queue": "document_processing"},
    "tasks.entity_extraction.*": {"queue": "entity_extraction"},
}

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Task Orchestration Service"}


@app.on_event("startup")
async def startup_event():
    logger.info("Task Orchestration Service starting up")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Task Orchestration Service shutting down")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host=settings.SERVICE_HOST,
        port=settings.SERVICE_PORT,
        reload=settings.DEBUG,
    )
