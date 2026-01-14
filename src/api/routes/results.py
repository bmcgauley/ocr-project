"""Results retrieval endpoints."""

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/results", tags=["results"])


@router.get("/{doc_id}")
async def get_results(doc_id: str):
    """Get OCR results for a document.

    Args:
        doc_id: Document ID

    Returns:
        Extracted data and confidence scores
    """
    # TODO: Implement results retrieval
    pass
