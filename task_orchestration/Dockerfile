FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false

# Copy dependency files first for better caching
COPY pyproject.toml ./
COPY task_orchestration/pyproject.toml ./task_orchestration/
COPY shared/pyproject.toml ./shared/

# Install dependencies
# Root dependencies first, excluding other microservices
RUN cd /app && poetry install --no-root --no-dev --without api_gateway,document_ingestion,document_processing,entity_extraction

# Copy code
COPY shared ./shared
COPY task_orchestration ./task_orchestration

# Install shared module as a package in editable mode
RUN pip install -e ./shared

# Set working directory to task_orchestration
WORKDIR /app/task_orchestration

# Command will be specified in docker-compose.yml
# Using a script that can start either the API or Celery worker
COPY task_orchestration/scripts/start.sh ./
RUN chmod +x ./start.sh

CMD ["./start.sh"]
