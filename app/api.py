from fastapi import FastAPI
from pydantic import BaseModel

from app.embeddings import create_embeddings
from app.vectorstore import search_documents
from app.rag import generate_answer


app = FastAPI()


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {"message": "PDF Chatbot API is running."}


@app.post("/ask")
def ask_question(request: QuestionRequest):
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