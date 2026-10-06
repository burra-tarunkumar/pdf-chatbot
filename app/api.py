import logging

from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field

from app.service import ask_question

logger = logging.getLogger(__name__)

app = FastAPI()


class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=1000
    )

class AnswerResponse(BaseModel):
    question: str
    answer: str
    pages: list[int]


@app.get("/")
def root():
    return {"message": "PDF Chatbot API is running."}


@app.post("/ask",response_model=AnswerResponse)
def ask_question_endpoint(request: QuestionRequest):

    try:
        result = ask_question(request.question)

        return result
    except Exception:
        logger.exception("Error while processing question")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing the question"
        )