from backend.app.services.rag_service import answer_question


question = input("Enter your question: ")


result = answer_question(
    question,
    top_k=5,
    source_type="user_document"
)


print("\n==============================")
print("ANSWER")
print("==============================")

print(result["answer"])


print("\n==============================")
print("SOURCES")
print("==============================")


for citation in result["citations"]:

    print("------------------------------")

    print(
        "Document:",
        citation["document_name"]
    )

    print(
        "Page:",
        citation["page"]
    )

    print(
        "Chunk:",
        citation["chunk_id"]
    )

    print(
        "Distance:",
        citation["distance"]
    )


print("\n==============================")
print("RETRIEVAL EVALUATION")
print("==============================")

print(
    "Best distance:",
    result["evaluation"]["best_distance"]
)

print(
    "Average top-3 distance:",
    result["evaluation"]["average_top_3_distance"]
)

print(
    "Top-1 to Top-3 gap:",
    result["evaluation"]["gap_top1_top3"]
)