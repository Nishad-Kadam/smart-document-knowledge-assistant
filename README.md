# 📚 Smart Document Knowledge Assistant

A web-based **Retrieval-Augmented Generation (RAG)** application that allows students to upload PDF or TXT documents and ask questions about their contents.

The system retrieves the most relevant sections of the uploaded document and uses an LLM to generate answers based only on the retrieved document content.

## 🎯 Problem Statement

Students and researchers often work with unstructured PDFs, research articles, lab manuals, and text notes. Finding specific information using traditional search can be difficult when the required information involves concepts, synonyms, or relationships across different parts of a document.

This project implements a **Smart Document Knowledge Assistant** that uses RAG to provide context-aware answers from uploaded documents.

## ✨ Features

- Upload **PDF and TXT** documents
- Extract text from uploaded documents
- Split documents into smaller text chunks
- Generate embeddings for document chunks
- Perform similarity-based retrieval
- Retrieve the **top 3 most relevant chunks**
- Generate answers using Google's Gemini API
- Chat-style question and answer interface
- Maintain conversation history during the session
- Display the document chunks referenced for an answer
- Refuse to answer when the information cannot be found in the uploaded document

## 🧠 How It Works

The application follows a simple RAG pipeline:

```text
              Uploaded Document
                     │
                     ▼
              Text Extraction
                     │
                     ▼
                Text Chunks
                     │
                     ▼
              Gemini Embeddings
                     │
                     ▼
                Vector Data
                     │
               User Question
                     │
                     ▼
            Question Embedding
                     │
                     ▼
            Similarity Comparison
                     │
                     ▼
            Top 3 Relevant Chunks
                     │
                     ▼
                Gemini LLM
                     │
                     ▼
              Grounded Answer
                     │
                     ▼
             Referenced Chunks
```

### Two AI components are used:

**Embedding model — `gemini-embedding-001`**

Converts document chunks and user questions into numerical vectors. These vectors are compared using cosine similarity to find relevant information.

**Generation model — `gemini-3.5-flash-lite`**

Receives the user's question together with the retrieved document chunks and generates an answer based only on that context.

## 🛠️ Technology Stack

- **Python**
- **Streamlit** — Web application interface
- **PyMuPDF** — PDF text extraction
- **Google Gemini API** — Embeddings and answer generation
- **Cosine Similarity** — Document retrieval
- **Git & GitHub** — Version control and project hosting

## 📁 Project Structure

```text
smart-document-assistant/
│
├── .streamlit/
│   └── secrets.toml       # API key (not committed to GitHub)
│
├── app.py                 # Main application
├── requirements.txt       # Python dependencies
├── .gitignore             # Files excluded from Git
├── README.md              # Project documentation
└── venv/                  # Python virtual environment
```

## 🚀 Setup and Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd smart-document-assistant
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Gemini API key

Create the following file:

```text
.streamlit/secrets.toml
```

Add:

```toml
GEMINI_API_KEY = "your_api_key_here"
```

The secrets file should **never be committed to GitHub**.

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 💡 Example Usage

1. Upload a PDF containing lecture notes or other study material.
2. Wait for the document to be processed.
3. Ask a question about the uploaded document.
4. The system retrieves the most relevant sections.
5. Gemini generates an answer using those sections.
6. The retrieved document chunks are displayed below the answer for reference.

For example:

```text
User:
What is the objective of Problem 02?

Assistant:
[Answer generated from the uploaded document]

Referenced Document Chunks:
Chunk 4
Similarity: 0.82
[Relevant document text]
```

If the requested information is not present in the retrieved document context, the assistant responds:

```text
I could not find the answer in the uploaded document.
```

## 🔒 API Key Security

The Gemini API key is stored using **Streamlit Secrets** rather than directly inside the Python source code.

The following file is excluded using `.gitignore`:

```text
.streamlit/secrets.toml
```

This prevents the API key from being accidentally pushed to the public repository.

## 📌 Current Limitations

- The application currently processes one uploaded document at a time.
- Document embeddings are created when a document is loaded.
- Retrieval currently uses the top 3 most similar chunks.
- The system depends on the Gemini API for embeddings and answer generation.

## 🔮 Future Improvements

Possible future improvements include:

- Support for multiple documents simultaneously
- Persistent vector storage
- More efficient embedding generation
- Improved chunking based on document structure
- Better source/reference formatting
- Deployment as a publicly accessible web application

## 👨‍💻 Project

This project was developed as a practical implementation of **Retrieval-Augmented Generation (RAG)** for document-based question answering.
