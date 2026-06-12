from sqlalchemy.orm import Session
from backend.modules.memory.ingestion.file_type_detector import FileTypeDetector
from backend.modules.memory.ingestion.content_extractor import ContentExtractor
from backend.modules.memory.ingestion.decision_engine import DecisionEngine
from backend.modules.memory.ingestion.adaptive_chunker import AdaptiveChunker
from backend.modules.rag.embedder import Embedder
from backend.modules.rag.vector_store import VectorStore
from backend.repositories.document_repository import DocumentRepository
from backend.models.document import Document


class RAGService:

    @staticmethod
    def upload_file(file_bytes: bytes, filename: str, doc_id: str, db: Session = None, user_id: int = None) -> dict:
        file_type = FileTypeDetector.detect(filename)
        text = ContentExtractor.extract(file_bytes, file_type)

        if not text:
            return {"status": "error", "message": "No text could be extracted"}

        decision = DecisionEngine.decide(text, file_type)
        chunks = AdaptiveChunker.chunk(text, decision["chunking_strategy"])
        embeddings = Embedder.embed_texts(chunks)

        VectorStore.store_chunks(
            collection_name=decision["collection"],
            chunks=chunks,
            embeddings=embeddings,
            doc_id=doc_id
        )

        # Save record to PostgreSQL if db is provided
        if db:
            document = Document(
                user_id=user_id,
                filename=filename,
                file_type=file_type,
                file_size=len(file_bytes),
                word_count=decision["word_count"],
                chunk_count=len(chunks),
                collection_name=decision["collection"],
                doc_id=doc_id,
                status="success"
            )
            DocumentRepository.create(db, document)

        return {
            "status": "success",
            "doc_id": doc_id,
            "filename": filename,
            "file_type": file_type,
            "word_count": decision["word_count"],
            "size_category": decision["size_category"],
            "chunking_strategy": decision["chunking_strategy"],
            "collection": decision["collection"],
            "chunks_stored": len(chunks)
        }

    @staticmethod
    def store_text_snippet(text: str, doc_id: str) -> dict:
        decision = DecisionEngine.decide(text, "text_snippet")
        chunks = AdaptiveChunker.chunk(text, decision["chunking_strategy"])
        embeddings = Embedder.embed_texts(chunks)
        VectorStore.store_chunks(
            collection_name=decision["collection"],
            chunks=chunks,
            embeddings=embeddings,
            doc_id=doc_id
        )
        return {
            "status": "success",
            "doc_id": doc_id,
            "chunking_strategy": decision["chunking_strategy"],
            "collection": decision["collection"],
            "chunks_stored": len(chunks)
        }

    @staticmethod
    def query(question: str, collections: list = None, top_k: int = 3) -> list:
        if collections is None:
            collections = ["knowledge_base", "personal_memory", "code_memory"]
        query_embedding = Embedder.embed_query(question)
        all_results = []
        for collection in collections:
            try:
                results = VectorStore.query(
                    collection_name=collection,
                    query_embedding=query_embedding,
                    top_k=top_k
                )
                all_results.extend(results)
            except Exception:
                continue
        return all_results[:top_k]