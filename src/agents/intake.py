"""Document Intake Agent.

Handles document loading, quality assessment, and classification.
"""

from pathlib import Path
from typing import Tuple, Optional
from dataclasses import dataclass


@dataclass
class DocumentInfo:
    """Information about a loaded document."""

    path: Path
    quality_score: float  # 0-10 scale
    document_type: str  # 'printed', 'handwritten', 'mixed'
    resolution: Tuple[int, int]  # (width, height)


def load_document(image_path: Path) -> Tuple[Optional[DocumentInfo], Optional[str]]:
    """Load and assess a document image.

    Args:
        image_path: Path to the image file

    Returns:
        Tuple of (document_info, error_message)
    """
    # TODO: Implement document loading
    pass


def classify_document(image_path: Path) -> str:
    """Classify document type.

    Args:
        image_path: Path to the image file

    Returns:
        Document type: 'printed', 'handwritten', or 'mixed'
    """
    # TODO: Implement document classification
    pass
