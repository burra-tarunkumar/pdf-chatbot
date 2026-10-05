from sentence_transformers import SentenceTransformer

model=SentenceTransformer("all-MiniLM-L6-v2")

def create_embeddings(text:list[str]):
    embeddings=model.encode(text)
    return embeddings
