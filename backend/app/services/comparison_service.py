from backend.app.services.vector_store import (
    get_all_chunks
)

from backend.app.services.llm_service import (
    generate_answer
)


def get_document_chunks(document_id):
    data = get_all_chunks()

    chunks = []

    for document, metadata in zip(
        data["documents"],
        data["metadatas"]
    ):
        if metadata.get("document_id") == document_id:
            chunks.append({
                "text": document,
                "page": metadata.get("page"),
                "section": metadata.get("section")
            })

    return chunks


def build_document_context(chunks, max_chars=30000):

    context = []
    total_chars = 0

    for chunk in chunks:

        text = chunk["text"]

        block = (
            f"[Page {chunk['page']}]\n"
            f"{text}"
        )

        if total_chars + len(block) > max_chars:
            break

        context.append(block)
        total_chars += len(block)

    return "\n\n".join(context)


def compare_documents(
    document_a_id,
    document_b_id
):

    chunks_a = get_document_chunks(
        document_a_id
    )

    chunks_b = get_document_chunks(
        document_b_id
    )

    if not chunks_a:
        raise ValueError(
            "Document A was not found."
        )

    if not chunks_b:
        raise ValueError(
            "Document B was not found."
        )

    context_a = build_document_context(
        chunks_a
    )

    context_b = build_document_context(
        chunks_b
    )

    prompt = f"""
You are a legal document comparison assistant.

Compare the two documents below using ONLY
the provided document content.

Do not use outside knowledge.

Identify:

1. Key similarities
2. Key differences
3. Clauses, obligations, dates, amounts,
   conditions, or other provisions that differ
4. Potential issues requiring human review

For every important difference, mention the
relevant page number from Document A or
Document B when available.

Do not provide legal advice.

Use this format:

## Similarities

- ...

## Key Differences

- **Topic:** ...
  - Document A: ...
  - Document B: ...
  - Pages: ...

## Potential Issues for Human Review

- ...

If the documents do not contain enough information
for a comparison, clearly state that.

DOCUMENT A:

{context_a}

DOCUMENT B:

{context_b}

COMPARISON:
"""

    answer = generate_answer(prompt)

    return {
        "document_a_id": document_a_id,
        "document_b_id": document_b_id,
        "answer": answer,
        "document_a_pages": len(chunks_a),
        "document_b_pages": len(chunks_b)
    }