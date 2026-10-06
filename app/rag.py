import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()


llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite"
)


def generate_answer(question: str, context: str):
    prompt = f"""
You are a helpful PDF question-answering assistant.

Answer the question using only the provided context.

If the context does not contain enough information to answer the
question, say that the information is not available in the provided
document.

Do not invent facts.

Context:
{context}

Question:
{question}

Answer:
"""
    response=llm.invoke(prompt)
    if isinstance(response.content,list):
        return response.content[0]["text"]
    return response.content