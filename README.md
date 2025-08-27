# OCR Tech - Multi-page PDF Processing

This project provides OCR (Optical Character Recognition) capabilities for processing multi-page PDF documents using PaddleOCR's PPStructureV3.

## Features

- Convert multi-page PDFs to images
- Process PDF pages through advanced OCR with structure analysis
- Extract text, tables, and layout information
- Save results in Markdown and JSON formats

## Installation

1. Install dependencies:

```bash
pip install -e .
```

2. Ensure you have the required system dependencies for pdf2image:
   - On Windows: Install Poppler for Windows
   - On macOS: `brew install poppler`
   - On Linux: `sudo apt-get install poppler-utils`

## Usage

### Method 1: Using the main script

Edit `main.py` and replace the `pdf_path` variable with your PDF file path:

```python
pdf_path = "path/to/your/document.pdf"
```

Then run:

```bash
python main.py
```

### Method 2: Using the command-line tool

Use the `process_pdf.py` script for command-line processing:

```bash
# Basic usage
python process_pdf.py path/to/your/document.pdf

# With custom DPI (higher DPI for better quality but slower processing)
python process_pdf.py path/to/your/document.pdf --dpi 400
```

### Method 3: Programmatic usage

```python
from utils.ingest import document_to_images
from ocr.structure import ocr_document

# Convert PDF to images
images = document_to_images("path/to/your/document.pdf", dpi=300)

# Process through OCR
ocr_document(images)
```

## Output

The OCR results are saved in the `output/` directory:

- `image_1.md`, `image_2.md`, etc. - Markdown files with structured content
- JSON files with detailed OCR results including text, tables, and layout information

## Supported File Formats

- PDF documents (multi-page)
- DOCX documents (converted to PDF first)
- Image files (JPG, PNG, TIFF, BMP)

## Dependencies

- PaddleOCR PPStructureV3
- pdf2image for PDF conversion
- docx2pdf for DOCX conversion
- PIL/Pillow for image processing
- OpenCV for image preprocessing

## Notes

- For best results, use PDFs with at least 300 DPI resolution
- Processing time increases with higher DPI and more pages
- GPU acceleration is enabled by default for faster processing
