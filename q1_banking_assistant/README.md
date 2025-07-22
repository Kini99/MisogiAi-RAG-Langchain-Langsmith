# Banking AI Assistant - LangChain RAG Implementation

A comprehensive AI-powered banking assistant that answers questions about loan products, regulatory requirements, and internal policies using Retrieval-Augmented Generation (RAG) with LangChain framework.

## 🏦 Overview

This banking assistant leverages advanced AI technologies to provide accurate, compliant, and helpful responses based on banking documents. It addresses key RAG challenges including table context preservation, cross-reference handling, and compliance risk mitigation.

## ✨ Key Features

- **Table-Aware Document Processing**: Custom chunking strategies that preserve table relationships
- **Multi-Format Document Support**: PDF, DOCX, CSV, TXT, and Markdown files
- **Compliance-Focused Responses**: Banking-specific prompts ensuring regulatory accuracy
- **Conversational Memory**: Maintains context across multiple interactions
- **Structured Data Extraction**: Specialized queries for loan and compliance information
- **Cost-Effective Implementation**: Optimized for enterprise use with detailed cost analysis
- **Web API Interface**: FastAPI-based REST API with comprehensive documentation

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Document      │    │   Vector        │    │   LLM           │
│   Processor     │───▶│   Store         │───▶│   Manager       │
│                 │    │   (ChromaDB)    │    │   (Gemini)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Custom        │    │   Retrieval     │    │   FastAPI       │
│   Chunking      │    │   Chain         │    │   Web API       │
│   Strategy      │    │   (RAG)         │    │   Interface     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Google AI API Key (for Gemini model)
- 8GB+ RAM (for local processing)
- Optional: GPU for enhanced performance

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd q1_banking_assistant
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file
   echo "GOOGLE_API_KEY=your_api_key_here" > .env
   ```
   
   Get your Google AI API key from: https://makersuite.google.com/app/apikey

5. **Run the example**
   ```bash
   python example_usage.py
   ```

6. **Start the web server**
   ```bash
   python main.py
   ```

## 📚 Usage Examples

### Basic Usage

```python
from src.banking_assistant import BankingAssistant

# Initialize assistant
assistant = BankingAssistant()

# Load documents
result = assistant.load_documents("path/to/banking/documents")
print(f"Loaded {result['document_count']} document chunks")

# Ask questions
response = assistant.ask_question("What are the interest rates for personal loans?")
print(response['answer'])
```

### Conversational Queries

```python
# Ask with conversation history
conversation_history = [
    {"question": "What loan products do you offer?", "answer": "We offer personal, mortgage, and business loans..."},
    {"question": "What are the requirements for personal loans?", "answer": "Good credit score (650+), stable income..."}
]

response = assistant.conversational_ask(
    "What are the interest rates for these loans?",
    conversation_history
)
```

### Structured Queries

```python
# Get loan information in structured format
loan_info = assistant.get_loan_information("personal")
print(loan_info['data'])

# Get compliance requirements
compliance = assistant.get_compliance_requirements("AML")
print(compliance['data'])
```

## 🌐 Web API

The assistant provides a comprehensive REST API:

### Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /upload-document` - Upload single document
- `POST /upload-directory` - Upload all documents from directory
- `POST /ask` - Ask a question
- `POST /loan-information` - Get structured loan information
- `POST /compliance-requirements` - Get compliance requirements
- `POST /search-documents` - Search documents
- `GET /stats` - Get knowledge base statistics
- `POST /clear-conversation` - Clear conversation history
- `POST /reset-knowledge-base` - Reset entire knowledge base

### API Documentation

Once the server is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

### Example API Usage

```bash
# Upload a document
curl -X POST "http://localhost:8000/upload-document" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@loan_handbook.pdf"

# Ask a question
curl -X POST "http://localhost:8000/ask" \
     -H "accept: application/json" \
     -H "Content-Type: application/json" \
     -d '{"question": "What are the interest rates for personal loans?"}'
```

## 🖥️ Web Frontend

A modern Streamlit-based frontend is available for easy interaction with the banking assistant.

### Features

- **Interactive Chat Interface**: Natural conversation with the assistant
- **Document Upload**: Easy drag-and-drop document upload
- **Loan Information**: Structured access to loan products
- **Compliance Requirements**: Quick access to regulatory information
- **Document Search**: Search through uploaded documents
- **Knowledge Base Management**: View stats and manage documents

### Quick Start

1. **Install frontend dependencies:**
   ```bash
   pip install -r frontend_requirements.txt
   ```

2. **Start the frontend:**
   ```bash
   python run_frontend.py
   ```
   
   Or use the convenience scripts:
   - Windows: `start_frontend.bat`
   - Unix/Linux/Mac: `./start_frontend.sh`

3. **Access the application:**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000

### Frontend Usage

- **Chat Tab**: Ask questions and view conversation history
- **Loan Info Tab**: Browse loan products and requirements
- **Compliance Tab**: Access regulatory requirements
- **Search Tab**: Search through uploaded documents
- **Sidebar**: Upload documents, view stats, and manage the knowledge base

For detailed frontend documentation, see: [FRONTEND_README.md](FRONTEND_README.md)

## 📊 Cost Analysis

