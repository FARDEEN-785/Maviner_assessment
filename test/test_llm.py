from src.ingestion.pdf_loader import load_pdf
from src.ingestion.text_cleaner import clean_text
from src.ingestion.chunker import chunk_documents
from src.retrieval.vector_store import VectorStore
from src.generation.llm import generate_answer


PDF_PATH = "data/raw/TS_23.501_R18.pdf"

documents = load_pdf(PDF_PATH)

for doc in documents:
    doc["text"] = clean_text(doc["text"])

chunks = chunk_documents(documents)

store = VectorStore()
store.build(chunks)

question = "What is N3IWF?"

results = store.search(question, k=5)

context = "\n\n".join(
    f"[Page {r['metadata']['page']}]\n{r['text']}"
    for r in results
)

answer = generate_answer(question, context)

print("\nANSWER ->\n")
print(answer)