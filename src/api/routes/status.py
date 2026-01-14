"""Processing status endpoints."""

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/status", tags=["status"])


@router.get("/{doc_id}")
async def get_status(doc_id: str):
    """Get processing status for a document.

    Args:
        doc_id: Document ID

    Returns:
        Processing status and progress
    """
    # TODO: Implement status checking
    pass
