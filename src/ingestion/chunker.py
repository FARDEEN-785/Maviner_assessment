from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200
    )

    chunks = []

    for doc in documents:
        texts = splitter.split_text(doc["text"])

        for text in texts:
            chunks.append({
                "text": text,
                "metadata": doc["metadata"]
            })

    return chunks