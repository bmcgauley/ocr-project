"""Quick test script to verify OCR engines are working.

This script tests all three OCR engines with a simple test image
and displays which ones are available and working.
"""

import cv2
import numpy as np
from pathlib import Path


def create_test_image():
    """Create a simple test image with text."""
    print("\n[*] Creating test image...")
    img = np.ones((200, 800, 3), dtype=np.uint8) * 255
    cv2.putText(
        img,
        "Hello World OCR Test",
        (50, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.5,
        (0, 0, 0),
        2,
    )
    return img


def test_tesseract(image):
    """Test Tesseract OCR engine."""
    print("\n[TEST] Testing Tesseract...")
    try:
        from src.agents.ocr_engine import run_tesseract

        text, confidence, metadata = run_tesseract(image)
        print(f"[OK] Tesseract is WORKING!")
        print(f"     Text: '{text}'")
        print(f"     Confidence: {confidence:.2f}%")
        print(f"     Words detected: {metadata['word_count']}")
        print(f"     Processing time: {metadata['processing_time']:.2f}s")
        return True
    except RuntimeError as e:
        if "not installed" in str(e):
            print(f"[WARN] Tesseract binary not installed")
            print(
                f"       Install from: https://github.com/UB-Mannheim/tesseract/wiki"
            )
        else:
            print(f"[FAIL] Tesseract error: {e}")
        return False
    except Exception as e:
        print(f"[FAIL] Tesseract error: {e}")
        return False


def test_paddleocr(image):
    """Test PaddleOCR engine."""
    print("\n[TEST] Testing PaddleOCR...")
    try:
        from src.agents.ocr_engine import run_paddleocr

        print("       (This may take a while on first run - downloading models...)")
        text, confidence, metadata = run_paddleocr(image)
        print(f"[OK] PaddleOCR is WORKING!")
        print(f"     Text: '{text}'")
        print(f"     Confidence: {confidence:.2f}")
        print(f"     Blocks detected: {metadata['block_count']}")
        print(f"     Processing time: {metadata['processing_time']:.2f}s")
        return True
    except RuntimeError as e:
        if "not installed" in str(e):
            print(f"[WARN] PaddleOCR not installed")
            print(f"       Install with: pip install paddleocr paddlepaddle")
        else:
            print(f"[FAIL] PaddleOCR error: {e}")
        return False
    except Exception as e:
        print(f"[FAIL] PaddleOCR error: {e}")
        return False


def test_easyocr(image):
    """Test EasyOCR engine."""
    print("\n[TEST] Testing EasyOCR...")
    try:
        from src.agents.ocr_engine import run_easyocr

        print("       (This may take a while on first run - downloading models...)")
        text, confidence, metadata = run_easyocr(image)
        print(f"[OK] EasyOCR is WORKING!")
        print(f"     Text: '{text}'")
        print(f"     Confidence: {confidence:.2f}")
        print(f"     Blocks detected: {metadata['block_count']}")
        print(f"     Processing time: {metadata['processing_time']:.2f}s")
        return True
    except RuntimeError as e:
        if "not installed" in str(e):
            print(f"[WARN] EasyOCR not installed")
            print(f"       Install with: pip install easyocr")
        else:
            print(f"[FAIL] EasyOCR error: {e}")
        return False
    except Exception as e:
        print(f"[FAIL] EasyOCR error: {e}")
        return False


def main():
    """Run quick tests on all OCR engines."""
    print("=" * 70)
    print("QUICK OCR ENGINE TEST")
    print("=" * 70)

    # Create test image
    test_image = create_test_image()

    # Test all engines
    results = {
        "Tesseract": test_tesseract(test_image),
        "PaddleOCR": test_paddleocr(test_image),
        "EasyOCR": test_easyocr(test_image),
    }

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    working = sum(1 for v in results.values() if v)
    total = len(results)

    for engine, status in results.items():
        status_icon = "[OK]" if status else "[FAIL]"
        print(f"{status_icon} {engine}: {'WORKING' if status else 'NOT AVAILABLE'}")

    print(f"\n[RESULT] {working}/{total} engines are working")

    if working == 0:
        print("\n[TIP] Run the following to install dependencies:")
        print("      pip install pytesseract paddleocr paddlepaddle easyocr")
        print("\n      For Tesseract binary:")
        print("      https://github.com/UB-Mannheim/tesseract/wiki")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
