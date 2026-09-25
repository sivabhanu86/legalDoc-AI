from backend.app.services.retrieval_service import (
    retrieve_relevant_chunks
)

from backend.app.services.keyword_search import (
    KeywordSearch
)


keyword_search = KeywordSearch()


def reciprocal_rank_fusion(
    semantic_results,
    keyword_results,
    k=60
):
    fused = {}

    # Add semantic search results
    for rank, result in enumerate(
        semantic_results,
        start=1
    ):
        chunk_id = result["metadata"]["chunk_id"]

        if chunk_id not in fused:
            fused[chunk_id] = {
                "text": result["text"],
                "metadata": result["metadata"],
                "semantic_distance": result.get(
                    "semantic_distance"
                ),
                "keyword_score": 0.0,
                "rrf_score": 0.0
            }

        fused[chunk_id]["rrf_score"] += (
            1 / (k + rank)
        )

    # Add keyword search results
    for rank, result in enumerate(
        keyword_results,
        start=1
    ):
        chunk_id = result["metadata"]["chunk_id"]

        if chunk_id not in fused:
            fused[chunk_id] = {
                "text": result["text"],
                "metadata": result["metadata"],
                "semantic_distance": None,
                "keyword_score": result["score"],
                "rrf_score": 0.0
            }
        else:
            fused[chunk_id]["keyword_score"] = (
                result["score"]
            )

        fused[chunk_id]["rrf_score"] += (
            1 / (k + rank)
        )

    ranked_results = sorted(
        fused.values(),
        key=lambda result: result["rrf_score"],
        reverse=True
    )

    return ranked_results


def hybrid_search(
    question,
    semantic_top_k=20,
    keyword_top_k=20,
    candidate_k=20,
    document_id=None,
    source_type=None
):

    # -----------------------------
    # 1. Semantic search
    # -----------------------------

    semantic_raw = retrieve_relevant_chunks(
        question=question,
        top_k=semantic_top_k,
        document_id=document_id,
        source_type=source_type
    )

    semantic_results = []

    for document, metadata, distance in zip(
        semantic_raw["documents"],
        semantic_raw["metadatas"],
        semantic_raw["distances"]
    ):
        semantic_results.append({
            "text": document,
            "metadata": metadata,
            "semantic_distance": distance
        })


    # -----------------------------
    # 2. Keyword search
    # -----------------------------

    keyword_results = keyword_search.search(
        query=question,
        top_k=keyword_top_k,
        document_id=document_id
    )


    # -----------------------------
    # 3. RRF Fusion
    # -----------------------------

    fused_results = reciprocal_rank_fusion(
        semantic_results,
        keyword_results
    )


    # -----------------------------
    # 4. Return larger candidate pool
    # -----------------------------

    return fused_results[:candidate_k]