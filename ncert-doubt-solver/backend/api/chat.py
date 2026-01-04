from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from backend.rag.pipeline import RAGPipeline

router = APIRouter()

class ChatRequest(BaseModel):
    class_no: int
    question: str
    language: str | None = None
    history: list[dict] | None = None 

pipeline = RAGPipeline()

@router.post("/")
async def chat_endpoint(req: ChatRequest):
    result = pipeline.answer(
        question=req.question, 
        class_no=req.class_no, 
        language=req.language,
        history=req.history
    )
    return result
