from fastapi import APIRouter, HTTPException

from backend.app.models.schemas import (
    ComparisonRequest,
    ComparisonResponse
)

from backend.app.services.document_service import (
    get_document
)

from backend.app.services.comparison_service import (
    compare_documents
)


router = APIRouter(
    prefix="/comparison",
    tags=["Comparison"]
)


@router.post(
    "",
    response_model=ComparisonResponse
)
def compare(request: ComparisonRequest):

    if (
        request.document_a_id
        == request.document_b_id
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                "Please select two different documents."
            )
        )

    document_a = get_document(
        request.document_a_id
    )

    document_b = get_document(
        request.document_b_id
    )

    if document_a is None:
        raise HTTPException(
            status_code=404,
            detail="Document A not found."
        )

    if document_b is None:
        raise HTTPException(
            status_code=404,
            detail="Document B not found."
        )

    try:

        result = compare_documents(
            request.document_a_id,
            request.document_b_id
        )

        return result

    except Exception as error:

        print(
            "COMPARISON ERROR:",
            repr(error)
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )