from pydantic import BaseModel, Field
from typing import List, Optional

class ChatRequest(BaseModel):
    query: str = Field(..., description="The user's question or message")
    session_id: Optional[str] = Field("default", description="Session identifier for conversation memory")

class ChatResponse(BaseModel):
    answer: str = Field(..., description="The agent's response to the query")
    sources: Optional[List[str]] = Field(default=[], description="List of source snippets used to answer")

class UploadResponse(BaseModel):
    filename: str = Field(..., description="Name of the uploaded file")
    status: str = Field(..., description="Processing status (e.g., 'success')")
    num_chunks: int = Field(..., description="Number of document chunks processed")
    message: str = Field(..., description="Detailed message")
