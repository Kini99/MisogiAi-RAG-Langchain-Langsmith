"""
Streamlit Frontend for Banking AI Assistant
"""
import streamlit as st
import requests
import json
import os
from pathlib import Path
from typing import List, Dict, Any
import time

# Configuration
API_BASE_URL = "http://localhost:8000"

def check_api_health():
    """Check if the API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200, response.json()
    except requests.exceptions.RequestException:
        return False, None

def upload_document(file):
    """Upload a document to the API"""
    try:
        files = {"file": file}
        response = requests.post(f"{API_BASE_URL}/upload-document", files=files)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"success": False, "message": f"Upload failed: {str(e)}"}

def ask_question(question, conversation_history=None):
    """Ask a question to the API"""
    try:
        data = {"question": question}
        if conversation_history:
            data["conversation_history"] = conversation_history
        
        response = requests.post(f"{API_BASE_URL}/ask", json=data)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"success": False, "answer": f"Request failed: {str(e)}"}

def get_loan_information(loan_type=None):
    """Get loan information from the API"""
    try:
        data = {}
        if loan_type:
            data["loan_type"] = loan_type
        
        response = requests.post(f"{API_BASE_URL}/loan-information", json=data)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Request failed: {str(e)}"}

def get_compliance_requirements(regulation_type=None):
    """Get compliance requirements from the API"""
    try:
        data = {}
        if regulation_type:
            data["regulation_type"] = regulation_type
        
        response = requests.post(f"{API_BASE_URL}/compliance-requirements", json=data)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Request failed: {str(e)}"}

def search_documents(query, k=5):
    """Search documents in the knowledge base"""
    try:
        data = {"query": query, "k": k}
        response = requests.post(f"{API_BASE_URL}/search-documents", json=data)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Request failed: {str(e)}"}

def get_stats():
    """Get knowledge base statistics"""
    try:
        response = requests.get(f"{API_BASE_URL}/stats")
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Request failed: {str(e)}"}

def clear_conversation():
    """Clear conversation history"""
    try:
        response = requests.post(f"{API_BASE_URL}/clear-conversation")
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Request failed: {str(e)}"}

def reset_knowledge_base():
    """Reset the knowledge base"""
    try:
        response = requests.post(f"{API_BASE_URL}/reset-knowledge-base")
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Request failed: {str(e)}"}

def get_documents():
    """Get list of all documents in the knowledge base"""
    try:
        response = requests.get(f"{API_BASE_URL}/documents")
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Request failed: {str(e)}"}

def delete_document(document_id: str):
    """Delete a document from the knowledge base"""
    try:
        response = requests.delete(f"{API_BASE_URL}/documents/{document_id}")
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Request failed: {str(e)}"}

def load_sample_documents():
    """Load sample documents into the knowledge base"""
    try:
        response = requests.post(f"{API_BASE_URL}/load-sample-documents")
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Request failed: {str(e)}"}

def main():
    st.set_page_config(
        page_title="Banking AI Assistant",
        page_icon="🏦",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .status-success {
        color: #28a745;
        font-weight: bold;
    }
    .status-error {
        color: #dc3545;
        font-weight: bold;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">🏦 Banking AI Assistant</h1>', unsafe_allow_html=True)
    
    # Check API health
    api_healthy, health_data = check_api_health()
    
    if not api_healthy:
        st.error("❌ Cannot connect to the Banking Assistant API. Please make sure the backend is running on http://localhost:8000")
        st.info("To start the backend, run: `python main.py` from the project directory")
        return
    
    # Sidebar for navigation and controls
    with st.sidebar:
        st.header("🔧 Controls")
        
        # Health status
        if api_healthy:
            st.success("✅ API Connected")
            if health_data:
                st.info(f"📊 Knowledge Base: {health_data.get('knowledge_base', {}).get('document_count', 0)} documents")
        else:
            st.error("❌ API Disconnected")
        
        st.divider()
        
        # Document upload
        st.subheader("📄 Upload Documents")
        uploaded_file = st.file_uploader(
            "Choose a document",
            type=['txt', 'pdf', 'docx', 'xlsx', 'csv'],
            help="Upload banking documents to the knowledge base"
        )
        
        if uploaded_file is not None:
            if st.button("Upload Document"):
                with st.spinner("Uploading document..."):
                    result = upload_document(uploaded_file)
                    if result.get("success"):
                        st.success(f"✅ {result.get('message')}")
                        st.info(f"📊 Total documents: {result.get('document_count')}")
                    else:
                        st.error(f"❌ {result.get('message')}")
        
        st.divider()
        
        # Knowledge base management
        st.subheader("🗄️ Knowledge Base")
        
        # Load sample documents button
        if st.button("📚 Load Sample Documents"):
            with st.spinner("Loading sample documents..."):
                result = load_sample_documents()
                if result.get("success"):
                    st.success(f"✅ {result.get('message')}")
                    st.info(f"📊 Documents loaded: {result.get('document_count')}")
                else:
                    st.error(f"❌ {result.get('error')}")
        
        # Document management
        st.subheader("📋 Document Management")
        
        # Get and display documents
        with st.spinner("Loading documents..."):
            docs_result = get_documents()
        
        if docs_result.get("success"):
            documents = docs_result.get("documents", [])
            total_docs = docs_result.get("total_documents", 0)
            total_chunks = docs_result.get("total_chunks", 0)
            
            st.info(f"📊 Total Documents: {total_docs} | Total Chunks: {total_chunks}")
            
            if documents:
                for doc in documents:
                    with st.expander(f"📄 {doc.get('file_name', doc.get('file_path', 'Unknown'))}"):
                        st.write(f"**File:** {doc.get('file_path', 'Unknown')}")
                        st.write(f"**Chunks:** {doc.get('chunk_count', 0)}")
                        st.write(f"**Content Types:** {', '.join(doc.get('content_types', []))}")
                        st.write(f"**Upload Date:** {doc.get('upload_date', 'Unknown')}")
                        
                        # Delete button
                        if st.button(f"🗑️ Delete", key=f"delete_{doc.get('file_path', 'unknown')}"):
                            with st.spinner("Deleting document..."):
                                delete_result = delete_document(doc.get('file_path', ''))
                                if delete_result.get("success"):
                                    st.success("✅ Document deleted successfully")
                                    st.rerun()
                                else:
                                    st.error(f"❌ {delete_result.get('error')}")
            else:
                st.info("📭 No documents in knowledge base")
        else:
            st.error(f"❌ {docs_result.get('error')}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 Get Stats"):
                with st.spinner("Fetching statistics..."):
                    stats = get_stats()
                    if stats.get("success"):
                        st.json(stats)
                    else:
                        st.error(f"❌ {stats.get('error')}")
        
        with col2:
            if st.button("🗑️ Reset KB"):
                if st.checkbox("Confirm reset"):
                    with st.spinner("Resetting knowledge base..."):
                        result = reset_knowledge_base()
                        if result.get("success"):
                            st.success("✅ Knowledge base reset successfully")
                        else:
                            st.error(f"❌ {result.get('error')}")
        
        st.divider()
        
        # Quick actions
        st.subheader("⚡ Quick Actions")
        
        if st.button("🗣️ Clear Chat"):
            with st.spinner("Clearing conversation..."):
                result = clear_conversation()
                if result.get("success"):
                    st.success("✅ Conversation cleared")
                    st.rerun()
                else:
                    st.error(f"❌ {result.get('error')}")
    
    # Main content area
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["💬 Chat", "💰 Loan Info", "📋 Compliance", "🔍 Search", "📄 Documents"])
    
    # Initialize session state for conversation
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Tab 1: Chat Interface
    with tab1:
        st.header("💬 Chat with Banking Assistant")
        
        # Display conversation history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask me about banking, loans, compliance, or any banking-related questions..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get assistant response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    # Prepare conversation history for API
                    conversation_history = []
                    for msg in st.session_state.messages[:-1]:  # Exclude current message
                        if msg["role"] == "user":
                            conversation_history.append({"role": "user", "content": msg["content"]})
                        elif msg["role"] == "assistant":
                            conversation_history.append({"role": "assistant", "content": msg["content"]})
                    
                    response = ask_question(prompt, conversation_history)
                    
                    if response.get("success"):
                        answer = response.get("answer", "No answer provided")
                        st.markdown(answer)
                        
                        # Display sources if available
                        sources = response.get("sources", [])
                        if sources:
                            with st.expander("📚 Sources"):
                                for i, source in enumerate(sources, 1):
                                    st.markdown(f"**Source {i}:** {source.get('title', 'Unknown')}")
                                    st.markdown(f"**Content:** {source.get('content', 'No content')[:200]}...")
                        
                        # Display confidence if available
                        confidence = response.get("confidence")
                        if confidence:
                            st.info(f"🎯 Confidence: {confidence}")
                        
                        # Add assistant response to chat history
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    else:
                        error_msg = response.get("answer", "An error occurred")
                        st.error(f"❌ {error_msg}")
    
    # Tab 2: Loan Information
    with tab2:
        st.header("💰 Loan Information")
        
        loan_type = st.selectbox(
            "Select Loan Type",
            ["", "Personal Loan", "Home Loan", "Business Loan", "Auto Loan", "Student Loan"],
            help="Select a specific loan type or leave empty for general information"
        )
        
        if st.button("Get Loan Information"):
            with st.spinner("Fetching loan information..."):
                result = get_loan_information(loan_type if loan_type else None)
                
                if result.get("success"):
                    loan_info = result.get("loan_information", {})
                    
                    # Display loan information in a structured way
                    if loan_info:
                        for category, details in loan_info.items():
                            with st.expander(f"📋 {category}"):
                                if isinstance(details, dict):
                                    for key, value in details.items():
                                        st.markdown(f"**{key}:** {value}")
                                elif isinstance(details, list):
                                    for item in details:
                                        st.markdown(f"• {item}")
                                else:
                                    st.markdown(details)
                    else:
                        st.info("No specific loan information found. Try asking a question in the chat tab.")
                else:
                    st.error(f"❌ {result.get('error', 'Failed to fetch loan information')}")
    
    # Tab 3: Compliance Requirements
    with tab3:
        st.header("📋 Compliance Requirements")
        
        regulation_type = st.selectbox(
            "Select Regulation Type",
            ["", "KYC", "AML", "GDPR", "SOX", "Basel III", "Dodd-Frank"],
            help="Select a specific regulation type or leave empty for general compliance information"
        )
        
        if st.button("Get Compliance Requirements"):
            with st.spinner("Fetching compliance requirements..."):
                result = get_compliance_requirements(regulation_type if regulation_type else None)
                
                if result.get("success"):
                    compliance_info = result.get("compliance_requirements", {})
                    
                    # Display compliance information
                    if compliance_info:
                        for category, details in compliance_info.items():
                            with st.expander(f"📋 {category}"):
                                if isinstance(details, dict):
                                    for key, value in details.items():
                                        st.markdown(f"**{key}:** {value}")
                                elif isinstance(details, list):
                                    for item in details:
                                        st.markdown(f"• {item}")
                                else:
                                    st.markdown(details)
                    else:
                        st.info("No specific compliance information found. Try asking a question in the chat tab.")
                else:
                    st.error(f"❌ {result.get('error', 'Failed to fetch compliance requirements')}")
    
    # Tab 4: Document Search
    with tab4:
        st.header("🔍 Search Documents")
        
        search_query = st.text_input(
            "Enter search query",
            placeholder="Search for specific information in uploaded documents..."
        )
        
        k_results = st.slider("Number of results", min_value=1, max_value=20, value=5)
        
        if st.button("Search Documents"):
            if search_query.strip():
                with st.spinner("Searching documents..."):
                    result = search_documents(search_query, k_results)
                    
                    if result.get("success"):
                        documents = result.get("documents", [])
                        
                        if documents:
                            st.success(f"Found {len(documents)} relevant documents")
                            
                            for i, doc in enumerate(documents, 1):
                                with st.expander(f"📄 Document {i}: {doc.get('title', 'Untitled')}"):
                                    st.markdown(f"**Source:** {doc.get('source', 'Unknown')}")
                                    st.markdown(f"**Score:** {doc.get('score', 'N/A')}")
                                    st.markdown("**Content:**")
                                    st.markdown(doc.get('content', 'No content available'))
                        else:
                            st.info("No relevant documents found for your search query.")
                    else:
                        st.error(f"❌ {result.get('error', 'Search failed')}")
            else:
                st.warning("Please enter a search query.")
    
    # Tab 5: Document Management
    with tab5:
        st.header("📄 Document Management")
        
        # Document upload section
        st.subheader("📤 Upload New Documents")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded_file = st.file_uploader(
                "Choose a document to upload",
                type=['txt', 'pdf', 'docx', 'xlsx', 'csv'],
                help="Upload banking documents to the knowledge base"
            )
        
        with col2:
            if uploaded_file is not None:
                if st.button("Upload Document", type="primary"):
                    with st.spinner("Uploading and processing document..."):
                        result = upload_document(uploaded_file)
                        if result.get("success"):
                            st.success(f"✅ {result.get('message')}")
                            st.info(f"📊 Total documents: {result.get('document_count')}")
                            st.rerun()
                        else:
                            st.error(f"❌ {result.get('message')}")
        
        st.divider()
        
        # Document status and management
        st.subheader("📋 Knowledge Base Status")
        
        # Get documents list
        with st.spinner("Loading document information..."):
            docs_result = get_documents()
        
        if docs_result.get("success"):
            documents = docs_result.get("documents", [])
            total_docs = docs_result.get("total_documents", 0)
            total_chunks = docs_result.get("total_chunks", 0)
            
            # Status overview
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Documents", total_docs)
            with col2:
                st.metric("Total Chunks", total_chunks)
            with col3:
                if total_docs > 0:
                    st.metric("Avg Chunks/Doc", round(total_chunks / total_docs, 1))
                else:
                    st.metric("Avg Chunks/Doc", 0)
            
            if documents:
                st.subheader("📚 Uploaded Documents")
                
                for i, doc in enumerate(documents):
                    with st.expander(f"📄 {doc.get('file_name', doc.get('file_path', 'Unknown'))} ({doc.get('chunk_count', 0)} chunks)"):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.write(f"**File Path:** {doc.get('file_path', 'Unknown')}")
                            st.write(f"**Chunks:** {doc.get('chunk_count', 0)}")
                            st.write(f"**Content Types:** {', '.join(doc.get('content_types', []))}")
                            st.write(f"**Upload Date:** {doc.get('upload_date', 'Unknown')}")
                        
                        with col2:
                            if st.button(f"🗑️ Delete", key=f"delete_tab_{i}"):
                                with st.spinner("Deleting document..."):
                                    delete_result = delete_document(doc.get('file_path', ''))
                                    if delete_result.get("success"):
                                        st.success("✅ Document deleted successfully")
                                        st.rerun()
                                    else:
                                        st.error(f"❌ {delete_result.get('error')}")
            else:
                st.info("📭 No documents in knowledge base")
                st.info("💡 Upload documents or load sample documents to get started!")
                
                # Load sample documents option
                if st.button("📚 Load Sample Documents"):
                    with st.spinner("Loading sample documents..."):
                        result = load_sample_documents()
                        if result.get("success"):
                            st.success(f"✅ {result.get('message')}")
                            st.info(f"📊 Documents loaded: {result.get('document_count')}")
                            st.rerun()
                        else:
                            st.error(f"❌ {result.get('error')}")
        else:
            st.error(f"❌ {docs_result.get('error')}")
        
        st.divider()
        
        # Knowledge base actions
        st.subheader("⚙️ Knowledge Base Actions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Get Statistics"):
                with st.spinner("Fetching statistics..."):
                    stats = get_stats()
                    if stats.get("success"):
                        st.json(stats)
                    else:
                        st.error(f"❌ {stats.get('error')}")
        
        with col2:
            if st.button("🗣️ Clear Chat History"):
                with st.spinner("Clearing conversation..."):
                    result = clear_conversation()
                    if result.get("success"):
                        st.success("✅ Conversation cleared")
                    else:
                        st.error(f"❌ {result.get('error')}")
        
        with col3:
            if st.button("🗑️ Reset Knowledge Base", type="secondary"):
                if st.checkbox("Confirm reset - this will delete ALL documents"):
                    with st.spinner("Resetting knowledge base..."):
                        result = reset_knowledge_base()
                        if result.get("success"):
                            st.success("✅ Knowledge base reset successfully")
                            st.rerun()
                        else:
                            st.error(f"❌ {result.get('error')}")

if __name__ == "__main__":
    main() 