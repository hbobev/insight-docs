from fastapi import FastAPI

app = FastAPI(
    title="InsightDocs - document processing Service",
    description="API for the document processing service of InsightDocs document processing pipeline",
    version="0.1.0",
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "document_processing"}
