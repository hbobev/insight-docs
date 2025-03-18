FROM python:3.12-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry==2.1.1

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock* ./

# Configure Poetry to not create a virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies required for api_gateway
RUN poetry install --with api_gateway --no-root

# Copy shared code and service-specific code
COPY shared/ ./shared/
COPY api_gateway/ ./api_gateway/

# Test dependencies
RUN echo "import fastapi; import uvicorn; print('All api_gateway dependencies successfully installed!')" > test_deps.py

# Default command to run the FastAPI service
CMD ["uvicorn", "api_gateway.app:app", "--host", "0.0.0.0", "--port", "8000"]
