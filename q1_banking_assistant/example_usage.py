#!/usr/bin/env python3
"""
Example usage of Banking AI Assistant
"""
import os
import sys
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent / "src"))

from src.banking_assistant import BankingAssistant
from src.config import settings


def create_sample_documents():
    """Create sample banking documents for testing"""
    documents_dir = Path("sample_documents")
    documents_dir.mkdir(exist_ok=True)
    
    # Sample loan handbook
    loan_handbook = documents_dir / "loan_handbook.txt"
    loan_handbook.write_text("""
LOAN PRODUCTS HANDBOOK

1. PERSONAL LOANS
   Interest Rate: 8.5% - 12.5% APR
   Term Length: 12-60 months
   Minimum Amount: $1,000
   Maximum Amount: $50,000
   Requirements: Good credit score (650+), stable income, proof of employment

2. MORTGAGE LOANS
   Interest Rate: 4.25% - 6.75% APR
   Term Length: 15-30 years
   Minimum Down Payment: 3.5% (FHA), 5% (Conventional)
   Requirements: Credit score 620+, debt-to-income ratio <43%, proof of income

3. BUSINESS LOANS
   Interest Rate: 6.5% - 15% APR
   Term Length: 1-10 years
   Minimum Amount: $10,000
   Maximum Amount: $500,000
   Requirements: Business plan, financial statements, collateral

FEES AND CHARGES:
- Application Fee: $50
- Origination Fee: 1-3% of loan amount
- Late Payment Fee: $25
- Prepayment Penalty: 2% of remaining balance (first 3 years)

Table 1.1: Loan Comparison
| Loan Type | Min Rate | Max Rate | Min Term | Max Term | Min Amount |
|-----------|----------|----------|----------|----------|------------|
| Personal  | 8.5%     | 12.5%    | 12 months| 60 months| $1,000     |
| Mortgage  | 4.25%    | 6.75%    | 15 years | 30 years | $50,000    |
| Business  | 6.5%     | 15%      | 1 year   | 10 years | $10,000    |
""")
    
    # Sample compliance manual
    compliance_manual = documents_dir / "compliance_manual.txt"
    compliance_manual.write_text("""
REGULATORY COMPLIANCE MANUAL

1. ANTI-MONEY LAUNDERING (AML) REQUIREMENTS
   - Customer Due Diligence (CDD) required for all accounts
   - Suspicious Activity Reports (SAR) must be filed within 30 days
   - Transaction monitoring for amounts over $10,000
   - Annual AML training for all employees

2. KNOW YOUR CUSTOMER (KYC) PROCEDURES
   - Verify customer identity with government-issued ID
   - Collect proof of address (utility bill, bank statement)
   - Risk assessment based on customer profile
   - Enhanced due diligence for high-risk customers

3. FAIR LENDING COMPLIANCE
   - Equal Credit Opportunity Act (ECOA) compliance
   - No discrimination based on race, color, religion, national origin, sex, marital status, age
   - Fair lending monitoring and reporting
   - Regular fair lending audits

4. DATA PRIVACY REQUIREMENTS
   - Gramm-Leach-Bliley Act (GLBA) compliance
   - Customer privacy notices required
   - Secure handling of customer information
   - Annual privacy training for employees

Table 2.1: Compliance Deadlines
| Requirement | Frequency | Deadline | Responsible Party |
|-------------|-----------|----------|-------------------|
| AML Training | Annual    | Dec 31   | HR Department     |
| SAR Filing  | As needed | 30 days  | Compliance Team   |
| Privacy Audit| Annual    | Jun 30   | Internal Audit    |
| KYC Review  | Ongoing   | 90 days  | Branch Managers   |

PENALTIES FOR NON-COMPLIANCE:
- AML violations: Up to $250,000 per violation
- Fair lending violations: Up to $10,000 per day
- Privacy violations: Up to $100 per violation per day
""")
    
    # Sample rate sheet
    rate_sheet = documents_dir / "rate_sheet.txt"
    rate_sheet.write_text("""
CURRENT INTEREST RATES - EFFECTIVE JANUARY 2024

DEPOSIT ACCOUNTS:
| Account Type | Minimum Balance | Interest Rate | APY |
|--------------|-----------------|---------------|-----|
| Savings      | $100           | 0.50%         | 0.50% |
| Money Market | $2,500         | 1.25%         | 1.26% |
| CD 12-month  | $1,000         | 2.75%         | 2.78% |
| CD 24-month  | $1,000         | 3.00%         | 3.04% |
| CD 36-month  | $1,000         | 3.25%         | 3.30% |

LOAN RATES:
| Loan Type | Credit Score | Interest Rate | APR |
|-----------|--------------|---------------|-----|
| Personal  | 750+         | 8.50%         | 8.75% |
| Personal  | 650-749      | 10.50%        | 10.80% |
| Personal  | 600-649      | 12.50%        | 12.85% |
| Mortgage  | 760+         | 4.25%         | 4.35% |
| Mortgage  | 700-759      | 4.50%         | 4.60% |
| Mortgage  | 650-699      | 5.00%         | 5.15% |
| Business  | 680+         | 6.50%         | 6.75% |
| Business  | 650-679      | 8.50%         | 8.80% |
| Business  | 620-649      | 12.00%        | 12.35% |

FEES:
- Monthly Maintenance Fee: $12 (waived with $1,500 minimum balance)
- Overdraft Fee: $35
- Stop Payment Fee: $30
- Wire Transfer Fee: $25 domestic, $45 international
- Cashier's Check Fee: $10
""")
    
    print("✅ Sample documents created in 'sample_documents' directory")


