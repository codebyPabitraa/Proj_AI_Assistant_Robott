from sentence_transformers import SentenceTransformer

class Embedder:

    # Load model once when class is first used
    # Not on every function call — that would be slow
    _model = SentenceTransformer("all-MiniLM-L6-v2")

    @staticmethod
    def embed_texts(texts: list[str]) -> list[list[float]]:
        """
        Takes a list of text chunks.
        Returns a list of embeddings (each embedding is a list of floats).
        """
        embeddings = Embedder._model.encode(texts, show_progress_bar=True)
        return embeddings.tolist()

    @staticmethod
    def embed_query(query: str) -> list[float]:
        """
        Takes a single query string.
        Returns one embedding (list of floats).
        """
        embedding = Embedder._model.encode([query])
        return embedding[0].tolist()