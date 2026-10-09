# PDF Chatbot — Retrieval-Augmented Generation (RAG)

A document question-answering API that allows users to ask questions about PDF documents and receive context-grounded answers with source page references.

Built using Python, FastAPI, LangChain, ChromaDB, Sentence Transformers, Google Gemini, and Docker.

## Features

- **PDF loading:** Extracts text and metadata from PDF documents.
- **Text chunking:** Splits documents into manageable chunks with configurable overlap.
- **Semantic embeddings:** Uses `all-MiniLM-L6-v2` to represent document content as vectors.
- **Vector search:** Retrieves relevant chunks using ChromaDB.
- **LLM-powered answers:** Uses Google Gemini to generate answers grounded in retrieved context.
- **Source references:** Returns the PDF page numbers associated with retrieved content.
- **Input validation:** Validates questions using Pydantic.
- **Error handling and logging:** Handles API failures without exposing internal exception details to clients.
- **Automated tests:** Tests API responses, validation, and error handling.
- **Docker support:** Runs the API in a container with persistent vector database storage.

## Architecture

```text
PDF Document
     |
     v
PDF Loader (PyPDFLoader)
     |
     v
Text Splitter
     |
     v
Sentence Transformer Embeddings
     |
     v
ChromaDB Vector Store
     |
     v
User Question
     |
     v
Question Embedding
     |
     v
Semantic Retrieval (Top 3 Chunks)
     |
     v
Context + Question
     |
     v
Google Gemini
     |
     v
Answer + Source Page Numbers
```

Document ingestion and question answering are separate operations. PDFs must be ingested into ChromaDB before they can be queried.

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python |
| API framework | FastAPI |
| API validation | Pydantic |
| PDF loading | PyPDF |
| Text splitting | LangChain Text Splitters |
| Embedding model | Sentence Transformers — `all-MiniLM-L6-v2` |
| Vector database | ChromaDB |
| LLM | Google Gemini |
| LLM integration | `langchain-google-genai` |
| Testing | Pytest |
| Containerization | Docker |

## Project Structure

```text
pdf-chatbot/
├── app/
│   ├── __init__.py
│   ├── api.py
│   ├── embeddings.py
│   ├── ingest.py
│   ├── loader.py
│   ├── main.py
│   ├── rag.py
│   ├── service.py
│   ├── splitter.py
│   └── vectorstore.py
├── data/
│   └── pdfs/
│       └── sample.pdf
├── tests/
│   └── test_api.py
├── chroma_db/
├── .env
├── .env.example
├── .gitignore
├── .dockerignore
├── Dockerfile
├── README.md
└── requirements.txt
```

The `chroma_db/` directory is generated during ingestion and should not be committed to Git. Local PDFs and environment files should also remain untracked unless intentionally shared.

## Prerequisites

- Python 3.12
- Git
- Docker Desktop (for containerized execution)
- A Google Gemini API key supported by the configured integration

## Local Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd pdf-chatbot
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and add your Gemini API key:

```env
GOOGLE_API_KEY=your_api_key_here
```

Keep `.env` private. Never commit API keys to GitHub.

### 5. Add a PDF

Place the PDF you want to query inside:

```text
data/pdfs/
```

Update the PDF path in `app/ingest.py` if you use a different filename.

### 6. Ingest the document

```powershell
python -m app.ingest
```

The ingestion process loads the PDF, splits its contents into chunks, generates embeddings, and stores them in ChromaDB.

Run ingestion again whenever you replace or update the document. For a production multi-document system, ingestion should also handle document IDs, updates, and duplicate prevention.

### 7. Start the API

```powershell
uvicorn app.api:app --reload
```

Open the interactive API documentation:

[http://localhost:8000/docs](http://localhost:8000/docs)

## API Usage

### Health check

**Endpoint:** `GET /`

Example response:

```json
{
  "message": "PDF Chatbot API is running."
}
```

### Ask a question

**Endpoint:** `POST /ask`

Request:

```json
{
  "question": "What is G-DINA?"
}
```

Example response:

```json
{
  "question": "What is G-DINA?",
  "answer": "G-DINA stands for the Generalized Deterministic Inputs, Noisy AND Gate model...",
  "pages": [4, 5]
}
```

The answer and page numbers above illustrate the response format; actual results depend on the indexed document and retrieval quality.

### Validation

- Questions must contain at least one character.
- Questions longer than 1,000 characters are rejected.
- Invalid request bodies return a validation error.
- Processing errors return a generic server error while internal details are logged.

## Docker Deployment

### 1. Build the image

```powershell
docker build -t pdf-chatbot .
```

### 2. Create the local database directory

```powershell
New-Item -ItemType Directory -Force .\chroma_db
```

### 3. Ingest the PDF inside Docker

The Docker image excludes local PDFs and the local vector database. Mount your PDF directory and database so ingestion can access the source document and persist the vectors:

```powershell
docker run --rm --env-file "$PWD\.env" --mount "type=bind,source=$($PWD.Path)\data\pdfs,target=/app/data/pdfs,readonly" --mount "type=bind,source=$($PWD.Path)\chroma_db,target=/app/chroma_db" pdf-chatbot python -m app.ingest
```

Run this command from the project directory. Make sure the PDF path configured in `app/ingest.py` exists inside the mounted directory.

### 4. Start the API container

```powershell
docker run -d --name pdf-chatbot-container -p 8000:8000 --env-file "$PWD\.env" --mount "type=bind,source=$($PWD.Path)\chroma_db,target=/app/chroma_db" pdf-chatbot
```

### 5. Test the deployment

Open:

[http://localhost:8000/docs](http://localhost:8000/docs)

Useful commands:

```powershell
docker ps
docker logs --tail 50 pdf-chatbot-container
docker stop pdf-chatbot-container
docker rm pdf-chatbot-container
```

The database mount must be used for both ingestion and API execution so that the API can access the stored embeddings.

## Running Tests

Run the automated test suite:

```powershell
python -m pytest
```

The current test suite covers API functionality, request validation, mocked successful responses, and error handling.

Most API tests mock the service layer, so passing unit tests does not replace end-to-end tests with an actual PDF, vector database, and Gemini API.

## Security Considerations

- Store credentials in environment variables.
- Keep `.env` out of version control.
- Avoid committing private documents and generated vector databases.
- Do not expose internal exception details in API responses.
- Restrict access to the API before deploying it publicly.
- Review document privacy, API usage limits, and model costs before production use.

## Limitations

- Retrieval quality depends on document structure, chunking, embeddings, and the selected top-k results.
- Answers can still be incomplete or incorrect even when grounded in retrieved text.
- Source page references identify retrieved chunks; they do not independently guarantee that every claim is supported by those pages.
- The current ingestion script is configured for a specific PDF path and is not yet a complete multi-document ingestion service.
- The project does not currently provide a graphical chat interface.

## Future Improvements

- Support uploading and indexing multiple PDFs.
- Add document-level filtering and deletion.
- Improve retrieval using hybrid search and reranking.
- Add a RAG evaluation dataset and retrieval-quality metrics.
- Improve citation precision and grounding validation.
- Add structured configuration, monitoring, and deployment automation.
- Build a frontend for interactive document conversations.

## License

Choose and add an appropriate open-source license before publicly distributing this project.
