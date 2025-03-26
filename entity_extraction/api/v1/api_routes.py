from fastapi import APIRouter

from api.v1.endpoints import extraction, health

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(extraction.router, prefix="/extract", tags=["Extraction"])
