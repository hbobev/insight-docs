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
COPY api_gateway/pyproject.toml ./api_gateway/
COPY shared/pyproject.toml ./shared/

# Install dependencies
# Root dependencies first, excluding other microservices
RUN cd /app && poetry install --no-root --no-dev --without document_ingestion,document_processing,entity_extraction,task_orchestration

# Copy code
COPY shared ./shared
COPY api_gateway ./api_gateway

# Install shared module as a package in editable mode
RUN pip install -e ./shared

# Set working directory to api_gateway
WORKDIR /app/api_gateway

# Command will be specified in docker-compose.yml
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
