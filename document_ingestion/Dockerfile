FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for Pillow
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==2.1.1

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock* ./

# Configure Poetry to not create a virtual environment
RUN poetry config virtualenvs.create false

# Install only the dependencies required for document_ingestion
RUN poetry install --with document_ingestion --no-root

# Copy shared code and service-specific code
COPY shared/ ./shared/
COPY document_ingestion/ ./document_ingestion/

# Test dependencies
RUN echo "import pymongo; import motor; import PIL; print('All document_ingestion dependencies successfully installed!')" > test_deps.py

# Default command to run the FastAPI service
CMD ["uvicorn", "document_ingestion.app:app", "--host", "0.0.0.0", "--port", "8001"]
