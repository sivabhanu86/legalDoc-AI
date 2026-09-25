from pypdf import PdfReader

from backend.app.services.ocr_service import (
    ocr_pdf
)


def extract_text_from_pdf(pdf_path):

    reader = PdfReader(pdf_path)

    pages = []

    for page_number, page in enumerate(
        reader.pages,
        start=1
    ):
        text = page.extract_text()

        if text and text.strip():
            pages.append({
                "page": page_number,
                "text": text
            })

    # Normal PDF extraction worked
    if pages:
        return pages

    # No usable text → OCR fallback
    print(
        "No extractable text found. "
        "Starting OCR..."
    )

    return ocr_pdf(pdf_path)