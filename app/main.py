from loader import load_pdf
from splitter import split_document

pdf_path="data/pdfs/sample.pdf"
documents=load_pdf(pdf_path)
chunks=split_document(documents)
print(f"Number of chunk:{len(chunks)}")
print(f"First chunk length: {len(chunks[0].page_content)} characters")
print("\nFirst Chunk\n")
print(chunks[0].page_content)

print("\nFirst chunk metadata:")
print(chunks[0].metadata)