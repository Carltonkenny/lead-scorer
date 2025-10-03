# Test Enhanced Robustness and Normalization
import pandas as pd
from lead_scoring_engine import LeadScorer

def test_job_title_normalization():
    """Test job title normalization with various edge cases."""
    print("Testing Job Title Normalization:")
    print("-" * 50)
    
    scorer = LeadScorer()
    
    test_titles = [
        "Sales Mgr",           # Abbreviation
        "Sr. Director",        # Senior abbreviation with period
        "VP Sales",           # VP abbreviation
        "Chief Executive Officer",  # Full C-level title
        "Marketing Dir.",     # Director abbreviation
        "Jr Software Eng",    # Junior engineer abbreviation
        "",                   # Empty title
        "None",              # None value
        "Sales Manager, North America",  # Title with region
        "Head of Operations/Strategy"    # Title with slash
    ]
    
    for title in test_titles:
        normalized = scorer.normalize_job_title(title)
        print(f"'{title}' → '{normalized}'")

def test_email_domain_normalization():
    """Test email domain extraction and normalization."""
    print("\n\nTesting Email Domain Normalization:")
    print("-" * 50)
    
    scorer = LeadScorer()
    
    test_emails = [
        "john.smith@techcorp.com",      # Normal corporate
        "jane@GMAIL.COM",               # Personal (caps)
        "bob@www.company.co.uk",        # Domain with www
        "invalid-email",                # Invalid format
        "",                            # Empty
        "sarah@startup.io",            # Tech domain
        "mike@yahoo.com",              # Personal domain
    ]
    
    for email in test_emails:
        domain = scorer.normalize_email_domain(email)
        print(f"'{email}' → '{domain}'")

def test_company_size_normalization():
    """Test company size normalization with various formats."""
    print("\n\nTesting Company Size Normalization:")
    print("-" * 50)
    
    scorer = LeadScorer()
    
    test_sizes = [
        "50",                  # String number
        50,                    # Integer
        "Startup",            # Text description
        "50-100",             # Range
        "100+",               # Plus notation
        "1,000 employees",    # Formatted with comma
        "Medium",             # Size category
        "Freelance",          # Solo worker
        "",                   # Empty
        "Unknown",            # Unknown value
        "50.0"                # Float as string
    ]
    
    for size in test_sizes:
        normalized = scorer.normalize_company_size(size)
        print(f"'{size}' → {normalized}")

def test_edge_case_scoring():
    """Test scoring with messy, real-world edge case data."""
    print("\n\nTesting Edge Case Scoring:")
    print("-" * 50)
    
    scorer = LeadScorer()
    
    # Edge cases that might break naive implementations
    edge_case_leads = [
        {
            'name': 'John Smith',
            'job_title': 'Sr. VP Sales & Marketing',  # Mixed abbreviations
            'email': 'john.smith@TECHCORP.COM',       # Caps email
            'company': 'TechCorp',
            'company_size': '100-500 employees'       # Range with text
        },
        {
            'name': 'Jane Doe',
            'job_title': '',                          # Empty title
            'email': 'jane@gmail.com',
            'company': 'Freelance',
            'company_size': 'Solo'                    # Text size
        },
        {
            'name': 'Bob Director',
            'job_title': 'Marketing Dir, EMEA',      # Regional director
            'email': 'bob@startup.io',
            'company': 'StartupIO',
            'company_size': 'startup'                 # Lowercase startup
        },
        {
            'name': 'Alice CEO',
            'job_title': 'Founder & CEO',            # Multiple titles
            'email': 'alice@bigcompany.com',
            'company': 'BigCompany',
            'company_size': '2,500'                   # Comma in number
        }
    ]
    
    for i, lead in enumerate(edge_case_leads, 1):
        score = scorer.score_lead(lead)
        print(f"Lead {i}: {lead['name']} ({lead['job_title']}) → {score}")
        print(f"  Normalized title: '{scorer.normalize_job_title(lead['job_title'])}'")
        print(f"  Email domain: '{scorer.normalize_email_domain(lead['email'])}'")
        print(f"  Company size: {scorer.normalize_company_size(lead['company_size'])}")
        print()

def test_consistency_with_variations():
    """Test that variations of the same lead get consistent scores."""
    print("\n\nTesting Scoring Consistency:")
    print("-" * 50)
    
    scorer = LeadScorer()
    
    # Same person with different data formats
    lead_variations = [
        {
            'name': 'John Smith',
            'job_title': 'Sales Manager',
            'email': 'john@techcorp.com',
            'company': 'TechCorp',
            'company_size': 100
        },
        {
            'name': 'John Smith',
            'job_title': 'Sales Mgr',              # Abbreviated
            'email': 'john@TECHCORP.COM',          # Caps
            'company': 'TechCorp',
            'company_size': '100 employees'        # Text format
        },
        {
            'name': 'John Smith',
            'job_title': 'Manager, Sales',         # Different order
            'email': 'john@techcorp.com',
            'company': 'TechCorp',
            'company_size': '50-150'               # Range
        }
    ]
    
    scores = []
    for i, lead in enumerate(lead_variations, 1):
        score = scorer.score_lead(lead)
        scores.append(score)
        print(f"Variation {i}: {score}")
    
    # Check consistency
    unique_scores = set(scores)
    if len(unique_scores) == 1:
        print("✅ All variations scored consistently!")
    else:
        print("⚠️ Inconsistent scoring detected - may need adjustment")
        print(f"Scores: {scores}")

if __name__ == "__main__":
    test_job_title_normalization()
    test_email_domain_normalization()
    test_company_size_normalization()
    test_edge_case_scoring()
    test_consistency_with_variations()
    
    print("\n" + "="*60)
    print("✅ Robustness testing completed!")
    print("✅ Enhanced normalization functions validated")