import os
import shutil
import tempfile
from fastapi import APIRouter, File, UploadFile, HTTPException
from loguru import logger
from ..models.schemas import ChatRequest, ChatResponse, UploadResponse
from ..services.document_processor import document_processor
from ..services.agent import agent_service

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
def upload_document(file: UploadFile = File(...)):
    logger.info(f"Received upload request for file: {file.filename}")
    
    if not file.filename.endswith((".pdf", ".csv")):
        logger.warning(f"Invalid file type uploaded: {file.filename}")
        raise HTTPException(status_code=400, detail="Only PDF and CSV files are supported.")
    
    try:
        # Create a temporary file to save the uploaded content
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name
            
        # Process the file
        num_chunks = document_processor.process_file(tmp_path, file.filename)
        
        # Cleanup temporary file
        os.remove(tmp_path)
        
        return UploadResponse(
            filename=file.filename,
            status="success",
            num_chunks=num_chunks,
            message="Document successfully processed and indexed."
        )
    except Exception as e:
        logger.error(f"Error processing file {file.filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@router.post("/chat", response_model=ChatResponse)
def chat_with_agent(request: ChatRequest):
    logger.info(f"Received chat request: {request.query}")
    
    try:
        answer = agent_service.invoke(request.query)
        return ChatResponse(answer=answer)
    except Exception as e:
        logger.error(f"Error generating chat response: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate a response.")
