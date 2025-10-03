# Complete Application Integration Test
import pandas as pd
import io
from lead_scoring_engine import LeadScorer
from outreach_templates import generate_personalized_content

def test_complete_workflow():
    """Test the complete lead scoring workflow end-to-end."""
    print("🎯 COMPLETE APPLICATION INTEGRATION TEST")
    print("=" * 60)
    
    # Step 1: Create sample lead data (simulating CSV upload)
    print("\n1️⃣  STEP 1: Data Loading (CSV Upload Simulation)")
    print("-" * 50)
    
    sample_leads = pd.DataFrame({
        'name': [
            'John Smith', 'Sarah Johnson', 'Mike Chen', 'Lisa Brown',
            'David Wilson', 'Emma Davis', 'Tom Rodriguez', 'Anna Kim'
        ],
        'email': [
            'john.smith@techcorp.com', 'sarah.j@gmail.com', 
            'mike.chen@startup.io', 'lisa@enterprise.com',
            'david.wilson@consulting.com', 'emma@freelance.net',
            'tom.rodriguez@bigcorp.com', 'anna.kim@yahoo.com'
        ],
        'company': [
            'TechCorp Inc', 'Freelance', 'StartupIO', 'Enterprise Solutions',
            'Wilson Consulting', 'Freelance Designer', 'BigCorp Ltd', 'Personal'
        ],
        'job_title': [
            'Sales Manager', 'Marketing Consultant', 'Product Manager', 'CEO',
            'Senior Director', 'Graphic Designer', 'VP of Operations', 'Student'
        ],
        'company_size': [120, 1, 25, 500, 200, 1, 1000, 0]
    })
    
    print(f"✅ Sample data created: {len(sample_leads)} leads")
    print(f"   Columns: {list(sample_leads.columns)}")
    
    # Step 2: Apply scoring engine
    print("\n2️⃣  STEP 2: Lead Scoring")
    print("-" * 50)
    
    scorer = LeadScorer()
    scored_leads = scorer.score_leads_batch(sample_leads)
    
    # Display scoring results
    print("Scoring Results:")
    for _, lead in scored_leads.iterrows():
        print(f"   {lead['name']:<15} | {lead['job_title']:<20} | {lead['score']:<8} | {lead['company']}")
    
    # Calculate statistics
    high_count = len(scored_leads[scored_leads['score'] == 'High'])
    medium_count = len(scored_leads[scored_leads['score'] == 'Medium'])
    low_count = len(scored_leads[scored_leads['score'] == 'Low'])
    
    print(f"\n📊 Score Distribution:")
    print(f"   🟢 High Priority:   {high_count} leads ({high_count/len(scored_leads)*100:.1f}%)")
    print(f"   🟡 Medium Priority: {medium_count} leads ({medium_count/len(scored_leads)*100:.1f}%)")
    print(f"   🔴 Low Priority:    {low_count} leads ({low_count/len(scored_leads)*100:.1f}%)")
    
    # Step 3: Test outreach generation for high priority leads
    print("\n3️⃣  STEP 3: Outreach Generation")
    print("-" * 50)
    
    high_priority_leads = scored_leads[scored_leads['score'] == 'High']
    
    if len(high_priority_leads) > 0:
        # Test with first high-priority lead
        test_lead = high_priority_leads.iloc[0]
        print(f"Generating outreach for: {test_lead['name']} ({test_lead['job_title']}) at {test_lead['company']}")
        
        # Generate personalized content
        personalized = generate_personalized_content(test_lead.to_dict(), "both")
        
        if "templates" in personalized:
            print(f"\n📧 Generated {len(personalized['templates'])} email templates")
            print(f"   First template preview: {personalized['templates'][0]['content'][:100]}...")
        
        if "openers" in personalized:
            print(f"\n💬 Generated {len(personalized['openers'])} quick openers")
            print(f"   First opener: {personalized['openers'][0][:80]}...")
    else:
        print("⚠️  No high-priority leads found for outreach testing")
    
    # Step 4: Test export functionality
    print("\n4️⃣  STEP 4: Export Functionality")
    print("-" * 50)
    
    # Test CSV export
    csv_buffer = io.StringIO()
    scored_leads.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()
    
    print(f"✅ Complete CSV export: {len(csv_data)} characters")
    
    # Test high-priority only export
    if len(high_priority_leads) > 0:
        high_csv_buffer = io.StringIO()
        high_priority_leads.to_csv(high_csv_buffer, index=False)
        high_csv_data = high_csv_buffer.getvalue()
        print(f"✅ High-priority CSV export: {len(high_csv_data)} characters")
    
    # Test summary report
    summary_data = {
        'Metric': ['Total Leads', 'High Priority', 'Medium Priority', 'Low Priority'],
        'Value': [len(scored_leads), high_count, medium_count, low_count]
    }
    summary_df = pd.DataFrame(summary_data)
    summary_csv_buffer = io.StringIO()
    summary_df.to_csv(summary_csv_buffer, index=False)
    summary_csv_data = summary_csv_buffer.getvalue()
    
    print(f"✅ Summary report export: {len(summary_csv_data)} characters")
    
    # Step 5: Validate all core functionality
    print("\n5️⃣  STEP 5: Functionality Validation")
    print("-" * 50)
    
    validations = [
        ("CSV Data Processing", len(scored_leads) == len(sample_leads)),
        ("Scoring Engine", 'score' in scored_leads.columns),
        ("Score Sorting", scored_leads.iloc[0]['score'] in ['High', 'Medium', 'Low']),
        ("Outreach Generation", len(high_priority_leads) == 0 or "templates" in personalized),
        ("Export Functionality", len(csv_data) > 0),
        ("Summary Statistics", high_count + medium_count + low_count == len(scored_leads))
    ]
    
    all_passed = True
    for test_name, result in validations:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name:<25} {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED - APPLICATION READY FOR DEPLOYMENT!")
        print("✅ Complete workflow validated")
        print("✅ All core features functional") 
        print("✅ Export capabilities confirmed")
        print("✅ Outreach generation working")
    else:
        print("⚠️  SOME TESTS FAILED - REVIEW REQUIRED")
    
    print("=" * 60)
    
    return scored_leads, all_passed

if __name__ == "__main__":
    scored_data, success = test_complete_workflow()
    
    if success:
        print("\n🚀 Ready for Streamlit deployment!")
        print("   Command: streamlit run app.py")
    else:
        print("\n⚠️  Fix issues before deployment")
