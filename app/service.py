from app.embeddings import create_embeddings
from app.vectorstore import search_documents
from app.rag import generate_answer


def ask_question(question: str):
    query_embedding = create_embeddings([question])[0]

    results = search_documents(
        query_embedding,
        top_k=3
    )

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
        question,
        context
    )

    pages = sorted(
        set(metadata["page"] + 1 for metadata in retrieved_metadatas)
    )

    return {
        "question": question,
        "answer": answer,
        "pages": pages
    }