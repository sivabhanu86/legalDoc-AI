import { useState } from "react";
import { uploadDocument } from "../services/api";

function FileUpload({ onUpload }) {

    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleUpload = async () => {
    if (!file) {
        setError("Please select a PDF first.");
        return;
    }

    setLoading(true);
    setError("");

    try {
        const result = await uploadDocument(file);

        console.log("Upload successful:", result);

        setFile(null);

        try {
            await onUpload();
        } catch (error) {
            console.error(
                "Document refresh failed:",
                error
            );
        }

    } catch (error) {
        console.error("Upload error:", error);

        setError(
            error.response?.data?.detail ||
            error.message ||
            "Upload failed."
        );
    } finally {
        setLoading(false);
    }
    };

    return (
        <div className="upload-card">

            <h2>Upload Legal Document</h2>

            <input
                type="file"
                accept=".pdf"
                onChange={(event) =>
                    setFile(event.target.files[0])
                }
            />

            <button
                onClick={handleUpload}
                disabled={loading}
            >
                {loading ? "Processing..." : "Upload PDF"}
            </button>

            {error && (
                <p className="error">
                    {error}
                </p>
            )}

        </div>
    );
}

export default FileUpload;