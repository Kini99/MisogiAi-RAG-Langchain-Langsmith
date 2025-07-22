"""
Configuration settings for the Banking AI Assistant
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Google AI Settings
    GOOGLE_API_KEY: str = ""
    
    # Vector Database Settings
    CHROMA_PERSIST_DIRECTORY: str = "./chroma_db"
    CHROMA_COLLECTION_NAME: str = "banking_documents"
    
    # Document Processing Settings
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    MAX_CHUNKS_PER_DOCUMENT: int = 100
    
    # LLM Settings
    MODEL_NAME: str = "gemini-2.0-flash-exp"
    TEMPERATURE: float = 0.1
    MAX_TOKENS: int = 4000
    
    # Embedding Settings
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings() 