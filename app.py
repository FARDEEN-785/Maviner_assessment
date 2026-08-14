import streamlit as st

from src.ingestion.pdf_loader import load_pdf
from src.ingestion.text_cleaner import clean_text
from src.ingestion.chunker import chunk_documents
from src.retrieval.vector_store import VectorStore
from src.generation.llm import generate_answer


PDF_PATH = "data/raw/TS_23.501_R18.pdf"


@st.cache_resource
def build_rag():

    documents = load_pdf(PDF_PATH)

    for document in documents:
        document["text"] = clean_text(document["text"])

    chunks = chunk_documents(documents)

    vector_store = VectorStore()
    vector_store.build(chunks)

    return vector_store


st.set_page_config(
    page_title="3GPP RAG Assistant",
    layout="centered"
)

st.title("3GPP TS 23.501 RAG Assistant")

st.write(
    "Ask questions about the 3GPP TS 23.501 Release 18 "
    "standard. Answers are generated only from the provided document."
)

with st.spinner("Loading 3GPP knowledge base"):
    vector_store = build_rag()

question = st.text_input(
    "Ask a question",
    placeholder="Example: What is the role of the AMF?"
)

if st.button("Ask") and question:

    with st.spinner("Searching 3GPP documentation"):

        results = vector_store.search(question, k=8)

        context_parts = []

        for result in results:

            text = result["text"]
            page = result["metadata"].get("page")

            context_parts.append(
                f"[Page {page}]\n{text}"
            )

        context = "\n\n".join(context_parts)

        answer = generate_answer(
            question,
            context
        )

    st.markdown("# Answer")
    st.write(answer)