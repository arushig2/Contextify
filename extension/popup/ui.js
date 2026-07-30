import { SOURCE_LABELS } from "./constants.js";

export function displayPageInfo(title, loader) {

    document.getElementById("page-url").textContent = title;

    document.getElementById("source-type").textContent =
        SOURCE_LABELS[loader];
}

export function updateIngestionStatus(message, type = "info") {
    const status = document.getElementById("status");
    status.textContent = message;
    status.className = type;
}

export function updateQueryStatus(message, type = "info") {
    const status = document.getElementById("query-status");
    status.textContent = message;
    status.className = type;
}

export function displayAnswer(answer) {
    document
        .getElementById("answer")
        .textContent = answer;
}

export function setButtonLoading(buttonId, loadingText) {
    const button = document.getElementById(buttonId);
    button.disabled = true;
    button.dataset.originalText = button.textContent;
    button.textContent = loadingText;
}

export function resetButton(buttonId) {
    const button = document.getElementById(buttonId);
    button.disabled = false;
    button.textContent = button.dataset.originalText;
}