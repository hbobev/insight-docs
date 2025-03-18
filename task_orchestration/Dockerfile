FROM python:3.12-slim

WORKDIR /app

# Install system dependencies that might be needed for processing tasks
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==2.1.1

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock* ./

# Configure Poetry to not create a virtual environment
RUN poetry config virtualenvs.create false

# Install only the dependencies required for task_orchestration
# True microservices should be independent in production
RUN poetry install --with task_orchestration --no-root

# Copy shared code and service-specific code
COPY shared/ ./shared/
COPY task_orchestration/ ./task_orchestration/

# Test dependencies
RUN echo "import celery; import redis; print('All task_orchestration dependencies successfully installed!')" > test_deps.py

# Default command to run the FastAPI service
# This will be overridden for the worker in docker-compose.yml
CMD ["uvicorn", "task_orchestration.app:app", "--host", "0.0.0.0", "--port", "8004"]
