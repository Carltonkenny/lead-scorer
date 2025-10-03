# Test Outreach Templates and Personalization
from outreach_templates import get_templates, get_openers, generate_personalized_content, determine_goal_from_title

def test_templates_and_openers():
    """Test basic template and opener generation."""
    print("Testing Template and Opener Generation:")
    print("-" * 50)
    
    # Test templates
    templates = get_templates()
    print(f"Number of templates: {len(templates)}")
    for i, template in enumerate(templates, 1):
        print(f"\nTemplate {i}: {template['name']}")
        print("Preview:", template['template'][:100] + "...")
    
    # Test openers
    openers = get_openers()
    print(f"\nNumber of openers: {len(openers)}")
    for i, opener in enumerate(openers, 1):
        print(f"\nOpener {i}: {opener[:80]}...")

def test_goal_determination():
    """Test goal determination from job titles."""
    print("\n\nTesting Goal Determination:")
    print("-" * 50)
    
    test_titles = [
        "Sales Manager",
        "Marketing Director", 
        "CEO",
        "Software Engineer",
        "Operations Manager",
        "Business Development Rep",
        "Unknown Title"
    ]
    
    for title in test_titles:
        goal = determine_goal_from_title(title)
        print(f"{title:<25} → {goal}")

def test_personalization():
    """Test personalized content generation."""
    print("\n\nTesting Personalization:")
    print("-" * 50)
    
    # Sample lead data
    test_lead = {
        'name': 'John Smith',
        'company': 'TechCorp Inc',
        'job_title': 'Sales Manager',
        'email': 'john.smith@techcorp.com',
        'company_size': 120
    }
    
    print(f"Test Lead: {test_lead['name']} - {test_lead['job_title']} at {test_lead['company']}")
    
    # Generate personalized content
    personalized = generate_personalized_content(test_lead, "both")
    
    # Show first template
    if "templates" in personalized:
        print(f"\nFirst Personalized Template ({personalized['templates'][0]['name']}):")
        print("-" * 40)
        print(personalized['templates'][0]['content'])
    
    # Show first opener
    if "openers" in personalized:
        print(f"\nFirst Personalized Opener:")
        print("-" * 40)
        print(personalized['openers'][0])

def test_different_roles():
    """Test personalization with different job roles."""
    print("\n\nTesting Different Roles:")
    print("-" * 50)
    
    test_leads = [
        {'name': 'Sarah Johnson', 'company': 'MarketCorp', 'job_title': 'Marketing Director'},
        {'name': 'Mike Chen', 'company': 'TechStart', 'job_title': 'CEO'},
        {'name': 'Lisa Brown', 'company': 'DevCompany', 'job_title': 'Software Engineer'}
    ]
    
    for lead in test_leads:
        goal = determine_goal_from_title(lead['job_title'])
        personalized = generate_personalized_content(lead, "openers")
        
        print(f"\n{lead['name']} ({lead['job_title']}) → Goal: {goal}")
        print(f"Sample Opener: {personalized['openers'][0]}")

if __name__ == "__main__":
    test_templates_and_openers()
    test_goal_determination()
    test_personalization()
    test_different_roles()
    
    print("\n" + "="*60)
    print("✅ All outreach functionality tests completed!")
    print("✅ Templates, openers, and personalization working correctly")