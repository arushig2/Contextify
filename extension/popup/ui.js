import { SOURCE_LABELS } from "./constants.js";

export function displayPageInfo(title, loader) {

    document.getElementById("page-url").textContent = title;

    document.getElementById("source-type").textContent =
        SOURCE_LABELS[loader];
}

export function updateStatus(message) {

    document.getElementById("status").textContent = message;
}

export function displayAnswer(answer) {

    document
        .getElementById("answer")
        .textContent = answer;

}