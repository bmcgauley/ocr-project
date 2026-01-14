"""Unit tests for image_utils module."""

import pytest
from pathlib import Path
import numpy as np
import cv2
from src.utils.image_utils import (
    load_image,
    assess_quality,
    get_quality_details,
    save_image,
    _assess_blur,
    _assess_contrast,
    _assess_resolution,
)


class TestLoadImage:
    """Test suite for image loading functions."""

    def test_load_image_success_jpg(self, tmp_path: Path) -> None:
        """Test loading a valid JPG image."""
        # Create a test image
        test_image_path = tmp_path / "test.jpg"
        test_array = np.zeros((100, 100, 3), dtype=np.uint8)
        test_array[:, :] = [255, 0, 0]  # Blue image in BGR
        cv2.imwrite(str(test_image_path), test_array)

        # Load the image
        image, error = load_image(test_image_path)

        assert error is None
        assert image is not None
        assert image.shape == (100, 100, 3)
        # JPG is lossy, so check approximate equality instead of exact
        assert np.allclose(image, test_array, atol=5)

    def test_load_image_success_png(self, tmp_path: Path) -> None:
        """Test loading a valid PNG image."""
        test_image_path = tmp_path / "test.png"
        test_array = np.zeros((50, 50, 3), dtype=np.uint8)
        test_array[:, :] = [0, 255, 0]  # Green image in BGR
        cv2.imwrite(str(test_image_path), test_array)

        image, error = load_image(test_image_path)

        assert error is None
        assert image is not None
        assert image.shape == (50, 50, 3)

    def test_load_image_grayscale(self, tmp_path: Path) -> None:
        """Test loading a grayscale image."""
        test_image_path = tmp_path / "test_gray.png"
        test_array = np.ones((100, 100), dtype=np.uint8) * 128
        cv2.imwrite(str(test_image_path), test_array)

        image, error = load_image(test_image_path)

        assert error is None
        assert image is not None
        # OpenCV may load grayscale as 2D or 3D depending on format
        assert len(image.shape) in (2, 3)

    def test_load_image_file_not_found(self, tmp_path: Path) -> None:
        """Test loading a non-existent file."""
        non_existent_path = tmp_path / "nonexistent.jpg"

        image, error = load_image(non_existent_path)

        assert image is None
        assert error is not None
        assert "not found" in error.lower()

    def test_load_image_invalid_path(self, tmp_path: Path) -> None:
        """Test loading with a directory path instead of file."""
        image, error = load_image(tmp_path)

        assert image is None
        assert error is not None
        assert "not a file" in error.lower()

    def test_load_image_corrupted(self, tmp_path: Path) -> None:
        """Test loading a corrupted image file."""
        corrupted_path = tmp_path / "corrupted.jpg"
        # Write invalid image data
        with open(corrupted_path, "wb") as f:
            f.write(b"not an image")

        image, error = load_image(corrupted_path)

        # Should fail to load
        assert image is None
        assert error is not None


class TestAssessQuality:
    """Test suite for quality assessment functions."""

    def test_assess_quality_high_quality(self) -> None:
        """Test quality assessment on a high-quality image."""
        # Create a sharp, high-contrast, high-resolution image
        image = np.random.randint(0, 256, (2000, 2000, 3), dtype=np.uint8)

        score = assess_quality(image)

        # Should be a reasonable score (not necessarily 10 due to random noise)
        assert 0 <= score <= 10
        assert isinstance(score, float)

    def test_assess_quality_low_contrast(self) -> None:
        """Test quality assessment on a low-contrast image."""
        # Create a uniform gray image (very low contrast)
        image = np.ones((1000, 1000, 3), dtype=np.uint8) * 128

        score = assess_quality(image)

        # Should have low score due to low contrast
        assert 0 <= score <= 10
        # Low contrast should result in lower score
        assert score < 5

    def test_assess_quality_blurry(self) -> None:
        """Test quality assessment on a blurry image."""
        # Create a sharp image first
        image = np.zeros((500, 500, 3), dtype=np.uint8)
        cv2.rectangle(image, (100, 100), (400, 400), (255, 255, 255), -1)

        # Blur it heavily
        blurry = cv2.GaussianBlur(image, (51, 51), 0)

        score = assess_quality(blurry)

        # Should have low score due to blur
        assert 0 <= score <= 10
        assert score < 7  # Blurry images should score lower

    def test_assess_quality_small_resolution(self) -> None:
        """Test quality assessment on a small image."""
        # Create a very small image
        image = np.ones((100, 100, 3), dtype=np.uint8) * 128

        score = assess_quality(image)

        # Low resolution should contribute to lower score
        assert 0 <= score <= 10

    def test_assess_quality_none_input(self) -> None:
        """Test quality assessment with None input."""
        with pytest.raises(ValueError, match="cannot be None"):
            assess_quality(None)

    def test_assess_quality_empty_input(self) -> None:
        """Test quality assessment with empty array."""
        empty_array = np.array([])

        with pytest.raises(ValueError, match="cannot be None or empty"):
            assess_quality(empty_array)

    def test_assess_quality_grayscale(self) -> None:
        """Test quality assessment on grayscale image."""
        # Create a grayscale image
        image = np.random.randint(0, 256, (1000, 1000), dtype=np.uint8)

        score = assess_quality(image)

        # Should work with grayscale
        assert 0 <= score <= 10


