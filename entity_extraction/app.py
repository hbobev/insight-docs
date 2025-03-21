from fastapi import FastAPI

app = FastAPI(
    title="InsightDocs - entity extraction Service",
    description="API for the entity extraction service of InsightDocs document processing pipeline",
    version="0.1.0",
)


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy", "service": "entity_extraction"}
