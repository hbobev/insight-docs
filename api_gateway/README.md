# InsightDocs - API Gateway Service

The API Gateway service acts as the entry point for all client applications to the InsightDocs document processing pipeline. It routes requests to the appropriate microservices and handles cross-cutting concerns like authentication, rate limiting, and response formatting.

## Responsibilities

- Provide a unified API endpoint for client applications
- Route requests to appropriate backend microservices
- Handle authentication and authorization
- Implement rate limiting and request validation
- Aggregate responses from multiple services when needed
- Provide API documentation via Swagger/OpenAPI

## API Endpoints

Currently implemented:
- `GET /health`: Service health check

Future endpoints will be added as they are implemented.

## Configuration

Key configuration options:

- `API_PREFIX`: Prefix for all API routes
- `AUTH_ENABLED`: Enable/disable authentication
- `RATE_LIMIT`: Number of requests allowed per minute
- Service URLs for each downstream microservice

## Local Development

```bash
# Run with live reload
cd api_gateway
uvicorn app:app --reload --port 8000
```

Dependencies are managed through the root `pyproject.toml` file and should be installed from the project root with `poetry install`.

## Testing

```bash
# Run unit tests
pytest
```

## Docker

```bash
# Build and run with Docker
docker build -t insightdocs-api-gateway -f Dockerfile .
docker run -p 8000:8000 insightdocs-api-gateway
```
