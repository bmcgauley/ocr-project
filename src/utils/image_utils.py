"""Image utility functions for loading, quality assessment, and saving."""

from pathlib import Path
from typing import Tuple, Optional, Dict, Any
import numpy as np
import cv2
from PIL import Image
import logging

logger = logging.getLogger(__name__)


def load_image(image_path: Path) -> Tuple[Optional[np.ndarray], Optional[str]]:
    """Load image from file with support for multiple formats.

    Supports common image formats (JPG, PNG, TIFF, BMP, etc.) and PDFs.
    For PDFs, converts the first page to an image.

    Args:
        image_path: Path to image file

    Returns:
        Tuple of (image_array, error_message)
        - If successful: (numpy array in BGR format, None)
        - If failed: (None, error description)

    Example:
        >>> img, err = load_image(Path("document.jpg"))
        >>> if err is None:
        ...     print(f"Loaded image with shape: {img.shape}")
    """
    if not image_path.exists():
        return None, f"File not found: {image_path}"

    if not image_path.is_file():
        return None, f"Path is not a file: {image_path}"

    try:
        # Handle PDF files
        if image_path.suffix.lower() == ".pdf":
            return _load_pdf_as_image(image_path)

        # Try loading with OpenCV first (handles most formats)
        image = cv2.imread(str(image_path))

        if image is not None:
            return image, None

        # Fallback to PIL for formats OpenCV doesn't support
        pil_image: Image.Image = Image.open(image_path)

        # Convert PIL image to OpenCV format (BGR)
        if pil_image.mode == "RGBA":
            pil_image = pil_image.convert("RGB")
        elif pil_image.mode not in ("RGB", "L"):
            pil_image = pil_image.convert("RGB")

        image = np.array(pil_image)

        # Convert RGB to BGR for OpenCV compatibility
        if len(image.shape) == 3 and image.shape[2] == 3:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        return image, None

    except Exception as e:
        return None, f"Failed to load image: {str(e)}"


def _load_pdf_as_image(pdf_path: Path) -> Tuple[Optional[np.ndarray], Optional[str]]:
    """Load first page of PDF as image.

    Args:
        pdf_path: Path to PDF file

    Returns:
        Tuple of (image_array, error_message)
    """
    try:
        # Try using pdf2image if available
        try:
            from pdf2image import convert_from_path  # type: ignore

            images = convert_from_path(str(pdf_path), first_page=1, last_page=1)
            if images:
                pil_image = images[0]
                image = np.array(pil_image)
                # Convert RGB to BGR
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                return image, None
            return None, "No pages found in PDF"
        except ImportError:
            return None, "pdf2image not installed. Run: pip install pdf2image"

    except Exception as e:
        return None, f"Failed to load PDF: {str(e)}"


def assess_quality(image: np.ndarray) -> float:
    """Assess image quality on 0-10 scale.

    Evaluates image quality based on:
    - Blur detection (Laplacian variance)
    - Contrast (pixel value standard deviation)
    - Resolution (image dimensions)

    Args:
        image: Input image (BGR or grayscale)

    Returns:
        Quality score (0-10, where 10 is best)
        - 0-3: Poor quality (needs heavy preprocessing)
        - 4-7: Medium quality (needs standard preprocessing)
        - 8-10: High quality (minimal preprocessing needed)

    Raises:
        ValueError: If image is None or empty

    Example:
        >>> img, _ = load_image(Path("document.jpg"))
        >>> score = assess_quality(img)
        >>> if score < 4:
        ...     print("Image needs heavy preprocessing")
    """
    if image is None or image.size == 0:
        raise ValueError("Image cannot be None or empty")

    # Get individual quality metrics
    blur_score = _assess_blur(image)
    contrast_score = _assess_contrast(image)
    resolution_score = _assess_resolution(image)

    # Weighted average (blur is most important for OCR)
    quality_score = (
        (blur_score * 0.5) + (contrast_score * 0.3) + (resolution_score * 0.2)
    )

    # Clamp to 0-10 range and round to 2 decimal places
    return round(max(0.0, min(10.0, quality_score)), 2)


