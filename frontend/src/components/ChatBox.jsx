import { useState } from "react";
import { streamQuestion } from "../services/api";
import AnswerCard from "./AnswerCard";

function ChatBox({ documentId }) {
    const [question, setQuestion] = useState("");
    const [mode, setMode] = useState("my_document");
    const [answer, setAnswer] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleAsk = async () => {

    if (!question.trim()) {
        return;
    }

    setLoading(true);
    setError("");

    setAnswer({
        answer: "",
        citations: [],
        evaluation: {}
    });

    try {

        await streamQuestion(
            question,
            mode,
            mode === "my_document"
                ? documentId
                : null,

            (token) => {

                setAnswer((current) => ({
                    ...current,
                    answer:
                        current.answer +
                        token
                }));

            },

            (result) => {

                setAnswer((current) => ({
                    ...current,
                    citations:
                        result.citations || [],
                    evaluation:
                        result.evaluation || {}
                }));

                setLoading(false);
            },

            (message) => {

                setError(message);
                setAnswer(null);
                setLoading(false);
            }
        );

    } catch (error) {

        console.error(
            "Streaming query error:",
            error
        );

        setError(
            error.message ||
            "Failed to get answer."
        );

        setAnswer(null);
        setLoading(false);
    }
};

    return (
        <div className="chat-card">

            <h2>Ask LegalDoc AI</h2>

            <label>
                Query Mode
            </label>

            <select
                value={mode}
                onChange={(event) =>
                    setMode(event.target.value)
                }
            >
                <option value="my_document">
                    My Document
                </option>

                <option value="legal_research">
                    Legal Research
                </option>

                <option value="combined">
                    Combined Research
                </option>
            </select>

            <textarea
                value={question}
                onChange={(event) =>
                    setQuestion(event.target.value)
                }
                placeholder="Ask a question about the document..."
                rows="4"
            />

            <button
                onClick={handleAsk}
                disabled={
                    loading ||
                    !question.trim() ||
                    (
                        mode === "my_document" &&
                        !documentId
                    )
                }
            >
                {loading
                        ? "Generating..."
                        : "Ask Question"}
            </button>

            {error && (
                <p className="error">
                    {error}
                </p>
            )}

            {answer && (
                 <AnswerCard result={answer} />
            )}

        </div>
    );
}

export default ChatBox;