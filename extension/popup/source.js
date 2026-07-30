export function detectSourceType(url) {

    if (!url)
        return "unknown";

    if (
        url.includes("youtube.com/watch") ||
        url.includes("youtu.be/")
    ) {
        return "youtube";
    }

    if (
        url.startsWith("http://") ||
        url.startsWith("https://")
    ) {
        return "webpage";
    }

    return "unsupported";
}