"""
Document processing module with custom chunking strategies for banking documents
"""
import os
import re
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime

from langchain_community.document_loaders import (
    UnstructuredFileLoader,
    PyPDFLoader,
    Docx2txtLoader,
    CSVLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.document_loaders.base import BaseLoader

from .config import settings


class BankingDocumentProcessor:
    """Custom document processor for banking documents with table-aware chunking"""
    
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
    def load_document(self, file_path: str) -> List[Document]:
        """Load document based on file type"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Document not found: {file_path}")
            
        file_extension = file_path.suffix.lower()
        
        try:
            if file_extension == '.pdf':
                loader = PyPDFLoader(str(file_path))
            elif file_extension == '.docx':
                loader = Docx2txtLoader(str(file_path))
            elif file_extension == '.csv':
                loader = CSVLoader(str(file_path))
            elif file_extension in ['.txt', '.md']:
                loader = UnstructuredFileLoader(str(file_path))
            else:
                # Try unstructured loader for other formats
                loader = UnstructuredFileLoader(str(file_path))
                
            documents = loader.load()
            return self._process_documents(documents, file_path)
            
        except Exception as e:
            raise Exception(f"Error loading document {file_path}: {str(e)}")
    
    def _process_documents(self, documents: List[Document], file_path: Path) -> List[Document]:
        """Process documents with table-aware chunking"""
        processed_docs = []
        upload_timestamp = datetime.now().isoformat()
        
        for doc in documents:
            # Extract table information
            table_data = self._extract_tables(doc.page_content)
            
            if table_data:
                # Handle documents with tables
                processed_docs.extend(self._chunk_with_tables(doc, table_data, file_path, upload_timestamp))
            else:
                # Handle regular text documents
                chunks = self.text_splitter.split_text(doc.page_content)
                for i, chunk in enumerate(chunks):
                    processed_docs.append(Document(
                        page_content=chunk,
                        metadata={
                            **doc.metadata,
                            'chunk_id': i,
                            'file_path': str(file_path),
                            'file_name': file_path.name,
                            'content_type': 'text',
                            'upload_date': upload_timestamp,
                            'total_chunks': len(chunks)
                        }
                    ))
        
        return processed_docs
    
    def _extract_tables(self, content: str) -> List[Dict[str, Any]]:
        """Extract table information from content"""
        tables = []
        
        # Pattern to identify table-like structures
        table_patterns = [
            r'(\|[^\n]*\|[^\n]*\n)+',  # Markdown tables
            r'(\s+\w+\s+\w+\s+\w+\s*\n)+',  # Space-separated tables
            r'(Table\s+\d+\.?\d*[^\n]*\n.*?)(?=\n\n|\n[A-Z]|\Z)',  # Table references
        ]
        
        for pattern in table_patterns:
            matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)
            for match in matches:
                table_text = match.group(0)
                tables.append({
                    'text': table_text,
                    'start_pos': match.start(),
                    'end_pos': match.end(),
                    'type': 'structured_table'
                })
        
        return tables
    
    def _chunk_with_tables(self, doc: Document, tables: List[Dict[str, Any]], file_path: Path, upload_timestamp: str) -> List[Document]:
        """Chunk documents while preserving table context"""
        content = doc.page_content
        chunks = []
        
        # Sort tables by position
        tables.sort(key=lambda x: x['start_pos'])
        
        current_pos = 0
        for table in tables:
            # Add text before table
            if table['start_pos'] > current_pos:
                pre_table_text = content[current_pos:table['start_pos']].strip()
                if pre_table_text:
                    pre_chunks = self.text_splitter.split_text(pre_table_text)
                    for i, chunk in enumerate(pre_chunks):
                        chunks.append(Document(
                            page_content=chunk,
                            metadata={
                                **doc.metadata,
                                'chunk_id': len(chunks),
                                'file_path': str(file_path),
                                'file_name': file_path.name,
                                'content_type': 'text',
                                'upload_date': upload_timestamp
                            }
                        ))
            
            # Add table as a single chunk to preserve structure
            chunks.append(Document(
                page_content=table['text'],
                metadata={
                    **doc.metadata,
                    'chunk_id': len(chunks),
                    'file_path': str(file_path),
                    'file_name': file_path.name,
                    'content_type': 'table',
                    'table_id': f"table_{len(chunks)}",
                    'upload_date': upload_timestamp
                }
            ))
            
            current_pos = table['end_pos']
        
        # Add remaining text after last table
        if current_pos < len(content):
            remaining_text = content[current_pos:].strip()
            if remaining_text:
                remaining_chunks = self.text_splitter.split_text(remaining_text)
                for i, chunk in enumerate(remaining_chunks):
                    chunks.append(Document(
                        page_content=chunk,
                        metadata={
                            **doc.metadata,
                            'chunk_id': len(chunks),
                            'file_path': str(file_path),
                            'file_name': file_path.name,
                            'content_type': 'text',
                            'upload_date': upload_timestamp
                        }
                    ))
        
        return chunks
    
    def load_documents_from_directory(self, directory_path: str) -> List[Document]:
        """Load all documents from a directory"""
        directory = Path(directory_path)
        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        
        all_documents = []
        supported_extensions = {'.pdf', '.docx', '.csv', '.txt', '.md'}
        
        for file_path in directory.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                try:
                    documents = self.load_document(str(file_path))
                    all_documents.extend(documents)
                except Exception as e:
                    print(f"Warning: Could not load {file_path}: {e}")
        
        return all_documents 