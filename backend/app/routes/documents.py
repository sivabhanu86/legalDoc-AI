from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)

import os
import shutil

from backend.app.services.document_service import (
    ingest_document,
    get_documents,
    get_document,
    remove_document
)


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


UPLOAD_DIR = "data/user_documents"


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    os.makedirs(
        UPLOAD_DIR,
        exist_ok=True
    )

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    try:

        document = ingest_document(
            file_path
        )

        return {
            "message": "Document uploaded and indexed successfully.",
            "document": document
        }

    except Exception as error:
        print("UPLOAD ERROR:", repr(error))
        if os.path.exists(file_path):
            os.remove(file_path)

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@router.get("/")
def list_documents():

    return {
        "documents": get_documents()
    }


@router.get("/{document_id}")
def get_document_by_id(
    document_id: str
):

    document = get_document(
        document_id
    )

    if document is None:

        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    return document


@router.delete("/{document_id}")
def delete_document_by_id(
    document_id: str
):

    deleted = remove_document(
        document_id
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    return {
        "message": "Document deleted successfully.",
        "document_id": document_id
    }