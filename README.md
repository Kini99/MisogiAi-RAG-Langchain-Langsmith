# 🏦 Banking AI Assistant (LangChain + Chroma)

This project implements an **AI-powered Retrieval-Augmented Generation (RAG) assistant** for banks, capable of answering questions about **loan products, regulatory requirements, and internal policies**.  

It uses the **LangChain framework** for document processing, embeddings, retrieval, and orchestration, with **Chroma** as the local vector store.  

---

## 📌 Features

- **Document Processing**
  - Handles diverse banking documents: loan handbooks, compliance manuals, policy docs, and rate sheets  
  - Preprocessing and chunking using custom strategies to reduce table context loss  

- **Vector Search**
  - Uses **Chroma** for embedding storage and retrieval  
  - Optimized for handling cross-references and structured data  

- **RAG Pipeline**
  - Built on **LangChain RetrievalQA**  
  - Supports conversational context with memory  
  - Integrates custom LLM manager for flexible model usage  

- **Evaluation Datasets**
  - Includes test sets for loan products, compliance, and table cross-references  

- **Frontend Prototype**
  - Basic interface to interact with the assistant  
  - Launchable with `run_frontend.py`  

---

## 🗂 Project Structure

```
banking-assistant/
│── main.py                     # Entry point
│── example_usage.py             # Example usage script
│── requirements.txt             # Backend dependencies
│── frontend.py                  # Streamlit/Gradio frontend
│── run_frontend.py              # Run frontend server
│── FRONTEND_README.md           # Frontend setup instructions
│── Cost-Effective_RAG_Implementation_Guide.md
│── IMPLEMENTATION_SUMMARY.md
│── datasets/                    # Evaluation datasets
│── sample_documents/            # Example banking documents
│── chroma_db/                   # Local vector database
│── src/
│   ├── api.py                   # API endpoints
│   ├── banking_assistant.py     # Core RAG pipeline
│   ├── document_processor.py    # Document loading & chunking
│   ├── llm_manager.py           # LLM integration layer
│   └── config.py                # Configuration
```

---

## 🚀 Getting Started

### 1️⃣ Clone Repository
```bash
git clone https://github.com/your-username/banking-ai-assistant.git
cd banking-ai-assistant
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Setup Environment
- Copy `.env` or use `env_template.txt`  
- Add your API keys (e.g., OpenAI, HuggingFace)  

### 4️⃣ Run Backend
```bash
python main.py
```

### 5️⃣ Run Frontend
```bash
python run_frontend.py
```

---

## 📊 Cost Optimization

See **[Cost-Effective RAG Implementation Guide](./Cost-Effective_RAG_Implementation_Guide.md)** for detailed analysis of:  
- Premium setup (e.g., GPT-4 + Pinecone)  
- Optimized setup (e.g., Local LLM + Chroma)  
- Hybrid approaches with trade-offs & ROI  

---

## 📚 Resources

- [LangChain Documentation](https://docs.langchain.com/)  
- [Chroma Vector DB](https://www.trychroma.com/)  

---

## 🛠️ Future Improvements

- Enhanced table-aware chunking  
- Multi-modal document support (PDFs with images/diagrams)  
- Advanced evaluation with LangSmith  

---
