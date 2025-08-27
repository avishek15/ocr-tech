from ocr.advanced_ocr import advanced_ocr_document
from utils.ingest import document_to_images
from utils.preprocess import preprocess_for_ocr
import requests
import os


def test_advanced_ocr():
    print("Testing Advanced OCR on multiple images...")

    # Process Utility bill
    print("\n1. Processing Utility bill...")
    try:
        utility_images = document_to_images(r"C:\Projects\Utility bill.jpeg")
        preprocessed_utility = [preprocess_for_ocr(
            img) for img in utility_images]
        advanced_ocr_document(preprocessed_utility)
    except Exception as e:
        print(f"Error processing Utility bill: {e}")
        import traceback
        traceback.print_exc()

    # Process demo image (download if needed)
    # print("\n2. Processing demo image...")
    # try:
    #     # Check if demo_image.png exists, download if not
    #     if not os.path.exists("demo_image.png"):
    #         print("Downloading demo image...")
    #         url = "https://paddle-model-ecology.bj.bcebos.com/paddlex/imgs/demo_image/pp_structure_v3_demo.png"
    #         response = requests.get(url, timeout=30)
    #         if response.status_code == 200:
    #             with open("demo_image.png", "wb") as f:
    #                 f.write(response.content)
    #             print("Demo image downloaded successfully")
    #         else:
    #             print(f"Failed to download demo image: {response.status_code}")
    #             return

    #     # Process the demo image
    #     from PIL import Image
    #     demo_image = Image.open("demo_image.png")
    #     preprocessed_demo = preprocess_for_ocr(demo_image)
    #     advanced_ocr_document([preprocessed_demo])

    except Exception as e:
        print(f"Error processing demo image: {e}")
        import traceback
        traceback.print_exc()

    print("\nAdvanced OCR testing completed!")


if __name__ == "__main__":
    test_advanced_ocr()
