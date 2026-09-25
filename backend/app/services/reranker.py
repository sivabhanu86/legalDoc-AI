from sentence_transformers import CrossEncoder


model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank(
    question,
    candidates,
    top_k=5
):
    pairs = []

    for candidate in candidates:
        pairs.append([
            question,
            candidate["text"]
        ])

    scores = model.predict(pairs)

    ranked_results = []

    for candidate, score in zip(
        candidates,
        scores
    ):
        result = candidate.copy()

        result["reranker_score"] = float(score)

        ranked_results.append(result)

    ranked_results.sort(
        key=lambda result: result["reranker_score"],
        reverse=True
    )

    return ranked_results[:top_k]