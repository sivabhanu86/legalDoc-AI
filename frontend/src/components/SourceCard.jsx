function SourceCard({ citation }) {
    return (
        <div className="citation">

            <div className="document-name">
                {citation.document_name ||
                    "Unknown document"}
            </div>

            <p>
                <strong>Page:</strong>{" "}
                {citation.page ?? "—"}
            </p>

            <p>
                <strong>Section:</strong>{" "}
                {citation.section || "Not detected"}
            </p>

            <p>
                <strong>Source:</strong>{" "}
                {citation.source_type ===
                "legal_corpus"
                    ? "Legal Corpus"
                    : "Uploaded Document"}
            </p>

        </div>
    );
}

export default SourceCard;