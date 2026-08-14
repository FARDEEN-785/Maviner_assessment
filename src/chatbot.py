from src.ingestion.pdf_loader import load_pdf
from src.ingestion.text_cleaner import clean_text
from src.ingestion.chunker import chunk_documents
from src.retrieval.vector_store import VectorStore
from src.generation.llm import generate_answer


PDF_PATH = "data/raw/TS_23.501_R18.pdf"


def build_rag():

    print("Loading 3GPP document")

    documents = load_pdf(PDF_PATH)

    for document in documents:
        document["text"] = clean_text(document["text"])

    chunks = chunk_documents(documents)

    print(f"Loaded {len(documents)} pages")
    print(f"Created {len(chunks)} chunks")

    vector_store = VectorStore()
    vector_store.build(chunks)

    return vector_store


def main():

    vector_store = build_rag()

    print("\n ->")
    print("3GPP TS 23.501 RAG CHATBOT")
    print("Type 'exit' to quit")
 

    while True:

        question = input("\nYou: ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

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

        print("\nAssistant:")
        print(answer)


if __name__ == "__main__":
    main()