from app.loader import load_pdf
from app.splitter import split_document
from app.embeddings import create_embeddings
from app.vectorstore import add_documents


pdf_path = "data/pdfs/sample.pdf"

documents = load_pdf(pdf_path)

chunks = split_document(documents)

texts = [chunk.page_content for chunk in chunks]

embeddings = create_embeddings(texts)

add_documents(chunks, embeddings)

print(f"Ingested {len(chunks)} chunks successfully.")