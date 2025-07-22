"""
Vector store management using ChromaDB for banking documents
"""
import os
from typing import List, Dict, Any, Optional
from pathlib import Path

import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

from .config import settings


class BankingVectorStore:
    """Vector store manager for banking documents using ChromaDB"""
    
    def __init__(self):
        self.persist_directory = settings.CHROMA_PERSIST_DIRECTORY
        self.collection_name = settings.CHROMA_COLLECTION_NAME
        
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=ChromaSettings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Initialize vector store
        self.vector_store = None
        self._initialize_vector_store()
    
    def _initialize_vector_store(self):
        """Initialize the vector store"""
        try:
            # Check if collection exists
            collections = self.client.list_collections()
            collection_exists = any(col.name == self.collection_name for col in collections)
            
            if collection_exists:
                # Load existing collection
                self.vector_store = Chroma(
                    client=self.client,
                    collection_name=self.collection_name,
                    embedding_function=self.embeddings
                )
            else:
                # Create new collection
                self.vector_store = Chroma(
                    client=self.client,
                    collection_name=self.collection_name,
                    embedding_function=self.embeddings,
                    persist_directory=self.persist_directory
                )
                
        except Exception as e:
            raise Exception(f"Failed to initialize vector store: {str(e)}")
    
    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the vector store"""
        if not documents:
            return
            
        try:
            # Add documents to vector store
            self.vector_store.add_documents(documents)
            
            # Persist changes
            self.vector_store.persist()
            
            print(f"Successfully added {len(documents)} documents to vector store")
            
        except Exception as e:
            raise Exception(f"Failed to add documents to vector store: {str(e)}")
    
    def similarity_search(
        self, 
        query: str, 
        k: int = 4,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """Perform similarity search"""
        try:
            results = self.vector_store.similarity_search(
                query=query,
                k=k,
                filter=filter_dict
            )
            return results
        except Exception as e:
            raise Exception(f"Failed to perform similarity search: {str(e)}")
    
    def similarity_search_with_score(
        self, 
        query: str, 
        k: int = 4,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[tuple[Document, float]]:
        """Perform similarity search with scores"""
        try:
            results = self.vector_store.similarity_search_with_score(
                query=query,
                k=k,
                filter=filter_dict
            )
            return results
        except Exception as e:
            raise Exception(f"Failed to perform similarity search with score: {str(e)}")
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get collection statistics"""
        try:
            collection = self.client.get_collection(self.collection_name)
            count = collection.count()
            
            return {
                'collection_name': self.collection_name,
                'document_count': count,
                'persist_directory': self.persist_directory
            }
        except Exception as e:
            raise Exception(f"Failed to get collection stats: {str(e)}")
    
    def delete_collection(self) -> None:
        """Delete the entire collection"""
        try:
            self.client.delete_collection(self.collection_name)
            self.vector_store = None
            print(f"Collection '{self.collection_name}' deleted successfully")
        except Exception as e:
            raise Exception(f"Failed to delete collection: {str(e)}")
    
    def reset_vector_store(self) -> None:
        """Reset the vector store (delete and recreate)"""
        try:
            self.delete_collection()
            self._initialize_vector_store()
            print("Vector store reset successfully")
        except Exception as e:
            raise Exception(f"Failed to reset vector store: {str(e)}")
    
    def search_by_metadata(
        self, 
        metadata_filter: Dict[str, Any], 
        k: int = 10
    ) -> List[Document]:
        """Search documents by metadata"""
        try:
            results = self.vector_store.get(
                where=metadata_filter,
                limit=k
            )
            return results
        except Exception as e:
            raise Exception(f"Failed to search by metadata: {str(e)}") 
    
    def get_all_documents(self, limit: int = 1000) -> List[Document]:
        """Get all documents from the vector store"""
        try:
            # Get all documents from the collection
            results = self.vector_store.get()
            documents = []
            
            for i, (content, metadata) in enumerate(zip(results['documents'], results['metadatas'])):
                if i >= limit:
                    break
                documents.append(Document(
                    page_content=content,
                    metadata=metadata
                ))
            
            return documents
        except Exception as e:
            raise Exception(f"Failed to get all documents: {str(e)}")
    
    def delete_documents_by_source(self, source_path: str) -> None:
        """Delete documents by source file path"""
        try:
            # Get all documents
            all_docs = self.get_all_documents()
            
            # Find documents to delete
            docs_to_delete = []
            for doc in all_docs:
                if doc.metadata.get('file_path') == source_path:
                    docs_to_delete.append(doc)
            
            if docs_to_delete:
                # Delete documents from collection
                # Note: This is a simplified approach. In production, you might want to use document IDs
                self.vector_store.delete(documents=docs_to_delete)
                print(f"Deleted {len(docs_to_delete)} chunks from {source_path}")
            else:
                print(f"No documents found for source: {source_path}")
                
        except Exception as e:
            raise Exception(f"Failed to delete documents by source: {str(e)}") 