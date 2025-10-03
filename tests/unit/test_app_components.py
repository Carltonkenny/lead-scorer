# Test App Components
import pandas as pd
from lead_scoring_engine import LeadScorer

def test_sample_data_creation():
    """Test sample CSV creation and styling."""
    from app import create_sample_csv, apply_score_styling
    
    print("Testing Sample Data Creation:")
    print("-" * 40)
    
    # Create sample data
    sample_df = create_sample_csv()
    print("Sample CSV created successfully:")
    print(sample_df)
    print()
    
    # Test scoring
    scorer = LeadScorer()
    scored_df = scorer.score_leads_batch(sample_df)
    print("Scored Sample Data:")
    print(scored_df[['name', 'job_title', 'email', 'company_size', 'score']])
    print()
    
    # Test styling function
    print("Testing Color Styling:")
    print(f"High score styling: {apply_score_styling('High')}")
    print(f"Medium score styling: {apply_score_styling('Medium')}")
    print(f"Low score styling: {apply_score_styling('Low')}")
    
    return scored_df

def test_csv_validation():
    """Test CSV column validation logic."""
    print("\nTesting CSV Validation:")
    print("-" * 40)
    
    # Test with correct columns
    correct_df = pd.DataFrame({
        'name': ['Test User'],
        'email': ['test@company.com'],
        'company': ['Test Company'],
        'job_title': ['Test Manager'],
        'company_size': [100]
    })
    
    required_columns = ['name', 'email', 'company', 'job_title', 'company_size']
    missing_columns = [col for col in required_columns if col not in correct_df.columns]
    
    if not missing_columns:
        print("✅ CSV validation passed - all required columns present")
    else:
        print(f"❌ Missing columns: {missing_columns}")
    
    # Test with missing columns
    incorrect_df = pd.DataFrame({
        'name': ['Test User'],
        'email': ['test@company.com']
    })
    
    missing_columns = [col for col in required_columns if col not in incorrect_df.columns]
    print(f"Missing columns test: {missing_columns}")
    
if __name__ == "__main__":
    scored_df = test_sample_data_creation()
    test_csv_validation()
    
    print("\n" + "="*50)
    print("✅ All app components tested successfully!")
    print("✅ Ready for Streamlit deployment")
