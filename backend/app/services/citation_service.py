def create_citations(metadatas, distances):

    citations = []

    for metadata, distance in zip(metadatas, distances):

        citations.append({
            "document_id": metadata.get("document_id"),
            "document_name": metadata.get("document_name"),
            "source_type": metadata.get("source_type"),
            "page": metadata.get("page"),
            "section": metadata.get("section"),
            "chunk_id": metadata.get("chunk_id"),
            "distance": distance
        })

    return citations