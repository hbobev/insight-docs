FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    # For spaCy and transformers
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false

# Copy dependency files first for better caching
COPY pyproject.toml ./
COPY entity_extraction/pyproject.toml ./entity_extraction/
COPY shared/pyproject.toml ./shared/

# Install dependencies
# Root dependencies first, excluding other microservices
RUN cd /app && poetry install --no-root --no-dev --without api_gateway,document_ingestion,document_processing,task_orchestration

# Copy code
COPY shared ./shared
COPY entity_extraction ./entity_extraction

# Install shared module as a package in editable mode
RUN pip install -e ./shared

# Set working directory to entity_extraction
WORKDIR /app/entity_extraction

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Command will be specified in docker-compose.yml
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8003"]
