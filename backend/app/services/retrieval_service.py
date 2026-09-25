from backend.app.services.embedding_service import generate_embeddings
from backend.app.services.vector_store import search


def retrieve_relevant_chunks(
    question,
    top_k=5,
    document_id=None,
    source_type=None
):

    question_embedding = generate_embeddings(
        [question]
    )[0]

    results = search(
        question_embedding,
        top_k=top_k,
        document_id=document_id,
        source_type=source_type
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    evaluation = {
        "best_distance": distances[0],
        "average_top_3_distance": (
            sum(distances[:3])
            / min(3, len(distances))
        ),
        "gap_top1_top3": (
            distances[2] - distances[0]
            if len(distances) >= 3
            else None
        )
    }

    return {
        "documents": documents,
        "metadatas": metadatas,
        "distances": distances,
        "evaluation": evaluation
    }