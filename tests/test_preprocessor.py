"""Unit tests for preprocessor module."""

import pytest
from pathlib import Path
import numpy as np
import cv2
from src.agents.preprocessor import (
    preprocess_image,
    to_grayscale,
    deskew_image,
    enhance_contrast,
    remove_noise,
    binarize_image,
)


class TestToGrayscale:
    """Test suite for grayscale conversion."""

    def test_to_grayscale_color_image(self) -> None:
        """Test conversion of color image to grayscale."""
        # Create BGR color image
        color_image = np.zeros((100, 100, 3), dtype=np.uint8)
        color_image[:, :] = [255, 0, 0]  # Blue

        gray = to_grayscale(color_image)

        assert len(gray.shape) == 2
        assert gray.shape == (100, 100)

    def test_to_grayscale_already_gray(self) -> None:
        """Test that grayscale image is returned unchanged."""
        gray_image = np.ones((100, 100), dtype=np.uint8) * 128

        result = to_grayscale(gray_image)

        assert len(result.shape) == 2
        assert np.array_equal(result, gray_image)

    def test_to_grayscale_invalid_shape(self) -> None:
        """Test that invalid image shape raises error."""
        invalid_image = np.ones((100, 100, 4), dtype=np.uint8)  # RGBA

        with pytest.raises(ValueError, match="Unsupported image shape"):
            to_grayscale(invalid_image)


class TestDeskewImage:
    """Test suite for image deskewing."""

    def test_deskew_image_straight(self) -> None:
        """Test that straight image is not rotated."""
        # Create straight horizontal lines
        image = np.ones((500, 500), dtype=np.uint8) * 255
        for i in range(0, 500, 50):
            cv2.line(image, (0, i), (500, i), 0, 2)

        deskewed = deskew_image(image)

        # Should have similar dimensions (no significant rotation)
        assert deskewed is not None
        assert deskewed.shape[0] == pytest.approx(image.shape[0], rel=0.2)

    def test_deskew_image_rotated(self) -> None:
        """Test deskewing of rotated image."""
        # Create image with horizontal lines
        image = np.ones((500, 500), dtype=np.uint8) * 255
        for i in range(0, 500, 50):
            cv2.line(image, (0, i), (500, i), 0, 2)

        # Rotate by known angle
        center = (250, 250)
        rotation_matrix = cv2.getRotationMatrix2D(center, 15, 1.0)
        rotated = cv2.warpAffine(image, rotation_matrix, (500, 500))

        # Deskew
        deskewed = deskew_image(rotated)

        # Should produce valid output
        assert deskewed is not None
        assert deskewed.size > 0

    def test_deskew_image_no_lines(self) -> None:
        """Test deskewing when no lines are detected."""
        # Uniform image with no features
        image = np.ones((500, 500), dtype=np.uint8) * 128

        deskewed = deskew_image(image)

        # Should return similar image when no lines detected
        assert deskewed is not None
        assert deskewed.shape == image.shape

    def test_deskew_image_none(self) -> None:
        """Test that None input raises error."""
        with pytest.raises(ValueError, match="cannot be None"):
            deskew_image(None)

    def test_deskew_image_empty(self) -> None:
        """Test that empty array raises error."""
        empty = np.array([])

        with pytest.raises(ValueError, match="cannot be None or empty"):
            deskew_image(empty)


