# PDF Loading Setup Guide

## Issue

The sample documents in `tests/sample_documents/` are PDF files. To load PDFs as images, we need two things:

1. **pdf2image** Python library (✓ installed)
2. **poppler** system utility (❌ needs manual installation)

## Current Status

When trying to load PDFs, you'll see this error:
```
ERROR: Failed to load PDF: Unable to get page count. Is poppler installed and in PATH?
```

## Solution: Install Poppler

### Windows

1. Download poppler for Windows:
   - Go to: https://github.com/oschwartz10612/poppler-windows/releases/
   - Download the latest release (e.g., `Release-24.08.0-0.zip`)

2. Extract the ZIP file to a permanent location, e.g.:
   ```
   C:\Program Files\poppler\
   ```

3. Add poppler's `bin` folder to your PATH:
   - Open System Properties → Environment Variables
   - Edit the `Path` variable
   - Add: `C:\Program Files\poppler\Library\bin`
   - Click OK to save

4. **Restart your terminal** for PATH changes to take effect

5. Verify installation:
   ```bash
   pdftoppm -v
   ```
   Should show version info if installed correctly.

### macOS

```bash
brew install poppler
```

### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install poppler-utils
```

## Testing

After installing poppler, run the test script:

```bash
python test_pdf_loading.py
```

This will:
1. Check if pdf2image is installed
2. Check if poppler is available
3. Try to load all sample PDFs
4. Show quality assessment for each document

## Expected Output

```
================================================================================
PDF Loading Test Script
================================================================================
✓ pdf2image is installed

Checking for poppler (required by pdf2image)...
✓ poppler is installed and working!

================================================================================
Testing all sample documents
================================================================================

Found 5 PDF files

S028089.pdf
--------------------------------------------------------------------------------
✓ Successfully loaded!
  Dimensions: 1700 x 2200 pixels
  Quality Score: 7.45/10
  Recommendation: High quality - minimal preprocessing needed

[... etc for other PDFs ...]

================================================================================
Results: 5 succeeded, 0 failed
================================================================================

✓ All PDFs loaded successfully!
```

## Alternative: Convert PDFs to Images

If you don't want to install poppler, you can convert the PDFs to PNG/JPG files manually:

1. Open each PDF in a PDF viewer
2. Export/Save as PNG or JPG
3. Save to `tests/sample_documents/`

The image loading functions will work with these formats without requiring poppler.

## For Development

When running tests that involve PDFs:

- **With poppler**: All functionality works, PDFs load directly
- **Without poppler**: PDF loading will fail, but all other image formats (PNG, JPG, TIFF) work fine

The preprocessing and quality assessment functions work on images regardless of their source format.
