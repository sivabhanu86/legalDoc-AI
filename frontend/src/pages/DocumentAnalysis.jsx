import { useEffect, useState } from "react";
import { getDocuments } from "../services/api";
import axios from "axios";

function DocumentAnalysis() {
    const [documents, setDocuments] = useState([]);
    const [documentA, setDocumentA] = useState("");
    const [documentB, setDocumentB] = useState("");
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    useEffect(() => {
        loadDocuments();
    }, []);

    const loadDocuments = async () => {
        try {
            const response = await getDocuments();

            setDocuments(
                response.documents || []
            );
        } catch (error) {
            console.error(
                "Failed to load documents:",
                error
            );

            setError(
                "Unable to load documents."
            );
        }
    };

    const handleCompare = async () => {
        if (!documentA || !documentB) {
            setError(
                "Please select two documents."
            );
            return;
        }

        if (documentA === documentB) {
            setError(
                "Please select two different documents."
            );
            return;
        }

        setLoading(true);
        setError("");
        setResult(null);

        try {
            const response = await axios.post(
                "http://127.0.0.1:8000/comparison",
                {
                    document_a_id: documentA,
                    document_b_id: documentB
                }
            );

            setResult(response.data);

        } catch (error) {
            console.error(
                "Comparison error:",
                error
            );

            setError(
                error.response?.data?.detail ||
                error.message ||
                "Comparison failed."
            );

        } finally {
            setLoading(false);
        }
    };

    const documentAName =
        documents.find(
            (document) =>
                document.document_id ===
                documentA
        )?.document_name;

    const documentBName =
        documents.find(
            (document) =>
                document.document_id ===
                documentB
        )?.document_name;

    return (
        <div className="app">

            <header className="navbar">

                <div className="logo">
                    ⚖ LegalDoc-AI
                </div>

                <nav className="nav-links">

                    <a href="/">
                        Research
                    </a>

                    <a href="/analysis">
                        Document Analysis
                    </a>

                    <a href="/#documents">
                        Documents
                    </a>

                </nav>

            </header>

            <main className="analysis-page">

                <section className="analysis-header">

                    <h1>
                        Document Comparison
                    </h1>

                    <p>
                        Compare two legal documents
                        and identify important
                        differences for human review.
                    </p>

                </section>

                <section className="comparison-card">

                    <div className="comparison-field">

                        <label>
                            Document A
                        </label>

                        <select
                            value={documentA}
                            onChange={(event) =>
                                setDocumentA(
                                    event.target.value
                                )
                            }
                        >
                            <option value="">
                                Select document
                            </option>

                            {documents.map(
                                (document) => (
                                    <option
                                        key={
                                            document.document_id
                                        }
                                        value={
                                            document.document_id
                                        }
                                    >
                                        {
                                            document.document_name
                                        }
                                    </option>
                                )
                            )}

                        </select>

                    </div>

                    <div className="comparison-field">

                        <label>
                            Document B
                        </label>

                        <select
                            value={documentB}
                            onChange={(event) =>
                                setDocumentB(
                                    event.target.value
                                )
                            }
                        >
                            <option value="">
                                Select document
                            </option>

                            {documents.map(
                                (document) => (
                                    <option
                                        key={
                                            document.document_id
                                        }
                                        value={
                                            document.document_id
                                        }
                                    >
                                        {
                                            document.document_name
                                        }
                                    </option>
                                )
                            )}

                        </select>

                    </div>

                    <button
                        onClick={handleCompare}
                        disabled={
                            loading ||
                            !documentA ||
                            !documentB
                        }
                    >
                        {loading
                            ? "Analyzing..."
                            : "Compare Documents"}
                    </button>

                </section>

                {error && (
                    <p className="error">
                        {error}
                    </p>
                )}

                {loading && (
                    <div className="analysis-loading">

                        <div className="loading-spinner">
                        </div>

                        <p>
                            AI is comparing the
                            selected documents...
                        </p>

                    </div>
                )}

                {result && !loading && (

                    <section className="comparison-result">

                        <div className="result-summary">

                            <div className="document-summary">

                                <span>
                                    DOCUMENT A
                                </span>

                                <strong>
                                    {documentAName}
                                </strong>

                                <small>
                                    Indexed pages:{" "}
                                    {
                                        result.document_a_pages
                                    }
                                </small>

                            </div>

                            <div className="document-summary">

                                <span>
                                    DOCUMENT B
                                </span>

                                <strong>
                                    {documentBName}
                                </strong>

                                <small>
                                    Indexed pages:{" "}
                                    {
                                        result.document_b_pages
                                    }
                                </small>

                            </div>

                        </div>

                        <div className="review-notice">

                            <strong>
                                Human review recommended
                            </strong>

                            <p>
                                AI-generated comparison
                                results are intended to
                                help identify areas for
                                review. Verify important
                                information against the
                                original documents.
                            </p>

                        </div>

                        <div className="comparison-answer">

                            <div className="result-title">

                                <div className="result-icon">
                                    AI
                                </div>

                                <div>
                                    <h2>
                                        Comparison Results
                                    </h2>

                                    <p>
                                        Document-level
                                        analysis
                                    </p>
                                </div>

                            </div>

                            <div className="comparison-text">
                                {result.answer}
                            </div>

                        </div>

                    </section>

                )}

            </main>

            <footer
                style={{
                    textAlign: "center",
                    padding: "30px",
                    color: "#64748b",
                    fontSize: "13px"
                }}
            >
                LegalDoc-AI • Document Intelligence
            </footer>

        </div>
    );
}

export default DocumentAnalysis;