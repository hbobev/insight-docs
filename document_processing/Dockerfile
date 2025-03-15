FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    # Additional dependencies for OpenCV and Tesseract
    libgl1-mesa-glx \
    libglib2.0-0 \
    tesseract-ocr \
    libtesseract-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false

# Copy dependency files first for better caching
COPY pyproject.toml ./
COPY document_processing/pyproject.toml ./document_processing/
COPY shared/pyproject.toml ./shared/

# Install dependencies
# Root dependencies first, excluding other microservices
RUN cd /app && poetry install --no-root --no-dev --without api_gateway,document_ingestion,entity_extraction,task_orchestration

# Copy code
COPY shared ./shared
COPY document_processing ./document_processing

# Install shared module as a package in editable mode
RUN pip install -e ./shared

# Set working directory to document_processing
WORKDIR /app/document_processing

# Command will be specified in docker-compose.yml
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8002"]
