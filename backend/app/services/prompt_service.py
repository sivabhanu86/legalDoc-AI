def build_prompt(question, retrieved_documents, retrieved_metadata):

    context_parts = []

    for i, document in enumerate(retrieved_documents):

        page = retrieved_metadata[i]["page"]

        context_parts.append(
            f"[Page {page}]\n{document}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are a document research assistant.

Answer the user's question using ONLY the information
provided in the document context below.

If the context does not contain enough information to
answer the question, say:

"I don't have enough information in the provided document
to answer this question."

Do not invent facts or use outside knowledge.

DOCUMENT CONTEXT:

{context}

USER QUESTION:

{question}

ANSWER:
"""

    return prompt