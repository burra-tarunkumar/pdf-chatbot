from embeddings import create_embeddings
from vectorstore import search_documents
from rag import generate_answer



question = input("\nEnter your question: ")
while question.lower() != "exit":
    query_embedding = create_embeddings([question])[0]

    results = search_documents(query_embedding, top_k=3)

    retrieved_documents = results["documents"][0]
    retrieved_metadata = results["metadatas"][0]

    context_parts = []

    for document, metadata in zip(retrieved_documents, retrieved_metadata):
        page_number = metadata["page"] + 1

        context_parts.append(
            f"[Page: {page_number}]\n{document}"
        )

    context = "\n\n".join(context_parts)


    

    answer = generate_answer(question, context)

    print("\nAnswer:")
    print(answer)


    pages = sorted(
        set(metadata["page"] + 1 for metadata in retrieved_metadata)
    )

    print("\nSources:")
    for page in pages:
        print(f"- Page {page}")
    question = input("\nEnter your question: ")