# ⚖️ LegalDoc-AI

### Indian Legal Research & Document Intelligence Assistant

LegalDoc-AI is a domain-specific **Retrieval-Augmented Generation (RAG)** application designed to help users research Indian legal documents and interact with uploaded PDFs using natural language.

The system combines **semantic search, keyword search, cross-encoder reranking, document-aware retrieval, OCR, and LLM-based generation** to provide answers grounded in relevant document content with page-level source citations.

> **Disclaimer:** LegalDoc-AI is an AI-powered research and document-assistance system. It is not a lawyer, does not provide professional legal advice, and should not be used as a substitute for qualified legal counsel or authoritative legal sources.

---

## 🚀 Features

### 📄 PDF Question Answering

Upload a PDF and ask questions about its contents using natural language.

### 🔎 Legal Research

Search across a curated legal document corpus containing selected Indian legal documents.

### 🔗 Combined Research

Retrieve information from both the legal corpus and a user's uploaded document.

### 🧠 Hybrid Retrieval

LegalDoc-AI combines two retrieval approaches:

* **Semantic Search** using sentence embeddings
* **Keyword Search** using BM25

The results are combined using **Reciprocal Rank Fusion (RRF)** before reranking.

### 🎯 Cross-Encoder Reranking

Retrieved documents are reranked using a cross-encoder model to improve the relevance of the final context supplied to the LLM.

### 📑 Source Citations

Answers include document metadata such as:

* Document name
* Page number
* Section
* Chunk ID
* Retrieval information

This allows users to trace an answer back to its source document.

### 🖨️ OCR Fallback

For scanned or image-based PDFs where normal text extraction fails, the system can use **Tesseract OCR** to extract text.

### 📊 Document Comparison

Users can compare two uploaded documents and receive an AI-generated analysis containing:

* Similarities
* Key differences
* Potential issues for human review
* Relevant page references

### ⚡ Streaming Responses

The application supports streaming LLM responses so that answers appear progressively instead of waiting for the complete response.

### 🛡️ Evidence & Relevance Validation

Retrieved content is evaluated before generation to reduce the possibility of producing answers from irrelevant document context.

---

# 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │      React UI        │
                    │                      │
                    │ Upload / Search / QA │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      FastAPI         │
                    │      Backend         │
                    └──────────┬───────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                ▼              ▼              ▼
        ┌────────────┐  ┌────────────┐  ┌────────────┐
        │ PDF        │  │ OCR        │  │ Document   │
        │ Extraction │  │ Fallback   │  │ Processing │
        └─────┬──────┘  └─────┬──────┘  └─────┬──────┘
              │                │                │
              └────────────────┼────────────────┘
                               ▼
                       ┌───────────────┐
                       │   Chunking    │
                       │ + Metadata    │
                       └───────┬───────┘
                               │
                               ▼
                     ┌──────────────────┐
                     │ Sentence         │
                     │ Embeddings       │
                     └────────┬─────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │   ChromaDB       │
                     │ Vector Store     │
                     └────────┬─────────┘
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
        ┌──────────────┐             ┌──────────────┐
        │ Semantic     │             │ BM25 Keyword │
        │ Retrieval    │             │ Retrieval    │
        └──────┬───────┘             └──────┬───────┘
               └──────────────┬──────────────┘
                              ▼
                     ┌──────────────────┐
                     │ Hybrid Retrieval │
                     │      (RRF)       │
                     └────────┬─────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │ Cross-Encoder    │
                     │   Reranking      │
                     └────────┬─────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │ Relevance /      │
                     │ Evidence Check   │
                     └────────┬─────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │ Prompt + Context │
                     └────────┬─────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │ Groq LLM         │
                     │ Generation       │
                     └────────┬─────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │ Answer + Sources │
                     └──────────────────┘
```

---

# 🔄 RAG Pipeline

LegalDoc-AI follows a document-grounded RAG pipeline:

```text
PDF
 │
 ▼
