import { detectSourceType } from "./source.js";
import { ingest, query } from "./api.js";
import {
    displayPageInfo,
    displayAnswer,
    updateIngestionStatus,
    updateQueryStatus,
    setButtonLoading,
    resetButton
} from "./ui.js";
import {
    saveQueryState,
    loadQueryState
} from "./storage.js";

let currentUrl = "";
let currentLoader = "";
const citationsContainer =
    () => document.getElementById("citations");

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

    const savedState = await loadQueryState();

    if (savedState) {
        document.getElementById("question").value =
            savedState.question ?? "";
        displayAnswer(savedState.answer ?? "No answer yet.");
        displayCitations(savedState.citations ?? []);
    }

    document
        .getElementById("ingest-btn")
        .addEventListener("click", ingestCurrentPage);

    document
        .getElementById("query-btn")
        .addEventListener("click", askQuestion);

    document
        .getElementById("copy-btn")
        .addEventListener("click", copyAnswer);
}

async function ingestCurrentPage() {

    if (currentLoader === "unsupported") {
        updateIngestionStatus("Unsupported page.");
        return;
    }

    try {
        setButtonLoading("ingest-btn", "Indexing...");
        
        const result = await ingest(
            currentUrl,
            currentLoader
        );

        updateIngestionStatus(result.message);
    } catch (error) {
        updateIngestionStatus(error.message);
    } finally {
        resetButton("ingest-btn");
    }
}

async function askQuestion() {

    const question = document
        .getElementById("question")
        .value
        .trim();

    if (!question) {
        updateQueryStatus("Enter a question.");
        return;
    }

    try {
        setButtonLoading("query-btn", "Thinking...");
        updateQueryStatus("Thinking...");

        displayCitations([]);

        const result = await query(question);
        displayAnswer(result.answer);
        displayCitations(result.citations);

        updateQueryStatus("");

        await saveQueryState({
            question,
            answer: result.answer,
            citations: result.citations
        });

    } catch (error) {
        displayCitations([]);
        updateQueryStatus(error.message);
    } finally {
        resetButton("query-btn");
    }

}

async function copyAnswer() {

    const button = document.getElementById("copy-btn");

    const answer = document.getElementById("answer").textContent;

    if (!answer || answer === "No answer yet."){
        return;
    }

    await navigator.clipboard.writeText(answer);

    button.textContent = "✅ Copied";

    setTimeout(() => {
        button.textContent = "📋 Copy";
    }, 1500);
}

function displayCitations(citations) {

    const container = citationsContainer();
    container.innerHTML = "";

    if (!citations || citations.length === 0) {
        return;
    }

    const heading = document.createElement("h4");
    heading.textContent = "Sources";

    container.appendChild(heading);

    citations.forEach(citation => {

        const link = document.createElement("a");

        const icon =
            citation.source_type === "youtube"
                ? "🎥"
                : "🌐";

        link.href = citation.source;
        link.target = "_blank";
        link.className = "citation-link";
        link.textContent = `${icon} ${citation.source}`;

        container.appendChild(link);
    });
}