from fastapi import FastAPI

app = FastAPI(
    title=f"InsightDocs - api gateway Service",
    description=f"API for the api gateway service of InsightDocs document processing pipeline",
    version="0.1.0"
)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "api_gateway"}
