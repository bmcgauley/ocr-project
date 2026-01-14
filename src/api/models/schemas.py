"""Pydantic models for API requests and responses."""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class DocumentUploadResponse(BaseModel):
    """Response after document upload."""

    document_id: str
    status: str
    message: str


class ProcessingStatus(BaseModel):
    """Document processing status."""

    document_id: str
    status: str  # 'queued', 'processing', 'completed', 'failed'
    progress: float = Field(ge=0, le=100)  # Percentage
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class OCRResults(BaseModel):
    """OCR extraction results."""

    document_id: str
    extracted_data: Dict[str, Any]
    confidence: float = Field(ge=0, le=1)
    processing_time: float
    review_required: bool
