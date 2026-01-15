"""Demo: Preprocessing pipeline on sample PDFs with visualizations."""

from pathlib import Path
from src.utils.image_utils import load_image, assess_quality, get_quality_details
from src.agents.preprocessor import preprocess_image
import cv2
import numpy as np

print("=" * 80)
print("PREPROCESSING PIPELINE DEMO")
print("=" * 80)

# Create output directory for visualizations
output_dir = Path("output/preprocessing_demo")
output_dir.mkdir(parents=True, exist_ok=True)

# Process all sample PDFs
sample_dir = Path("tests/sample_documents")
pdf_files = sorted(list(sample_dir.glob("*.pdf")))

print(f"\nProcessing {len(pdf_files)} documents...\n")

for pdf_file in pdf_files:
    print(f"\n{'=' * 80}")
    print(f"Processing: {pdf_file.name}")
    print('=' * 80)

    # Load image
    original, error = load_image(pdf_file)
    if error:
        print(f"[X] Error loading: {error}")
        continue

    # Assess quality
    quality = assess_quality(original)
    details = get_quality_details(original)

    print(f"\nQuality Assessment:")
    print(f"  Overall Score:    {details['overall_score']:.2f}/10")
    print(f"  Blur Score:       {details['blur_score']:.2f}/10")
    print(f"  Contrast Score:   {details['contrast_score']:.2f}/10")
    print(f"  Resolution Score: {details['resolution_score']:.2f}/10")
    print(f"  Dimensions:       {details['dimensions'][0]}x{details['dimensions'][1]}")
    print(f"  Recommendation:   {details['recommendation']}")

    # Determine preprocessing path
    if quality >= 7:
        path = "HIGH QUALITY -> Minimal processing (grayscale only)"
    elif quality >= 4:
        path = "MEDIUM QUALITY -> Standard pipeline (deskew + enhance + denoise)"
    else:
        path = "LOW QUALITY -> Full enhancement (all operations + binarize)"

    print(f"\nPreprocessing Path: {path}")

    # Apply preprocessing
    processed, error = preprocess_image(original, quality)
    if error:
        print(f"[X] Preprocessing error: {error}")
        continue

    print(f"[OK] Preprocessing complete!")

    # Save visualizations
    # Original (convert to grayscale for fair comparison)
    if len(original.shape) == 3:
        original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    else:
        original_gray = original

    # Create side-by-side comparison
    # Resize for display (reduce size for easier viewing)
    scale = 0.3
    orig_small = cv2.resize(original_gray, None, fx=scale, fy=scale)
    proc_small = cv2.resize(processed, None, fx=scale, fy=scale)

    # Stack horizontally
    comparison = np.hstack([orig_small, proc_small])

    # Add labels
    h, w = comparison.shape[:2]
    labeled = cv2.copyMakeBorder(comparison, 50, 0, 0, 0, cv2.BORDER_CONSTANT, value=255)

    # Add text labels (white background at top)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(labeled, "ORIGINAL", (50, 30), font, 0.7, 0, 2)
    cv2.putText(labeled, "PREPROCESSED", (w//2 + 50, 30), font, 0.7, 0, 2)

    # Save comparison
    output_file = output_dir / f"{pdf_file.stem}_comparison.png"
    cv2.imwrite(str(output_file), labeled)
    print(f"  Saved comparison: {output_file}")

    # Also save full-size processed version
    full_output = output_dir / f"{pdf_file.stem}_preprocessed.png"
    cv2.imwrite(str(full_output), processed)
    print(f"  Saved processed:  {full_output}")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"\nAll visualizations saved to: {output_dir}/")
print("\nPreprocessing paths used:")
print("  - High quality (>=7):   Grayscale only")
print("  - Medium quality (4-7): Deskew + CLAHE + Denoise")
print("  - Low quality (<4):     Full pipeline + Binarize")
print("\nResults show adaptive preprocessing based on document quality!")
print("=" * 80)