def _assess_blur(image: np.ndarray) -> float:
    """Assess image sharpness using Laplacian variance.

    Args:
        image: Input image

    Returns:
        Blur score (0-10, higher is sharper)
    """
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    # Calculate Laplacian variance
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

    # Map variance to 0-10 scale
    # Empirical thresholds:
    # < 100: Very blurry (0-3)
    # 100-500: Moderate (4-7)
    # > 500: Sharp (8-10)
    if laplacian_var < 100:
        score = (laplacian_var / 100) * 3
    elif laplacian_var < 500:
        score = 3 + ((laplacian_var - 100) / 400) * 4
    else:
        score = 7 + min(((laplacian_var - 500) / 1000) * 3, 3)

    return score


def _assess_contrast(image: np.ndarray) -> float:
    """Assess image contrast using standard deviation.

    Args:
        image: Input image

    Returns:
        Contrast score (0-10, higher is better)
    """
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    # Calculate standard deviation of pixel values
    std_dev = float(np.std(gray))  # type: ignore[arg-type]

    # Map std_dev to 0-10 scale
    # Empirical thresholds:
    # < 20: Very low contrast (0-3)
    # 20-60: Moderate contrast (4-7)
    # > 60: High contrast (8-10)
    score: float
    if std_dev < 20:
        score = (std_dev / 20) * 3
    elif std_dev < 60:
        score = 3 + ((std_dev - 20) / 40) * 4
    else:
        score = 7 + min(((std_dev - 60) / 60) * 3, 3)

    return score


def _assess_resolution(image: np.ndarray) -> float:
    """Assess image resolution quality.

    Args:
        image: Input image

    Returns:
        Resolution score (0-10, higher is better)
    """
    height, width = image.shape[:2]
    total_pixels = height * width

    # Map resolution to 0-10 scale
    # Empirical thresholds for document scanning:
    # < 500k pixels: Low resolution (0-3)
    # 500k-2M pixels: Medium resolution (4-7)
    # > 2M pixels: High resolution (8-10)
    if total_pixels < 500_000:
        score = (total_pixels / 500_000) * 3
    elif total_pixels < 2_000_000:
        score = 3 + ((total_pixels - 500_000) / 1_500_000) * 4
    else:
        score = 7 + min(((total_pixels - 2_000_000) / 2_000_000) * 3, 3)

    return score


def get_quality_details(image: np.ndarray) -> Dict[str, Any]:
    """Get detailed quality assessment breakdown.

    Args:
        image: Input image

    Returns:
        Dictionary with quality metrics:
        - overall_score: Overall quality (0-10)
        - blur_score: Sharpness score (0-10)
        - contrast_score: Contrast score (0-10)
        - resolution_score: Resolution score (0-10)
        - dimensions: (height, width)
        - recommendation: String describing preprocessing needs

    Example:
        >>> img, _ = load_image(Path("document.jpg"))
        >>> details = get_quality_details(img)
        >>> print(f"Overall: {details['overall_score']:.1f}")
        >>> print(f"Recommendation: {details['recommendation']}")
    """
    blur_score = _assess_blur(image)
    contrast_score = _assess_contrast(image)
    resolution_score = _assess_resolution(image)
    overall_score = assess_quality(image)

    # Determine recommendation
    if overall_score >= 7:
        recommendation = "High quality - minimal preprocessing needed"
    elif overall_score >= 4:
        recommendation = "Medium quality - standard preprocessing recommended"
    else:
        recommendation = "Low quality - full enhancement pipeline needed"

    return {
        "overall_score": float(round(overall_score, 2)),
        "blur_score": float(round(blur_score, 2)),
        "contrast_score": float(round(contrast_score, 2)),
        "resolution_score": float(round(resolution_score, 2)),
        "dimensions": (image.shape[0], image.shape[1]),
        "recommendation": recommendation,
    }


def save_image(image: np.ndarray, output_path: Path) -> None:
    """Save image to file.

    Args:
        image: Image to save (BGR format)
        output_path: Output file path

    Raises:
        ValueError: If image is None or empty
        IOError: If save operation fails

    Example:
        >>> img, _ = load_image(Path("input.jpg"))
        >>> save_image(img, Path("output.png"))
    """
    if image is None or image.size == 0:
        raise ValueError("Image cannot be None or empty")

    # Create parent directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        success = cv2.imwrite(str(output_path), image)
        if not success:
            raise IOError(f"Failed to save image to {output_path}")
    except Exception as e:
        raise IOError(f"Failed to save image: {str(e)}")