def example_usage():
    """Demonstrate the banking assistant functionality"""
    print("🏦 Banking AI Assistant - Example Usage")
    print("=" * 50)
    
    # Check API key
    if not settings.GOOGLE_API_KEY:
        print("❌ Please set GOOGLE_API_KEY in your environment variables")
        print("You can get one from: https://makersuite.google.com/app/apikey")
        return
    
    try:
        # Create sample documents
        create_sample_documents()
        
        # Initialize banking assistant
        print("\n🔧 Initializing Banking Assistant...")
        assistant = BankingAssistant()
        
        # Load sample documents
        print("\n📚 Loading sample documents...")
        result = assistant.load_documents("sample_documents")
        print(f"✅ {result['message']}")
        
        # Example questions
        questions = [
            "What are the interest rates for personal loans?",
            "What are the requirements for a mortgage loan?",
            "What are the AML compliance requirements?",
            "What are the current CD rates?",
            "What fees are charged for wire transfers?"
        ]
        
        print("\n🤖 Testing Banking Assistant Questions:")
        print("-" * 40)
        
        for i, question in enumerate(questions, 1):
            print(f"\n{i}. Question: {question}")
            result = assistant.ask_question(question)
            
            if result["success"]:
                print(f"✅ Answer: {result['answer'][:200]}...")
                print(f"📊 Confidence: {result['confidence']}")
                print(f"📄 Sources: {len(result['sources'])} documents")
            else:
                print(f"❌ Error: {result['answer']}")
        
        # Test structured queries
        print("\n📊 Testing Structured Queries:")
        print("-" * 40)
        
        # Loan information
        loan_result = assistant.get_loan_information("personal")
        if loan_result["success"]:
            print("✅ Loan information retrieved successfully")
        else:
            print(f"❌ Error: {loan_result['error']}")
        
        # Compliance requirements
        compliance_result = assistant.get_compliance_requirements("AML")
        if compliance_result["success"]:
            print("✅ Compliance requirements retrieved successfully")
        else:
            print(f"❌ Error: {compliance_result['error']}")
        
        # Get stats
        stats = assistant.get_knowledge_base_stats()
        if stats["success"]:
            print(f"\n📈 Knowledge Base Stats:")
            print(f"   Documents: {stats['stats']['document_count']}")
            print(f"   Collection: {stats['stats']['collection_name']}")
        
        print("\n🎉 Example usage completed successfully!")
        print("\n💡 To start the web server, run: python main.py")
        print("📚 API documentation will be available at: http://localhost:8000/docs")
        
    except Exception as e:
        print(f"❌ Error in example usage: {e}")


if __name__ == "__main__":
    example_usage() 