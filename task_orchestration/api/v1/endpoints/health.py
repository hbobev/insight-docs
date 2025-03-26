from fastapi import APIRouter, status

router = APIRouter()


@router.get(
    "/",
    summary="Check service health",
    status_code=status.HTTP_200_OK,
)
async def health_check():
    return {
        "status": "healthy",
        "service": "task_orchestration",
        "version": "0.1.0",
    }
