import chromadb

client=chromadb.PersistentClient(path="chroma_db")

collection=client.get_or_create_collection(name="pdf_documents")

def add_documents(chunks,embeddings):
    collection.upsert(
        ids=[str(i) for i in range(len(chunks))],
        documents=[chunk.page_content for chunk in chunks],
        embeddings=embeddings.tolist(),
        metadatas=[chunk.metadata for chunk in chunks]
    )

def search_documents(query_embedding,top_k=3):
    results=collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results