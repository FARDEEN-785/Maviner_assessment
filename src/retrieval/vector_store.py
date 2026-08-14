import faiss
from sentence_transformers import SentenceTransformer


class VectorStore:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.chunks = []

    def build(self, chunks):
        self.chunks = chunks

        texts = [chunk["text"] for chunk in chunks]

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True
        ).astype("float32")

        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)

    def search(self, query, k=5):
        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True
        ).astype("float32")

        distances, indices = self.index.search(
            query_embedding,
            k
        )

        results = []

        for distance, index in zip(distances[0], indices[0]):
            results.append({
                "text": self.chunks[index]["text"],
                "metadata": self.chunks[index]["metadata"],
                "score": float(distance)
            })

        return results