This implementation includes a comprehensive cost analysis document: `Cost-Effective_RAG_Implementation_Guide.md`

### Key Cost Optimizations

1. **Local LLM Support**: Use Ollama with open-source models
2. **Self-Hosted Vector Database**: ChromaDB eliminates hosting fees
3. **Embedding Caching**: Reduces redundant computations
4. **Batch Processing**: Offline document processing
5. **Tiered LLM Strategy**: Route queries to appropriate models

### Cost Comparison (1,000 daily queries)

| Setup Type | Monthly Cost | Annual Cost | ROI |
|------------|--------------|-------------|-----|
| Premium (GPT-4 + Pinecone) | $650 | $7,800 | 626% |
| Optimized (Local + ChromaDB) | $175 | $2,100 | 2,598% |
| Hybrid (Mixed approach) | $130 | $1,560 | 3,531% |

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Required
GOOGLE_API_KEY=your_google_api_key_here

# Optional (with defaults)
CHROMA_PERSIST_DIRECTORY=./chroma_db
CHROMA_COLLECTION_NAME=banking_documents
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
MODEL_NAME=gemini-2.0-flash-exp
TEMPERATURE=0.1
MAX_TOKENS=4000
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false
```

### Customization

#### Document Processing
```python
# Custom chunking strategy
from src.document_processor import BankingDocumentProcessor

processor = BankingDocumentProcessor()
# Modify chunk_size and chunk_overlap in config.py
```

#### Vector Store
```python
# Custom embedding model
from src.vector_store import BankingVectorStore

# Change embedding model in config.py
# EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"
```

#### LLM Configuration
```python
# Use different LLM
from src.llm_manager import BankingLLMManager

# Change model in config.py
# MODEL_NAME = "gemini-1.5-pro"
```

## 📁 Project Structure

```
q1_banking_assistant/
├── src/
│   ├── __init__.py
│   ├── config.py              # Configuration settings
│   ├── document_processor.py  # Document loading and chunking
│   ├── vector_store.py        # ChromaDB vector store management
│   ├── llm_manager.py         # Google Gemini LLM integration
│   ├── retrieval_chain.py     # RAG chain implementation
│   ├── banking_assistant.py   # Main assistant class
│   └── api.py                 # FastAPI web application
├── main.py                    # Application entry point
├── example_usage.py           # Usage examples
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
└── Cost-Effective_RAG_Implementation_Guide.md  # Cost analysis
```

## 🧪 Testing

### Run Example Usage
```bash
python example_usage.py
```

### Test API Endpoints
```bash
# Start server
python main.py

# Test health endpoint
curl http://localhost:8000/health

# Test question endpoint
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "What loan products are available?"}'
```

## 🔒 Security Considerations

1. **API Key Management**: Store API keys securely in environment variables
2. **Document Privacy**: All processing is done locally by default
3. **Access Control**: Implement authentication for production use
4. **Data Encryption**: Enable HTTPS for production deployments
5. **Audit Logging**: Monitor all queries and responses

## 🚀 Deployment

### Local Development
```bash
python main.py
```

### Production Deployment

1. **Using Docker** (recommended)
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["python", "main.py"]
   ```

2. **Using Gunicorn**
   ```bash
   pip install gunicorn
   gunicorn src.api:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

3. **Using Systemd Service**
   ```ini
   [Unit]
   Description=Banking AI Assistant
   After=network.target

   [Service]
   Type=simple
   User=banking-assistant
   WorkingDirectory=/opt/banking-assistant
   Environment=PATH=/opt/banking-assistant/venv/bin
   ExecStart=/opt/banking-assistant/venv/bin/python main.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

## 📈 Performance Optimization

### For High Volume Usage

1. **Increase Chunk Size**: Modify `CHUNK_SIZE` in config
2. **Use GPU**: Install CUDA-enabled PyTorch
3. **Enable Caching**: Implement Redis for response caching
4. **Load Balancing**: Use multiple server instances
5. **Database Optimization**: Tune ChromaDB settings

### Monitoring

```python
# Get performance stats
stats = assistant.get_knowledge_base_stats()
print(f"Documents: {stats['stats']['document_count']}")
print(f"Collection: {stats['stats']['collection_name']}")
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Common Issues

1. **API Key Error**: Ensure `GOOGLE_API_KEY` is set in environment
2. **Memory Issues**: Reduce `CHUNK_SIZE` or use smaller documents
3. **Slow Performance**: Enable GPU support or use smaller models
4. **Import Errors**: Ensure all dependencies are installed

### Getting Help

- Check the example usage: `python example_usage.py`
- Review API documentation: http://localhost:8000/docs
- Check the cost analysis guide for optimization tips
- Open an issue for bugs or feature requests

## 🎯 Roadmap

- [ ] Multi-language support
- [ ] Advanced table parsing
- [ ] Real-time document updates
- [ ] Integration with banking systems
- [ ] Advanced analytics dashboard
- [ ] Mobile application
- [ ] Voice interface
- [ ] Multi-modal document support

## 🙏 Acknowledgments

- LangChain team for the excellent framework
- Google AI for Gemini models
- ChromaDB team for the vector database
- FastAPI team for the web framework
- The open-source community for various dependencies

---

**Built with ❤️ for the banking industry**