Text Extraction
 │
 ├── Normal PDF text
 │
 └── OCR fallback
       │
       ▼
Document Chunking
       │
       ▼
Metadata Creation
       │
       ▼
Embedding Generation
       │
       ▼
ChromaDB
       │
       ▼
User Query
       │
       ├───────────────┐
       ▼               ▼
Semantic Search    BM25 Search
       │               │
       └───────┬───────┘
               ▼
        Hybrid Retrieval
               │
               ▼
         RRF Combination
               │
               ▼
       Cross-Encoder Reranking
               │
               ▼
       Relevance Validation
               │
               ▼
       Relevant Context
               │
               ▼
            LLM
               │
               ▼
      Grounded Answer
               │
               ▼
       Page Citations
```

---

# 🔍 Query Modes

LegalDoc-AI supports three research scopes.

### 1. Legal Research

Searches the preloaded legal corpus.

```text
User Question
      ↓
Legal Corpus
      ↓
Hybrid Retrieval
      ↓
Reranking
      ↓
LLM
```

### 2. My Document

Searches only the document uploaded by the user.

```text
User Question
      ↓
Uploaded PDF
      ↓
Hybrid Retrieval
      ↓
Reranking
      ↓
LLM
```

### 3. Combined Research

Searches both the legal corpus and uploaded document.

```text
User Question
      ↓
Legal Corpus + Uploaded Document
      ↓
Hybrid Retrieval
      ↓
Reranking
      ↓
LLM
```

---

# 🧰 Tech Stack

## Backend

| Technology            | Purpose                       |
| --------------------- | ----------------------------- |
| Python                | Core backend and AI pipeline  |
| FastAPI               | REST API                      |
| Uvicorn               | ASGI server                   |
| PyPDF                 | PDF text extraction           |
| PyMuPDF               | PDF processing                |
| Tesseract OCR         | OCR for scanned documents     |
| Sentence Transformers | Text embeddings and reranking |
| ChromaDB              | Vector database               |
| BM25                  | Keyword retrieval             |
| NumPy                 | Numerical processing          |
| Groq API              | LLM inference                 |

## Frontend

| Technology   | Purpose             |
| ------------ | ------------------- |
| React        | User interface      |
| Vite         | Frontend build tool |
| React Router | Client-side routing |
| Axios        | API communication   |
| JavaScript   | Frontend logic      |
| CSS          | UI styling          |

---

# 🤖 AI Models

### Embedding Model

```text
all-MiniLM-L6-v2
```

Used to convert document chunks and user queries into vector representations.

### Reranker

```text
cross-encoder/ms-marco-MiniLM-L-6-v2
```

Used to rerank retrieved document chunks based on query-document relevance.

### Large Language Model

```text
openai/gpt-oss-20b
```

Accessed through the Groq API for final answer generation.

---

# 📂 Project Structure

```text
LegalDoc-AI/
│
├── frontend/
│   ├── public/
│   └── src/
│       ├── components/
│       │   ├── AnswerCard.jsx
│       │   ├── ChatBox.jsx
│       │   ├── DocumentList.jsx
│       │   ├── FileUpload.jsx
│       │   └── SourceCard.jsx
│       │
│       ├── pages/
│       │   └── DocumentAnalysis.jsx
│       │
│       ├── services/
│       │   └── api.js
│       │
│       ├── App.jsx
│       ├── App.css
│       ├── index.css
│       └── main.jsx
│
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   └── schemas.py
│   │   │
│   │   ├── routes/
│   │   │   ├── comparison.py
│   │   │   ├── documents.py
│   │   │   └── query.py
│   │   │
│   │   ├── services/
│   │   │   ├── chunker.py
│   │   │   ├── citation_service.py
│   │   │   ├── comparison_service.py
│   │   │   ├── document_service.py
│   │   │   ├── embedding_service.py
│   │   │   ├── hybrid_retrieval.py
│   │   │   ├── keyword_search.py
│   │   │   ├── llm_service.py
│   │   │   ├── ocr_service.py
│   │   │   ├── pdf_extractor.py
│   │   │   ├── prompt_service.py
│   │   │   ├── rag_service.py
│   │   │   ├── relevance_service.py
│   │   │   ├── reranker.py
│   │   │   ├── retrieval_service.py
│   │   │   └── vector_store.py
│   │   │
│   │   └── main.py
│   │
│   ├── .env.example
│   └── requirements.txt
│
├── data/
│   └── legal_corpus/
│       └── acts/
│
├── scripts/
│   ├── ingest_document.py
│   ├── query_document.py
│   └── search.py
│
├── vector_store/
├── .gitignore
├── README.md
└── architecture.png
```

> `vector_store/`, uploaded user documents, generated processing files, Python cache files, and `.env` are excluded from version control.

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/LegalDoc-AI.git
cd LegalDoc-AI
```

