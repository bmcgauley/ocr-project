"""OCR Engine Agent.

Handles multiple OCR engines and result aggregation.
"""

import time

import numpy as np
import pytesseract  # type: ignore[import-untyped]
from dataclasses import dataclass, field
from pytesseract import Output  # type: ignore[import-untyped]
from typing import List, Tuple, Dict, Any


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
        data = pytesseract.image_to_data(image, output_type=Output.DICT, config=config)

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
        overall_confidence = sum(confidences) / len(confidences) if confidences else 0.0

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


def run_paddleocr(
    image: np.ndarray,
    use_angle_cls: bool = True,
    min_confidence: float = 0.5,
    lang: str = "en",
) -> Tuple[str, float, Dict[str, Any]]:
    """Run PaddleOCR with angle detection and confidence extraction.

    Args:
        image: Input image (numpy array)
        use_angle_cls: Enable angle classification for rotated text (default: True)
        min_confidence: Minimum confidence threshold for filtering (0.0-1.0)
        lang: Language code (default: "en" for English)

    Returns:
        Tuple of (text, average_confidence, metadata)
        metadata contains detected text blocks, angles, and bounding boxes

    Raises:
        ValueError: If image is None or empty
        RuntimeError: If PaddleOCR fails to process image

    Example:
        >>> img = cv2.imread("document.jpg")
        >>> text, conf, meta = run_paddleocr(img, use_angle_cls=True)
        >>> print(f"Confidence: {conf:.2f}")
    """
    if image is None or image.size == 0:
        raise ValueError("Image cannot be None or empty")

    start_time = time.time()

    try:
        # Import here to avoid loading if not used
        from paddleocr import PaddleOCR  # type: ignore[import-untyped]

        # Initialize PaddleOCR with configuration
        # use_textline_orientation: Enables detection and correction of rotated text
        # lang: Language model to use
        # show_log: Suppress verbose logging
        # device: Use CPU for compatibility
        ocr = PaddleOCR(
            use_textline_orientation=use_angle_cls,
            lang=lang,
            show_log=False,
            device="cpu",  # CPU mode for compatibility
        )

        # Run OCR on image
        # PaddleOCR expects BGR image (OpenCV format)
        result = ocr.ocr(image, cls=use_angle_cls)

        # Parse results
        text_blocks = []
        confidences = []
        full_text_parts = []

        if result and result[0]:
            for line in result[0]:
                # Each line: [box_coordinates, (text, confidence)]
                box = line[0]  # [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
                text_info = line[1]
                text = text_info[0]
                confidence = float(text_info[1])

                # Filter by confidence threshold
                if confidence >= min_confidence:
                    text_blocks.append(
                        {
                            "text": text,
                            "confidence": confidence,
                            "box": {
                                "top_left": box[0],
                                "top_right": box[1],
                                "bottom_right": box[2],
                                "bottom_left": box[3],
                            },
                        }
                    )
                    confidences.append(confidence)
                    full_text_parts.append(text)

        # Calculate overall confidence
        overall_confidence = sum(confidences) / len(confidences) if confidences else 0.0

        # Build full text (join with spaces)
        full_text = " ".join(full_text_parts)

        processing_time = time.time() - start_time

        # Build metadata
        metadata = {
            "block_count": len(text_blocks),
            "blocks": text_blocks,
            "use_angle_cls": use_angle_cls,
            "language": lang,
            "min_confidence_threshold": min_confidence,
            "processing_time": processing_time,
        }

        return full_text, overall_confidence, metadata

    except ImportError as e:
        raise RuntimeError(
            "PaddleOCR not installed. Install with: pip install paddleocr paddlepaddle"
        ) from e
    except Exception as e:
        raise RuntimeError(f"PaddleOCR failed: {str(e)}") from e


def run_easyocr(
    image: np.ndarray,
    languages: list[str] = ["en"],
    min_confidence: float = 0.5,
    use_gpu: bool = False,
) -> Tuple[str, float, Dict[str, Any]]:
    """Run EasyOCR with confidence extraction.

    Args:
        image: Input image (numpy array)
        languages: List of language codes (default: ["en"])
        min_confidence: Minimum confidence threshold for filtering (0.0-1.0)
        use_gpu: Enable GPU acceleration (default: False for compatibility)

    Returns:
        Tuple of (text, average_confidence, metadata)
        metadata contains detected blocks with bounding boxes and confidence

    Raises:
        ValueError: If image is None or empty
        RuntimeError: If EasyOCR fails to process image

    Example:
        >>> img = cv2.imread("document.jpg")
        >>> text, conf, meta = run_easyocr(img, languages=["en"])
        >>> print(f"Confidence: {conf:.2f}")

    Note:
        EasyOCR excels at:
        - Handwritten text
        - Scene text in natural images
        - Mixed language documents
        Use as fallback when Tesseract/PaddleOCR have low confidence.
    """
    if image is None or image.size == 0:
        raise ValueError("Image cannot be None or empty")

    start_time = time.time()

    try:
        # Import here to avoid loading if not used
        import easyocr  # type: ignore[import-untyped]

        # Initialize EasyOCR reader
        # Note: Reader initialization is expensive, consider caching in production
        reader = easyocr.Reader(
            languages,
            gpu=use_gpu,
            quantize=not use_gpu,  # Dynamic quantization for CPU performance
        )

        # Run OCR on image
        # Returns list of [bbox, text, confidence]
        result = reader.readtext(image)

        # Parse results
        text_blocks = []
        confidences = []
        full_text_parts = []

        for detection in result:
            bbox = detection[0]  # [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
            text = detection[1]
            confidence = float(detection[2])

            # Filter by confidence threshold
            if confidence >= min_confidence:
                text_blocks.append(
                    {
                        "text": text,
                        "confidence": confidence,
                        "box": {
                            "top_left": bbox[0],
                            "top_right": bbox[1],
                            "bottom_right": bbox[2],
                            "bottom_left": bbox[3],
                        },
                    }
                )
                confidences.append(confidence)
                full_text_parts.append(text)

        # Calculate overall confidence
        overall_confidence = sum(confidences) / len(confidences) if confidences else 0.0

        # Build full text (join with spaces)
        full_text = " ".join(full_text_parts)

        processing_time = time.time() - start_time

        # Build metadata
        metadata = {
            "block_count": len(text_blocks),
            "blocks": text_blocks,
            "languages": languages,
            "use_gpu": use_gpu,
            "min_confidence_threshold": min_confidence,
            "processing_time": processing_time,
        }

        return full_text, overall_confidence, metadata

    except ImportError as e:
        raise RuntimeError(
            "EasyOCR not installed. Install with: pip install easyocr"
        ) from e
    except Exception as e:
        raise RuntimeError(f"EasyOCR failed: {str(e)}") from e


def ensemble_results(results: List[OCRResult]) -> OCRResult:
    """Combine multiple OCR results using voting.

    Args:
        results: List of OCR results

    Returns:
        Best combined result
    """
    # TODO: Implement ensemble logic (Story 3.4/4.1)
    raise NotImplementedError("Ensemble results not yet implemented")
