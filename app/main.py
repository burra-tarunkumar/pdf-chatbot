from loader import load_pdf
from splitter import split_document
from embeddings import create_embeddings
from vectorstore import add_documents,search_documents

pdf_path="data/pdfs/sample.pdf"
documents=load_pdf(pdf_path)
chunks=split_document(documents)
texts=[chunk.page_content for chunk in chunks]
embeddings=create_embeddings(texts)
add_documents(chunks,embeddings)
question = "What is G-DINA?"
query_embedding = create_embeddings([question])[0]
results=search_documents(query_embedding,top_k=3)

print("\nQuestion:")
print(question)

print("\nRetrieved documents:")

for i,document in enumerate(results["documents"][0]):
    print(f"Result {i+1}:")
    print(document)
    print()