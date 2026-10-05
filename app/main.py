from loader import load_pdf

pdf_path="data/pdfs/sample.pdf"
documents=load_pdf(pdf_path)
print(f"Number of pages:{len(documents)}")
print("\nFirst Page\n")
print(documents[0].page_content)