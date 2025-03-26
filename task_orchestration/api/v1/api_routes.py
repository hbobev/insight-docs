from fastapi import APIRouter

from api.v1.endpoints import health, workflows

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(workflows.router, prefix="/workflows", tags=["Workflows"])
