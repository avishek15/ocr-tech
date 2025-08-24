from paddleocr import PaddleOCR
from PIL import Image
import numpy as np

# Initialize OCR (only once)
ocr = PaddleOCR(
    # Disables document orientation classification model via this parameter
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,  # Disables text image rectification model via this parameter
    # Disables text line orientation classification model via this parameter
    use_textline_orientation=False,
    lang="en",
    # device="cpu",
)


# Process each page
def ocr_document(images: list[Image.Image]):
    for i, pil_image in enumerate(images):
        print(f"Processing image {i + 1}")

        # Convert PIL Image to numpy array
        if hasattr(pil_image, 'shape'):
            # Already a numpy array
            img_array = pil_image
        else:
            # PIL Image - convert to numpy array
            img_array = np.array(pil_image)

        # Run OCR
        result = ocr.predict(img_array)

        # Handle the new result structure
        if result and len(result) > 0:
            page_result = result[0]
            print(page_result.keys())
            print("=" * 25)
            if page_result and 'rec_texts' in page_result:
                # New API structure
                texts = page_result['rec_texts']
                scores = page_result['rec_scores']
                bboxes = page_result['rec_boxes']

                for text, score, bbox in zip(texts, scores, bboxes):
                    print(
                        f"Page {i + 1} | Text: {text} | Conf: {score:.2f} | BBox: {bbox}"
                    )
            else:
                # Fallback to old structure or empty result
                print(f"Page {i + 1}: No text detected")
        else:
            print(f"Page {i + 1}: No text detected")
