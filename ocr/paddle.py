from utils.preprocess import preprocess_for_ocr
from paddleocr import PaddleOCR
from paddleocr import PPStructureV3
from PIL import Image
import numpy as np
import json
from typing import List, Dict, Any, Tuple
import sys
from pathlib import Path

# Add the parent directory to path to import utils
sys.path.append(str(Path(__file__).parent.parent))

# Initialize OCR (only once)
ocr = PaddleOCR(
    use_doc_orientation_classify=True,
    use_doc_unwarping=True,
    use_textline_orientation=True,
    device="gpu",
)


def arrange_text_by_position(rec_texts: List[str], rec_boxes: List[List[float]], y_threshold: int = 15) -> str:
    """
    Arrange text based on spatial position (top-to-bottom, left-to-right)

    Args:
        rec_texts: List of recognized text strings
        rec_boxes: List of bounding boxes [x1, y1, x2, y2]
        y_threshold: Vertical distance threshold to consider lines as same row

    Returns:
        String with spatially arranged text
    """
    if not rec_texts or not rec_boxes:
        return ""

    # Combine text with position info
    text_items = []
    for i, (text, box) in enumerate(zip(rec_texts, rec_boxes)):
        if len(box) >= 4:
            x1, y1, x2, y2 = box[:4]
            center_y = (y1 + y2) / 2
            center_x = (x1 + x2) / 2
            text_items.append({
                'text': text,
                'center_y': center_y,
                'center_x': center_x,
                'box': box
            })

    if not text_items:
        return ""

    # Sort by Y first (top to bottom), then by X (left to right)
    text_items.sort(key=lambda item: (item['center_y'], item['center_x']))

    # Group items that are on similar Y levels (same row/line)
    grouped_lines = []
    current_line = []
    current_y = None

    for item in text_items:
        if current_y is None or abs(item['center_y'] - current_y) <= y_threshold:
            # Same line
            current_line.append(item)
            current_y = item['center_y'] if current_y is None else current_y
        else:
            # New line
            if current_line:
                # Sort current line by X coordinate
                current_line.sort(key=lambda x: x['center_x'])
                grouped_lines.append(current_line)
            current_line = [item]
            current_y = item['center_y']

    # Don't forget the last line
    if current_line:
        current_line.sort(key=lambda x: x['center_x'])
        grouped_lines.append(current_line)

    # Convert to text with appropriate spacing
    result_lines = []
    prev_y = None

    for line_group in grouped_lines:
        # Join texts in the same line with spaces
        line_text = ' '.join([item['text'] for item in line_group])

        # Add extra spacing for significant Y gaps (new paragraphs/sections)
        current_y = line_group[0]['center_y']
        if prev_y is not None and current_y - prev_y > 30:  # Large gap = new section
            result_lines.append('')  # Add blank line

        result_lines.append(line_text)
        prev_y = current_y

    return '\n'.join(result_lines)


def process_image_direct(image) -> Dict[str, Any]:
    """
    Process an image through OCR and return structured results without saving files.

    Args:
        image: PIL Image or numpy array

    Returns:
        Dictionary with OCR results including text, boxes, and arranged text
    """
    try:
        # Preprocess the image first (resize, enhance, etc.)
        if hasattr(image, 'shape'):
            # Already a numpy array - convert to PIL Image for preprocessing
            if len(image.shape) == 3 and image.shape[2] == 3:
                # Convert BGR to RGB if needed (OpenCV format)
                if image.dtype != np.uint8:
                    image = (image * 255).astype(np.uint8)
                pil_image = Image.fromarray(image)
            else:
                # Handle other numpy array formats
                pil_image = Image.fromarray(image)
        else:
            # Already a PIL Image
            pil_image = image

        # Apply preprocessing (resize to max 1024px, enhance contrast, etc.)
        preprocessed_img = preprocess_for_ocr(pil_image)

        # Run OCR on the preprocessed image
        output = ocr.predict(preprocessed_img)

        # Extract text and boxes from OCR results
        results = []
        for res in output:
            # Check if the result has the expected OCR data in JSON
            if hasattr(res, 'json') and 'res' in res.json:
                json_data = res.json['res']
                rec_texts = json_data.get('rec_texts', [])
                rec_boxes = json_data.get('rec_boxes', [])
                rec_scores = json_data.get('rec_scores', [])

                if rec_texts and rec_boxes:
                    arranged_text = arrange_text_by_position(
                        rec_texts, rec_boxes)
                    results.append({
                        'texts': rec_texts,
                        'boxes': rec_boxes,
                        'scores': rec_scores,
                        'arranged_text': arranged_text
                    })
                else:
                    # Still add an empty result to maintain structure
                    results.append({
                        'texts': [],
                        'boxes': [],
                        'scores': [],
                        'arranged_text': ''
                    })
            else:
                # Still add an empty result to maintain structure
                results.append({
                    'texts': [],
                    'boxes': [],
                    'scores': [],
                    'arranged_text': ''
                })

        return {
            'success': True,
            'results': results,
            'total_pages': len(results)
        }

    except Exception as e:
        import traceback
        print(f"DEBUG: Exception occurred: {str(e)}")
        print(f"DEBUG: Traceback: {traceback.format_exc()}")
        return {
            'success': False,
            'error': str(e),
            'results': []
        }


def ocr_document(images: list, output_dir="output"):
    """
    Process a list of images (either PIL Images or numpy arrays) through OCR.
    """
    for i, image in enumerate(images):
        print(f"Processing image {i + 1}")

        # Preprocess the image first (resize, enhance, etc.)
        if hasattr(image, 'shape'):
            # Already a numpy array - convert to PIL Image for preprocessing
            if len(image.shape) == 3 and image.shape[2] == 3:
                # Convert BGR to RGB if needed (OpenCV format)
                if image.dtype != np.uint8:
                    image = (image * 255).astype(np.uint8)
                pil_image = Image.fromarray(image)
            else:
                # Handle other numpy array formats
                pil_image = Image.fromarray(image)
        else:
            # Already a PIL Image
            pil_image = image

        # Apply preprocessing (resize to max 1024px, enhance contrast, etc.)
        preprocessed_img = preprocess_for_ocr(pil_image)

        print(
            f"Original image shape: {np.array(pil_image).shape if hasattr(pil_image, 'size') else image.shape}")
        print(
            f"Preprocessed image shape: {preprocessed_img.shape}, dtype: {preprocessed_img.dtype}")

        # Run OCR
        print("Running OCR...")
        try:
            output = ocr.predict(preprocessed_img)
            print("OCR completed successfully")

            # Save the result as Markdown
            for res in output:
                res.save_to_img(f"{output_dir}/output_image_{i + 1}.png")
                # res.save_to_markdown("output")
                res.save_to_json(f"{output_dir}/output_image_{i + 1}.json")
                print(f"Saved results for image {i + 1}")

        except Exception as e:
            print(f"Error processing image {i + 1}: {e}")
            import traceback
            traceback.print_exc()
