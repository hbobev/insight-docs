from fastapi import APIRouter

from api.v1.endpoints import (
    auth,
    document_processing,
    document_uploads,
    extractions,
    health,
    stats,
    users,
    workflows,
)

api_router = APIRouter()

# System Monitoring
api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(stats.router, prefix="/stats", tags=["Statistics"])

# Authentication and User Management
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["User Management"])

# Document Processing Pipeline
api_router.include_router(
    document_uploads.router, prefix="/documents", tags=["Document Management"]
)
api_router.include_router(
    document_processing.router,
    prefix="/document-processing",
    tags=["Document Processing"],
)
api_router.include_router(
    extractions.router, prefix="/extractions", tags=["Extractions"]
)
api_router.include_router(workflows.router, prefix="/workflows", tags=["Workflows"])
