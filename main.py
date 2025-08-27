from utils.ingest import document_to_images
from matplotlib import pyplot as plt
from utils.preprocess import preprocess_for_ocr
from ocr.paddle import ocr_document
from ocr.structure import ocr_document as structure_ocr_document


def main():
    print("Hello from ocr-tech!")

    # Example: Process a PDF file
    # Replace with your PDF file path
    # Change this to your PDF file path
    pdf_path = r"C:\Projects\C 4.2.European Flax Manual and SOP.pdf"

    # Convert PDF to images
    images = document_to_images(pdf_path)

    # Preprocess images for OCR
    preprocessed_images = [preprocess_for_ocr(img) for img in images]

    # Process through OCR structure analysis
    structure_ocr_document(preprocessed_images)

    # plt.imshow(preprocessed_images[0], cmap="gray")
    # plt.show()


if __name__ == "__main__":
    main()
