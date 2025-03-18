from fastapi import FastAPI

app = FastAPI(
    title=f"InsightDocs - task orchestration Service",
    description=f"API for the task orchestration service of InsightDocs document processing pipeline",
    version="0.1.0"
)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "task_orchestration"}
