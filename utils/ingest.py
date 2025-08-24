import os
from PIL import Image

# import cv2
# import numpy as np
from pdf2image import convert_from_path
from docx2pdf import convert as docx2pdf_convert
import tempfile
import shutil


def document_to_images(input_path, dpi=300, output_dir=None):
    """
    Convert PDF, DOCX, or image file to a list of PIL Images (one per page).
    Output images are grayscale, 300 DPI, optimized for OCR.
    """
    file_ext = os.path.splitext(input_path)[1].lower()
    temp_dir = None
    image_paths = []

    try:
        # Handle PDF
        if file_ext == ".pdf":
            images = convert_from_path(input_path, dpi=dpi)
            return images  # List of PIL Images

        # Handle DOCX
        elif file_ext == ".docx":
            temp_dir = tempfile.mkdtemp()
            pdf_path = os.path.join(temp_dir, "temp.pdf")
            docx2pdf_convert(input_path, pdf_path)
            images = convert_from_path(pdf_path, dpi=dpi)
            return images

        # Handle image files (JPG, PNG, etc.)
        elif file_ext in [".jpg", ".jpeg", ".png", ".tiff", ".bmp"]:
            img = Image.open(input_path)
            # Ensure high DPI
            if img.info.get("dpi") != (dpi, dpi):
                img = img.resize(
                    (int(img.width * dpi / 72), int(img.height * dpi / 72)),
                    Image.LANCZOS,
                )
            # Convert to grayscale
            img = img.convert("L")
            return [img]

        else:
            raise ValueError(f"Unsupported file type: {file_ext}")

    finally:
        # Clean up temp files
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
