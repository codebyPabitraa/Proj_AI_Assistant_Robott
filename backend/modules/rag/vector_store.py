import chromadb
from chromadb.config import Settings

class VectorStore:

    # Initialize ChromaDB client once
    # persist_directory = where ChromaDB saves data on disk
    _client = chromadb.PersistentClient(path="chroma_db")

    @staticmethod
    def get_collection(collection_name: str):
        """
        Gets existing collection or creates new one.
        Collection = like a table in PostgreSQL but for embeddings.
        """
        return VectorStore._client.get_or_create_collection(
            name=collection_name
        )

    @staticmethod
    def store_chunks(collection_name: str, chunks: list[str], embeddings: list[list[float]], doc_id: str):
        """
        Stores text chunks + their embeddings in ChromaDB.
        
        collection_name: name of the collection (e.g. "knowledge_base")
        chunks: list of text pieces
        embeddings: list of embedding vectors
        doc_id: unique identifier for this document
        """
        collection = VectorStore.get_collection(collection_name)

        # Each chunk needs a unique ID
        ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]

        collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings
        )

    @staticmethod
    def query(collection_name: str, query_embedding: list[float], top_k: int = 3) -> list[str]:
        """
        Searches ChromaDB for most similar chunks to the query.
        Returns top K matching text chunks.
        """
        collection = VectorStore.get_collection(collection_name)

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        # results["documents"] is a list of lists — we want the inner list
        return results["documents"][0]