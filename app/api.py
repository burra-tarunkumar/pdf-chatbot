from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field

from app.embeddings import create_embeddings
from app.vectorstore import search_documents
from app.rag import generate_answer


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
def ask_question(request: QuestionRequest):

    try:
        query_embedding = create_embeddings([request.question])[0]

        results = search_documents(query_embedding, top_k=3)

        retrieved_documents = results["documents"][0]
        retrieved_metadatas = results["metadatas"][0]

        context_parts = []

        for document, metadata in zip(
            retrieved_documents,
            retrieved_metadatas
        ):
            page_number = metadata["page"] + 1

            context_parts.append(
                f"[Page: {page_number}]\n{document}"
            )

        context = "\n\n".join(context_parts)

        answer = generate_answer(
            request.question,
            context
        )

        pages = sorted(
            set(metadata["page"] + 1 for metadata in retrieved_metadatas)
        )

        return {
            "question": request.question,
            "answer": answer,
            "pages": pages
        }
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing the question"
        )