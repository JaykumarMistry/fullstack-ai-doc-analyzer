import os
import tempfile
import pandas as pd
from PyPDF2 import PdfReader
from loguru import logger
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

class DocumentProcessor:
    def __init__(self):
        # We use a simple RecursiveCharacterTextSplitter for "Semantic Chunking"
        # 500 characters with 50 character overlap is a good default for dense text
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = None
        self.vector_store_path = os.getenv("VECTOR_STORE_PATH", "./faiss_index")

    def process_file(self, file_path: str, filename: str) -> int:
        logger.info(f"Processing document: {filename}")
        documents = []

        if filename.endswith(".pdf"):
            documents = self._process_pdf(file_path, filename)
        elif filename.endswith(".csv"):
            documents = self._process_csv(file_path, filename)
        else:
            logger.error(f"Unsupported file type: {filename}")
            raise ValueError("Unsupported file type. Please upload PDF or CSV.")

        if not documents:
            logger.warning("No text extracted from document.")
            return 0

        logger.debug(f"Extracted {len(documents)} initial documents. Chunking...")
        chunks = self.text_splitter.split_documents(documents)
        logger.info(f"Created {len(chunks)} chunks. Updating Vector Store...")

        if self.vector_store is None:
            if os.path.exists(self.vector_store_path):
                self.vector_store = FAISS.load_local(self.vector_store_path, self.embeddings, allow_dangerous_deserialization=True)
                self.vector_store.add_documents(chunks)
            else:
                self.vector_store = FAISS.from_documents(chunks, self.embeddings)
        else:
            self.vector_store.add_documents(chunks)

        # Save to disk for persistence
        self.vector_store.save_local(self.vector_store_path)
        logger.info(f"Successfully processed and indexed {len(chunks)} chunks.")
        
        return len(chunks)

    def _process_pdf(self, file_path: str, filename: str):
        docs = []
        try:
            reader = PdfReader(file_path)
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    docs.append(Document(page_content=text, metadata={"source": filename, "page": i}))
        except Exception as e:
            logger.error(f"Error reading PDF {filename}: {e}")
            raise e
        return docs

    def _process_csv(self, file_path: str, filename: str):
        docs = []
        try:
            df = pd.read_csv(file_path)
            # Convert each row to a document string
            for index, row in df.iterrows():
                content = ", ".join([f"{col}: {val}" for col, val in row.items()])
                docs.append(Document(page_content=content, metadata={"source": filename, "row": index}))
        except Exception as e:
            logger.error(f"Error reading CSV {filename}: {e}")
            raise e
        return docs

document_processor = DocumentProcessor()
