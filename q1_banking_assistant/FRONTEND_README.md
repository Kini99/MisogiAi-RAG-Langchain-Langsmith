# Banking Assistant Frontend

A modern Streamlit-based frontend for the Banking AI Assistant that provides an intuitive interface for interacting with the banking knowledge base.

## Features

### 🎯 Core Features
- **Interactive Chat Interface**: Natural conversation with the banking assistant
- **Document Upload**: Easy upload of banking documents to the knowledge base
- **Loan Information**: Structured access to loan product information
- **Compliance Requirements**: Quick access to regulatory compliance information
- **Document Search**: Search through uploaded documents
- **Knowledge Base Management**: View stats and manage the knowledge base

### 🎨 User Interface
- **Modern Design**: Clean, professional banking interface
- **Responsive Layout**: Works on desktop and mobile devices
- **Real-time Updates**: Live status indicators and progress tracking
- **Tabbed Interface**: Organized sections for different functionalities

## Quick Start

### Prerequisites
1. Make sure the backend is running (see main README.md)
2. Install frontend dependencies

### Installation

1. **Install frontend dependencies:**
   ```bash
   pip install -r frontend_requirements.txt
   ```

2. **Start the frontend:**
   ```bash
   python run_frontend.py
   ```

   Or run Streamlit directly:
   ```bash
   streamlit run frontend.py
   ```

3. **Access the application:**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000

## Usage Guide

### 💬 Chat Interface
- Ask natural language questions about banking topics
- View conversation history
- See source documents and confidence scores
- Clear conversation history when needed

### 📄 Document Management
- Upload documents (PDF, DOCX, TXT, XLSX, CSV)
- View knowledge base statistics
- Reset knowledge base if needed

### 💰 Loan Information
- Browse different loan types
- Get structured loan information
- View terms, rates, and requirements

### 📋 Compliance
- Access regulatory requirements
- Browse different compliance frameworks
- Get structured compliance information

### 🔍 Document Search
- Search through uploaded documents
- Adjust number of results
- View document relevance scores

## API Integration

The frontend integrates with all existing FastAPI endpoints:

- `GET /health` - Health check
- `POST /upload-document` - Document upload
- `POST /ask` - Question answering
- `POST /loan-information` - Loan data retrieval
- `POST /compliance-requirements` - Compliance data
- `POST /search-documents` - Document search
- `GET /stats` - Knowledge base statistics
- `POST /clear-conversation` - Clear chat history
- `POST /reset-knowledge-base` - Reset knowledge base

## Configuration

### Environment Variables
The frontend uses the same environment configuration as the backend:
- `GOOGLE_API_KEY` - Required for AI functionality
- Other settings are configured in `src/config.py`

### Frontend Settings
- **Port**: 8501 (configurable in `run_frontend.py`)
- **Host**: localhost
- **API Base URL**: http://localhost:8000

## Troubleshooting

### Common Issues

1. **"Cannot connect to API"**
   - Ensure the backend is running: `python main.py`
   - Check if port 8000 is available
   - Verify API key is set in environment

2. **"Upload failed"**
   - Check file format (supported: PDF, DOCX, TXT, XLSX, CSV)
   - Ensure file size is reasonable
   - Check backend logs for detailed error

3. **"Question processing failed"**
   - Verify Google API key is valid
   - Check internet connection
   - Review backend logs for API errors

### Debug Mode
To run in debug mode:
```bash
streamlit run frontend.py --logger.level debug
```

## Development

### Adding New Features
1. The frontend is built with Streamlit for easy modification
2. All API calls are centralized in functions at the top of `frontend.py`
3. UI components are organized in tabs for clarity

### Customization
- Modify CSS in the `st.markdown` section for styling
- Add new tabs for additional functionality
- Extend API integration functions as needed

## Security Notes

- The frontend runs on localhost by default
- API calls are made to localhost:8000
- No sensitive data is stored in the frontend
- All data processing happens on the backend

## Support

For issues or questions:
1. Check the main project README.md
2. Review backend logs for API errors
3. Ensure all dependencies are installed
4. Verify environment configuration 