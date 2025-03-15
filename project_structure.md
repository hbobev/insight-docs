# InsightDocs Project Structure

This document details the directory structure for the InsightDocs automated document processing pipeline.

## Overview

The project follows a microservices architecture with the following services:
- API Gateway
- Document Ingestion
- Document Processing
- Entity Extraction
- Task Orchestration

Each service has its own directory with a consistent structure, and shared components are in a separate `shared` directory.

## Directory Structure

```
insight-docs/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   └── feature.md
│   └── workflows/
│       ├── test.yml
│       └── build.yml
├── api_gateway/
│   ├── __init__.py
│   ├── app.py
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── documents.py
│   │           └── health.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   └── README.md
├── document_ingestion/
│   ├── __init__.py
│   ├── app.py
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── upload.py
│   │           └── health.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── upload_service.py
│   │   └── preprocessing_service.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   └── README.md
├── document_processing/
│   ├── __init__.py
│   ├── app.py
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── processing.py
│   │           └── health.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ocr_service.py
│   │   └── text_extraction_service.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   └── README.md
├── entity_extraction/
│   ├── __init__.py
│   ├── app.py
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── extraction.py
│   │           └── health.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── entity_recognition_service.py
│   │   └── validation_service.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   └── README.md
├── task_orchestration/
│   ├── __init__.py
│   ├── app.py
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── tasks.py
│   │           └── health.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── task_service.py
│   │   └── queue_service.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   └── README.md
├── shared/
│   ├── __init__.py
│   ├── pyproject.toml
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── mongodb.py
│   │   └── postgres.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── document.py
│   │   └── entity.py
│   └── utils/
│       ├── __init__.py
│       ├── logging.py
│       └── file_utils.py
├── data/
│   ├── raw/
│   │   └── .gitkeep
│   ├── processed/
│   │   └── .gitkeep
│   └── models/
│       ├── document_classifier/
│       │   ├── __init__.py
│       │   └── model.py
│       ├── entity_extractor/
│       │   ├── __init__.py
│       │   └── model.py
│       └── layout_analyzer/
│           ├── __init__.py
│           └── model.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── api_gateway/
│   │   │   └── __init__.py
│   │   ├── document_ingestion/
│   │   │   └── __init__.py
│   │   ├── document_processing/
│   │   │   └── __init__.py
│   │   ├── entity_extraction/
│   │   │   └── __init__.py
│   │   └── task_orchestration/
│   │       └── __init__.py
│   ├── integration/
│   │   ├── __init__.py
│   │   └── test_document_flow.py
│   └── e2e/
│       ├── __init__.py
│       └── test_complete_pipeline.py
├── scripts/
│   ├── setup.sh
│   ├── start.sh
│   ├── test.sh
│   └── deploy.sh
├── configs/
│   ├── dev.env
│   ├── test.env
│   └── prod.env
├── .env.example
├── .gitignore
├── docker-compose.yml
├── docker-compose.dev.yml
├── pyproject.toml
├── README.md
└── LICENSE
```

## Service Structure

Each service follows a common structure:

- **app.py**: Main FastAPI application entry point
- **api/**: Contains all API-related code
  - **v1/**: API version 1
    - **router.py**: Main router for the API
    - **endpoints/**: Endpoint implementations
- **services/**: Business logic components
- **core/**: Core configurations and utilities
- **Dockerfile**: Service-specific Docker configuration
- **pyproject.toml**: Service-specific dependencies

## Shared Components

The `shared` directory contains components used across multiple services:

- **config/**: Configuration management
- **database/**: Database connections (MongoDB, PostgreSQL)
- **models/**: Shared data models
- **utils/**: Utility functions and helpers

## Data Management

- **data/raw/**: Raw ingested documents
- **data/processed/**: Processed documents
- **data/models/**: ML models for document processing

## Development and Deployment

- **configs/**: Environment-specific configurations
- **scripts/**: Utility scripts for development and deployment
- **docker-compose.yml**: Main Docker Compose configuration
- **docker-compose.dev.yml**: Development-specific Docker Compose configuration

## Testing

- **tests/unit/**: Unit tests for each service
- **tests/integration/**: Integration tests for service interactions
- **tests/e2e/**: End-to-end tests for complete workflows
