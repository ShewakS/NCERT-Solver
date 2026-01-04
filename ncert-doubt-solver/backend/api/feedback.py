from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Feedback(BaseModel):
    question_id: str | None = None
    rating: int
    comment: str | None = None

@router.post("/")
def submit_feedback(payload: Feedback):
    # TODO: persist feedback (DB/file)
    return {"status": "received", "rating": payload.rating}
