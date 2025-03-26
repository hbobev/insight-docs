import logging

import httpx

from core.config import settings

logger = logging.getLogger(__name__)


async def upload_document(file_content, filename, content_type, metadata=None):
    """Upload a document to the document ingestion service."""
    try:
        async with httpx.AsyncClient() as client:
            files = {"file": (filename, file_content, content_type)}
            form_data = {}
            if metadata:
                form_data["metadata"] = metadata

            response = await client.post(
                f"{settings.DOCUMENT_INGESTION_SERVICE_URL}/api/v1/upload/",
                files=files,
                data=form_data,
            )
            return response.json()
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        raise


async def create_workflow(document_id):
    """Create a document processing workflow."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.TASK_ORCHESTRATION_SERVICE_URL}/api/v1/workflows/",
                json={"document_id": document_id},
            )
            return response.json()
    except Exception as e:
        logger.error(f"Error creating workflow: {str(e)}")
        raise


async def get_workflow_status(workflow_id):
    """Get the status of a workflow."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.TASK_ORCHESTRATION_SERVICE_URL}/api/v1/workflows/{workflow_id}"
            )
            return response.json()
    except Exception as e:
        logger.error(f"Error getting workflow status: {str(e)}")
        raise