class TestEnhanceContrast:
    """Test suite for contrast enhancement."""

    def test_enhance_contrast_low_contrast(self) -> None:
        """Test that low contrast image is enhanced."""
        # Create low contrast image (narrow range of values)
        low_contrast = np.random.randint(100, 150, (500, 500), dtype=np.uint8)

        enhanced = enhance_contrast(low_contrast)

        # Enhanced image should have wider range of values
        assert enhanced.std() >= low_contrast.std()
        assert enhanced.min() <= low_contrast.min()
        assert enhanced.max() >= low_contrast.max()

    def test_enhance_contrast_preserves_shape(self) -> None:
        """Test that contrast enhancement preserves image shape."""
        image = np.random.randint(0, 256, (300, 400), dtype=np.uint8)

        enhanced = enhance_contrast(image)

        assert enhanced.shape == image.shape

    def test_enhance_contrast_color_input(self) -> None:
        """Test that color image is converted and enhanced."""
        color_image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)

        enhanced = enhance_contrast(color_image)

        # Should return grayscale
        assert len(enhanced.shape) == 2

    def test_enhance_contrast_none(self) -> None:
        """Test that None input raises error."""
        with pytest.raises(ValueError, match="cannot be None"):
            enhance_contrast(None)


class TestRemoveNoise:
    """Test suite for noise removal."""

    def test_remove_noise_reduces_variance(self) -> None:
        """Test that noise removal reduces image variance."""
        # Create image with noise
        clean = np.ones((500, 500), dtype=np.uint8) * 128
        noise = np.random.randint(-20, 20, (500, 500), dtype=np.int16)
        noisy = np.clip(clean + noise, 0, 255).astype(np.uint8)

        denoised = remove_noise(noisy)

        # Denoised should have lower standard deviation
        assert denoised.std() < noisy.std()

    def test_remove_noise_preserves_shape(self) -> None:
        """Test that noise removal preserves image shape."""
        image = np.random.randint(0, 256, (200, 300), dtype=np.uint8)

        denoised = remove_noise(image)

        assert denoised.shape == image.shape

    def test_remove_noise_preserves_edges(self) -> None:
        """Test that bilateral filter preserves edges."""
        # Create image with sharp edge
        image = np.ones((500, 500), dtype=np.uint8) * 50
        image[:, 250:] = 200

        # Add noise
        noise = np.random.randint(-10, 10, (500, 500), dtype=np.int16)
        noisy = np.clip(image + noise, 0, 255).astype(np.uint8)

        denoised = remove_noise(noisy)

        # Edge should still exist (check difference across middle)
        left_mean = denoised[:, 100:150].mean()
        right_mean = denoised[:, 350:400].mean()
        assert abs(right_mean - left_mean) > 50  # Significant difference preserved

    def test_remove_noise_none(self) -> None:
        """Test that None input raises error."""
        with pytest.raises(ValueError, match="cannot be None"):
            remove_noise(None)


class TestBinarizeImage:
    """Test suite for image binarization."""

    def test_binarize_image_output_values(self) -> None:
        """Test that binarized image only contains 0 and 255."""
        image = np.random.randint(0, 256, (500, 500), dtype=np.uint8)

        binary = binarize_image(image)

        # Should only contain black (0) and white (255)
        unique_values = np.unique(binary)
        assert all(val in [0, 255] for val in unique_values)

    def test_binarize_image_preserves_shape(self) -> None:
        """Test that binarization preserves image shape."""
        image = np.random.randint(0, 256, (300, 400), dtype=np.uint8)

        binary = binarize_image(image)

        assert binary.shape == image.shape

    def test_binarize_image_text_like(self) -> None:
        """Test binarization on text-like image."""
        # Create image with varied intensities
        image = np.ones((500, 500), dtype=np.uint8) * 180
        # Add darker rectangle on left
        image[:, :250] = 100
        # Add lighter rectangle on right
        image[:, 250:] = 220

        binary = binarize_image(image)

        # Should be binary (only 0 and 255)
        unique_values = np.unique(binary)
        assert all(val in [0, 255] for val in unique_values)

        # Should contain both black and white pixels
        assert len(unique_values) == 2

    def test_binarize_image_none(self) -> None:
        """Test that None input raises error."""
        with pytest.raises(ValueError, match="cannot be None"):
            binarize_image(None)


