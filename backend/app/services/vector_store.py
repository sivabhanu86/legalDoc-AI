import chromadb


client = chromadb.PersistentClient(
    path="vector_store"
)

collection = client.get_or_create_collection(
    name="legal_documents"
)


def add_chunks(chunks, embeddings, document_id, document_name, source_type):
    ids = []
    documents = []
    metadatas = []

    for index, chunk in enumerate(chunks):

        chunk_id = f"{document_id}_chunk_{index}"

        ids.append(chunk_id)

        documents.append(
            chunk["text"]
        )

        metadatas.append({
        "document_id": document_id,
        "document_name": document_name,
        "source_type": source_type,
        "page": chunk["page"],
        "section": chunk.get("section") or "Unknown",
        "chunk_id": chunk_id
        })

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )


def search(
    query_embedding,
    top_k=5,
    document_id=None,
    source_type=None
):
    where_conditions = []

    if document_id:
        where_conditions.append({
            "document_id": document_id
        })

    if source_type:
        where_conditions.append({
            "source_type": source_type
        })

    where = None

    if len(where_conditions) == 1:
        where = where_conditions[0]

    elif len(where_conditions) > 1:
        where = {
            "$and": where_conditions
        }

    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=top_k,
        where=where
    )

    return results


def delete_document(document_id):

    collection.delete(
        where={
            "document_id": document_id
        }
    )

def get_all_chunks():
    results = collection.get(
        include=["documents", "metadatas"]
    )

    return {
        "documents": results["documents"],
        "metadatas": results["metadatas"]
    }