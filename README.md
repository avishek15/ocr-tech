# OCR Tech - Multi-page Document Processing API

This project provides OCR (Optical Character Recognition) capabilities for processing various document types with spatial text arrangement, exposed through a FastAPI interface.

## Features

- **Unified API Interface**: Process PDFs, images, DOCX, and other document types through a single API
- **Spatial Text Arrangement**: Intelligently arrange OCR results based on document layout
- **No Intermediate Files**: Process documents directly in memory without generating temporary files
- **Multiple File Support**: Handle PDF, DOCX, JPG, PNG, TIFF, BMP files
- **Real-time Processing**: Fast processing with GPU acceleration support

## API Endpoints

### POST `/process/image`

Process an image file through OCR with spatial text arrangement

- **Content-Type**: `multipart/form-data`
- **Parameters**: `file` (required) - image file
- **Response**: JSON with OCR results including arranged text

### POST `/process/document`

Process a document file (PDF, DOCX) through OCR

- **Content-Type**: `multipart/form-data`
- **Parameters**: `file` (required), `dpi` (optional, default: 300)
- **Response**: JSON with multi-page OCR results

### POST `/process/multiple`

Process multiple files in a single request

- **Content-Type**: `multipart/form-data`
- **Parameters**: `files` (required) - multiple files
- **Response**: JSON with results for each file

### GET `/health`

Health check endpoint

- **Response**: API status information

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

### Running the API Server

```bash
cd api
python main.py
```

The API will be available at `http://localhost:8000`

### API Usage Examples

**Using curl:**

```bash
# Process an image
curl -X POST -F "file=@document.pdf" http://localhost:8000/process/document

# Process multiple files
curl -X POST -F "files=@image1.png" -F "files=@image2.png" http://localhost:8000/process/multiple
```

**Using Python requests:**

```python
import requests

# Process a document
with open('document.pdf', 'rb') as f:
    response = requests.post('http://localhost:8000/process/document', files={'file': f})
    print(response.json())

# Process multiple images
files = [
    ('files', ('image1.png', open('image1.png', 'rb'), 'image/png')),
    ('files', ('image2.png', open('image2.png', 'rb'), 'image/png'))
]
response = requests.post('http://localhost:8000/process/multiple', files=files)
print(response.json())
```

### Programmatic Usage

```python
from utils.ingest import document_to_images
from ocr.paddle import process_image_direct

# Process document and get images
images = document_to_images("path/to/your/document.pdf", dpi=300)

# Process each image directly without file I/O
for image in images:
    result = process_image_direct(image)
    if result['success']:
        for page_result in result['results']:
            print(page_result['arranged_text'])
```

## Response Format

Successful responses include:

```json
{
  "success": true,
  "filename": "document.pdf",
  "total_pages": 3,
  "results": [
    {
      "texts": ["extracted", "text", "elements"],
      "boxes": [[x1, y1, x2, y2], ...],
      "scores": [0.95, 0.87, ...],
      "arranged_text": "spatially arranged text content",
      "page_number": 1
    }
  ],
  "processed_at": "2024-01-01T12:00:00.000000"
}
```

## Supported File Formats

- **PDF documents** (multi-page)
- **DOCX documents** (converted to PDF first)
- **Image files**: JPG, PNG, TIFF, BMP
- **Text files**: RTF, TXT (future support)
- **Spreadsheets**: XLSX, XLS (future support)
- **Presentations**: PPT, PPTX (future support)

## Dependencies

- PaddleOCR PPStructureV3
- FastAPI for API framework
- pdf2image for PDF conversion
- docx2pdf for DOCX conversion
- PIL/Pillow for image processing
- OpenCV for image preprocessing

## Performance Notes

- GPU acceleration is enabled by default for faster processing
- Processing time increases with higher DPI and more pages
- For best results, use documents with at least 300 DPI resolution
- Memory usage optimized for direct processing without file I/O

## Testing

Run the test suite to verify API functionality:

```bash
python test_api.py
```

## Development

The API is built with FastAPI and includes:

- Automatic OpenAPI documentation at `/docs`
- Comprehensive error handling
- Input validation
- Health monitoring
- Support for batch processing
