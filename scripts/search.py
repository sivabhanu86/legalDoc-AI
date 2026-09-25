from backend.app.services.retrieval_service import retrieve_relevant_chunks


question = input("Enter your question: ")


results = retrieve_relevant_chunks(question)


documents = results["documents"][0]
metadatas = results["metadatas"][0]
distances = results["distances"][0]


for i, document in enumerate(documents):

    print("\n==============================")
    print(f"Result {i + 1}")
    print("==============================")

    print("Page:", metadatas[i]["page"])
    print("Distance:", distances[i])

    print("\nText:")
    print(document)