import re

from rank_bm25 import BM25Okapi

from backend.app.services.vector_store import (
    get_all_chunks
)


def tokenize(text):

    return re.findall(
        r"\b\w+\b",
        text.lower()
    )


class KeywordSearch:

    def __init__(self):

        self.documents = []
        self.metadatas = []
        self.bm25 = None

    def build_index(self):

        data = get_all_chunks()

        self.documents = data["documents"]
        self.metadatas = data["metadatas"]

        tokenized_documents = [
            tokenize(document)
            for document in self.documents
        ]

        if tokenized_documents:

            self.bm25 = BM25Okapi(
                tokenized_documents
            )

    def search(
        self,
        query,
        top_k=5,
        document_id=None
    ):

        if self.bm25 is None:
            self.build_index()

        if self.bm25 is None:
            return []

        query_tokens = tokenize(query)

        scores = self.bm25.get_scores(
            query_tokens
        )

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda index: scores[index],
            reverse=True
        )

        results = []

        for index in ranked_indices:

            metadata = self.metadatas[index]

            if (
                document_id
                and metadata.get("document_id")
                != document_id
            ):
                continue

            results.append({
                "text": self.documents[index],
                "metadata": metadata,
                "score": float(scores[index])
            })

            if len(results) >= top_k:
                break

        return results