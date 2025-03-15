#!/bin/bash
# This script allows the container to start either the API or a Celery worker

# Default to API if not specified
SERVICE_TYPE=${SERVICE_TYPE:-api}

if [ "$SERVICE_TYPE" = "api" ]; then
    echo "Starting Task Orchestration API..."
    exec uvicorn app:app --host 0.0.0.0 --port 8004
elif [ "$SERVICE_TYPE" = "worker" ]; then
    echo "Starting Celery worker..."
    exec celery -A worker worker --loglevel=info
else
    echo "Unknown SERVICE_TYPE: $SERVICE_TYPE"
    echo "Use 'api' or 'worker'"
    exit 1
fi
