from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from backend.services.rag_service import RAGService
import uuid

router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_bytes = await file.read()
    doc_id = str(uuid.uuid4())
    result = RAGService.upload_file(
        file_bytes=file_bytes,
        filename=file.filename,
        doc_id=doc_id
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