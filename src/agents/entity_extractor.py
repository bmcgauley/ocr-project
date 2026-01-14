"""Entity Extraction Agent.

Extracts structured entities from OCR text using regex and NER.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ExtractedEntity:
    """Extracted entity with metadata."""

    type: str  # 'date', 'name', 'number', 'location', etc.
    value: str
    confidence: float
    start_pos: int
    end_pos: int


def extract_entities(text: str) -> Dict[str, List[ExtractedEntity]]:
    """Extract all entities from text.

    Args:
        text: OCR extracted text

    Returns:
        Dictionary of entity_type -> list of entities
    """
    # TODO: Implement entity extraction
    pass


def extract_dates(text: str) -> List[ExtractedEntity]:
    """Extract dates from text.

    Args:
        text: Input text

    Returns:
        List of date entities
    """
    # TODO: Implement date extraction
    pass


def extract_names(text: str) -> List[ExtractedEntity]:
    """Extract person names from text.

    Args:
        text: Input text

    Returns:
        List of name entities
    """
    # TODO: Implement name extraction
    pass


def extract_locations(text: str) -> List[ExtractedEntity]:
    """Extract locations from text.

    Args:
        text: Input text

    Returns:
        List of location entities
    """
    # TODO: Implement location extraction
    pass
