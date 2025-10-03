# Lead Prioritization Tool - Streamlit App
# Caprae Capital AI-Readiness Challenge

import streamlit as st
import pandas as pd
import io
from scoring_engine import LeadScorer
from outreach_templates import get_templates, get_openers, generate_personalized_content

def apply_score_styling(score):
    """Apply color styling based on lead score."""
    if score == 'High':
        return 'background-color: #d4edda; color: #155724; font-weight: bold'
    elif score == 'Medium':
        return 'background-color: #fff3cd; color: #856404; font-weight: bold'
    elif score == 'Low':
        return 'background-color: #f8d7da; color: #721c24; font-weight: bold'
    return ''

def create_sample_csv():
    """Create a sample CSV for users to download and test."""
    sample_data = {
        'name': ['John Smith', 'Sarah Johnson', 'Mike Chen', 'Lisa Brown'],
        'email': ['john.smith@techcorp.com', 'sarah.j@gmail.com', 'mike.chen@startup.io', 'lisa@enterprise.com'],
        'company': ['TechCorp Inc', 'Freelance', 'StartupIO', 'Enterprise Solutions'],
        'job_title': ['Sales Manager', 'Marketing Consultant', 'Product Manager', 'CEO'],
        'company_size': [120, 1, 25, 500]
    }
    return pd.DataFrame(sample_data)

