import sys
import os

from backend.app.services.document_service import (
    ingest_document
)


def main():

    if len(sys.argv) < 2:
        print(
            "Usage: python -m scripts.ingest_document <pdf_path>"
        )
        return

    pdf_path = sys.argv[1]

    if not os.path.exists(pdf_path):
        print("File not found:", pdf_path)
        return

    document = ingest_document(
        pdf_path,
        source_type="legal_corpus"
    )

    print("\nLegal document indexed successfully.")
    print("Document ID:", document["document_id"])
    print("Document:", document["document_name"])
    print("Pages:", document["pages"])
    print("Chunks:", document["chunks"])


if __name__ == "__main__":
    main()