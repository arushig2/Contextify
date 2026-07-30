import {
    API_BASE_URL,
    DEFAULT_CHUNKER
} from "./constants.js";

export async function ingest(source, loader) {

    const response = await fetch(`${API_BASE_URL}/ingest`, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            source,
            loader,
            chunker: DEFAULT_CHUNKER
        })

    });

    if (!response.ok) {
        throw new Error("Failed to ingest source.");
    }

    return await response.json();
}

export async function query(question) {

    const response = await fetch(`${API_BASE_URL}/query`, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            question
        })

    });

    if (!response.ok) {
        throw new Error("Failed to query knowledge base.");
    }

    return await response.json();
}