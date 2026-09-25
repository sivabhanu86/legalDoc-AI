def check_relevance(
    ranked_results,
    threshold=-2.0
):
    if not ranked_results:
        return {
            "relevant": False,
            "best_score": None
        }

    best_score = ranked_results[0].get(
        "reranker_score"
    )

    if best_score is None:
        return {
            "relevant": False,
            "best_score": None
        }

    return {
        "relevant": best_score >= threshold,
        "best_score": best_score
    }