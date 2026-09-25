import axios from "axios";


const API = axios.create({
    baseURL: "http://127.0.0.1:8000"
});


export const uploadDocument = async (file) => {

    const formData = new FormData();

    formData.append("file", file);

    const response = await API.post(
        "/documents/upload",
        formData
    );

    return response.data;
};


export const getDocuments = async () => {

    const response = await API.get(
        "/documents/"
    );

    return response.data;
};


export const deleteDocument = async (documentId) => {

    const response = await API.delete(
        `/documents/${documentId}`
    );

    return response.data;
};


export const askQuestion = async (
    question,
    mode,
    documentId = null,
    topK = 5
) => {

    const response = await API.post(
        "/query",
        {
            question: question,
            mode: mode,
            document_id: documentId,
            top_k: topK
        }
    );

    return response.data;
};
export const streamQuestion = async (
    question,
    mode,
    documentId,
    onToken,
    onDone,
    onError
) => {

    const response = await fetch(
        "http://127.0.0.1:8000/query/stream",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question,
                mode: mode,
                document_id: documentId,
                top_k: 5
            })
        }
    );

    if (!response.ok) {

        const error = await response.json();

        throw new Error(
            error.detail ||
            "Streaming request failed."
        );
    }

    const reader =
        response.body.getReader();

    const decoder =
        new TextDecoder();

    let buffer = "";

    while (true) {

        const {
            value,
            done
        } = await reader.read();

        if (done) {
            break;
        }

        buffer += decoder.decode(
            value,
            {
                stream: true
            }
        );

        const events =
            buffer.split("\n\n");

        buffer =
            events.pop() || "";

        for (const event of events) {

            if (!event.startsWith("data: ")) {
                continue;
            }

            const payload =
                JSON.parse(
                    event.slice(6)
                );

            if (
                payload.type === "token"
            ) {

                onToken(
                    payload.content
                );
            }

            if (
                payload.type === "done"
            ) {

                onDone(
                    payload
                );
            }

            if (
                payload.type === "error"
            ) {

                onError(
                    payload.content
                );
            }
        }
    }
};