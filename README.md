# InsightDocs

InsightDocs is an automated document processing pipeline that extracts structured information from unstructured documents like invoices, receipts, forms, and other business documents. The system uses computer vision and NLP techniques to identify document types, extract relevant fields, validate information, and store results in a structured format.

## Features

- **Document Ingestion**: Upload and preprocess documents from various sources
- **Document Classification**: Automatically identify document types
- **OCR and Text Extraction**: Convert document images to machine-readable text
- **Named Entity Recognition**: Extract key fields and data points
- **Data Validation**: Verify extracted information with confidence scoring
- **Structured Output**: Store processed data in standardized formats
- **REST API**: Comprehensive API endpoints for integration
- **Feedback Loop**: Continuous model improvement through user feedback

## Architecture

InsightDocs follows a microservices architecture with the following components:

- **API Gateway**: Central entry point for all client requests
- **Document Ingestion Service**: Handles document uploads and preprocessing
- **Document Processing Service**: Performs OCR and text extraction
- **Entity Extraction Service**: Extracts structured information from text
- **Task Orchestration Service**: Manages asynchronous processing workflows

## Tech Stack

- **Core Framework**: FastAPI
- **Document Processing**: Tesseract OCR, OpenCV, PyPDF2, spaCy
- **ML Components**: Hugging Face Transformers, layoutparser
- **Data Storage**: MongoDB (documents), PostgreSQL (structured data)
- **Pipeline Orchestration**: Celery, RabbitMQ
- **Containerization**: Docker, Docker Compose
- **CI/CD**: GitHub Actions

## Getting Started

### Prerequisites

- Python 3.12+
- Docker and Docker Compose
- Poetry (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/hbobev/insight-docs.git
   cd insight-docs
   ```

2. Set up the environment:
   ```bash
   make setup
   # Edit .env with your specific settings
   ```

### Development Commands

This project uses a Makefile to simplify common development tasks:

- `make setup` - Set up the development environment (install dependencies)
- `make install` - Explicitly install dependencies
- `make test` - Run tests
- `make format` - Format code with black and isort
- `make lint` - Run linters (flake8 and mypy)
- `make run` - Start the development servers via docker-compose
- `make clean` - Clean up build artifacts and caches
- `make docker-build` - Build Docker images
- `make docker-up` - Start Docker containers
- `make docker-down` - Stop Docker containers

### Running with Docker

Start all services with Docker Compose:

```bash
make docker-up
```

Alternatively, you can use Docker Compose directly:

```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

### Running Locally

Start each service individually:

```bash
# API Gateway
cd api_gateway
uvicorn app:app --reload --port 8000

# Document Ingestion
cd document_ingestion
uvicorn app:app --reload --port 8001

# Document Processing
cd document_processing
uvicorn app:app --reload --port 8002

# Entity Extraction
cd entity_extraction
uvicorn app:app --reload --port 8003

# Task Orchestration
cd task_orchestration
uvicorn app:app --reload --port 8004
```

## API Documentation

Once the services are running, you can access the interactive API documentation:

- API Gateway: http://localhost:8000/docs
- Document Ingestion: http://localhost:8001/docs
- Document Processing: http://localhost:8002/docs
- Entity Extraction: http://localhost:8003/docs
- Task Orchestration: http://localhost:8004/docs

## Development

### Project Structure

The project follows a modular structure with separate directories for each service. See [project_structure.md](project_structure.md) for detailed information.

### Running Tests

```bash
./scripts/test.sh
```

This will run unit, integration, and end-to-end tests.

### Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## Deployment

### Development Environment

For development:

```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

### Production Environment

For production:

```bash
docker-compose up -d
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [spaCy](https://spacy.io/)
- [Hugging Face Transformers](https://huggingface.co/transformers/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [layoutparser](https://layout-parser.github.io/)