class TestAssessBlur:
    """Test suite for blur assessment."""

    def test_assess_blur_sharp_image(self) -> None:
        """Test blur assessment on a sharp image."""
        # Create a sharp checkerboard pattern
        image = np.zeros((500, 500), dtype=np.uint8)
        image[::50, :] = 255
        image[:, ::50] = 255

        score = _assess_blur(image)

        # Sharp image should have high blur score
        assert score > 5
        assert 0 <= score <= 10

    def test_assess_blur_blurry_image(self) -> None:
        """Test blur assessment on a blurry image."""
        # Create and blur an image
        image = np.zeros((500, 500), dtype=np.uint8)
        image[::50, :] = 255
        blurry = cv2.GaussianBlur(image, (51, 51), 0)

        score = _assess_blur(blurry)

        # Blurry image should have low score
        assert score < 5
        assert 0 <= score <= 10


class TestAssessContrast:
    """Test suite for contrast assessment."""

    def test_assess_contrast_high_contrast(self) -> None:
        """Test contrast assessment on high-contrast image."""
        # Create black and white image
        image = np.zeros((500, 500), dtype=np.uint8)
        image[::2, :] = 255

        score = _assess_contrast(image)

        # High contrast should score high
        assert score > 5
        assert 0 <= score <= 10

    def test_assess_contrast_low_contrast(self) -> None:
        """Test contrast assessment on low-contrast image."""
        # Create uniform gray image
        image = np.ones((500, 500), dtype=np.uint8) * 128

        score = _assess_contrast(image)

        # Low contrast should score low
        assert score < 3
        assert 0 <= score <= 10


class TestAssessResolution:
    """Test suite for resolution assessment."""

    def test_assess_resolution_high_res(self) -> None:
        """Test resolution assessment on high-resolution image."""
        # Create 4MP image
        image = np.zeros((2000, 2000), dtype=np.uint8)

        score = _assess_resolution(image)

        # High resolution should score high
        assert score > 7
        assert 0 <= score <= 10

    def test_assess_resolution_low_res(self) -> None:
        """Test resolution assessment on low-resolution image."""
        # Create small image (0.01 MP)
        image = np.zeros((100, 100), dtype=np.uint8)

        score = _assess_resolution(image)

        # Low resolution should score low
        assert score < 3
        assert 0 <= score <= 10


