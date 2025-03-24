import os
import shutil
import uuid

from fastapi import UploadFile
from pymongo import MongoClient

from core.config import settings
from schemas.document_schema import (
    DocumentCreate,
    DocumentResponse,
    DocumentStatus,
    DocumentType,
    ValidationResult,
)
from shared.exceptions.base import DataProcessingError, NotFoundError, ValidationError


class DocumentService:
    def __init__(self):
        self.settings = settings
        self.client = MongoClient(self.settings.MONGO_URI)
        self.db = self.client[self.settings.MONGO_DATABASE]
        self.collection = self.db[self.settings.MONGO_COLLECTION]

        # Ensure upload directory exists
        os.makedirs(self.settings.UPLOAD_FOLDER, exist_ok=True)

    def _is_allowed_file(self, filename: str) -> bool:
        """Check if the file extension is allowed."""
        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower() in self.settings.ALLOWED_EXTENSIONS
        )

    async def upload_document(self, file: UploadFile) -> DocumentResponse:
        """Upload a document and save metadata to database."""
        if not file or not file.filename:
            raise ValidationError("No file provided")

        if not self._is_allowed_file(file.filename):
            raise ValidationError(
                f"File extension not allowed. Allowed extensions: {self.settings.ALLOWED_EXTENSIONS}"
            )

        file_extension = (
            file.filename.rsplit(".", 1)[1].lower()
            if file.filename and "." in file.filename
            else ""
        )
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(self.settings.UPLOAD_FOLDER, unique_filename)

        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            document = DocumentCreate(
                filename=unique_filename,
                original_filename=file.filename,
                file_size=os.path.getsize(file_path),
                mime_type=file.content_type,
                file_extension=file_extension,
            )

            document_dict = document.model_dump()
            document_dict["_id"] = str(uuid.uuid4())
            document_dict["storage_path"] = file_path

            self.collection.insert_one(document_dict)

            return DocumentResponse(
                id=document_dict["_id"],
                filename=document.filename,
                original_filename=document.original_filename,
                file_size=document.file_size,
                mime_type=document.mime_type,
                file_extension=document.file_extension,
                upload_timestamp=document.upload_timestamp,
                status=document.status,
                storage_path=file_path,
                document_type=document.document_type,
            )
        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            raise DataProcessingError(f"Failed to upload document: {str(e)}")

    def get_document(self, document_id: str) -> DocumentResponse:
        """Get document by ID."""
        document = self.collection.find_one({"_id": document_id})
        if not document:
            raise NotFoundError("Document", document_id)

        return DocumentResponse(
            id=document["_id"],
            filename=document["filename"],
            original_filename=document["original_filename"],
            file_size=document["file_size"],
            mime_type=document["mime_type"],
            file_extension=document["file_extension"],
            upload_timestamp=document["upload_timestamp"],
            status=DocumentStatus(document["status"]),
            storage_path=document["storage_path"],
            document_type=DocumentType(document["document_type"])
            if document.get("document_type")
            else None,
            processing_timestamp=document.get("processing_timestamp"),
            preview_url=document.get("preview_url"),
        )

    def list_documents(self, skip: int = 0, limit: int = 100) -> list[DocumentResponse]:
        """List all documents with pagination."""
        documents = list(self.collection.find().skip(skip).limit(limit))
        return [
            DocumentResponse(
                id=doc["_id"],
                filename=doc["filename"],
                original_filename=doc["original_filename"],
                file_size=doc["file_size"],
                mime_type=doc["mime_type"],
                file_extension=doc["file_extension"],
                upload_timestamp=doc["upload_timestamp"],
                status=DocumentStatus(doc["status"]),
                storage_path=doc["storage_path"],
                document_type=DocumentType(doc["document_type"])
                if doc.get("document_type")
                else None,
                processing_timestamp=doc.get("processing_timestamp"),
                preview_url=doc.get("preview_url"),
            )
            for doc in documents
        ]

    def validate_document(self, document_id: str) -> ValidationResult:
        """Validate a document and return validation results."""
        document = self.collection.find_one({"_id": document_id})
        if not document:
            raise NotFoundError("Document", document_id)

        # Basic validation
        # In a real implementation, this would include more sophisticated checks
        file_path = document["storage_path"]
        if not os.path.exists(file_path):
            return ValidationResult(
                is_valid=False,
                errors=["Document file not found on disk"],
                confidence_score=0.0,
            )

        # Placeholder for more sophisticated validation
        # In a real implementation, this would include:
        # - Image quality checks
        # - OCR quality assessment
        # - Document type classification
        # - Required fields detection

        # Update document status
        self.collection.update_one(
            {"_id": document_id}, {"$set": {"status": DocumentStatus.VALIDATED.value}}
        )

        return ValidationResult(
            is_valid=True,
            warnings=["Basic validation only. Full validation not implemented."],
            document_type=DocumentType.OTHER,
            confidence_score=0.8,
        )
