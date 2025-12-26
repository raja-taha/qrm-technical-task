# Document Intelligence System

A Django-based document processing and question-answering system powered by AI agents. The system ingests documents (PDFs and images), processes them with OCR and text extraction, indexes them into a vector database, and enables intelligent querying over document contents.

## Table of Contents

- [System Architecture](#system-architecture)
- [Agent Responsibilities](#agent-responsibilities)
- [API Endpoints](#api-endpoints)
- [Setup Instructions](#setup-instructions)
- [Technology Stack](#technology-stack)

## System Architecture

### Core Components

1. **REST API Layer** - Django REST Framework endpoints for client interactions
2. **Document Orchestrator** - Coordinates the workflow between agents
3. **AI Agents** - Specialized components for different tasks
4. **Vector Store** - FAISS-based vector database for semantic search
5. **LLM Integration** - Language model for question answering

## Agent Responsibilities

### 1. **Ingestion Agent** (`agents/ingestion_agent.py`)

**Purpose**: Extract and process text from documents

**Key Features**:

- Extracts text from PDF files using `pdfplumber`
- Performs OCR on scanned documents using `EasyOCR`
- Handles both text-based and image-based PDFs
- Splits extracted text into semantic chunks using `RecursiveCharacterTextSplitter`

**Process**:

```
Document (PDF/Image) → Extraction → Text Splitting → Chunks
```

**Configuration**:

- Chunk size: 500 tokens
- Chunk overlap: 100 tokens

---

### 2. **Indexing Agent** (`agents/indexing_agent.py`)

**Purpose**: Create and maintain the vector database index

**Key Features**:

- Generates embeddings for document chunks
- Stores embeddings in FAISS vector database
- Supports clearing old indices or appending to existing ones
- Persists vector store to disk

**Configuration**:

- `CLEAR_VECTOR_STORE_ON_UPLOAD`: Clears old index before new uploads (currently `True`)

---

### 3. **QA Agent** (`agents/qa_agent.py`)

**Purpose**: Answer questions based on document content

**Key Features**:

- Retrieves relevant document chunks using semantic search
- Generates contextual answers using the LLM
- Returns top-5 relevant documents for each query

**Process**:

```
Question → Vector Similarity Search → Context Retrieval → LLM Generation → Answer
```

---

## API Endpoints

All endpoints are prefixed with `/api/`

### 1. **Upload Document**

- **URL**: `POST /api/upload/`
- **Description**: Upload a PDF or image document for processing
- **Request**:
  ```
  Content-Type: multipart/form-data
  Parameter: file (File object)
  ```
- **Response**:
  ```json
  {
    "message": "Document processed successfully"
  }
  ```
- **Supported Formats**: PDF, PNG, JPG, JPEG, and other image formats

---

### 2. **Ask Question**

- **URL**: `POST /api/ask/`
- **Description**: Ask a question about uploaded documents
- **Request**:
  ```json
  {
    "question": "What is the main topic of the document?"
  }
  ```
- **Response**:
  ```json
  {
    "answer": "The document discusses..."
  }
  ```

---

### 3. **Read Vector Store**

- **URL**: `GET /api/store/`
- **Description**: Retrieve information about stored documents and embeddings
- **Response**:
  ```json
  {
    "status": "success",
    "total_vectors": 150,
    "document_count": 5,
    "documents": [
      {
        "id": "doc_1",
        "content": "First 200 characters of the document..."
      }
    ],
    "vector_store_path": "vector_store"
  }
  ```

---

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd document-intelligence
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows (PowerShell)**:

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt)**:

```cmd
venv\Scripts\activate.bat
```

**Linux/macOS**:

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Navigate to Backend Directory

```bash
cd backend
```

### 6. Apply Database Migrations

```bash
python manage.py migrate
```

### 7. Create Superuser (Optional - for Django Admin)

```bash
python manage.py createsuperuser
```

### 8. Run Development Server

```bash
python manage.py runserver
```

The server will start at `http://localhost:8000/`

---

## Testing the System

### Test Upload and Q&A Flow

**1. Upload a document**:

```bash
curl -X POST http://localhost:8000/api/upload/ \
  -F "file=@path/to/document.pdf"
```

**2. Ask a question**:

```bash
curl -X POST http://localhost:8000/api/ask/ \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the main topic?"}'
```

**3. Check vector store**:

```bash
curl http://localhost:8000/api/store/
```

---

## Technology Stack

### Backend Framework

- **Django** (4.2+) - Web framework
- **Django REST Framework** (3.14+) - API framework

### AI & NLP

- **LangChain** (0.2.0+) - LLM framework and orchestration
- **Sentence Transformers** (2.2.2+) - Embedding models
- **Transformers** (4.36+) - Pre-trained models
- **PyTorch** (2.0+) - Deep learning framework

### Document Processing

- **pdfplumber** (0.10.3+) - PDF text extraction
- **EasyOCR** - Optical character recognition
- **Tesseract** - OCR engine (optional)
- **PyMuPDF** - PDF manipulation
- **Pillow** (10.0+) - Image processing

### Vector Database

- **FAISS** (1.7.4+) - Vector similarity search

### Utilities

- **NumPy** (1.24+) - Numerical computing
- **python-dotenv** (1.0+) - Environment variable management
- **psycopg2** (2.9+) - PostgreSQL adapter

---

## Project Structure

```
document-intelligence/
├── backend/
│   ├── agents/                    # AI agent implementations
│   │   ├── ingestion_agent.py    # Document processing
│   │   ├── indexing_agent.py     # Vector store management
│   │   ├── qa_agent.py           # Question answering
│   │   ├── llm.py                # LLM initialization
│   │   ├── vector_store.py       # Vector DB operations
│   │   ├── langchain_embeddings.py
│   │   ├── prompts.py            # LLM prompts
│   │   └── models.py             # Agent models
│   ├── documents/                 # Document management app
│   │   ├── views.py              # API endpoints
│   │   ├── models.py             # Document models
│   │   ├── urls.py               # URL routing
│   │   └── migrations/           # DB migrations
│   ├── orchestrator/              # Workflow orchestration
│   │   └── document_orchestrator.py
│   ├── backend/                   # Django settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── manage.py                  # Django management script
│   ├── vector_store/              # Vector database storage
│   │   └── index.faiss
│   └── media/                     # Uploaded documents
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

---

## Configuration

### Environment Variables

Create a `.env` file in the project root (optional):

```env
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://user:password@localhost/dbname
```

### Vector Store Configuration

- **Location**: `backend/vector_store/index.faiss`
- **Clear on Upload**: Set `CLEAR_VECTOR_STORE_ON_UPLOAD = False` in `agents/indexing_agent.py` to preserve existing embeddings

---

## Troubleshooting

### Import Errors

```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Database Errors

```bash
# Reset migrations
python manage.py migrate zero
python manage.py migrate
```

### OCR Issues

```bash
# EasyOCR may download models on first run
# Ensure internet connection is available
# Models are cached in ~/.EasyOCR/model_zoo/
```

### Vector Store Errors

```bash
# Rebuild vector store by clearing existing index
# Delete: backend/vector_store/index.faiss
# Reupload documents
```

---

## Notes on Trade-offs

### Design Decisions

- **FAISS Over Managed Vector DB**: Chose FAISS for simplicity and offline capability, at the cost of limited query features and no built-in backup/replication
- **Synchronous Processing**: Current implementation uses synchronous document ingestion for simplicity; scales better with async processing but adds complexity
- **Single Vector Store**: All documents share one index; supports multi-document queries but lacks document-level isolation and fine-grained access control
- **In-Memory Embeddings**: Embeddings loaded into memory for faster retrieval; not suitable for very large datasets (100k+ vectors)
- **Sentence Transformers**: Trade accuracy for speed and lower computational requirements; consider fine-tuned models for domain-specific queries
- **Fixed Chunk Size**: Using fixed chunk size (500 tokens) for consistency; overlapping chunks increase storage but improve context continuity

### Performance Considerations

- **Response Latency**: OCR on large scanned documents can take 10-30 seconds; consider async processing for better UX
- **Memory Usage**: Vector store and embeddings require RAM proportional to document volume; GPU acceleration not implemented
- **Scalability**: Current architecture suitable for 100-1000 documents; beyond that requires distributed vector store and batch processing

---

## Future Enhancements

- [ ] Support for more document formats (DOCX, TXT, etc.)
- [ ] Multi-document comparison and analysis
- [ ] Fine-tuned LLM models for domain-specific queries
- [ ] Batch document processing
- [ ] Web UI for easier interaction
- [ ] Authentication and multi-user support
- [ ] Export answers in multiple formats (PDF, JSON, etc.)
- [ ] Document metadata extraction

---

## License

This project is provided as-is for educational and development purposes.

---

## Support

For issues or questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review Django documentation: https://docs.djangoproject.com/
3. Check LangChain documentation: https://python.langchain.com/
