"""
Main router for the API Gateway.
Includes all endpoint routers from different modules.
"""
from fastapi import APIRouter

from api.v1.endpoints import health

api_router = APIRouter()


api_router.include_router(health.router, prefix="/health", tags=["Health"])
