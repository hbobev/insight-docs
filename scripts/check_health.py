import asyncio
import httpx

async def check_service_health(service_name, url):
    """Check the health of a service."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{url}/api/v1/health/")
            if response.status_code == 200:
                status = "healthy"
            else:
                status = f"unhealthy (status code: {response.status_code})"
    except Exception as e:
        status = f"unreachable ({str(e)})"
    
    print(f"{service_name}: {status}")
    return status

async def check_all_services():
    """Check the health of all services in the pipeline."""
    services = {
        "API Gateway": "http://localhost:8000",
        "Document Ingestion": "http://localhost:8001",
        "Document Processing": "http://localhost:8002",
        "Entity Extraction": "http://localhost:8003",
        "Task Orchestration": "http://localhost:8004"
    }
    
    print("Checking service health...\n")
    
    results = {}
    for name, url in services.items():
        status = await check_service_health(name, url)
        results[name] = status
    
    print("\nSummary:")
    all_healthy = all(status == "healthy" for status in results.values())
    print(f"Overall system status: {'HEALTHY' if all_healthy else 'DEGRADED'}")

if __name__ == "__main__":
    asyncio.run(check_all_services())
