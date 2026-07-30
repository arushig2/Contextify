import { detectSourceType } from "./source.js";
import { ingest, query } from "./api.js";

import {
    displayPageInfo,
    updateStatus,
    displayAnswer
} from "./ui.js";

let currentUrl = "";
let currentLoader = "";

document.addEventListener("DOMContentLoaded", initializePopup);

async function initializePopup() {

    const [tab] = await chrome.tabs.query({
        active: true,
        currentWindow: true
    });

    currentUrl = tab.url;
    currentLoader = detectSourceType(currentUrl);

    displayPageInfo(
        tab.title,
        currentLoader
    );

    document
        .getElementById("ingest-btn")
        .addEventListener("click", ingestCurrentPage);

    document
        .getElementById("query-btn")
        .addEventListener("click", askQuestion);
}

async function ingestCurrentPage() {

    if (currentLoader === "unsupported") {

        updateStatus("Unsupported page.");

        return;
    }

    try {

        updateStatus("Indexing...");

        const result = await ingest(
            currentUrl,
            currentLoader
        );

        updateStatus(result.message);

    } catch (error) {

        updateStatus(error.message);

    }
}

async function askQuestion() {

    const question = document
        .getElementById("question")
        .value
        .trim();

    if (!question) {

        updateStatus("Enter a question.");

        return;

    }

    try {

        updateStatus("Thinking...");

        const result = await query(question);

        displayAnswer(result.answer);

        updateStatus("Done.");

    } catch (error) {

        updateStatus(error.message);

    }

}