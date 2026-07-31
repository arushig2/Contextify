export async function saveQueryState(state) {
    await chrome.storage.local.set({
        queryState: state
    });
}

export async function loadQueryState() {
    const result = await chrome.storage.local.get("queryState");
    return result.queryState ?? null;
}

export async function clearQueryState() {
    await chrome.storage.local.remove("queryState");
}