from langchain_core.documents import Document


def extract_citations(documents: list[Document]) -> list[dict]:
    seen = set()
    citations = []

    for doc in documents:
        source = doc.metadata.get("source")

        if not source or source in seen:
            continue

        seen.add(source)

        citations.append({
            "source": source,
            "source_type": doc.metadata.get("source_type"),
        })

    return citations