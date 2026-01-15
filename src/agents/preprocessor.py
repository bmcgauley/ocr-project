"""Image Preprocessing Agent.

Handles image enhancement and preprocessing operations for OCR optimization.
"""

import numpy as np
import cv2
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)


def preprocess_image(
    image: np.ndarray, quality_score: float
) -> Tuple[np.ndarray, Optional[str]]:
    """Apply preprocessing pipeline based on quality score.

    Adaptive preprocessing based on image quality:
    - High quality (>=7): Minimal processing (grayscale only)
    - Medium quality (4-7): Standard pipeline (deskew, enhance, denoise)
    - Low quality (<4): Full enhancement (all operations including binarization)

    Args:
        image: Input image as numpy array (BGR format)
        quality_score: Quality score from assess_quality (0-10)

    Returns:
        Tuple of (processed_image, error_message)
        - If successful: (processed image, None)
        - If failed: (original image, error description)

    Example:
        >>> from src.utils.image_utils import load_image, assess_quality
        >>> img, _ = load_image(Path("document.jpg"))
        >>> quality = assess_quality(img)
        >>> processed, err = preprocess_image(img, quality)
    """
    if image is None or image.size == 0:
        return image, "Image cannot be None or empty"

    try:
        processed = image.copy()

        # Always convert to grayscale for processing
        gray = to_grayscale(processed)

        if quality_score >= 7:
            # High quality: minimal processing
            logger.info("High quality image - minimal preprocessing")
            return gray, None

        elif quality_score >= 4:
            # Medium quality: standard pipeline
            logger.info("Medium quality image - standard preprocessing")
            gray = deskew_image(gray)
            gray = enhance_contrast(gray)
            gray = remove_noise(gray)
            return gray, None

        else:
            # Low quality: full enhancement
            logger.info("Low quality image - full preprocessing pipeline")
            gray = deskew_image(gray)
            gray = enhance_contrast(gray)
            gray = remove_noise(gray)
            gray = binarize_image(gray)
            return gray, None

    except Exception as e:
        logger.error(f"Preprocessing failed: {str(e)}")
        return image, f"Preprocessing error: {str(e)}"


def to_grayscale(image: np.ndarray) -> np.ndarray:
    """Convert image to grayscale.

    Args:
        image: Input image (BGR or already grayscale)

    Returns:
        Grayscale image

    Example:
        >>> color_img = cv2.imread("image.jpg")
        >>> gray_img = to_grayscale(color_img)
    """
    if len(image.shape) == 2:
        # Already grayscale
        return image

    if len(image.shape) == 3 and image.shape[2] == 3:
        # Convert BGR to grayscale
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    raise ValueError(f"Unsupported image shape: {image.shape}")


def deskew_image(image: np.ndarray) -> np.ndarray:
    """Deskew rotated image using line detection.

    Uses Hough line transform to detect predominant angles and rotates
    the image to correct skew. Handles angles up to ±45 degrees.

    Args:
        image: Input grayscale image

    Returns:
        Deskewed image

    Raises:
        ValueError: If image is None or empty

    Example:
        >>> skewed_img = cv2.imread("skewed.jpg", cv2.IMREAD_GRAYSCALE)
        >>> straight_img = deskew_image(skewed_img)
    """
    if image is None or image.size == 0:
        raise ValueError("Image cannot be None or empty")

    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    # Edge detection
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Detect lines using Hough transform
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)

    if lines is None or len(lines) == 0:
        # No lines detected, return original
        return image

    # Calculate angles from detected lines
    angles = []
    for line in lines:
        rho, theta = line[0]  # type: ignore[index]
        angle = (theta * 180 / np.pi) - 90
        # Filter out near-vertical lines
        if -45 < angle < 45:
            angles.append(angle)

    if not angles:
        return image

    # Calculate median angle (more robust than mean)
    skew_angle = float(np.median(angles))

    # Only rotate if angle is significant (> 0.5 degrees)
    if abs(skew_angle) < 0.5:
        return image

    # Rotate image to deskew
    h, w = gray.shape[:2]
    center = (w // 2, h // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, skew_angle, 1.0)

    # Calculate new image size to prevent cropping
    cos_angle = abs(rotation_matrix[0, 0])
    sin_angle = abs(rotation_matrix[0, 1])
    new_w = int((h * sin_angle) + (w * cos_angle))
    new_h = int((h * cos_angle) + (w * sin_angle))

    # Adjust rotation matrix for new size
    rotation_matrix[0, 2] += (new_w / 2) - center[0]
    rotation_matrix[1, 2] += (new_h / 2) - center[1]

    # Perform rotation
    deskewed = cv2.warpAffine(
        image,
        rotation_matrix,
        (new_w, new_h),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE,
    )

    logger.info(f"Deskewed image by {skew_angle:.2f} degrees")
    return deskewed


def enhance_contrast(image: np.ndarray) -> np.ndarray:
    """Enhance image contrast using CLAHE (Contrast Limited Adaptive Histogram Equalization).

    CLAHE improves contrast locally in small regions, which is better for
    document images than global histogram equalization.

    Args:
        image: Input grayscale image

    Returns:
        Contrast-enhanced image

    Raises:
        ValueError: If image is None or empty

    Example:
        >>> low_contrast = cv2.imread("faded.jpg", cv2.IMREAD_GRAYSCALE)
        >>> enhanced = enhance_contrast(low_contrast)
    """
    if image is None or image.size == 0:
        raise ValueError("Image cannot be None or empty")

    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    # Create CLAHE object
    # clipLimit: Threshold for contrast limiting (higher = more contrast)
    # tileGridSize: Size of grid for histogram equalization
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

    # Apply CLAHE
    enhanced = clahe.apply(gray)

    return enhanced


def remove_noise(image: np.ndarray) -> np.ndarray:
    """Remove noise from image using bilateral filter.

    Bilateral filter reduces noise while preserving edges, which is
    ideal for document images with text.

    Args:
        image: Input grayscale image

    Returns:
        Denoised image

    Raises:
        ValueError: If image is None or empty

    Example:
        >>> noisy = cv2.imread("noisy.jpg", cv2.IMREAD_GRAYSCALE)
        >>> clean = remove_noise(noisy)
    """
    if image is None or image.size == 0:
        raise ValueError("Image cannot be None or empty")

    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    # Apply bilateral filter
    # d: Diameter of pixel neighborhood
    # sigmaColor: Filter sigma in the color space (larger = more colors mixed)
    # sigmaSpace: Filter sigma in the coordinate space (larger = farther pixels influence)
    denoised = cv2.bilateralFilter(gray, d=9, sigmaColor=75, sigmaSpace=75)

    return denoised


def binarize_image(image: np.ndarray) -> np.ndarray:
    """Binarize image using adaptive thresholding.

    Converts image to binary (black and white) using adaptive thresholding,
    which adjusts the threshold locally. This is better for documents with
    varying lighting conditions.

    Args:
        image: Input grayscale image

    Returns:
        Binarized image (0 or 255 values)

    Raises:
        ValueError: If image is None or empty

    Example:
        >>> gray = cv2.imread("document.jpg", cv2.IMREAD_GRAYSCALE)
        >>> binary = binarize_image(gray)
    """
    if image is None or image.size == 0:
        raise ValueError("Image cannot be None or empty")

    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    # Apply adaptive thresholding
    # blockSize: Size of pixel neighborhood for threshold calculation (must be odd)
    # C: Constant subtracted from weighted mean
    binary = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blockSize=11, C=2
    )

    return binary
