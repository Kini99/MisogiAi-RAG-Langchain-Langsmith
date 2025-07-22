"""
FastAPI web application for Banking Assistant
"""
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
from pathlib import Path

from .banking_assistant import BankingAssistant
from .config import settings


# Pydantic models for API requests/responses
class QuestionRequest(BaseModel):
    question: str
    conversation_history: Optional[List[Dict[str, str]]] = None


class DocumentUploadResponse(BaseModel):
    success: bool
    message: str
    document_count: int


class QuestionResponse(BaseModel):
    success: bool
    answer: str
    sources: List[Dict[str, Any]]
    confidence: str
    validation: Optional[Dict[str, Any]] = None


class LoanInfoRequest(BaseModel):
    loan_type: Optional[str] = None


class ComplianceRequest(BaseModel):
    regulation_type: Optional[str] = None


class SearchRequest(BaseModel):
    query: str
    k: int = 5


# Initialize FastAPI app
app = FastAPI(
    title="Banking AI Assistant",
    description="AI-powered banking assistant for loan products, regulatory requirements, and internal policies",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize banking assistant
banking_assistant = None


@app.on_event("startup")
async def startup_event():
    """Initialize the banking assistant on startup"""
    global banking_assistant
    try:
        banking_assistant = BankingAssistant()
        print("Banking Assistant API started successfully")
    except Exception as e:
        print(f"Failed to initialize Banking Assistant: {e}")
        raise e


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Banking AI Assistant API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        if banking_assistant is None:
            raise HTTPException(status_code=503, detail="Banking Assistant not initialized")
        
        stats = banking_assistant.get_knowledge_base_stats()
        return {
            "status": "healthy",
            "knowledge_base": stats
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Health check failed: {str(e)}")


@app.post("/upload-document", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload a single document"""
    try:
        if banking_assistant is None:
            raise HTTPException(status_code=503, detail="Banking Assistant not initialized")
        
        # Create uploads directory if it doesn't exist
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)
        
        # Save uploaded file
        file_path = upload_dir / file.filename
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Load document into knowledge base
        result = banking_assistant.load_documents(str(file_path))
        
        # Add additional information about the upload
        if result["success"]:
            result["message"] = f"Document '{file.filename}' uploaded and processed successfully. {result['document_count']} chunks created."
            result["filename"] = file.filename
            result["file_size"] = len(content)
        
        return DocumentUploadResponse(
            success=result["success"],
            message=result["message"],
            document_count=result["document_count"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@app.post("/upload-directory")
async def upload_directory(directory_path: str = Form(...)):
    """Upload all documents from a directory"""
    try:
        if banking_assistant is None:
            raise HTTPException(status_code=503, detail="Banking Assistant not initialized")
        
        result = banking_assistant.load_documents(directory_path)
        
        return {
            "success": result["success"],
            "message": result["message"],
            "document_count": result["document_count"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Directory upload failed: {str(e)}")


@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """Ask a question to the banking assistant"""
    try:
        if banking_assistant is None:
            raise HTTPException(status_code=503, detail="Banking Assistant not initialized")
        
        if request.conversation_history:
            result = banking_assistant.conversational_ask(
                request.question,
                request.conversation_history
            )
        else:
            result = banking_assistant.ask_question(request.question)
        
        return QuestionResponse(
            success=result["success"],
            answer=result["answer"],
            sources=result["sources"],
            confidence=result["confidence"],
            validation=result.get("validation")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Question processing failed: {str(e)}")


@app.post("/loan-information")
async def get_loan_information(request: LoanInfoRequest):
    """Get structured loan information"""
    try:
        if banking_assistant is None:
            raise HTTPException(status_code=503, detail="Banking Assistant not initialized")
        
        result = banking_assistant.get_loan_information(request.loan_type)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Loan information retrieval failed: {str(e)}")


@app.post("/compliance-requirements")
async def get_compliance_requirements(request: ComplianceRequest):
    """Get compliance requirements"""
    try:
        if banking_assistant is None:
            raise HTTPException(status_code=503, detail="Banking Assistant not initialized")
        
        result = banking_assistant.get_compliance_requirements(request.regulation_type)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Compliance requirements retrieval failed: {str(e)}")


@app.post("/search-documents")
async def search_documents(request: SearchRequest):
    """Search documents in the knowledge base"""
    try:
        if banking_assistant is None:
            raise HTTPException(status_code=503, detail="Banking Assistant not initialized")
        
        result = banking_assistant.search_documents(request.query, request.k)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document search failed: {str(e)}")


@app.get("/stats")
async def get_stats():
    """Get knowledge base statistics"""
    try:
        if banking_assistant is None:
            raise HTTPException(status_code=503, detail="Banking Assistant not initialized")
        
        result = banking_assistant.get_knowledge_base_stats()
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stats retrieval failed: {str(e)}")


@app.post("/clear-conversation")
async def clear_conversation():
    """Clear conversation history"""
    try:
        if banking_assistant is None:
            raise HTTPException(status_code=503, detail="Banking Assistant not initialized")
        
        result = banking_assistant.clear_conversation_history()
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversation clearing failed: {str(e)}")


@app.post("/reset-knowledge-base")
async def reset_knowledge_base():
    """Reset the entire knowledge base"""
    try:
        if banking_assistant is None:
            raise HTTPException(status_code=503, detail="Banking Assistant not initialized")
        
        result = banking_assistant.reset_knowledge_base()
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Knowledge base reset failed: {str(e)}")


@app.get("/documents")
async def get_documents():
    """Get list of all documents in the knowledge base"""
    try:
        if banking_assistant is None:
            raise HTTPException(status_code=503, detail="Banking Assistant not initialized")
        
        # Get documents from vector store
        result = banking_assistant.get_documents_list()
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document list retrieval failed: {str(e)}")


@app.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    """Delete a specific document from the knowledge base"""
    try:
        if banking_assistant is None:
            raise HTTPException(status_code=503, detail="Banking Assistant not initialized")
        
        result = banking_assistant.delete_document(document_id)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document deletion failed: {str(e)}")


@app.post("/load-sample-documents")
async def load_sample_documents():
    """Load sample documents into the knowledge base"""
    try:
        if banking_assistant is None:
            raise HTTPException(status_code=503, detail="Banking Assistant not initialized")
        
        result = banking_assistant.load_sample_documents()
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sample document loading failed: {str(e)}")


def run_server():
    """Run the FastAPI server"""
    uvicorn.run(
        "src.api:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )


if __name__ == "__main__":
    run_server() 