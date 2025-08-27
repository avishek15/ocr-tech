from paddleocr import PaddleOCR
import numpy as np
from typing import List, Dict, Any
import json


class AdvancedOCR:
    def __init__(self):
        self.ocr = PaddleOCR(
            use_doc_orientation_classify=True,
            use_doc_unwarping=True,
            use_textline_orientation=True,
            lang="en",
            # Use server models for better accuracy
            text_detection_model_name="PP-OCRv5_server_det",
            text_recognition_model_name="PP-OCRv5_server_rec",
            # Enable GPU if available for better performance
            device="gpu"  # Will fall back to CPU if GPU not available
        )

    def process_image(self, image):
        """
        Process an image (PIL Image or numpy array) and return structured results
        """
        # Convert to numpy array if needed
        if hasattr(image, 'shape'):
            img_array = image
        else:
            img_array = np.array(image)

        # Ensure proper format
        if len(img_array.shape) == 2:
            img_array = np.stack([img_array, img_array, img_array], axis=-1)
        elif img_array.shape[2] == 1:
            img_array = np.repeat(img_array, 3, axis=2)

        if img_array.dtype != np.uint8:
            img_array = (img_array * 255).astype(np.uint8)

        # Run OCR
        result = self.ocr.predict(img_array)
        return result

    def create_structured_markdown(self, ocr_result, save_path="output"):
        """
        Create well-structured markdown using text location and orientation information
        """
        if not ocr_result:
            return None

        # Get the first result (single image processing)
        res = ocr_result[0]

        # Extract structured data
        structured_data = self._extract_structured_data(res)

        # Generate markdown
        markdown_content = self._generate_markdown(structured_data)

        # Save results
        filename = f"{save_path}/structured_ocr_result.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        # Also save JSON with full details
        json_filename = f"{save_path}/structured_ocr_result.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(structured_data, f, ensure_ascii=False, indent=2)

        return markdown_content

    def _extract_structured_data(self, ocr_result):
        """
        Extract structured data from OCR result using location information
        """
        structured_data = {
            "text_blocks": [],
            "lines": [],
            "paragraphs": [],
            "layout": []
        }

        # Get text detection boxes and recognition results
        rec_boxes = ocr_result.get('rec_boxes', [])
        rec_texts = ocr_result.get('rec_texts', [])
        rec_scores = ocr_result.get('rec_scores', [])

        # Group text by Y-coordinate to identify lines
        lines = {}
        for i, (box, text, score) in enumerate(zip(rec_boxes, rec_texts, rec_scores)):
            y_center = (box[1] + box[3]) / 2  # Average of y_min and y_max

            # Find existing line or create new one
            line_key = None
            for existing_y in lines.keys():
                if abs(existing_y - y_center) < 20:  # Tolerance for line grouping
                    line_key = existing_y
                    break

            if line_key is None:
                line_key = y_center
                lines[line_key] = []

            lines[line_key].append({
                "text": text,
                "score": float(score),
                "box": box.tolist() if hasattr(box, 'tolist') else box,
                "x_min": int(box[0]),
                "x_max": int(box[2]),
                "y_min": int(box[1]),
                "y_max": int(box[3])
            })

        # Sort lines by Y position and sort words within lines by X position
        sorted_lines = []
        for y_pos in sorted(lines.keys()):
            line_words = lines[y_pos]
            sorted_words = sorted(line_words, key=lambda x: x['x_min'])
            line_text = ' '.join([word['text'] for word in sorted_words])

            sorted_lines.append({
                "y_position": y_pos,
                "words": sorted_words,
                "line_text": line_text,
                "confidence": sum(word['score'] for word in sorted_words) / len(sorted_words) if sorted_words else 0
            })

        # Group lines into paragraphs based on vertical spacing
        paragraphs = []
        current_paragraph = []

        for i, line in enumerate(sorted_lines):
            if not current_paragraph:
                current_paragraph.append(line)
                continue

            # Check vertical gap with previous line
            prev_line = sorted_lines[i-1]
            gap = line['y_position'] - prev_line['y_position']

            if gap > 40:  # Large gap indicates new paragraph
                paragraphs.append({
                    "lines": current_paragraph,
                    "paragraph_text": '\n'.join([l['line_text'] for l in current_paragraph])
                })
                current_paragraph = [line]
            else:
                current_paragraph.append(line)

        if current_paragraph:
            paragraphs.append({
                "lines": current_paragraph,
                "paragraph_text": '\n'.join([l['line_text'] for l in current_paragraph])
            })

        structured_data['lines'] = sorted_lines
        structured_data['paragraphs'] = paragraphs

        return structured_data

    def _generate_markdown(self, structured_data):
        """
        Generate well-structured markdown from extracted data
        """
        markdown_lines = []

        markdown_lines.append("# Document OCR Results\n")
        markdown_lines.append("## Structured Content\n")

        # Add paragraphs with proper spacing
        for i, paragraph in enumerate(structured_data['paragraphs']):
            markdown_lines.append(paragraph['paragraph_text'])
            markdown_lines.append("")  # Empty line for paragraph separation

        # Add detailed information section
        markdown_lines.append("## Detailed Information\n")
        markdown_lines.append(
            f"- Total paragraphs: {len(structured_data['paragraphs'])}")
        markdown_lines.append(
            f"- Total lines: {len(structured_data['lines'])}")

        # Add confidence information
        avg_confidence = sum(line['confidence'] for line in structured_data['lines']) / len(
            structured_data['lines']) if structured_data['lines'] else 0
        markdown_lines.append(f"- Average confidence: {avg_confidence:.3f}")

        return '\n'.join(markdown_lines)


def advanced_ocr_document(images: list):
    """
    Process images using advanced OCR with structured markdown output
    """
    ocr_processor = AdvancedOCR()

    for i, image in enumerate(images):
        print(f"Processing image {i + 1}")

        # Process image
        result = ocr_processor.process_image(image)

        # Create structured markdown
        markdown_content = ocr_processor.create_structured_markdown(
            result, "output")

        print(f"Completed processing image {i + 1}")
        print(f"Markdown saved to output/structured_ocr_result.md")

    return True
