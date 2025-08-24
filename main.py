from utils.ingest import document_to_images
from matplotlib import pyplot as plt
from utils.preprocess import preprocess_for_ocr
from ocr.paddle import ocr_document


def main():
    print("Hello from ocr-tech!")
    images = document_to_images(r"C:\Projects\Utility bill.jpeg")

    preprocessed_images = [preprocess_for_ocr(img) for img in images]

    ocr_document(preprocessed_images)

    plt.imshow(preprocessed_images[0], cmap="gray")
    plt.show()


if __name__ == "__main__":
    main()
