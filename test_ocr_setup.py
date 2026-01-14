"""Quick test to verify OCR engines are installed and functional."""

import sys
from pathlib import Path

print("=" * 60)
print("Testing OCR Engine Setup")
print("=" * 60)

# Test 1: Tesseract
print("\n1. Testing Tesseract...")
try:
    import pytesseract
    # Note: Tesseract binary must be installed separately on Windows
    print("   - pytesseract library: OK")
    print("   - Note: Tesseract binary installation will be tested with actual images")
except Exception as e:
    print(f"   - ERROR: {e}")
    sys.exit(1)

# Test 2: PaddleOCR
print("\n2. Testing PaddleOCR...")
try:
    from paddleocr import PaddleOCR
    print("   - PaddleOCR library: OK")
    print("   - Note: Models will be downloaded on first use")
except Exception as e:
    print(f"   - ERROR: {e}")
    sys.exit(1)

# Test 3: EasyOCR
print("\n3. Testing EasyOCR...")
try:
    import easyocr
    print("   - EasyOCR library: OK")
    print("   - Note: Models will be downloaded on first use")
except Exception as e:
    print(f"   - ERROR: {e}")
    sys.exit(1)

# Test 4: Transformers (for TrOCR)
print("\n4. Testing Transformers...")
try:
    from transformers import TrOCRProcessor, VisionEncoderDecoderModel
    print("   - Transformers library: OK")
    print("   - Note: TrOCR models will be downloaded when needed")
except Exception as e:
    print(f"   - ERROR: {e}")
    sys.exit(1)

# Test 5: Image Processing Libraries
print("\n5. Testing Image Processing Libraries...")
try:
    import cv2
    import PIL
    from PIL import Image
    import numpy as np
    from skimage import io
    print(f"   - OpenCV {cv2.__version__}: OK")
    print(f"   - Pillow {PIL.__version__}: OK")
    print(f"   - NumPy {np.__version__}: OK")
    print("   - scikit-image: OK")
except Exception as e:
    print(f"   - ERROR: {e}")
    sys.exit(1)

# Test 6: Supporting Libraries
print("\n6. Testing Supporting Libraries...")
try:
    import pandas as pd
    import fastapi
    import pytest
    import black
    import mypy
    print(f"   - Pandas {pd.__version__}: OK")
    print("   - FastAPI: OK")
    print("   - Pytest: OK")
    print("   - Black: OK")
    print("   - Mypy: OK")
except Exception as e:
    print(f"   - ERROR: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("SUCCESS: All libraries installed and importable!")
print("=" * 60)
print("\nNext steps:")
print("1. Install Tesseract binary for Windows (if not already installed)")
print("2. OCR engine models will download automatically on first use")
print("3. Ready to proceed with Day 2 tasks")
