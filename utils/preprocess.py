import cv2
import numpy as np


def preprocess_for_ocr(pil_image):
    """
    Convert PIL image to OpenCV format and enhance for OCR.
    Ensures the dimension of the max side is 1024px while maintaining aspect ratio.
    """
    # Convert PIL to OpenCV
    img = np.array(pil_image)
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Resize image to ensure max dimension is 1024px while maintaining aspect ratio
    height, width = img.shape[:2]
    max_dimension = 1024

    if max(height, width) > max_dimension:
        if height > width:
            new_height = max_dimension
            new_width = int(width * max_dimension / height)
        else:
            new_width = max_dimension
            new_height = int(height * max_dimension / width)

        img = cv2.resize(img, (new_width, new_height),
                         interpolation=cv2.INTER_AREA)

    # Grayscale (if not already)
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    img = clahe.apply(img)

    # Optional: Binary threshold (adaptive)
    # img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Convert back to 3-channel image (H, W, 3) — most reliable for PaddleOCR
    img_3c = np.stack([img, img, img], axis=-1)

    return img_3c  # Shape: (H, W, 3)
