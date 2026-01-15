"""Test script to troubleshoot PDF loading with sample documents."""

from pathlib import Path
from src.utils.image_utils import load_image, get_quality_details
import sys

print("=" * 80)
print("PDF Loading Test Script")
print("=" * 80)

# Check if pdf2image is installed
try:
    import pdf2image
    print("✓ pdf2image is installed")
except ImportError:
    print("✗ pdf2image is NOT installed")
    print("  Install with: pip install pdf2image")
    sys.exit(1)

# Check if poppler is available
print("\nChecking for poppler (required by pdf2image)...")
try:
    from pdf2image import convert_from_path

    # Try to get poppler version
    test_pdf = Path("tests/sample_documents/S028089.pdf")
    if test_pdf.exists():
        try:
            images = convert_from_path(str(test_pdf), first_page=1, last_page=1)
            print("✓ poppler is installed and working!")
        except Exception as e:
            print(f"✗ poppler is NOT properly installed or not in PATH")
            print(f"  Error: {str(e)}")
            print("\nHow to install poppler:")
            print("  Windows: Download from https://github.com/oschwartz10612/poppler-windows/releases/")
            print("           Extract and add bin/ folder to your PATH")
            print("  macOS:   brew install poppler")
            print("  Linux:   sudo apt-get install poppler-utils")
            sys.exit(1)
    else:
        print(f"✗ Test PDF not found at {test_pdf}")
        sys.exit(1)
except ImportError as e:
    print(f"✗ Error importing pdf2image: {e}")
    sys.exit(1)

# Test loading all sample PDFs
print("\n" + "=" * 80)
print("Testing all sample documents")
print("=" * 80)

sample_dir = Path("tests/sample_documents")
pdf_files = list(sample_dir.glob("*.pdf"))

if not pdf_files:
    print(f"No PDF files found in {sample_dir}")
    sys.exit(1)

print(f"\nFound {len(pdf_files)} PDF files\n")

success_count = 0
fail_count = 0

for pdf_file in sorted(pdf_files):
    print(f"\n{pdf_file.name}")
    print("-" * 80)

    # Try to load
    image, error = load_image(pdf_file)

    if error:
        print(f"✗ FAILED: {error}")
        fail_count += 1
        continue

    # Success - show quality details
    print(f"✓ Successfully loaded!")
    details = get_quality_details(image)
    print(f"  Dimensions: {details['dimensions'][0]} x {details['dimensions'][1]} pixels")
    print(f"  Quality Score: {details['overall_score']:.2f}/10")
    print(f"  Recommendation: {details['recommendation']}")
    success_count += 1

print("\n" + "=" * 80)
print(f"Results: {success_count} succeeded, {fail_count} failed")
print("=" * 80)

if fail_count > 0:
    print("\n⚠️  Some PDFs failed to load. See errors above for troubleshooting.")
    sys.exit(1)
else:
    print("\n✓ All PDFs loaded successfully!")
    sys.exit(0)
