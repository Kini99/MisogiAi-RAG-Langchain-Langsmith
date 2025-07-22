"""
LLM manager using Google Gemini for banking assistant
"""
import os
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate

from .config import settings


class BankingLLMManager:
    """LLM manager for banking assistant using Google Gemini"""
    
    def __init__(self):
        if not settings.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is required. Please set it in your environment variables.")
        
        # Set environment variable for LangChain Google GenAI
        os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY
        
        # Configure Google AI
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        
        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(
            model=settings.MODEL_NAME,
            temperature=settings.TEMPERATURE,
            max_output_tokens=settings.MAX_TOKENS,
            convert_system_message_to_human=True
        )
        
        # Banking-specific prompts
        self._initialize_prompts()
    
    def _initialize_prompts(self):
        """Initialize banking-specific prompts"""
        
        # Main banking assistant prompt - STRICT RAG ENFORCEMENT
        self.banking_prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are a banking assistant that can ONLY provide information from the uploaded banking documents. You MUST NOT use any external knowledge or general banking information.

CRITICAL RULES:
1. ONLY use information that is explicitly stated in the provided context/documents
2. If the information is not in the provided documents, say "I cannot answer this question based on the uploaded documents"
3. DO NOT use any general banking knowledge, industry standards, or external information
4. Quote specific text from the documents when possible
5. Always cite the source document when providing information
6. If asked about rates, terms, or conditions not in the documents, clearly state they are not available

Context from uploaded banking documents:
{context}

Question: {question}

Remember: You can ONLY use information from the above context. If the information is not there, you cannot provide it."""
        )
        
        # Table-specific prompt for handling structured data
        self.table_prompt = PromptTemplate(
            input_variables=["table_data", "question"],
            template="""You are analyzing banking table data from uploaded documents. You can ONLY use information from the provided table.

CRITICAL RULES:
1. ONLY use data that appears in the table below
2. If the question cannot be answered from this table, say "This information is not available in the uploaded table"
3. DO NOT use any external banking knowledge or industry standards
4. Quote exact values from the table when possible

Table Data from uploaded documents:
{table_data}

Question: {question}

Remember: You can ONLY use information from the above table. If the information is not there, you cannot provide it."""
        )
        
        # Compliance-focused prompt
        self.compliance_prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are a banking compliance expert analyzing uploaded compliance documents. You can ONLY use information from the provided documents.

CRITICAL RULES:
1. ONLY use compliance information that is explicitly stated in the provided context
2. If compliance requirements are not in the documents, say "This compliance information is not available in the uploaded documents"
3. DO NOT use any external compliance knowledge or regulatory standards
4. Quote specific text from the documents when possible
5. Always cite the source document

Compliance Context from uploaded documents:
{context}

Question: {question}

Remember: You can ONLY use information from the above context. If the information is not there, you cannot provide it."""
        )
    
    def generate_response(
        self, 
        question: str, 
        context: str,
        prompt_type: str = "banking"
    ) -> str:
        """Generate response using appropriate prompt"""
        try:
            if prompt_type == "table":
                prompt = self.table_prompt.format(
                    table_data=context,
                    question=question
                )
            elif prompt_type == "compliance":
                prompt = self.compliance_prompt.format(
                    context=context,
                    question=question
                )
            else:
                prompt = self.banking_prompt.format(
                    context=context,
                    question=question
                )
            
            # Generate response
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
            
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def generate_structured_response(
        self, 
        question: str, 
        context: str,
        response_format: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate structured response for specific banking queries"""
        try:
            # Create structured prompt
            structured_prompt = f"""Based on the following banking context, answer the question in the specified format.

            Context: {context}
            
            Question: {question}
            
            Required Format: {response_format}
            
            Please provide your response in the exact format specified above."""
            
            response = self.llm.invoke([HumanMessage(content=structured_prompt)])
            
            # Try to parse structured response
            try:
                import json
                return json.loads(response.content)
            except:
                return {"response": response.content, "format_error": True}
                
        except Exception as e:
            return {"error": str(e)}
    
    def validate_banking_response(self, response: str, context: str) -> Dict[str, Any]:
        """Validate banking response for accuracy and compliance"""
        try:
            validation_prompt = f"""Please validate the following banking response to ensure it ONLY uses information from the provided context.

Response to validate: {response}

Source context: {context}

CRITICAL VALIDATION RULES:
1. Check if the response ONLY uses information that appears in the source context
2. Identify any information that seems to come from external knowledge or general banking standards
3. Verify that all specific numbers, rates, and terms mentioned are in the source context
4. Check if the response properly cites sources when providing information

Please provide validation in the following format:
- Uses Only Provided Context: (yes/no)
- External Knowledge Detected: (yes/no - list any external information found)
- Accuracy: (high/medium/low)
- Source Attribution: (proper/improper/missing)
- Issues: (list any issues found)
- Recommendations: (suggestions for improvement)"""
            
            validation_response = self.llm.invoke([HumanMessage(content=validation_prompt)])
            
            return {
                "validation_response": validation_response.content,
                "original_response": response
            }
            
        except Exception as e:
            return {"error": f"Validation failed: {str(e)}"}
    
    def extract_key_information(self, text: str) -> Dict[str, Any]:
        """Extract key banking information from text"""
        try:
            extraction_prompt = f"""Extract key banking information from the following text:

            Text: {text}
            
            Please extract and organize the following information:
            - Loan terms and conditions
            - Interest rates and fees
            - Regulatory requirements
            - Compliance deadlines
            - Contact information
            - Important dates
            
            Format as a structured response."""
            
            response = self.llm.invoke([HumanMessage(content=extraction_prompt)])
            
            try:
                import json
                return json.loads(response.content)
            except:
                return {"extracted_info": response.content, "format_error": True}
                
        except Exception as e:
            return {"error": f"Extraction failed: {str(e)}"} 