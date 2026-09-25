import { useEffect, useState } from "react";

import {
    BrowserRouter,
    Routes,
    Route,
    Link
} from "react-router-dom";

import { getDocuments } from "./services/api";

import FileUpload from "./components/FileUpload";
import DocumentList from "./components/DocumentList";
import ChatBox from "./components/ChatBox";
import DocumentAnalysis from "./pages/DocumentAnalysis";


function Home() {

    const [documents, setDocuments] =
        useState([]);

    const [selectedDocument, setSelectedDocument] =
        useState(null);

    const [loading, setLoading] =
        useState(true);

    const [error, setError] =
        useState("");


    const loadDocuments = async () => {

        try {

            setError("");

            const result =
                await getDocuments();

            setDocuments(
                result.documents || []
            );

            setSelectedDocument(
                (current) => {

                    if (!current) {
                        return (
                            result.documents?.[0] ||
                            null
                        );
                    }

                    const exists =
                        result.documents?.find(
                            (document) =>
                                document.document_id ===
                                current.document_id
                        );

                    return (
                        exists ||
                        result.documents?.[0] ||
                        null
                    );
                }
            );

        } catch (error) {

            console.error(
                "Failed to load documents:",
                error
            );

            setError(
                "Unable to load documents."
            );

        } finally {

            setLoading(false);

        }
    };


    useEffect(() => {

        loadDocuments();

    }, []);


    return (

        <div className="app">

            <header className="navbar">

                <div className="logo">
                    ⚖ LegalDoc-AI
                </div>

                <nav className="nav-links">

                    <Link to="/">
                        Research
                    </Link>

                    <Link to="/analysis">
                        Document Analysis
                    </Link>

                    <a href="#documents">
                        Documents
                    </a>

                </nav>

            </header>


            <main className="page">

                <section className="hero">

                    <h1>
                        Indian Legal Research &
                        Document Intelligence
                    </h1>

                    <p>
                        Upload legal documents,
                        ask evidence-based
                        questions, compare
                        documents, and explore
                        answers with page-level
                        citations.
                    </p>

                </section>


                {error && (
                    <p className="error">
                        {error}
                    </p>
                )}


                <section className="dashboard">

                    <aside id="documents">

                        <FileUpload
                            onUpload={
                                loadDocuments
                            }
                        />


                        <div
                            className="card"
                            style={{
                                marginTop: "20px"
                            }}
                        >

                            <div className="card-header">

                                <h2>
                                    Your Documents
                                </h2>

                            </div>


                            <div className="card-body">

                                {loading ? (

                                    <div className="empty-state">
                                        Loading documents...
                                    </div>

                                ) : (

                                    <DocumentList
                                        documents={
                                            documents
                                        }

                                        selectedDocument={
                                            selectedDocument
                                        }

                                        onSelect={
                                            setSelectedDocument
                                        }

                                        onDelete={
                                            loadDocuments
                                        }
                                    />

                                )}

                            </div>

                        </div>

                    </aside>


                    <section>

                        <ChatBox
                            documentId={
                                selectedDocument
                                    ?.document_id
                            }
                        />

                    </section>

                </section>

            </main>


            <footer
                id="about"
                style={{
                    textAlign: "center",
                    padding: "30px",
                    color: "#64748b",
                    fontSize: "13px"
                }}
            >
                LegalDoc-AI • Indian Legal
                Research & Document Intelligence
            </footer>

        </div>

    );
}


function App() {

    return (

        <BrowserRouter>

            <Routes>

                <Route
                    path="/"
                    element={<Home />}
                />

                <Route
                    path="/analysis"
                    element={
                        <DocumentAnalysis />
                    }
                />

            </Routes>

        </BrowserRouter>

    );
}


export default App;