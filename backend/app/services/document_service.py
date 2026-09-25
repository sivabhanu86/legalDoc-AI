import json
import os
import uuid

from backend.app.services.pdf_extractor import (
    extract_text_from_pdf
)

from backend.app.services.chunker import (
    create_chunks
)

from backend.app.services.embedding_service import (
    generate_embeddings
)

from backend.app.services.vector_store import (
    add_chunks,
    delete_document
)


REGISTRY_PATH = "data/processed/documents.json"


def load_registry():

    if not os.path.exists(REGISTRY_PATH):
        return []

    with open(
        REGISTRY_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def save_registry(documents):

    os.makedirs(
        os.path.dirname(REGISTRY_PATH),
        exist_ok=True
    )

    with open(
        REGISTRY_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            documents,
            file,
            indent=4
        )


def ingest_document(
    pdf_path,
    source_type="user_document"
):

    document_id = str(uuid.uuid4())

    document_name = os.path.basename(
        pdf_path
    )

    # 1. Extract text

    pages = extract_text_from_pdf(
        pdf_path
    )

    # 2. Create chunks

    chunks = create_chunks(
        pages
    )

    # 3. Extract text from chunks

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    # 4. Generate embeddings

    embeddings = generate_embeddings(
        texts
    )

    # 5. Store in vector database

    add_chunks(
        chunks,
        embeddings,
        document_id,
        document_name,
        source_type
    )

    # 6. Create document record

    document = {
        "document_id": document_id,
        "document_name": document_name,
        "source_type": source_type,
        "file_path": pdf_path,
        "pages": len(pages),
        "chunks": len(chunks)
    }

    # 7. Save registry

    documents = load_registry()

    documents.append(document)

    save_registry(
        documents
    )

    return document


def get_documents():

    return load_registry()


def get_document(document_id):

    documents = load_registry()

    for document in documents:

        if document["document_id"] == document_id:
            return document

    return None


def remove_document(document_id):

    documents = load_registry()

    document = None

    for item in documents:

        if item["document_id"] == document_id:
            document = item
            break

    if document is None:
        return False

    # Delete vector chunks

    delete_document(
        document_id
    )

    # Delete physical PDF

    file_path = document.get(
        "file_path"
    )

    if file_path and os.path.exists(
        file_path
    ):

        os.remove(
            file_path
        )

    # Remove registry entry

    documents = [
        item
        for item in documents
        if item["document_id"] != document_id
    ]

    save_registry(
        documents
    )

    return True