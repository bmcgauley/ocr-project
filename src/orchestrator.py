"""Main orchestrator for OCR pipeline.

Coordinates all agents to process documents end-to-end.
"""

from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ProcessingResult:
    """Result of document processing."""

    document_id: str
    success: bool
    extracted_data: Dict[str, Any]
    confidence: float
    processing_time: float
    error_message: Optional[str] = None


def process_document(image_path: Path) -> ProcessingResult:
    """Process a single document through the full pipeline.

    Pipeline stages:
    1. Intake: Load and assess quality
    2. Preprocessing: Enhance image
    3. OCR: Extract text with multiple engines
    4. Entity Extraction: Extract structured data
    5. Formatting: Generate CSV output

    Args:
        image_path: Path to document image

    Returns:
        ProcessingResult with extracted data
    """
    # TODO: Implement full pipeline orchestration
    pass


def process_batch(image_paths: list[Path], output_dir: Path) -> list[ProcessingResult]:
    """Process multiple documents.

    Args:
        image_paths: List of image paths
        output_dir: Output directory for results

    Returns:
        List of ProcessingResults
    """
    # TODO: Implement batch processing
    pass
