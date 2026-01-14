"""Document upload endpoints."""

from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path

router = APIRouter(prefix="/api/upload", tags=["upload"])


@router.post("/")
async def upload_document(file: UploadFile = File(...)):
    """Upload a document for OCR processing.

    Args:
        file: Uploaded file

    Returns:
        Document ID and status
    """
    # TODO: Implement document upload
    pass
