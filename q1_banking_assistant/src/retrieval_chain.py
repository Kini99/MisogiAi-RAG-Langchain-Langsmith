"""
Retrieval chain implementation for banking assistant
"""
from typing import List, Dict, Any, Optional
from langchain.schema import Document
from langchain.memory import ConversationBufferMemory

from .vector_store import BankingVectorStore
from .llm_manager import BankingLLMManager
from .config import settings


class BankingRetrievalChain:
    """Retrieval chain for banking assistant with conversation memory"""
    
    def __init__(self):
        self.vector_store = BankingVectorStore()
        self.llm_manager = BankingLLMManager()
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Initialize retrieval chain
        self.retrieval_chain = None
        self._initialize_chain()
    
    def _initialize_chain(self):
        """Initialize the retrieval chain"""
        try:
            # For newer LangChain versions, we'll use direct retrieval and LLM calls
            # instead of the deprecated RetrievalQA chain
            print("Retrieval chain initialized successfully")
            
        except Exception as e:
            raise Exception(f"Failed to initialize retrieval chain: {str(e)}")
    
    def query(
        self, 
        question: str,
        filter_dict: Optional[Dict[str, Any]] = None,
        k: int = 4
    ) -> Dict[str, Any]:
        """Query the banking knowledge base"""
        try:
            # Perform similarity search
            relevant_docs = self.vector_store.similarity_search(
                query=question,
                k=k,
                filter_dict=filter_dict
            )
            
            if not relevant_docs:
                return {
                    "answer": "I cannot answer this question based on the uploaded documents. The information you're asking about is not available in the documents that have been loaded into the system.",
                    "sources": [],
                    "confidence": "low"
                }
            
            # Combine context from relevant documents
            context = self._combine_context(relevant_docs)
            
            # Determine prompt type based on content
            prompt_type = self._determine_prompt_type(relevant_docs)
            
            # Generate response
            answer = self.llm_manager.generate_response(
                question=question,
                context=context,
                prompt_type=prompt_type
            )
            
            # Validate response
            validation = self.llm_manager.validate_banking_response(answer, context)
            
            return {
                "answer": answer,
                "sources": [doc.metadata for doc in relevant_docs],
                "context": context,
                "validation": validation,
                "confidence": self._calculate_confidence(relevant_docs, answer)
            }
            
        except Exception as e:
            return {
                "answer": f"Error processing query: {str(e)}",
                "sources": [],
                "confidence": "error"
            }
    
    def _combine_context(self, documents: List[Document]) -> str:
        """Combine context from multiple documents"""
        context_parts = []
        
        for i, doc in enumerate(documents, 1):
            content = doc.page_content.strip()
            metadata = doc.metadata
            
            # Create clear source attribution
            source_info = f"DOCUMENT {i}: "
            if 'file_path' in metadata:
                filename = metadata['file_path'].split('/')[-1] if '/' in metadata['file_path'] else metadata['file_path']
                source_info += f"{filename}"
            elif 'source' in metadata:
                source_info += f"{metadata['source']}"
            else:
                source_info += "Unknown source"
            
            if 'page' in metadata:
                source_info += f" (Page: {metadata['page']})"
            
            # Format the content with clear source attribution
            formatted_content = f"{source_info}\n{content}"
            context_parts.append(formatted_content)
        
        return "\n\n---\n\n".join(context_parts)
    
    def _determine_prompt_type(self, documents: List[Document]) -> str:
        """Determine the appropriate prompt type based on document content"""
        for doc in documents:
            # Check if document contains table data
            if doc.metadata.get('content_type') == 'table':
                return "table"
            
            # Check for compliance-related keywords
            content_lower = doc.page_content.lower()
            compliance_keywords = [
                'regulation', 'compliance', 'regulatory', 'requirement',
                'deadline', 'audit', 'policy', 'procedure'
            ]
            
            if any(keyword in content_lower for keyword in compliance_keywords):
                return "compliance"
        
        return "banking"
    
    def _calculate_confidence(self, documents: List[Document], answer: str) -> str:
        """Calculate confidence level based on document relevance and answer quality"""
        try:
            # Check document relevance scores
            docs_with_scores = self.vector_store.similarity_search_with_score(
                query=answer,
                k=len(documents)
            )
            
            # Calculate average relevance score
            if docs_with_scores:
                avg_score = sum(score for _, score in docs_with_scores) / len(docs_with_scores)
                
                if avg_score > 0.8:
                    return "high"
                elif avg_score > 0.6:
                    return "medium"
                else:
                    return "low"
            
            return "medium"
            
        except Exception:
            return "medium"
    
    def conversational_query(
        self, 
        question: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """Handle conversational queries with memory"""
        try:
            # Add conversation history to memory if provided
            if conversation_history:
                for turn in conversation_history:
                    self.memory.save_context(
                        {"input": turn.get("question", "")},
                        {"output": turn.get("answer", "")}
                    )
            
            # Perform query
            result = self.query(question)
            
            # Save to memory
            self.memory.save_context(
                {"input": question},
                {"output": result["answer"]}
            )
            
            return result
            
        except Exception as e:
            return {
                "answer": f"Error in conversational query: {str(e)}",
                "sources": [],
                "confidence": "error"
            }
    
    def structured_query(
        self, 
        question: str,
        response_format: Dict[str, Any],
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Perform structured query with specific response format"""
        try:
            # Get relevant documents
            relevant_docs = self.vector_store.similarity_search(
                query=question,
                k=4,
                filter_dict=filter_dict
            )
            
            if not relevant_docs:
                return {
                    "error": "No relevant documents found",
                    "data": None
                }
            
            # Combine context
            context = self._combine_context(relevant_docs)
            
            # Generate structured response
            structured_response = self.llm_manager.generate_structured_response(
                question=question,
                context=context,
                response_format=response_format
            )
            
            return {
                "data": structured_response,
                "sources": [doc.metadata for doc in relevant_docs],
                "context": context
            }
            
        except Exception as e:
            return {
                "error": f"Structured query failed: {str(e)}",
                "data": None
            }
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get conversation history from memory"""
        try:
            return self.memory.chat_memory.messages
        except Exception:
            return []
    
    def clear_memory(self):
        """Clear conversation memory"""
        try:
            self.memory.clear()
        except Exception as e:
            print(f"Error clearing memory: {e}") 