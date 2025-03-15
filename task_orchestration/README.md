# InsightDocs - Task Orchestration Service

The Task Orchestration service manages asynchronous processing tasks across the InsightDocs pipeline, handling task queuing, scheduling, and status tracking.

## Responsibilities

- Coordinate the document processing workflow
- Manage asynchronous task queues
- Track processing status for documents
- Handle retries and error recovery
- Schedule document processing tasks
- Provide notifications for task completion
- Monitor system performance and backlogs

## API Endpoints

Currently implemented:
- `GET /health`: Service health check

Future endpoints will be added as they are implemented.

## Services

- **Task Service**: Manages task lifecycle and status
- **Queue Service**: Interfaces with RabbitMQ for task queuing
- **Worker Service**: Processes tasks from queues

## Technologies

- Celery for task processing
- RabbitMQ as message broker
- Redis for result storage and caching
- MongoDB for persistent task storage

## Local Development

```bash
# Run API with live reload
cd task_orchestration
uvicorn app:app --reload --port 8004

# Run Celery worker
celery -A task_orchestration.services.worker worker --loglevel=info
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
docker build -t insightdocs-task-orchestration -f Dockerfile .
docker run -p 8004:8000 insightdocs-task-orchestration
```
