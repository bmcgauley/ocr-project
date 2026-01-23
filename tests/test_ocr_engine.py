"""Unit tests for OCR engine module."""

import time
from pathlib import Path

import cv2
import numpy as np
import pytest

from src.agents.ocr_engine import OCRResult, run_tesseract


# Check if Tesseract is installed
def is_tesseract_installed():
    """Check if Tesseract binary is available."""
    try:
        import pytesseract

        pytesseract.get_tesseract_version()
        return True
    except Exception:
        return False


# Skip marker for tests requiring Tesseract
requires_tesseract = pytest.mark.skipif(
    not is_tesseract_installed(),
    reason="Tesseract binary not installed. Install from: "
    "https://github.com/UB-Mannheim/tesseract/wiki",
)


class TestRunTesseract:
    """Test suite for Tesseract OCR engine."""

    @pytest.fixture
    def sample_image(self):
        """Create a simple test image with text."""
        # Create white background
        img = np.ones((200, 600, 3), dtype=np.uint8) * 255

        # Add some text
        cv2.putText(
            img,
            "Hello World Test",
            (50, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (0, 0, 0),
            3,
        )

        # Convert to grayscale
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    @pytest.fixture
    def test_document_path(self):
        """Path to test document if it exists."""
        path = Path("tests/sample_documents/test_document.png")
        if path.exists():
            return path
        return None

    @requires_tesseract
    def test_run_tesseract_success(self, sample_image):
        """Test Tesseract runs successfully on valid image."""
        text, confidence, metadata = run_tesseract(sample_image)

        # Verify text extraction
        assert text is not None
        assert isinstance(text, str)
        assert len(text) > 0

        # Verify confidence score
        assert isinstance(confidence, float)
        assert 0.0 <= confidence <= 100.0

        # Verify metadata structure
        assert "word_count" in metadata
        assert "line_count" in metadata
        assert "words" in metadata
        assert "lines" in metadata
        assert "psm_mode" in metadata
        assert "processing_time" in metadata

    @requires_tesseract
    def test_run_tesseract_recognizes_text(self, sample_image):
        """Test that Tesseract recognizes the correct text."""
        text, confidence, metadata = run_tesseract(sample_image, psm_mode=6)

        # Should recognize "Hello" and "World"
        text_lower = text.lower()
        assert "hello" in text_lower or "world" in text_lower

    def test_run_tesseract_invalid_input_none(self):
        """Test Tesseract handles None input."""
        with pytest.raises(ValueError, match="Image cannot be None or empty"):
            run_tesseract(None)

    def test_run_tesseract_invalid_input_empty(self):
        """Test Tesseract handles empty array."""
        empty_img = np.array([])
        with pytest.raises(ValueError, match="Image cannot be None or empty"):
            run_tesseract(empty_img)

    @requires_tesseract
    def test_run_tesseract_psm_modes(self, sample_image):
        """Test different PSM modes work."""
        psm_modes = [3, 6, 11]  # Automatic, single block, sparse text

        for psm in psm_modes:
            text, confidence, metadata = run_tesseract(sample_image, psm_mode=psm)

            assert isinstance(text, str)
            assert isinstance(confidence, float)
            assert metadata["psm_mode"] == psm

    @requires_tesseract
    def test_run_tesseract_min_confidence_filter(self, sample_image):
        """Test that min_confidence threshold filters results."""
        # Run with very high threshold
        text, conf_high, meta_high = run_tesseract(
            sample_image, min_confidence=90
        )

        # Run with low threshold
        text, conf_low, meta_low = run_tesseract(sample_image, min_confidence=30)

        # Low threshold should capture more words
        assert meta_low["word_count"] >= meta_high["word_count"]

    @requires_tesseract
    def test_run_tesseract_confidence_range(self, sample_image):
        """Test confidence scores are in valid range."""
        text, confidence, metadata = run_tesseract(sample_image)

        # Overall confidence
        assert 0.0 <= confidence <= 100.0

        # Word-level confidences
        for word in metadata["words"]:
            assert 0 <= word["confidence"] <= 100

        # Line-level confidences
        for line in metadata["lines"]:
            assert 0.0 <= line["confidence"] <= 100.0
            assert 0 <= line["min_confidence"] <= 100
            assert 0 <= line["max_confidence"] <= 100

    @requires_tesseract
    def test_run_tesseract_word_metadata_structure(self, sample_image):
        """Test word metadata has correct structure."""
        text, confidence, metadata = run_tesseract(sample_image)

        if metadata["words"]:  # If words were detected
            word = metadata["words"][0]

            # Check required fields
            assert "text" in word
            assert "confidence" in word
            assert "box" in word
            assert "line_num" in word

            # Check box structure
            assert "left" in word["box"]
            assert "top" in word["box"]
            assert "width" in word["box"]
            assert "height" in word["box"]

    @requires_tesseract
    def test_run_tesseract_line_metadata_structure(self, sample_image):
        """Test line metadata has correct structure."""
        text, confidence, metadata = run_tesseract(sample_image)

        if metadata["lines"]:  # If lines were detected
            line = metadata["lines"][0]

            # Check required fields
            assert "text" in line
            assert "confidence" in line
            assert "min_confidence" in line
            assert "max_confidence" in line
            assert "word_count" in line

            # Check logical consistency
            assert line["min_confidence"] <= line["confidence"]
            assert line["confidence"] <= line["max_confidence"]
            assert line["word_count"] > 0

    @requires_tesseract
    def test_run_tesseract_processing_time(self, sample_image):
        """Test that processing time is recorded."""
        start = time.time()
        text, confidence, metadata = run_tesseract(sample_image)
        elapsed = time.time() - start

        # Processing time should be recorded and reasonable
        assert "processing_time" in metadata
        assert metadata["processing_time"] > 0
        assert metadata["processing_time"] <= elapsed + 0.1  # Allow small margin

    @requires_tesseract
    def test_run_tesseract_with_real_document(self, test_document_path):
        """Test Tesseract on real test document if available."""
        if test_document_path is None:
            pytest.skip("No test document available")

        img = cv2.imread(str(test_document_path), cv2.IMREAD_GRAYSCALE)
        text, confidence, metadata = run_tesseract(img)

        # Should extract some text
        assert len(text) > 0
        assert metadata["word_count"] > 0
        assert metadata["line_count"] > 0

    @requires_tesseract
    def test_run_tesseract_blank_image(self):
        """Test Tesseract handles blank/white image."""
        # Create completely white image
        blank = np.ones((500, 500), dtype=np.uint8) * 255

        # Should not crash
        text, confidence, metadata = run_tesseract(blank)

        # May have no text or very low confidence
        assert isinstance(text, str)
        assert isinstance(confidence, float)

    @requires_tesseract
    def test_run_tesseract_noisy_image(self, sample_image):
        """Test Tesseract handles noisy image."""
        # Add noise to image
        noise = np.random.randint(0, 50, sample_image.shape, dtype=np.uint8)
        noisy = cv2.add(sample_image, noise)

        # Should still work but may have lower confidence
        text, confidence, metadata = run_tesseract(noisy)

        assert isinstance(text, str)
        assert isinstance(confidence, float)
        assert 0.0 <= confidence <= 100.0


class TestOCRResult:
    """Test suite for OCRResult dataclass."""

    def test_ocr_result_creation(self):
        """Test OCRResult can be created."""
        result = OCRResult(
            text="Sample text",
            confidence=85.5,
            engine="tesseract",
            processing_time=1.2,
        )

        assert result.text == "Sample text"
        assert result.confidence == 85.5
        assert result.engine == "tesseract"
        assert result.processing_time == 1.2
        assert result.metadata == {}

    def test_ocr_result_with_metadata(self):
        """Test OCRResult with metadata."""
        metadata = {"word_count": 10, "line_count": 2}

        result = OCRResult(
            text="Sample text",
            confidence=85.5,
            engine="tesseract",
            processing_time=1.2,
            metadata=metadata,
        )

        assert result.metadata["word_count"] == 10
        assert result.metadata["line_count"] == 2
