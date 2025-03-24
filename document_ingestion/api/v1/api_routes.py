from fastapi import APIRouter

from api.v1.endpoints import document_uploads, document_validation, health

api_router = APIRouter()


api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(
    document_uploads.router, prefix="/documents", tags=["documents"]
)
api_router.include_router(
    document_validation.router, prefix="/documents", tags=["validation"]
)
