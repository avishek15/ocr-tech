import numpy as np
from ocr.structure import ocr_document
from utils.preprocess import preprocess_for_ocr
from utils.ingest import document_to_images
import os

#!/usr/bin/env python3
"""
Debug script to test PDF processing step by step.
"""


def debug_pdf_processing(pdf_path):
    """
    Debug PDF processing step by step to identify where it fails.
    """
    print(f"Testing PDF processing for: {pdf_path}")

    # Step 1: Convert PDF to images
    print("1. Converting PDF to images...")
    try:
        images = document_to_images(pdf_path)
        print(f"   Success: Converted {len(images)} pages")
        print(f"   First image type: {type(images[0])}")
        if hasattr(images[0], 'size'):
            print(f"   First image size: {images[0].size}")
    except Exception as e:
        print(f"   Error in PDF conversion: {e}")
        return

    # Step 2: Preprocess images
    print("2. Preprocessing images...")
    try:
        preprocessed_images = [preprocess_for_ocr(img) for img in images]
        print(f"   Success: Preprocessed {len(preprocessed_images)} images")
        print(
            f"   First preprocessed image shape: {preprocessed_images[0].shape}")
        print(
            f"   First preprocessed image dtype: {preprocessed_images[0].dtype}")
    except Exception as e:
        print(f"   Error in preprocessing: {e}")
        return

    # Step 3: Test structure OCR
    print("3. Testing OCR structure processing...")
    try:
        # Test with just the first image to debug
        test_image = preprocessed_images[0]
        print(
            f"   Testing with image shape: {test_image.shape}, dtype: {test_image.dtype}")

        # Check if the image needs conversion for PPStructureV3
        if len(test_image.shape) == 2:
            print("   Converting grayscale to 3-channel...")
            test_image = np.stack(
                [test_image, test_image, test_image], axis=-1)

        if test_image.dtype != np.uint8:
            print("   Converting to uint8...")
            test_image = (test_image * 255).astype(np.uint8)

        print(
            f"   Final image shape: {test_image.shape}, dtype: {test_image.dtype}")

        # Import pipeline directly for testing
        from paddleocr import PPStructureV3
        pipeline = PPStructureV3(
            use_doc_orientation_classify=True,
            use_doc_unwarping=True,
            use_textline_orientation=True,
            use_chart_recognition=True,
            device="gpu",
        )

        print("   Running pipeline.predict...")
        output = pipeline.predict(test_image)
        print(f"   Success: Got {len(output)} results")

        # Test saving
        for i, res in enumerate(output):
            res.save_to_markdown(f"debug_output/image_1.md")
            res.save_to_json("debug_output")
            print(f"   Saved result {i+1}")

    except Exception as e:
        print(f"   Error in OCR processing: {e}")
        import traceback
        traceback.print_exc()
        return

    print("All steps completed successfully!")


if __name__ == "__main__":
    # Test with a simple PDF or use command line argument
    # Replace with your test PDF
    test_pdf = r"C:\Projects\C 4.2.European Flax Manual and SOP.pdf"
    if os.path.exists(test_pdf):
        debug_pdf_processing(test_pdf)
    else:
        print(
            f"Test PDF '{test_pdf}' not found. Please provide a PDF path as argument.")
