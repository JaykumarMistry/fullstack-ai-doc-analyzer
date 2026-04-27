# Fullstack AI Document Analyzer 🤖📄

A production-ready "Vertical Slice" of an Agentic RAG (Retrieval-Augmented Generation) application. This tool allows users to upload documents (PDFs/CSVs), processes the data into a locally searchable vector format, and provides an intelligent chat interface powered by an autonomous AI agent to answer questions about the data.

## ✨ Features
* **Agentic Routing**: The LLM acts as an autonomous agent, deciding on-the-fly whether to answer from general knowledge or use its tools to search your uploaded documents.
* **Local Vector Storage**: Uses FAISS for incredibly fast, localized similarity search—no need to provision expensive cloud vector databases.
* **Semantic Chunking**: Intelligently slices documents into optimal chunks for accurate LLM context ingestion.
* **Beautiful UI**: A modern, responsive interface built with Next.js and Tailwind CSS.
* **Production Observability**: Structured JSON logging on the backend using `loguru`.

## 🛠️ Technology Stack
* **Frontend**: Next.js (React), Tailwind CSS, Lucide Icons.
* **Backend**: FastAPI (Python), Pydantic (Data Contracts).
* **AI & Data**: LangChain (Agent framework), FAISS (Vector DB), OpenAI, PyPDF2 & Pandas (Parsing).

---

## 🚀 Getting Started

### Prerequisites
* **Node.js** (v18+) and npm installed on your machine.
* **Python** (3.11+) installed on your machine.
* An **OpenAI API Key**.

### 1. Backend Setup (FastAPI)
The backend is responsible for API routing, file processing, and housing the LLM logic.

1. Open a terminal and navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your environment variables by creating `.env` and adding your API key:
   ```env
   OPENAI_API_KEY=your_real_openai_api_key_here
   ```
4. Start the FastAPI development server:
   ```bash
   uvicorn app.main:app --reload
   ```
   *The backend will run on `http://localhost:8000`.*

### 2. Frontend Setup (Next.js)
The frontend provides the user interface for uploading documents and chatting with the agent.

1. Open a **new** terminal and navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install the Node dependencies:
   ```bash
   npm install
   ```
3. Start the Next.js development server:
   ```bash
   npm run dev
   ```
   *The frontend will run on `http://localhost:3000`.*

---

## 💡 How to Use 
1. Open `http://localhost:3000` in your web browser.
2. Drag and drop a PDF or CSV file into the designated upload zone.
3. Click **Submit Document**. You will see a success message when the file is processed and indexed.
4. Use the chat interface to ask questions. 
   - *Example general question:* "What is the capital of France?" (The agent answers directly).
   - *Example specific question:* "Based on the document I just uploaded, what is the candidate's work experience?" (The agent autonomously queries the FAISS database to find the answer).

## 🔒 Security Note
The `.gitignore` is configured to prevent your `.env` (API keys) and local `faiss_index` database from being committed to version control. Never commit your secret API keys to GitHub!
