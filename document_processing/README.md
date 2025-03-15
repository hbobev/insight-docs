# InsightDocs - Document Processing Service

The Document Processing service performs optical character recognition (OCR) and other document analysis tasks to convert document images into machine-readable text and understand document layout.

## Responsibilities

- Perform OCR on document images
- Analyze document layout and structure
- Identify text regions, tables, and other document elements
- Classify document types
- Extract text from different document formats
- Process and normalize extracted text
- Provide confidence scores for OCR results

## API Endpoints

Currently implemented:
- `GET /health`: Service health check

Future endpoints will be added as they are implemented.

## Services

- **OCR Service**: Performs text extraction from images
- **Text Extraction Service**: Extracts and normalizes text from OCR results
- **Document Classification Service**: Identifies document types
- **Layout Analysis Service**: Analyzes document structure

## Technologies

- Tesseract OCR for text extraction
- OpenCV for image processing
- LayoutParser for document layout analysis
- Hugging Face Transformers for document classification

## Local Development

```bash
# Run with live reload
cd document_processing
uvicorn app:app --reload --port 8002
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
docker build -t insightdocs-document-processing -f Dockerfile .
docker run -p 8002:8000 insightdocs-document-processing
```
