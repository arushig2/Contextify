import requests
import streamlit as st

st.set_page_config(
    page_title="Contextify",
    page_icon="📚",
    layout="wide",
)


# -----------------------------
# Header
# -----------------------------

st.title("Contextify")
st.caption("Context-aware document question answering")


# -----------------------------
# Sidebar - Ingestion
# -----------------------------

with st.sidebar:
    API_BASE_URL = st.text_input(
        "Backend URL",
        value="http://localhost:8000",
    )

    st.header("Index Content")

    source_type = st.selectbox(
        "Source type",
        ["Webpage", "YouTube"],
    )

    source = st.text_input(
        "Source URL",
        placeholder="Enter URL...",
    )

    chunker = st.selectbox(
        "Chunker",
        ["recursive", "markdown"],
    )

    index_button = st.button(
        "Index",
        type="primary",
        use_container_width=True,
    )


# -----------------------------
# Index
# -----------------------------

if index_button:

    if not source.strip():
        st.sidebar.error("Please enter a URL.")

    else:
        loader = {
            "Webpage": "webpage",
            "YouTube": "youtube",
        }[source_type]

        payload = {
            "source": source,
            "loader": loader,
            "chunker": chunker,
        }

        try:
            with st.spinner("Indexing..."):
                response = requests.post(
                    f"{API_BASE_URL}/ingest",
                    json=payload,
                    timeout=120,
                )

            if response.ok:
                data = response.json()

                st.sidebar.success(data["message"])

                st.success("Content indexed successfully.")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Documents",
                        data["documents"],
                    )

                with col2:
                    st.metric(
                        "Chunks",
                        data["chunks"],
                    )

            else:
                st.sidebar.error(
                    f"Indexing failed ({response.status_code})"
                )

                try:
                    st.error(response.json())
                except requests.exceptions.JSONDecodeError:
                    st.error(response.text)

        except requests.exceptions.ConnectionError:
            st.sidebar.error(
                "Could not connect to the FastAPI server."
            )

        except requests.exceptions.Timeout:
            st.sidebar.error(
                "The indexing request timed out."
            )

        except requests.exceptions.RequestException as e:
            st.sidebar.error(f"Request failed: {e}")


# -----------------------------
# Query
# -----------------------------

st.header("Ask Contextify")

question = st.text_input(
    "Question",
    placeholder="Ask something about your indexed content...",
)

ask_button = st.button(
    "Ask",
    type="primary",
)


# -----------------------------
# Ask
# -----------------------------

if ask_button:

    if not question.strip():
        st.warning("Please enter a question.")

    else:

        payload = {
            "question": question,
        }

        try:
            with st.spinner("Thinking..."):
                response = requests.post(
                    f"{API_BASE_URL}/query",
                    json=payload,
                    timeout=120,
                )

            if response.ok:
                data = response.json()

                st.subheader("Answer")

                st.markdown(data["answer"])

            else:
                st.error(
                    f"Query failed ({response.status_code})"
                )

                try:
                    st.json(response.json())
                except requests.exceptions.JSONDecodeError:
                    st.error(response.text)

        except requests.exceptions.ConnectionError:
            st.error(
                "Could not connect to the FastAPI server."
            )

        except requests.exceptions.Timeout:
            st.error(
                "The query request timed out."
            )

        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")


# -----------------------------
# Retrieved Context
# -----------------------------

st.divider()

with st.expander("Retrieved Context"):
    st.write(
        "Retrieved documents will appear here."
    )