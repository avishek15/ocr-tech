
from paddleocr import PPStructureV3
from PIL import Image
import numpy as np


pipeline = PPStructureV3(
    use_doc_orientation_classify=True,
    use_doc_unwarping=True,
    use_textline_orientation=True,
    use_chart_recognition=True,
    device="gpu",
)

# Process each page


def ocr_document(images: list, output_dir="output"):
    """
    Process a list of images (either PIL Images or numpy arrays) through OCR.
    """
    for i, image in enumerate(images):
        print(f"Processing image {i + 1}")

        # Convert to numpy array if it's a PIL Image
        if hasattr(image, 'shape'):
            # Already a numpy array
            img_array = image
        else:
            # PIL Image - convert to numpy array
            img_array = np.array(image)

        # Ensure the array has the correct shape and type for PPStructureV3
        if len(img_array.shape) == 2:
            # Convert grayscale to 3-channel
            img_array = np.stack([img_array, img_array, img_array], axis=-1)
        elif img_array.shape[2] == 1:
            # Convert single channel to 3-channel
            img_array = np.repeat(img_array, 3, axis=2)

        # Ensure the array is uint8
        if img_array.dtype != np.uint8:
            img_array = (img_array * 255).astype(np.uint8)

        print(f"Image shape: {img_array.shape}, dtype: {img_array.dtype}")

        # Run OCR
        print("Running OCR...")
        try:
            output = pipeline.predict(img_array)
            print("OCR completed successfully")

            # Save the result as Markdown
            for res in output:
                res.save_to_markdown(f"{output_dir}/image_{i + 1}.md")
                res.save_to_json(f"{output_dir}")
                print(f"Saved results for image {i + 1}")

        except Exception as e:
            print(f"Error processing image {i + 1}: {e}")
            import traceback
            traceback.print_exc()
