import json

from src.ingestion.pdf_loader import load_pdf
from src.ingestion.text_cleaner import clean_text
from src.ingestion.chunker import chunk_documents
from src.retrieval.vector_store import VectorStore


PDF_PATH = "data/raw/TS_23.501_R18.pdf"
QUESTIONS_PATH = "data/evaluation/questions.json"


documents = load_pdf(PDF_PATH)

for document in documents:
    document["text"] = clean_text(document["text"])

chunks = chunk_documents(documents)

print(f"Pages: {len(documents)}")
print(f"Chunks: {len(chunks)}")



store = VectorStore()
store.build(chunks)


with open(QUESTIONS_PATH, "r", encoding="utf-8") as file:
    questions = json.load(file)

print("RETRIEVAL EVALUATION")


for item in questions:

    question = item["question"]
    answerable = item["answerable"]

    results = store.search(question, k=3)

    print("\n ->")
    print(f"Question: {question}")
    print(f"Expected ans: {answerable}")

    for i, result in enumerate(results, start=1):

        print(
            f"\nResult {i}"
            f"\nScore: {result['score']:.4f}"
            f"\nPage: {result['metadata'].get('page')}"
        )

        print(result["text"][:500])