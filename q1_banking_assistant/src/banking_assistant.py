"""
Main Banking Assistant class that orchestrates all components
"""
import os
from typing import List, Dict, Any, Optional
from pathlib import Path

from .document_processor import BankingDocumentProcessor
from .vector_store import BankingVectorStore
from .retrieval_chain import BankingRetrievalChain
from .config import settings


class BankingAssistant:
    """Main Banking Assistant class"""
    
    def __init__(self):
        """Initialize the banking assistant with all components"""
        try:
            self.document_processor = BankingDocumentProcessor()
            self.vector_store = BankingVectorStore()
            self.retrieval_chain = BankingRetrievalChain()
            
            print("Banking Assistant initialized successfully")
            
        except Exception as e:
            raise Exception(f"Failed to initialize Banking Assistant: {str(e)}")
    
    def load_documents(self, document_path: str) -> Dict[str, Any]:
        """Load documents into the knowledge base"""
        try:
            document_path = Path(document_path)
            
            if document_path.is_file():
                # Load single document
                documents = self.document_processor.load_document(str(document_path))
            elif document_path.is_dir():
                # Load all documents from directory
                documents = self.document_processor.load_documents_from_directory(str(document_path))
            else:
                raise FileNotFoundError(f"Path not found: {document_path}")
            
            if not documents:
                return {
                    "success": False,
                    "message": "No documents found or processed",
                    "document_count": 0
                }
            
            # Add documents to vector store
            self.vector_store.add_documents(documents)
            
            return {
                "success": True,
                "message": f"Successfully loaded {len(documents)} document chunks",
                "document_count": len(documents),
                "documents": [doc.metadata for doc in documents]
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error loading documents: {str(e)}",
                "document_count": 0
            }
    
    def ask_question(self, question: str) -> Dict[str, Any]:
        """Ask a question to the banking assistant"""
        try:
            if not question.strip():
                return {
                    "success": False,
                    "answer": "Please provide a valid question.",
                    "sources": [],
                    "confidence": "low"
                }
            
            # Get response from retrieval chain
            result = self.retrieval_chain.query(question)
            
            return {
                "success": True,
                "answer": result["answer"],
                "sources": result["sources"],
                "confidence": result["confidence"],
                "validation": result.get("validation", {})
            }
            
        except Exception as e:
            return {
                "success": False,
                "answer": f"Error processing question: {str(e)}",
                "sources": [],
                "confidence": "error"
            }
    
    def conversational_ask(
        self, 
        question: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """Ask a question with conversation context"""
        try:
            result = self.retrieval_chain.conversational_query(question, conversation_history)
            
            return {
                "success": True,
                "answer": result["answer"],
                "sources": result["sources"],
                "confidence": result["confidence"],
                "validation": result.get("validation", {})
            }
            
        except Exception as e:
            return {
                "success": False,
                "answer": f"Error in conversational query: {str(e)}",
                "sources": [],
                "confidence": "error"
            }
    
    def get_loan_information(self, loan_type: str = None) -> Dict[str, Any]:
        """Get structured loan information"""
        try:
            question = f"What are the terms and conditions for {loan_type} loans?" if loan_type else "What loan products are available?"
            
            response_format = {
                "loan_products": [
                    {
                        "name": "string",
                        "interest_rate": "string",
                        "term_length": "string",
                        "minimum_amount": "string",
                        "requirements": ["string"]
                    }
                ],
                "fees": [
                    {
                        "fee_type": "string",
                        "amount": "string",
                        "description": "string"
                    }
                ]
            }
            
            result = self.retrieval_chain.structured_query(question, response_format)
            
            return {
                "success": True,
                "data": result["data"],
                "sources": result["sources"]
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error getting loan information: {str(e)}"
            }
    
    def get_compliance_requirements(self, regulation_type: str = None) -> Dict[str, Any]:
        """Get compliance requirements"""
        try:
            question = f"What are the compliance requirements for {regulation_type}?" if regulation_type else "What are the main compliance requirements?"
            
            response_format = {
                "regulations": [
                    {
                        "name": "string",
                        "requirements": ["string"],
                        "deadlines": ["string"],
                        "penalties": ["string"]
                    }
                ],
                "procedures": [
                    {
                        "procedure_name": "string",
                        "steps": ["string"],
                        "responsible_party": "string"
                    }
                ]
            }
            
            result = self.retrieval_chain.structured_query(question, response_format)
            
            return {
                "success": True,
                "data": result["data"],
                "sources": result["sources"]
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error getting compliance requirements: {str(e)}"
            }
    
    def get_knowledge_base_stats(self) -> Dict[str, Any]:
        """Get knowledge base statistics"""
        try:
            stats = self.vector_store.get_collection_stats()
            
            return {
                "success": True,
                "stats": stats,
                "conversation_history_length": len(self.retrieval_chain.get_conversation_history())
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error getting stats: {str(e)}"
            }
    
    def search_documents(self, query: str, k: int = 5) -> Dict[str, Any]:
        """Search documents in the knowledge base"""
        try:
            documents = self.vector_store.similarity_search(query, k=k)
            
            return {
                "success": True,
                "documents": [
                    {
                        "content": doc.page_content[:500] + "..." if len(doc.page_content) > 500 else doc.page_content,
                        "metadata": doc.metadata
                    }
                    for doc in documents
                ],
                "count": len(documents)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error searching documents: {str(e)}"
            }
    
    def clear_conversation_history(self) -> Dict[str, Any]:
        """Clear conversation history"""
        try:
            self.retrieval_chain.clear_memory()
            
            return {
                "success": True,
                "message": "Conversation history cleared successfully"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error clearing conversation history: {str(e)}"
            }
    
    def reset_knowledge_base(self) -> Dict[str, Any]:
        """Reset the entire knowledge base"""
        try:
            self.vector_store.reset_vector_store()
            self.retrieval_chain.clear_memory()
            
            return {
                "success": True,
                "message": "Knowledge base reset successfully"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error resetting knowledge base: {str(e)}"
            } 

    def get_documents_list(self) -> Dict[str, Any]:
        """Get list of all documents in the knowledge base"""
        try:
            # Get all documents from vector store
            all_docs = self.vector_store.get_all_documents()
            
            # Group by source file
            documents_by_source = {}
            for doc in all_docs:
                source = doc.metadata.get('file_path', 'Unknown')
                if source not in documents_by_source:
                    documents_by_source[source] = {
                        'file_path': source,
                        'chunk_count': 0,
                        'content_types': set(),
                        'upload_date': doc.metadata.get('upload_date', 'Unknown')
                    }
                documents_by_source[source]['chunk_count'] += 1
                if 'content_type' in doc.metadata:
                    documents_by_source[source]['content_types'].add(doc.metadata['content_type'])
            
            # Convert sets to lists for JSON serialization
            for doc_info in documents_by_source.values():
                doc_info['content_types'] = list(doc_info['content_types'])
            
            return {
                "success": True,
                "documents": list(documents_by_source.values()),
                "total_documents": len(documents_by_source),
                "total_chunks": len(all_docs)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error getting documents list: {str(e)}"
            }
    
    def delete_document(self, document_id: str) -> Dict[str, Any]:
        """Delete a specific document from the knowledge base"""
        try:
            # For now, we'll delete by file path
            # In a more sophisticated system, you might want to use document IDs
            result = self.vector_store.delete_documents_by_source(document_id)
            
            return {
                "success": True,
                "message": f"Document {document_id} deleted successfully",
                "deleted_document": document_id
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error deleting document: {str(e)}"
            }
    
    def load_sample_documents(self) -> Dict[str, Any]:
        """Load sample documents into the knowledge base"""
        try:
            sample_dir = Path("sample_documents")
            if not sample_dir.exists():
                return {
                    "success": False,
                    "message": "Sample documents directory not found",
                    "document_count": 0
                }
            
            result = self.load_documents(str(sample_dir))
            
            return {
                "success": True,
                "message": f"Sample documents loaded: {result['message']}",
                "document_count": result['document_count']
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error loading sample documents: {str(e)}"
            } 