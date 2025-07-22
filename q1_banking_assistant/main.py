#!/usr/bin/env python3
"""
Main entry point for Banking AI Assistant
"""
import os
import sys
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent / "src"))

from src.banking_assistant import BankingAssistant
from src.api import run_server
from src.config import settings


def main():
    """Main function to run the banking assistant"""
    print("🚀 Starting Banking AI Assistant...")
    
    # Check if API key is set
    if not settings.GOOGLE_API_KEY:
        print("❌ Error: GOOGLE_API_KEY is required!")
        print("Please set your Google API key in the .env file or environment variables.")
        print("You can get one from: https://makersuite.google.com/app/apikey")
        return
    
    try:
        # Initialize banking assistant
        assistant = BankingAssistant()
        print("✅ Banking Assistant initialized successfully!")
        
        # Start the web server
        print(f"🌐 Starting web server on http://{settings.API_HOST}:{settings.API_PORT}")
        print("📚 API documentation available at: http://localhost:8000/docs")
        run_server()
        
    except Exception as e:
        print(f"❌ Error starting Banking Assistant: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 