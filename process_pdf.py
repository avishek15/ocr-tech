#!/usr/bin/env python3
"""
Script to process multi-page PDF files using OCR structure analysis.
"""

import argparse
import os
from utils.ingest import document_to_images
from ocr.structure import ocr_document


def process_pdf(pdf_path, dpi=300):
    """
    Process a multi-page PDF file through OCR structure analysis.

    Args:
        pdf_path (str): Path to the PDF file
        dpi (int): DPI for image conversion (default: 300)

    Returns:
        List of processed OCR results
    """
    # Check if file exists
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    # Convert PDF to images
    print(f"Converting PDF '{pdf_path}' to images...")
    images = document_to_images(pdf_path, dpi=dpi)
    print(f"Converted {len(images)} pages to images")

    # Process images through OCR
    print("Processing images through OCR structure analysis...")
    ocr_document(images)

    print(f"OCR processing completed! Results saved to 'output/' directory")
    return images


def main():
    parser = argparse.ArgumentParser(
        description="Process multi-page PDF files through OCR structure analysis")
    parser.add_argument("pdf_path", help="Path to the PDF file to process")
    parser.add_argument("--dpi", type=int, default=300,
                        help="DPI for image conversion (default: 300)")

    args = parser.parse_args()

    try:
        process_pdf(args.pdf_path, args.dpi)
    except Exception as e:
        print(f"Error processing PDF: {e}")
        raise


if __name__ == "__main__":
    main()