def main():
    st.title("🎯 Lead Prioritization Tool")
    st.markdown("### Upload CSV → Score Leads → Generate Outreach")
    st.markdown("---")
    
    # Initialize scorer
    if 'scorer' not in st.session_state:
        st.session_state.scorer = LeadScorer()
    
    # Sidebar with instructions
    st.sidebar.header("📋 Instructions")
    st.sidebar.markdown("""
    **Expected CSV Columns:**
    - `name`: Lead's full name
    - `email`: Email address
    - `company`: Company name
    - `job_title`: Job title/position
    - `company_size`: Number of employees
    
    **Scoring Rules:**
    - 🟢 **High**: Senior titles + corporate email + large company
    - 🟡 **Medium**: Some qualifying factors
    - 🔴 **Low**: Few/no qualifying factors
    """)
    
    # Sample CSV download
    sample_df = create_sample_csv()
    csv_buffer = io.StringIO()
    sample_df.to_csv(csv_buffer, index=False)
    st.sidebar.download_button(
        label="📥 Download Sample CSV",
        data=csv_buffer.getvalue(),
        file_name="sample_leads.csv",
        mime="text/csv"
    )
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📤 Upload Lead Data")
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type="csv",
            help="Upload a CSV file with lead data. Use the sample CSV format."
        )
    
    with col2:
        st.subheader("📊 Quick Stats")
        if uploaded_file is not None:
            # Load and process data
            try:
                df = pd.read_csv(uploaded_file)
                
                # Validate required columns
                required_columns = ['name', 'email', 'company', 'job_title', 'company_size']
                missing_columns = [col for col in required_columns if col not in df.columns]
                
                if missing_columns:
                    st.error(f"Missing required columns: {', '.join(missing_columns)}")
                    st.stop()
                
                # Apply scoring
                scored_df = st.session_state.scorer.score_leads_batch(df)
                
                # Display stats
                total_leads = len(scored_df)
                high_count = len(scored_df[scored_df['score'] == 'High'])
                medium_count = len(scored_df[scored_df['score'] == 'Medium'])
                low_count = len(scored_df[scored_df['score'] == 'Low'])
                
                st.metric("Total Leads", total_leads)
                st.metric("🟢 High Priority", high_count)
                st.metric("🟡 Medium Priority", medium_count)
                st.metric("🔴 Low Priority", low_count)
                
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
                st.stop()
    
    # Display scored leads
    if uploaded_file is not None and 'scored_df' in locals():
        st.markdown("---")
        st.subheader("🎯 Prioritized Leads")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            score_filter = st.selectbox(
                "Filter by Score",
                ["All", "High", "Medium", "Low"]
            )
        
        # Apply filter
        if score_filter != "All":
            display_df = scored_df[scored_df['score'] == score_filter].copy()
        else:
            display_df = scored_df.copy()
        
        if len(display_df) == 0:
            st.info(f"No leads found with {score_filter} priority.")
        else:
            # Style the DataFrame
            styled_df = display_df.style.map(
                apply_score_styling,
                subset=['score']
            )
            
            # Display table
            st.dataframe(
                styled_df,
                use_container_width=True,
                hide_index=True
            )
            
            # Store scored data in session state for export
            st.session_state.scored_leads = scored_df
            
            # Outreach suggestions for top leads
            st.markdown("---")
            st.subheader("📬 Outreach Suggestions")
            
            # Get high priority leads for outreach
            high_priority_leads = scored_df[scored_df['score'] == 'High'].head(3)
            
            if len(high_priority_leads) > 0:
                # Lead selection for outreach
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.markdown("**Select Lead:**")
                    selected_lead_idx = st.selectbox(
                        "Choose a high-priority lead",
                        range(len(high_priority_leads)),
                        format_func=lambda x: f"{high_priority_leads.iloc[x]['name']} - {high_priority_leads.iloc[x]['company']}",
                        key="lead_selector"
                    )
                    
                    # Content type selection
                    content_type = st.selectbox(
                        "Content Type",
                        ["Both", "Templates", "Openers"],
                        key="content_type_selector"
                    )
                
                with col2:
                    st.markdown("**Lead Details:**")
                    selected_lead = high_priority_leads.iloc[selected_lead_idx]
                    
                    st.info(f"""
                    **Name:** {selected_lead['name']}
                    **Company:** {selected_lead['company']}
                    **Title:** {selected_lead['job_title']}
                    **Score:** {selected_lead['score']}
                    """)
                
                # Generate personalized content
                lead_data = selected_lead.to_dict()
                content_type_map = {"Both": "both", "Templates": "templates", "Openers": "openers"}
                personalized_content = generate_personalized_content(lead_data, content_type_map[content_type])
                
                # Display outreach content
                if content_type in ["Templates", "Both"] and "templates" in personalized_content:
                    st.markdown("### 📧 Email Templates")
                    
                    for i, template in enumerate(personalized_content["templates"]):
                        with st.expander(f"{template['name']}", expanded=(i == 0)):
                            st.text_area(
                                "Template Content",
                                template["content"],
                                height=200,
                                key=f"template_{i}"
                            )
                            st.button(f"Copy {template['name']}", key=f"copy_template_{i}")
                
                if content_type in ["Openers", "Both"] and "openers" in personalized_content:
                    st.markdown("### 💬 Quick Openers")
                    st.markdown("*Perfect for LinkedIn messages or brief emails*")
                    
                    for i, opener in enumerate(personalized_content["openers"]):
                        st.text_area(
                            f"Opener {i+1}",
                            opener,
                            height=80,
                            key=f"opener_{i}"
                        )
                        
            else:
                st.info("📊 No high-priority leads found. Upload leads or adjust scoring criteria to see outreach suggestions.")
                
        # Export functionality
        st.markdown("---")
        st.subheader("📥 Export Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Export scored leads CSV
            csv_buffer = io.StringIO()
            scored_df.to_csv(csv_buffer, index=False)
            st.download_button(
                label="📈 Download Scored Leads CSV",
                data=csv_buffer.getvalue(),
                file_name="scored_leads.csv",
                mime="text/csv",
                help="Download the complete dataset with scores"
            )
        
        with col2:
            # Export high priority leads only
            high_priority_df = scored_df[scored_df['score'] == 'High']
            if len(high_priority_df) > 0:
                high_csv_buffer = io.StringIO()
                high_priority_df.to_csv(high_csv_buffer, index=False)
                st.download_button(
                    label="⭐ Download High Priority Only",
                    data=high_csv_buffer.getvalue(),
                    file_name="high_priority_leads.csv",
                    mime="text/csv",
                    help="Download only high-priority leads"
                )
            else:
                st.info("No high priority leads to export")
        
        with col3:
            # Export summary report
            summary_data = {
                'Metric': ['Total Leads', 'High Priority', 'Medium Priority', 'Low Priority', 'High Priority %'],
                'Value': [
                    len(scored_df),
                    len(scored_df[scored_df['score'] == 'High']),
                    len(scored_df[scored_df['score'] == 'Medium']),
                    len(scored_df[scored_df['score'] == 'Low']),
                    f"{len(scored_df[scored_df['score'] == 'High']) / len(scored_df) * 100:.1f}%" if len(scored_df) > 0 else "0%"
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            summary_csv_buffer = io.StringIO()
            summary_df.to_csv(summary_csv_buffer, index=False)
            st.download_button(
                label="📉 Download Summary Report",
                data=summary_csv_buffer.getvalue(),
                file_name="lead_scoring_summary.csv",
                mime="text/csv",
                help="Download scoring summary metrics"
            )
    
    else:
        # Show sample data when no file is uploaded
        st.markdown("---")
        st.subheader("📋 Sample Lead Data (Demo)")
        st.info("Upload your CSV file above to see prioritized leads, or download the sample CSV to get started.")
        
        # Process and display sample data
        sample_scored = st.session_state.scorer.score_leads_batch(sample_df)
        styled_sample = sample_scored.style.map(
            apply_score_styling,
            subset=['score']
        )
        
        st.dataframe(
            styled_sample,
            use_container_width=True,
            hide_index=True
        )

if __name__ == "__main__":
    main()
