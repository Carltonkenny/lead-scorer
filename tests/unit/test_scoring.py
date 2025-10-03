# Test Script for Lead Scoring Engine
import pandas as pd
from lead_scoring_engine import LeadScorer

def test_scoring_engine():
    """Test the lead scoring engine with sample data."""
    
    # Create sample lead data
    test_leads = [
        {
            'name': 'John Manager',
            'email': 'john.manager@techcorp.com',
            'company': 'TechCorp',
            'job_title': 'Sales Manager',
            'company_size': 75
        },
        {
            'name': 'Jane Doe', 
            'email': 'jane.doe@gmail.com',
            'company': 'Small Startup',
            'job_title': 'Junior Sales Rep',
            'company_size': 8
        },
        {
            'name': 'Bob Director',
            'email': 'bob.director@bigcompany.com', 
            'company': 'BigCompany Inc',
            'job_title': 'Marketing Director',
            'company_size': 150
        }
    ]
    
    # Initialize scorer
    scorer = LeadScorer()
    
    print("Testing Individual Lead Scoring:")
    print("-" * 40)
    
    for i, lead in enumerate(test_leads, 1):
        score = scorer.score_lead(lead)
        print(f"Lead {i}: {lead['name']}")
        print(f"  Title: {lead['job_title']}")
        print(f"  Email: {lead['email']}")
        print(f"  Company Size: {lead['company_size']}")
        print(f"  Score: {score}")
        print()
    
    # Test batch scoring
    print("Testing Batch Scoring:")
    print("-" * 40)
    
    df = pd.DataFrame(test_leads)
    scored_df = scorer.score_leads_batch(df)
    
    print(scored_df[['name', 'job_title', 'company_size', 'score']])

if __name__ == "__main__":
    test_scoring_engine()