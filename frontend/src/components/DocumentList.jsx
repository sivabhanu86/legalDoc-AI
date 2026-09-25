import { deleteDocument } from "../services/api";

function DocumentList({
    documents,
    selectedDocument,
    onSelect,
    onDelete
}) {

    const handleDelete = async (documentId) => {

        const confirmed = window.confirm(
            "Delete this document?"
        );

        if (!confirmed) {
            return;
        }

        try {

            await deleteDocument(documentId);

            onDelete();

        } catch (error) {

            console.error(
                "Delete failed:",
                error
            );

        }
    };

    return (
        <div className="documents-card">

            <h2>My Documents</h2>

            {documents.length === 0 && (
                <p>
                    No documents uploaded yet.
                </p>
            )}

            {documents.map((document) => (

                <div
                    key={document.document_id}
                    className={
                        selectedDocument === document.document_id
                            ? "document selected"
                            : "document"
                    }
                    onClick={() =>
                        onSelect(document.document_id)
                    }
                >

                    <div>

                        <strong>
                            {document.document_name}
                        </strong>

                        <p>
                            {document.pages} pages •{" "}
                            {document.chunks} chunks
                        </p>

                    </div>

                    <button
                        onClick={(event) => {
                            event.stopPropagation();

                            handleDelete(
                                document.document_id
                            );
                        }}
                    >
                        Delete
                    </button>

                </div>

            ))}

        </div>
    );
}

export default DocumentList;