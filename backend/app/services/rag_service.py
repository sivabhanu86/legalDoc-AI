from backend.app.services.relevance_service import check_relevance
from backend.app.services.hybrid_retrieval import hybrid_search
from backend.app.services.reranker import rerank
from backend.app.services.prompt_service import build_prompt
from backend.app.services.llm_service import (
    generate_answer,
    stream_answer
)

import json
from backend.app.services.citation_service import create_citations


def answer_question(
    question,
    top_k=5,
    document_id=None,
    source_type=None
):
    # 1. Retrieve candidate chunks using
    # semantic search + keyword search + RRF
    candidates = hybrid_search(
        question=question,
        semantic_top_k=20,
        keyword_top_k=20,
        candidate_k=20,
        document_id=document_id,
        source_type=source_type
    )

    # 2. Rerank the retrieved candidates
    ranked_results = rerank(
        question=question,
        candidates=candidates,
        top_k=top_k
    )
    relevance = check_relevance(
        ranked_results
    )

    if not relevance["relevant"]:
        return {
            "answer": (
                "I don't have enough information "
                "in the provided documents to answer "
                "this question."
            ),
            "citations": [],
            "evaluation": {
                "retrieval_method": "hybrid_rrf_reranker",
                "candidate_count": len(candidates),
                "final_count": len(ranked_results),
                "relevant": False,
                "best_reranker_score": relevance["best_score"]
            }
        }
    

    # 3. Extract text and metadata
    documents = [
        result["text"]
        for result in ranked_results
    ]

    metadatas = [
        result["metadata"]
        for result in ranked_results
    ]

    distances = [
        result.get("semantic_distance")
        for result in ranked_results
    ]

    # 4. Build prompt using the final retrieved context
    prompt = build_prompt(
        question,
        documents,
        metadatas
    )

    # 5. Generate answer using LLM
    answer = generate_answer(prompt)

    # 6. Create citations
    citations = create_citations(
        metadatas,
        distances
    )

    # 7. Return complete RAG response
    return {
        "answer": answer,
        "citations": citations,
        "evaluation": {
            "retrieval_method": "hybrid_rrf_reranker",
            "candidate_count": len(candidates),
            "final_count": len(ranked_results)
        }
    }
def stream_answer_question(
    question,
    top_k=5,
    document_id=None,
    source_type=None
):
    candidates = hybrid_search(
        question=question,
        semantic_top_k=20,
        keyword_top_k=20,
        candidate_k=20,
        document_id=document_id,
        source_type=source_type
    )

    ranked_results = rerank(
        question=question,
        candidates=candidates,
        top_k=top_k
    )

    relevance = check_relevance(
        ranked_results
    )

    if not relevance["relevant"]:

        message = (
            "I don't have enough information "
            "in the provided documents to answer "
            "this question."
        )

        yield (
            "data: "
            + json.dumps({
                "type": "error",
                "content": message
            })
            + "\n\n"
        )

        return

    documents = [
        result["text"]
        for result in ranked_results
    ]

    metadatas = [
        result["metadata"]
        for result in ranked_results
    ]

    distances = [
        result.get("semantic_distance")
        for result in ranked_results
    ]

    prompt = build_prompt(
        question,
        documents,
        metadatas
    )

    for token in stream_answer(prompt):

        yield (
            "data: "
            + json.dumps({
                "type": "token",
                "content": token
            })
            + "\n\n"
        )

    citations = create_citations(
        metadatas,
        distances
    )

    evaluation = {
        "retrieval_method":
            "hybrid_rrf_reranker",
        "candidate_count":
            len(candidates),
        "final_count":
            len(ranked_results)
    }

    yield (
        "data: "
        + json.dumps({
            "type": "done",
            "citations": citations,
            "evaluation": evaluation
        })
        + "\n\n"
    )