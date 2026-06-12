from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.services.rag_service import RAGService
import uuid

router = APIRouter()


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_bytes = await file.read()
    doc_id = str(uuid.uuid4())
    result = RAGService.upload_file(
        file_bytes=file_bytes,
        filename=file.filename,
        doc_id=doc_id,
        db=db
    )
    return result


class SnippetRequest(BaseModel):
    text: str


@router.post("/snippet")
def store_snippet(request: SnippetRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    doc_id = str(uuid.uuid4())
    result = RAGService.store_text_snippet(
        text=request.text,
        doc_id=doc_id
    )
    return result


class QueryRequest(BaseModel):
    question: str
    top_k: int = 3
    collections: list = None


@router.post("/query")
def query_knowledge_base(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    results = RAGService.query(
        question=request.question,
        collections=request.collections,
        top_k=request.top_k
    )
    return {
        "question": request.question,
        "results": results
    }


@router.get("/documents")
def get_documents(db: Session = Depends(get_db)):
    from backend.repositories.document_repository import DocumentRepository
    documents = DocumentRepository.get_all(db)
    return {"documents": [
        {
            "id": d.id,
            "filename": d.filename,
            "file_type": d.file_type,
            "word_count": d.word_count,
            "chunk_count": d.chunk_count,
            "collection": d.collection_name,
            "status": d.status,
            "created_at": str(d.created_at)
        }
        for d in documents
    ]}