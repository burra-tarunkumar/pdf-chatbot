from loader import load_pdf
from splitter import split_document
from embeddings import create_embeddings

pdf_path="data/pdfs/sample.pdf"
documents=load_pdf(pdf_path)
chunks=split_document(documents)
texts=[chunk.page_content for chunk in chunks]
embeddings=create_embeddings(texts)

print(f"Number of chunk:{len(chunks)}")
print(f"Number of embeddings:{len(embeddings)}")
print(f"Embedding dimensions:{len(embeddings[0])}")
print("\nFirst embeedding:\n")
print(f"First embedding (first 10 values): {embeddings[0][:10]}")

