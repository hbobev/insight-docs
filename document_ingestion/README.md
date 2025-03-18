# InsightDocs - Document Ingestion Service

The Document Ingestion service is responsible for handling document uploads, storing original documents, and performing initial preprocessing before OCR and information extraction.

## Responsibilities

- Accept document uploads in various formats (PDF, images, etc.)
- Validate uploaded documents (file type, size, content)
- Perform image preprocessing (resize, denoise, rotation correction)
- Extract basic metadata (file size, mime type, page count)
- Store original documents securely
- Queue documents for processing
- Track document status

## API Endpoints

Currently implemented:
- `GET /health`: Service health check

Future endpoints will be added as they are implemented.

## Services

- **Upload Service**: Handles document uploads and storage
- **Preprocessing Service**: Performs image enhancement and preparation for OCR

## Storage

Documents are stored in:
- MongoDB for metadata
- File system or object storage (S3/MinIO) for binary content

## Local Development

```bash
# Run with live reload
cd document_ingestion
uvicorn app:app --reload --port 8001
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
docker build -t insightdocs-document-ingestion -f Dockerfile .
docker run -p 8001:8000 insightdocs-document-ingestion
```