class TestGetQualityDetails:
    """Test suite for detailed quality assessment."""

    def test_get_quality_details_structure(self) -> None:
        """Test that quality details returns correct structure."""
        image = np.random.randint(0, 256, (1000, 1000, 3), dtype=np.uint8)

        details = get_quality_details(image)

        # Check all required keys exist
        assert "overall_score" in details
        assert "blur_score" in details
        assert "contrast_score" in details
        assert "resolution_score" in details
        assert "dimensions" in details
        assert "recommendation" in details

        # Check types and ranges
        assert isinstance(details["overall_score"], float)
        assert isinstance(details["blur_score"], float)
        assert isinstance(details["contrast_score"], float)
        assert isinstance(details["resolution_score"], float)
        assert isinstance(details["dimensions"], tuple)
        assert isinstance(details["recommendation"], str)

        assert 0 <= details["overall_score"] <= 10
        assert 0 <= details["blur_score"] <= 10
        assert 0 <= details["contrast_score"] <= 10
        assert 0 <= details["resolution_score"] <= 10

    def test_get_quality_details_dimensions(self) -> None:
        """Test that dimensions are correctly reported."""
        image = np.zeros((1234, 5678, 3), dtype=np.uint8)

        details = get_quality_details(image)

        assert details["dimensions"] == (1234, 5678)

    def test_get_quality_details_recommendations(self) -> None:
        """Test that recommendations are appropriate for different quality levels."""
        # High quality image
        high_quality = np.random.randint(0, 256, (2000, 2000, 3), dtype=np.uint8)
        high_details = get_quality_details(high_quality)

        # Low quality image (small, uniform)
        low_quality = np.ones((100, 100, 3), dtype=np.uint8) * 128
        low_details = get_quality_details(low_quality)

        # Recommendations should be different
        assert high_details["recommendation"] != low_details["recommendation"]
        assert (
            "minimal" in high_details["recommendation"].lower()
            or "high" in high_details["recommendation"].lower()
        )
        assert (
            "full" in low_details["recommendation"].lower()
            or "low" in low_details["recommendation"].lower()
        )


class TestSaveImage:
    """Test suite for image saving."""

    def test_save_image_success(self, tmp_path: Path) -> None:
        """Test successful image saving."""
        # Create test image
        image = np.zeros((100, 100, 3), dtype=np.uint8)
        image[:, :] = [255, 0, 0]
        output_path = tmp_path / "output.jpg"

        # Save image
        save_image(image, output_path)

        # Verify file exists
        assert output_path.exists()

        # Load and verify
        loaded = cv2.imread(str(output_path))
        assert loaded is not None
        assert loaded.shape == image.shape

    def test_save_image_creates_directory(self, tmp_path: Path) -> None:
        """Test that save_image creates parent directories."""
        image = np.zeros((100, 100, 3), dtype=np.uint8)
        output_path = tmp_path / "subdir" / "output.png"

        # Directory shouldn't exist yet
        assert not output_path.parent.exists()

        save_image(image, output_path)

        # Directory should be created
        assert output_path.parent.exists()
        assert output_path.exists()

    def test_save_image_none_input(self, tmp_path: Path) -> None:
        """Test saving None image raises error."""
        output_path = tmp_path / "output.jpg"

        with pytest.raises(ValueError, match="cannot be None"):
            save_image(None, output_path)

    def test_save_image_empty_array(self, tmp_path: Path) -> None:
        """Test saving empty array raises error."""
        empty_array = np.array([])
        output_path = tmp_path / "output.jpg"

        with pytest.raises(ValueError, match="cannot be None or empty"):
            save_image(empty_array, output_path)

    def test_save_image_different_formats(self, tmp_path: Path) -> None:
        """Test saving images in different formats."""
        image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)

        formats = ["jpg", "png", "bmp", "tiff"]
        for fmt in formats:
            output_path = tmp_path / f"output.{fmt}"
            save_image(image, output_path)
            assert output_path.exists()


class TestIntegration:
    """Integration tests for complete workflows."""

    def test_load_assess_save_workflow(self, tmp_path: Path) -> None:
        """Test complete workflow: load -> assess -> save."""
        # Create original image
        original_path = tmp_path / "original.jpg"
        original_array = np.random.randint(0, 256, (500, 500, 3), dtype=np.uint8)
        cv2.imwrite(str(original_path), original_array)

        # Load image
        image, error = load_image(original_path)
        assert error is None
        assert image is not None

        # Assess quality
        quality = assess_quality(image)
        assert 0 <= quality <= 10

        # Get details
        details = get_quality_details(image)
        assert details["overall_score"] == quality

        # Save to new location
        output_path = tmp_path / "processed.png"
        save_image(image, output_path)
        assert output_path.exists()

        # Load saved image and verify
        reloaded, error = load_image(output_path)
        assert error is None
        assert reloaded is not None
        assert reloaded.shape == image.shape
