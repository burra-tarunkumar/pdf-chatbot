
_model = None


def get_model():
    global _model

    if _model is None:
        from sentence_transformers import SentenceTransformer

        _model = SentenceTransformer("all-MiniLM-L6-v2")

    return _model


def create_embeddings(text: list[str]):
    model = get_model()
    embeddings = model.encode(text)
    return embeddings