## 2. Create a virtual environment

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install backend dependencies

```bash
pip install -r backend/requirements.txt
```

## 4. Configure environment variables

Create:

```text
backend/.env
```

Add:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Never commit `.env` to GitHub.

---

# ▶️ Running the Backend

From the project root:

```bash
uvicorn backend.app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

---

# ▶️ Running the Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at:

```text
http://localhost:5173
```

---

# 📚 Adding Legal Documents

LegalDoc-AI uses a curated legal document corpus.

Documents can be placed under:

```text
data/legal_corpus/
```

The ingestion pipeline extracts text, creates chunks, generates embeddings, and stores the resulting vectors and metadata in ChromaDB.

Example:

```bash
python scripts/ingest_document.py
```

The original legal documents remain the source material, while the vector database stores searchable representations.

---

# 🔐 Security & Privacy

The project follows several basic security practices:

* API keys are stored in environment variables.
* `.env` files are excluded from Git.
* User-uploaded documents are excluded from Git.
* Vector database files are excluded from Git.
* Generated processing files are excluded from Git.
* Uploaded documents are isolated using document identifiers.

For production deployment, additional controls such as authentication, authorization, encryption, file validation, rate limiting, malware scanning, and secure storage should be implemented.

---

# ⚠️ Limitations

LegalDoc-AI is a research prototype and has several limitations:

* The legal corpus is curated and does not represent all Indian laws.
* OCR accuracy depends on document quality.
* Retrieval quality depends on document chunking and indexing.
* LLM responses can still contain errors.
* Legal documents may be amended or replaced over time.
* The system does not independently determine the legal validity of a conclusion.
* Users should verify important information against current authoritative legal sources.

---

# 🔮 Future Improvements

Possible future development includes:

* Automated ingestion of larger legal corpora
* More advanced legal-domain embeddings
* Legal-domain reranking models
* Improved section and subsection extraction
* Court judgment retrieval
* Citation verification
* Temporal/version-aware legal research
* Multilingual Indian-language support
* User authentication
* Document access control
* Production deployment
* Evaluation datasets for retrieval and answer quality
* Automated hallucination detection
* More advanced document comparison

---

# 🎯 Learning Outcomes

This project demonstrates practical implementation of:

* Retrieval-Augmented Generation
* Natural Language Processing
* Vector databases
* Semantic search
* Keyword search
* Hybrid information retrieval
* Reciprocal Rank Fusion
* Cross-encoder reranking
* OCR
* Document processing
* REST API development
* Streaming responses
* React frontend development
* AI application architecture
* Evidence-grounded generation

---

# 👨‍💻 Project

**LegalDoc-AI — Indian Legal Research & Document Intelligence Assistant**

Built as an AI/ML + Full-Stack application combining document intelligence, information retrieval, and generative AI.

---

## ⚖️ Disclaimer

LegalDoc-AI is intended for **educational, research, and document-assistance purposes only**.

It does not constitute legal advice and does not establish an attorney-client relationship. Users should consult qualified legal professionals and verify important information using authoritative and up-to-date legal sources.
