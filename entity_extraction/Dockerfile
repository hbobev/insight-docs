FROM python:3.12-slim

WORKDIR /app

# Install dependencies needed for transformers and spaCy
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==2.1.1

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock* ./

# Configure Poetry to not create a virtual environment
RUN poetry config virtualenvs.create false

# Install only the dependencies required for entity_extraction
RUN poetry install --with entity_extraction --no-root

# Copy shared code and service-specific code
COPY shared/ ./shared/
COPY entity_extraction/ ./entity_extraction/

# Download a small spaCy model for testing
RUN python -m spacy download en_core_web_sm

# Test dependencies
RUN echo "import transformers; import spacy; import pandas; print('All entity_extraction dependencies successfully installed!')" > test_deps.py

# Default command to run the FastAPI service
CMD ["uvicorn", "entity_extraction.app:app", "--host", "0.0.0.0", "--port", "8003"]
