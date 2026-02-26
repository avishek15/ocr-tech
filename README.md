# OCR Tech

**Multi-page Document Processing API with Spatial Text Arrangement**

[![Build Status](https://github.com/avishek15/ocr-tech/actions/workflows/main.yml/badge.svg)](https://github.com/avishek15/ocr-tech/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/avishek15/ocr-tech.svg)](https://github.com/avishek15/ocr-tech/stargazers)

![Demo](demo_image.png)

## What It Does

FastAPI-powered OCR API that extracts text from documents while preserving spatial layout:
- **Multi-format support** — PDF, DOCX, images (JPG, PNG, TIFF, BMP)
- **Spatial arrangement** — Text output maintains document structure
- **Multi-page processing** — Handle 50+ page documents
- **GPU acceleration** — Fast processing with CUDA support
- **No temp files** — Everything processed in memory

## Why It Matters

Most OCR tools:
- Lose document structure (plain text dump)
- Require intermediate files (slow, disk I/O)
- Don't handle multi-page documents well

OCR Tech solves all three: fast, structured, in-memory processing.

## Quick Start

```bash
# Clone
git clone https://github.com/avishek15/ocr-tech.git
cd ocr-tech

# Install
pip install -e .

# Install Poppler (required for PDF processing)
# macOS: brew install poppler
# Linux: sudo apt-get install poppler-utils
# Windows: Download from poppler-windows

# Run
python main.py
```

API runs at `http://localhost:8000`

## Features

### Unified API
One endpoint for all file types — no need to handle different parsers.

### Spatial Text Arrangement
Text output maintains original document layout (tables, columns, sections).

### In-Memory Processing
No disk I/O = faster processing = better for serverless deployments.

### Multi-Page Support
Process 50+ page PDFs in a single request.

### GPU Acceleration
CUDA-enabled for 3-5x faster processing.

## API Endpoints

### POST `/process/image`

Process an image file (JPG, PNG, TIFF, BMP)

```bash
curl -X POST -F "file=@invoice.png" http://localhost:8000/process/image
```

**Response:**
```json
{
  "success": true,
  "filename": "invoice.png",
  "results": [
    {
      "arranged_text": "Invoice #1234\nDate: 2026-02-26\nAmount: $1,500.00",
      "texts": ["Invoice #1234", "Date: 2026-02-26", "Amount: $1,500.00"],
      "boxes": [[x1, y1, x2, y2], ...],
      "scores": [0.98, 0.95, 0.97]
    }
  ]
}
```

### POST `/process/document`

Process a PDF or DOCX document

```bash
curl -X POST -F "file=@contract.pdf" http://localhost:8000/process/document
```

**Parameters:**
- `file` (required) — Document file
- `dpi` (optional, default: 300) — Resolution for PDF rendering

**Response:**
```json
{
  "success": true,
  "filename": "contract.pdf",
  "total_pages": 5,
  "results": [
    {
      "page_number": 1,
      "arranged_text": "...",
      "texts": [...],
      "boxes": [...],
      "scores": [...]
    }
  ]
}
```

### POST `/process/multiple`

Process multiple files in one request

```bash
curl -X POST \
  -F "files=@page1.png" \
  -F "files=@page2.png" \
  http://localhost:8000/process/multiple
```

### GET `/health`

Health check endpoint

```bash
curl http://localhost:8000/health
```

## Tech Stack

| Layer | Technology |
|-------|------------|
| **API** | FastAPI |
| **OCR Engine** | PaddleOCR PPStructureV3 |
| **PDF Processing** | pdf2image |
| **DOCX Processing** | docx2pdf |
| **Image Processing** | PIL, OpenCV |

## Programmatic Usage

```python
from utils.ingest import document_to_images
from ocr.paddle import process_image_direct

# Convert document to images
images = document_to_images("contract.pdf", dpi=300)

# Process each image
for i, image in enumerate(images, 1):
    result = process_image_direct(image)
    if result['success']:
        print(f"Page {i}:")
        print(result['results'][0]['arranged_text'])
```

## Deployment

### Docker

```bash
docker build -t ocr-tech .
docker run -p 8000:8000 ocr-tech
```

### AWS Lambda

Use Mangum adapter for serverless deployment.

### Traditional Server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Use Cases

### 1. Invoice Extraction
Upload PDF invoices → get structured text → parse into database

### 2. Contract Analysis
Upload contracts → extract clauses → send to LLM for summarization

### 3. Document Digitization
Scan paper documents → OCR → searchable text archive

### 4. Receipt Processing
Upload receipts → extract line items → expense tracking

## Performance

| Document Type | Pages | Processing Time |
|---------------|-------|-----------------|
| Invoice (PDF) | 1 | ~2 seconds |
| Contract (PDF) | 10 | ~15 seconds |
| Report (PDF) | 50 | ~60 seconds |

*Benchmarks on CPU (Intel i7). GPU reduces time by 3-5x.*

## Supported Formats

| Format | Support | Notes |
|--------|---------|-------|
| PDF | ✅ | Multi-page supported |
| DOCX | ✅ | Converted to PDF first |
| JPG | ✅ | |
| PNG | ✅ | |
| TIFF | ✅ | Multi-page supported |
| BMP | ✅ | |
| XLSX | 🔄 | Coming soon |
| PPTX | 🔄 | Coming soon |

## Testing

```bash
python test_api.py
```

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

### Development Setup

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT License - see [LICENSE](LICENSE)

## Author

Built by **Avishek Majumder**

- 🌐 [invaritech.ai](https://invaritech.ai)
- 🐦 [@AviMajumder1503](https://x.com/AviMajumder1503)
- 💼 [LinkedIn](https://linkedin.com/in/avishek-majumder)
- 🐙 [GitHub](https://github.com/avishek15)

---

**Star ⭐ this repo if you find it useful!**