class TestPreprocessImage:
    """Test suite for full preprocessing pipeline."""

    def test_preprocess_high_quality(self) -> None:
        """Test that high quality images get minimal processing."""
        # Create high quality image
        image = np.random.randint(0, 256, (2000, 2000, 3), dtype=np.uint8)
        quality_score = 8.5

        processed, error = preprocess_image(image, quality_score)

        assert error is None
        assert processed is not None
        # Should be grayscale only
        assert len(processed.shape) == 2

    def test_preprocess_medium_quality(self) -> None:
        """Test that medium quality images get standard processing."""
        # Create medium quality image
        image = np.random.randint(0, 256, (1000, 1000, 3), dtype=np.uint8)
        quality_score = 5.5

        processed, error = preprocess_image(image, quality_score)

        assert error is None
        assert processed is not None
        assert len(processed.shape) == 2

    def test_preprocess_low_quality(self) -> None:
        """Test that low quality images get full processing."""
        # Create low quality image (small, uniform)
        image = np.ones((200, 200, 3), dtype=np.uint8) * 128
        quality_score = 2.5

        processed, error = preprocess_image(image, quality_score)

        assert error is None
        assert processed is not None
        assert len(processed.shape) == 2
        # Should be binarized (only 0 and 255 values)
        unique_values = np.unique(processed)
        assert all(val in [0, 255] for val in unique_values)

    def test_preprocess_none_image(self) -> None:
        """Test that None image returns error."""
        image, error = preprocess_image(None, 5.0)

        assert error is not None
        assert "cannot be None" in error

    def test_preprocess_empty_image(self) -> None:
        """Test that empty image returns error."""
        empty = np.array([])

        image, error = preprocess_image(empty, 5.0)

        assert error is not None
        assert "cannot be None or empty" in error

    def test_preprocess_grayscale_input(self) -> None:
        """Test preprocessing with grayscale input."""
        # Create grayscale image
        gray_image = np.random.randint(0, 256, (1000, 1000), dtype=np.uint8)
        quality_score = 5.0

        # Need to add third dimension for preprocess_image
        image_3d = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
        processed, error = preprocess_image(image_3d, quality_score)

        assert error is None
        assert processed is not None


class TestIntegration:
    """Integration tests for preprocessing workflows."""

    def test_full_pipeline_workflow(self, tmp_path: Path) -> None:
        """Test complete preprocessing workflow."""
        # Create test document
        doc = np.ones((1000, 1500, 3), dtype=np.uint8) * 255
        # Add text-like content
        for i in range(20):
            y = 100 + i * 40
            cv2.rectangle(doc, (100, y), (1400, y + 20), (0, 0, 0), -1)

        # Save and reload
        test_path = tmp_path / "test_doc.png"
        cv2.imwrite(str(test_path), doc)
        loaded = cv2.imread(str(test_path))

        # Test each processing step
        gray = to_grayscale(loaded)
        assert len(gray.shape) == 2

        enhanced = enhance_contrast(gray)
        assert enhanced.shape == gray.shape

        denoised = remove_noise(enhanced)
        assert denoised.shape == gray.shape

        binary = binarize_image(denoised)
        assert binary.shape == gray.shape
        assert all(val in [0, 255] for val in np.unique(binary))

    def test_preprocessing_quality_levels(self) -> None:
        """Test that different quality levels produce different outputs."""
        # Create base image
        image = np.random.randint(0, 256, (500, 500, 3), dtype=np.uint8)

        # Process with different quality scores
        high_q, _ = preprocess_image(image.copy(), 9.0)
        med_q, _ = preprocess_image(image.copy(), 5.0)
        low_q, _ = preprocess_image(image.copy(), 2.0)

        # All should be valid
        assert high_q is not None
        assert med_q is not None
        assert low_q is not None

        # Low quality should be binarized (only 0 and 255)
        unique_low = np.unique(low_q)
        assert all(val in [0, 255] for val in unique_low)

        # High quality should have more gray values
        unique_high = np.unique(high_q)
        assert len(unique_high) > 2
