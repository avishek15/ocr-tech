import os
from typing import List, Dict, Any
from datetime import datetime


class DocumentGenerator:
    """Generate markdown documents from OCR results."""

    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def create_markdown(self, ocr_results: List[Dict[str, Any]],
                        document_name: str = "document") -> str:
        """
        Create a markdown file from OCR results.

        Args:
            ocr_results: List of OCR results from each page
            document_name: Base name for the output file

        Returns:
            Path to the created markdown file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{document_name}_{timestamp}.md"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self._generate_header(document_name))

            for page_num, page_result in enumerate(ocr_results, 1):
                f.write(self._generate_page_section(page_num, page_result))

        return filepath

    def _generate_header(self, document_name: str) -> str:
        """Generate the markdown header."""
        return f"""# OCR Results: {document_name}

Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

"""

    def _generate_page_section(self, page_num: int, page_result: Dict[str, Any]) -> str:
        """Generate markdown content for a single page."""
        content = f"## Page {page_num}\n\n"

        if not page_result or 'rec_texts' not in page_result:
            content += "*No text detected on this page*\n\n"
            return content

        texts = page_result.get('rec_texts', [])
        scores = page_result.get('rec_scores', [])
        bboxes = page_result.get('rec_boxes', [])

        if not texts:
            content += "*No text detected on this page*\n\n"
            return content

        # Group text by approximate lines based on y-coordinate
        lines = self._group_text_by_lines(texts, bboxes, scores)

        for line_num, line_data in enumerate(lines, 1):
            line_text = ' '.join([item['text'] for item in line_data])
            avg_conf = sum(item['score']
                           for item in line_data) / len(line_data)

            content += f"{line_text}  \n"
            content += f"<!-- Line {line_num} - Confidence: {avg_conf:.2f} -->\n"

        content += "\n---\n\n"
        return content

    def _group_text_by_lines(self, texts: List[str], bboxes: List[List[float]],
                             scores: List[float]) -> List[List[Dict[str, Any]]]:
        """Group text elements by approximate lines based on y-coordinates."""
        if not texts or not bboxes:
            return []

        # Create text items with their properties
        items = []
        for text, bbox, score in zip(texts, bboxes, scores):
            if len(bbox) >= 4:
                # Calculate center y-coordinate
                y_coords = [bbox[i] for i in range(1, len(bbox), 2)]
                center_y = sum(y_coords) / len(y_coords)

                items.append({
                    'text': text,
                    'score': score,
                    'bbox': bbox,
                    'center_y': center_y
                })

        # Sort by y-coordinate, then by x-coordinate
        items.sort(key=lambda x: (x['center_y'], x['bbox'][0]))

        # Group into lines based on y-coordinate proximity
        lines = []
        if not items:
            return lines

        current_line = [items[0]]
        y_threshold = 20  # pixels

        for item in items[1:]:
            if abs(item['center_y'] - current_line[-1]['center_y']) <= y_threshold:
                current_line.append(item)
            else:
                lines.append(current_line)
                current_line = [item]

        if current_line:
            lines.append(current_line)

        return lines

    def create_detailed_report(self, ocr_results: List[Dict[str, Any]],
                               document_name: str = "document") -> str:
        """
        Create a detailed markdown report with bounding boxes and confidence scores.

        Args:
            ocr_results: List of OCR results from each page
            document_name: Base name for the output file

        Returns:
            Path to the created markdown file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{document_name}_detailed_{timestamp}.md"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self._generate_detailed_header(document_name))

            for page_num, page_result in enumerate(ocr_results, 1):
                f.write(self._generate_detailed_page_section(
                    page_num, page_result))

        return filepath

    def _generate_detailed_header(self, document_name: str) -> str:
        """Generate the detailed markdown header."""
        return f"""# Detailed OCR Report: {document_name}

Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

This report contains detailed information about each detected text element including bounding boxes and confidence scores.

---

"""

    def _generate_detailed_page_section(self, page_num: int, page_result: Dict[str, Any]) -> str:
        """Generate detailed markdown content for a single page."""
        content = f"## Page {page_num}\n\n"

        if not page_result or 'rec_texts' not in page_result:
            content += "*No text detected on this page*\n\n"
            return content

        texts = page_result.get('rec_texts', [])
        scores = page_result.get('rec_scores', [])
        bboxes = page_result.get('rec_boxes', [])

        if not texts:
            content += "*No text detected on this page*\n\n"
            return content

        content += "| Text | Confidence | Bounding Box |\n"
        content += "|------|------------|--------------|\n"

        for text, score, bbox in zip(texts, scores, bboxes):
            # Format bounding box as readable string
            bbox_str = str([int(x) for x in bbox]) if bbox else "N/A"
            content += f"| {text} | {score:.3f} | {bbox_str} |\n"

        content += "\n---\n\n"
        return content
