# InsightDocs - Entity Extraction Service

The Entity Extraction service is responsible for identifying and extracting structured information from document text using NLP and machine learning techniques.

## Responsibilities

- Extract named entities from document text (names, dates, amounts, etc.)
- Identify document-specific fields based on document type
- Extract tabular data
- Normalize extracted entities (standardize dates, amounts, etc.)
- Provide confidence scores for extracted entities
- Validate extracted data
- Support custom extraction templates for different document types

## API Endpoints

Currently implemented:
- `GET /health`: Service health check

Future endpoints will be added as they are implemented.

## Services

- **Entity Recognition Service**: Extracts entities from document text
- **Validation Service**: Validates extracted entities
- **Template Service**: Manages document-specific extraction templates

## Technologies

- spaCy for named entity recognition
- Hugging Face Transformers for entity extraction
- Custom rules and regex patterns for specific document types
- Machine learning models for field identification

## Local Development

```bash
# Run with live reload
cd entity_extraction
uvicorn app:app --reload --port 8003
```

Dependencies are managed through the root `pyproject.toml` file and should be installed from the project root with `poetry install`.

## Testing

```bash
# Run unit tests
pytest
```

## Docker

```bash
# Build and run with Docker
docker build -t insightdocs-entity-extraction -f Dockerfile .
docker run -p 8003:8000 insightdocs-entity-extraction
```
