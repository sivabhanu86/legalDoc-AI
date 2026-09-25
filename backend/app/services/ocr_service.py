import os
import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

import fitz


from PIL import Image


def ocr_pdf(pdf_path):
    """
    Extract text from a scanned PDF using OCR.
    """

    document = fitz.open(pdf_path)

    pages = []

    for page_number, page in enumerate(
        document,
        start=1
    ):
        pixmap = page.get_pixmap(
            matrix=fitz.Matrix(2, 2),
            alpha=False
        )

        image_path = (
            f"data/processed/ocr_page_{page_number}.png"
        )

        os.makedirs(
            "data/processed",
            exist_ok=True
        )

        pixmap.save(image_path)

        image = Image.open(image_path)

        text = pytesseract.image_to_string(
            image
        )

        if text.strip():
            pages.append({
                "page": page_number,
                "text": text
            })

        image.close()

        os.remove(image_path)

    document.close()

    return pages