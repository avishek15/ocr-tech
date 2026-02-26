# OCR-Tech — Multi-Page Document Processing API

**FastAPI-powered OCR for PDFs, images, and documents with spatial text arrangement.**

![Demo](demo.gif)

## What It Does

OCR-Tech extracts text from documents while preserving spatial layout. Upload a PDF, image, or DOCX — get structured text back with page-by-page organization.

**Why it matters:** Most OCR tools scramble text order. This one maintains the document's visual structure, making it usable for invoices, reports, and forms.

## Quick Start

```bash
# Clone
git clone https://github.com/avishek15/ocr-tech.git
cd ocr-tech

# Install
pip install -r requirements.txt

# Run
uvicorn app.main:app --reload
```

## Features

- **Multi-format support:** PDF, JPG, PNG, TIFF, BMP, DOCX
- **Spatial text arrangement:** Preserves document layout
- **Multi-page processing:** Handle 50+ page PDFs
- **GPU acceleration:** Optional CUDA support for faster processing
- **Memory efficient:** No intermediate files, direct processing

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/process/image` | POST | Process single image |
| `/process/document` | POST | Process PDF/DOCX |
| `/process/multiple` | POST | Batch processing |
| `/health` | GET | Health check |

### Example: Process Invoice

```bash
curl -X POST "http://localhost:8000/process/document" \
  -F "file=@invoice.pdf"
```

**Response:**
```json
{
  "pages": [
    {
      "page_number": 1,
      "text": "Invoice #12345\nDate: 2026-02-26\nTotal: $1,234.56",
      "confidence": 0.95
    }
  ]
}
```

## Tech Stack

- **Python 3.10+**
- **FastAPI** — Modern async API framework
- **Tesseract OCR** — Text extraction engine
- **pdf2image** — PDF to image conversion
- **Pillow** — Image processing

## Installation

### Prerequisites

- Python 3.10+
- Tesseract OCR (`apt-get install tesseract-ocr` on Ubuntu)

### Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# For GPU support (optional)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

## Use Cases

| Use Case | How It Helps |
|----------|--------------|
| **Invoice processing** | Extract vendor, amount, line items |
| **Report digitization** | Convert PDF reports to structured data |
| **Form automation** | Read handwritten or typed forms |
| **Document search** | Make scanned documents searchable |

## Demo

Live demo: [tools.invaritech.ai/ocr](https://tools.invaritech.ai/ocr)

## API Documentation

Full API docs available at `/docs` when running locally:

```bash
uvicorn app.main:app --reload
# Visit http://localhost:8000/docs
```

## Roadmap

- [ ] Invoice-specific extraction (vendor, amount, line items)
- [ ] Table detection and extraction
- [ ] Multi-language support
- [ ] Web UI for drag-and-drop processing

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE)

## Author

Built by [Avishek Majumder](https://invaritech.ai)

- X: [@AviMajumder1503](https://x.com/AviMajumder1503)
- LinkedIn: [avishek-majumder](https://linkedin.com/in/avishek-majumder)
- GitHub: [avishek15](https://github.com/avishek15)

---

**Used in production at [Invaritech](https://invaritech.ai)** — AI automation for enterprises.
