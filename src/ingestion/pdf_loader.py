import pdfplumber
from pathlib import Path


def load_pdf(pdf_path:str):

    documents = []

    pdf_path = Path(pdf_path)

    with pdfplumber.open(pdf_path) as pdf:

       for page_number, page in enumerate(pdf.pages, start=1):

            if page_number <= 30:
                continue

            text = page.extract_text()

            if not text:
                continue

            documents.append({
                "text": text.strip(),
                "metadata": {
                    "source": pdf_path.name,
                    "page": page_number
                }
            })

    return documents

if __name__ == "__main__":

    pdf_path = "data/raw/TS_23.501_R18.pdf"

    documents = load_pdf(pdf_path)

    print(f"Pages extracted: {len(documents)}")

    if documents:
        print("FIRST PAGE\n")
        print(documents[0]["text"][:2000])

        print("METADATA\n")
        print(documents[0]["metadata"])

                
            