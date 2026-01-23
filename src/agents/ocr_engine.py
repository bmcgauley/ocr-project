"""OCR Engine Agent.

Handles multiple OCR engines and result aggregation.
"""

import time
from pathlib import Path

import cv2
import numpy as np
import pytesseract  # type: ignore[import-untyped]
from dataclasses import dataclass, field
from pytesseract import Output  # type: ignore[import-untyped]
from typing import List, Tuple, Optional, Dict, Any


@dataclass
class OCRResult:
    """Result from OCR engine."""

    text: str
    confidence: float
    engine: str
    processing_time: float
    metadata: Dict[str, Any] = field(default_factory=dict)


def run_all_engines(image: np.ndarray) -> List[OCRResult]:
    """Run all OCR engines on the image.

    Args:
        image: Preprocessed image

    Returns:
        List of OCRResults from all engines
    """
    # TODO: Implement multi-engine OCR (Story 3.4)
    raise NotImplementedError("Multi-engine OCR not yet implemented")


def run_tesseract(
    image: np.ndarray, psm_mode: int = 3, min_confidence: int = 30
) -> Tuple[str, float, Dict[str, Any]]:
    """Run Tesseract OCR with confidence extraction.

    Args:
        image: Input image (numpy array)
        psm_mode: Page segmentation mode (default: 3 = fully automatic)
                 3 = Fully automatic (default)
                 4 = Single column variable sizes (forms)
                 6 = Single uniform block (clean text)
                 11 = Sparse text (complex layouts)
        min_confidence: Minimum confidence threshold for word filtering (0-100)

    Returns:
        Tuple of (text, average_confidence, metadata)
        metadata contains word-level and line-level details

    Raises:
        ValueError: If image is None or empty
        RuntimeError: If Tesseract fails to process image

    Example:
        >>> img = cv2.imread("document.jpg", cv2.IMREAD_GRAYSCALE)
        >>> text, conf, meta = run_tesseract(img, psm_mode=6)
        >>> print(f"Confidence: {conf:.2f}%")
    """
    if image is None or image.size == 0:
        raise ValueError("Image cannot be None or empty")

    start_time = time.time()

    try:
        # Configure Tesseract with specified PSM mode
        # OEM 3 = Default (LSTM + Legacy)
        config = f"--oem 3 --psm {psm_mode}"

        # Extract detailed data with confidence scores
        data = pytesseract.image_to_data(
            image, output_type=Output.DICT, config=config
        )

        # Extract full text for final output
        full_text = pytesseract.image_to_string(image, config=config)

        # Process word-level confidence
        n_boxes = len(data["text"])
        word_results = []
        confidences = []

        for i in range(n_boxes):
            conf = int(data["conf"][i])
            text = data["text"][i].strip()

            # Filter: conf=-1 means no detection, also apply min threshold
            if conf > -1 and text and conf >= min_confidence:
                word_results.append(
                    {
                        "text": text,
                        "confidence": conf,
                        "box": {
                            "left": data["left"][i],
                            "top": data["top"][i],
                            "width": data["width"][i],
                            "height": data["height"][i],
                        },
                        "line_num": data["line_num"][i],
                    }
                )
                confidences.append(conf)

        # Aggregate line-level confidence
        lines: Dict[int, Dict[str, Any]] = {}
        for i in range(n_boxes):
            conf = int(data["conf"][i])
            text = data["text"][i].strip()

            if conf > -1 and text:  # Include all valid detections for lines
                line_key = data["line_num"][i]
                if line_key not in lines:
                    lines[line_key] = {"texts": [], "confs": []}
                lines[line_key]["texts"].append(text)
                lines[line_key]["confs"].append(conf)

        line_results = []
        for line_num, line_data in lines.items():
            if line_data["confs"]:
                avg_conf = sum(line_data["confs"]) / len(line_data["confs"])
                line_results.append(
                    {
                        "text": " ".join(line_data["texts"]),
                        "confidence": avg_conf,
                        "min_confidence": min(line_data["confs"]),
                        "max_confidence": max(line_data["confs"]),
                        "word_count": len(line_data["texts"]),
                    }
                )

        # Calculate overall confidence
        overall_confidence = (
            sum(confidences) / len(confidences) if confidences else 0.0
        )

        processing_time = time.time() - start_time

        # Build metadata
        metadata = {
            "word_count": len(word_results),
            "line_count": len(line_results),
            "words": word_results,
            "lines": line_results,
            "psm_mode": psm_mode,
            "min_confidence_threshold": min_confidence,
            "processing_time": processing_time,
        }

        return full_text.strip(), overall_confidence, metadata

    except Exception as e:
        raise RuntimeError(f"Tesseract OCR failed: {str(e)}") from e


def run_paddleocr(image: np.ndarray) -> Tuple[str, float, Dict[str, Any]]:
    """Run PaddleOCR.

    Args:
        image: Input image

    Returns:
        Tuple of (text, confidence, metadata)
    """
    # TODO: Implement PaddleOCR integration (Story 3.2)
    raise NotImplementedError("PaddleOCR integration not yet implemented")


def run_easyocr(image: np.ndarray) -> Tuple[str, float, Dict[str, Any]]:
    """Run EasyOCR.

    Args:
        image: Input image

    Returns:
        Tuple of (text, confidence, metadata)
    """
    # TODO: Implement EasyOCR integration (Story 3.3)
    raise NotImplementedError("EasyOCR integration not yet implemented")


def ensemble_results(results: List[OCRResult]) -> OCRResult:
    """Combine multiple OCR results using voting.

    Args:
        results: List of OCR results

    Returns:
        Best combined result
    """
    # TODO: Implement ensemble logic (Story 3.4/4.1)
    raise NotImplementedError("Ensemble results not yet implemented")
