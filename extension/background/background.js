console.log("Contextify background service worker loaded.");

chrome.runtime.onInstalled.addListener(() => {
    console.log("Contextify extension installed.");
});