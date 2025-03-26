FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for OpenCV and Tesseract
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    tesseract-ocr-eng \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==2.1.1

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock* ./

# Configure Poetry to not create a virtual environment
RUN poetry config virtualenvs.create false

# Install only the dependencies required for document_processing
RUN poetry install --with document_processing --no-root

# Copy shared code and service-specific code
COPY shared/ ./shared/
COPY document_processing/ ./document_processing/

# Create a simple entrypoint file to test the installation
RUN echo "import numpy; import cv2; import pytesseract; import PIL; print('All document_processing dependencies successfully installed!')" > test_deps.py

# Default command to run the FastAPI service
CMD ["uvicorn", "document_processing.app:app", "--host", "0.0.0.0", "--port", "8002"]
