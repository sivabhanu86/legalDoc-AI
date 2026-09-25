from fastapi import APIRouter, HTTPException

from backend.app.models.schemas import (
    QueryRequest,
    QueryResponse
)

from backend.app.services.rag_service import (
    answer_question
)

from backend.app.services.document_service import (
    get_document
)


router = APIRouter(
    prefix="/query",
    tags=["Query"]
)


@router.post(
    "",
    response_model=QueryResponse
)
def query_document(request: QueryRequest):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    allowed_modes = [
        "legal_research",
        "my_document",
        "combined"
    ]

    if request.mode not in allowed_modes:
        raise HTTPException(
            status_code=400,
            detail="Invalid query mode."
        )

    if (
        request.mode == "my_document"
        and not request.document_id
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                "document_id is required "
                "for my_document mode."
            )
        )

    if request.document_id:

        document = get_document(
            request.document_id
        )

        if document is None:
            raise HTTPException(
                status_code=404,
                detail="Document not found."
            )

    document_id = None
    source_type = None

    # User uploaded document only
    if request.mode == "my_document":
        document_id = request.document_id

    # Preloaded legal corpus only
    elif request.mode == "legal_research":
        source_type = "legal_corpus"

    # Both legal corpus + user documents
    elif request.mode == "combined":
        pass

    result = answer_question(
        question=request.question,
        top_k=request.top_k,
        document_id=document_id,
        source_type=source_type
    )

    return result