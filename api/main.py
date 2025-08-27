# Import OCR functionality - add to path first
from datetime import datetime
import os
import shutil
import tempfile
import numpy as np
from PIL import Image
import io
from typing import List, Dict, Any
from fastapi.responses import JSONResponse
from fastapi import FastAPI, File, UploadFile, HTTPException
from utils.ingest import document_to_images
from ocr.paddle import process_image_direct
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))


app = FastAPI(
    title="OCR-Tech API",
    description="API for OCR processing of various document types with spatial text arrangement",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {"message": "OCR-Tech API is running", "status": "healthy"}


@app.post("/process/image")
async def process_image(file: UploadFile = File(...)):
    """
    Process an image file through OCR with spatial text arrangement
    """
    try:
        # Check file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400, detail="File must be an image")

        # Read and process image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        # Process image through OCR
        result = process_image_direct(image)

        if not result['success']:
            raise HTTPException(
                status_code=500, detail=f"OCR processing failed: {result['error']}")

        return {
            "success": True,
            "filename": file.filename,
            "total_pages": result['total_pages'],
            "results": result['results'],
            "processed_at": datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing image: {str(e)}")


@app.post("/process/document")
async def process_document(file: UploadFile = File(...), dpi: int = 300):
    """
    Process a document file (PDF, DOCX) through OCR with spatial text arrangement
    """
    temp_dir = None
    try:
        # Create temporary file
        temp_dir = tempfile.mkdtemp()
        temp_file_path = os.path.join(temp_dir, file.filename)

        # Save uploaded file
        contents = await file.read()
        with open(temp_file_path, 'wb') as f:
            f.write(contents)

        # Convert document to images
        images = document_to_images(temp_file_path, dpi=dpi)

        if not images:
            raise HTTPException(
                status_code=400, detail="Failed to convert document to images")

        # Process each image through OCR
        all_results = []
        for i, image in enumerate(images):
            result = process_image_direct(image)
            if result['success']:
                for page_result in result['results']:
                    page_result['page_number'] = i + 1
                    all_results.append(page_result)

        return {
            "success": True,
            "filename": file.filename,
            "total_pages": len(images),
            "results": all_results,
            "processed_at": datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing document: {str(e)}")

    finally:
        # Clean up temp files
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


@app.post("/process/multiple")
async def process_multiple_files(files: List[UploadFile] = File(...)):
    """
    Process multiple files in a single request
    """
    results = []

    for file in files:
        try:
            if file.content_type.startswith('image/'):
                # Process as image
                contents = await file.read()
                image = Image.open(io.BytesIO(contents))
                result = process_image_direct(image)

                if result['success']:
                    results.append({
                        "filename": file.filename,
                        "type": "image",
                        "success": True,
                        "total_pages": result['total_pages'],
                        "results": result['results']
                    })
                else:
                    results.append({
                        "filename": file.filename,
                        "type": "image",
                        "success": False,
                        "error": result['error']
                    })

            else:
                # Process as document (will need to save temporarily)
                temp_dir = tempfile.mkdtemp()
                temp_file_path = os.path.join(temp_dir, file.filename)

                contents = await file.read()
                with open(temp_file_path, 'wb') as f:
                    f.write(contents)

                images = document_to_images(temp_file_path)

                if images:
                    doc_results = []
                    for i, image in enumerate(images):
                        result = process_image_direct(image)
                        if result['success']:
                            for page_result in result['results']:
                                page_result['page_number'] = i + 1
                                doc_results.append(page_result)

                    results.append({
                        "filename": file.filename,
                        "type": "document",
                        "success": True,
                        "total_pages": len(images),
                        "results": doc_results
                    })
                else:
                    results.append({
                        "filename": file.filename,
                        "type": "document",
                        "success": False,
                        "error": "Failed to convert document to images"
                    })

                # Clean up temp files
                shutil.rmtree(temp_dir)

        except Exception as e:
            results.append({
                "filename": file.filename,
                "success": False,
                "error": str(e)
            })

    return {
        "processed_at": datetime.now().isoformat(),
        "total_files": len(files),
        "results": results
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "ocr-tech-api"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
