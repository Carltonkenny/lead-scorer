# Lead Prioritization Tool - Streamlit App
# Caprae Capital AI-Readiness Challenge

import streamlit as st
import pandas as pd
import io
import re
import sys
import os

# Add paths for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from scoring_engine import LeadScorer
from outreach_templates import get_templates, get_openers, generate_personalized_content
from enrichment import enrich_leads
from column_mapper import ColumnMapper

def validate_email_format(email):
    """Validate basic email format."""
    if pd.isna(email) or str(email).strip() == '':
        return False
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, str(email).strip()))

def validate_csv_data(df):
    """Comprehensive CSV validation with detailed feedback."""
    issues = []
    warnings = []
    
    # Check required columns
    required_columns = ['name', 'email', 'company', 'job_title', 'company_size']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        issues.append(f"❌ Missing required columns: {', '.join(missing_columns)}")
        return issues, warnings, False
    
    # Check for empty rows
    empty_rows = df[df.isnull().all(axis=1)]
    if len(empty_rows) > 0:
        warnings.append(f"⚠️ Found {len(empty_rows)} completely empty rows (will be removed)")
    
    # Validate email formats
    invalid_emails = []
    for idx, email in enumerate(df['email']):
        if not validate_email_format(email):
            invalid_emails.append(f"Row {idx+1}: '{email}'")
    
    if invalid_emails:
        warnings.append(f"⚠️ Invalid email formats found in {len(invalid_emails)} rows")
        if len(invalid_emails) <= 3:
            warnings.append(f"Examples: {'; '.join(invalid_emails[:3])}")
    
    # Check for missing critical data
    missing_names = df['name'].isnull().sum()
    missing_companies = df['company'].isnull().sum()
    missing_titles = df['job_title'].isnull().sum()
    
    if missing_names > 0:
        warnings.append(f"⚠️ {missing_names} leads missing names (will use 'Unknown')")
    if missing_companies > 0:
        warnings.append(f"⚠️ {missing_companies} leads missing company names")
    if missing_titles > 0:
        warnings.append(f"⚠️ {missing_titles} leads missing job titles (will affect scoring)")
    
    # Check company size format
    invalid_sizes = 0
    for size in df['company_size']:
        if pd.notna(size):
            try:
                int(size)
            except (ValueError, TypeError):
                invalid_sizes += 1
    
    if invalid_sizes > 0:
        warnings.append(f"⚠️ {invalid_sizes} leads have invalid company sizes (will use 0)")
    
    # Data quality summary
    total_leads = len(df)
    clean_leads = total_leads - len(empty_rows)
    
    if clean_leads != total_leads:
        warnings.append(f"📊 Processing {clean_leads} out of {total_leads} total rows")
    
    return issues, warnings, True

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
    """Load the complex test dataset for users to download and test."""
    try:
        # Load the complex test dataset from data folder
        complex_csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'complex_test_leads.csv')
        if os.path.exists(complex_csv_path):
            return pd.read_csv(complex_csv_path)
        else:
            # Fallback to simple sample if complex dataset not found
            sample_data = {
                'name': ['John Smith', 'Sarah Johnson', 'Mike Chen', 'Lisa Brown'],
                'email': ['john.smith@techcorp.com', 'sarah.j@gmail.com', 'mike.chen@startup.io', 'lisa@enterprise.com'],
                'company': ['TechCorp Inc', 'Freelance', 'StartupIO', 'Enterprise Solutions'],
                'job_title': ['Sales Manager', 'Marketing Consultant', 'Product Manager', 'CEO'],
                'company_size': [120, 1, 25, 500]
            }
            return pd.DataFrame(sample_data)
    except Exception as e:
        # Fallback to simple sample if any error occurs
        st.error(f"Note: Using simple sample data (complex dataset unavailable: {str(e)})")
        sample_data = {
            'name': ['John Smith', 'Sarah Johnson', 'Mike Chen', 'Lisa Brown'],
            'email': ['john.smith@techcorp.com', 'sarah.j@gmail.com', 'mike.chen@startup.io', 'lisa@enterprise.com'],
            'company': ['TechCorp Inc', 'Freelance', 'StartupIO', 'Enterprise Solutions'],
            'job_title': ['Sales Manager', 'Marketing Consultant', 'Product Manager', 'CEO'],
            'company_size': [120, 1, 25, 500]
        }
        return pd.DataFrame(sample_data)

def show_manual_column_mapping_interface(df, missing_columns, mapper):
    """
    Display manual column mapping interface when auto-mapping fails.
    
    Args:
        df (pd.DataFrame): Original DataFrame with unmapped columns
        missing_columns (List[str]): Columns that need manual mapping
        mapper (ColumnMapper): Column mapper instance
        
    Returns:
        dict: Manual mapping selections {standard_name: original_column}
    """
    st.markdown("---")
    st.subheader("🔧 Manual Column Mapping Required")
    st.info("Some columns couldn't be automatically mapped. Please help us identify them below:")
    
    # Get suggestions for missing columns
    suggestions = mapper.suggest_manual_mappings(df, missing_columns)
    
    # Create manual mapping interface
    manual_mapping = {}
    available_columns = ['None'] + list(df.columns)
    
    # Create columns for better layout
    col1, col2 = st.columns(2)
    
    for i, required_col in enumerate(missing_columns):
        # Alternate columns for better layout
        with col1 if i % 2 == 0 else col2:
            st.markdown(f"**Map '{required_col}' to:**")
            
            # Show column info to help user decide
            with st.expander(f"📊 Available columns preview", expanded=False):
                for col in df.columns:
                    content_type = mapper.detect_column_content_type(df, col)
                    sample_values = df[col].dropna().head(3).tolist()
                    sample_str = ', '.join([str(val)[:30] for val in sample_values])
                    
                    # Highlight suggested columns
                    if col in suggestions.get(required_col, []):
                        st.success(f"**{col}** (type: {content_type}) - *Suggested*")
                        st.success(f"Sample: {sample_str}")
                    else:
                        st.write(f"**{col}** (type: {content_type})")
                        st.write(f"Sample: {sample_str}")
            
            # Create selectbox with suggestions at the top
            suggested_options = suggestions.get(required_col, [])
            if suggested_options:
                ordered_options = ['None'] + suggested_options + [col for col in df.columns if col not in suggested_options]
            else:
                ordered_options = available_columns
            
            selected = st.selectbox(
                f"Select column for '{required_col}':",
                ordered_options,
                key=f"manual_map_{required_col}",
                help=f"Choose which column contains {required_col} data"
            )
            
            manual_mapping[required_col] = selected if selected != 'None' else None
            
            st.markdown("---")
    
    return manual_mapping

def show_column_mapping_results(mapping_log):
    """
    Display column mapping results in a user-friendly way.
    
    Args:
        mapping_log (List[str]): List of mapping descriptions
    """
    if mapping_log:
        st.success("🔄 **Column Mapping Applied:**")
        for mapping in mapping_log:
            st.success(f"✅ {mapping}")
        st.info("💡 **Your CSV columns have been automatically standardized for processing!**")
    else:
        st.info("✅ **Perfect!** Your CSV columns are already in the standard format.")

def main():
    st.title("🎯 Lead Prioritization Tool")
    st.markdown("### Upload CSV → Score Leads → Generate Outreach")
    st.markdown("---")
    
    # Initialize scorer
    if 'scorer' not in st.session_state:
        st.session_state.scorer = LeadScorer()
    
    # Sidebar with instructions and tips
    st.sidebar.header("📋 Instructions")
    st.sidebar.markdown("""
    **Required Data Fields:**
    - **Name**: Lead's full name
    - **Email**: Email address  
    - **Company**: Company name
    - **Job Title**: Job title/position
    - **Company Size**: Number of employees
    
    🔄 **Flexible Column Names**: Your CSV columns will be automatically mapped! Use any reasonable column names like 'Title' instead of 'job_title'.
    
    **Scoring Rules:**
    - 🟢 **High**: Senior titles + corporate email + large company
    - 🟡 **Medium**: Some qualifying factors
    - 🔴 **Low**: Few/no qualifying factors
    """)
    
    # Helpful tips section
    st.sidebar.markdown("---")
    st.sidebar.header("💡 Pro Tips")
    
    tips = [
        "🎯 **Sort by High priority first** for maximum efficiency",
        "📋 **Use the 40-lead sample CSV** to test all features",
        "⚙️ **Abbreviations work**: 'Sr. VP', 'Mgr', 'Dir' are recognized", 
        "🏢 **Company sizes can be text**: 'Startup', 'Medium', '50+' all work",
        "📧 **Corporate emails score higher** than Gmail/Yahoo",
        "📤 **Export high-priority leads** for focused outreach",
        "🌐 **International names supported**: Special characters handled",
        "🏢 **Multiple industries**: Sample includes 10 different business sectors"
    ]
    
    # Show tips with some personality
    for tip in tips:
        st.sidebar.info(tip)
    
    # Sample CSV download
    sample_df = create_sample_csv()
    csv_buffer = io.StringIO()
    sample_df.to_csv(csv_buffer, index=False)
    st.sidebar.download_button(
        label="📥 Download Sample CSV",
        data=csv_buffer.getvalue(),
        file_name="sample_leads.csv",
        mime="text/csv",
        help="Download a realistic 40-lead dataset with complex formatting and multiple industries for testing"
    )

    # Optional enhancements
    st.sidebar.markdown("---")
    st.sidebar.header("⚙️ Optional Enhancements")
    enhance_enrichment = st.sidebar.checkbox("Enrich data (domain, industry)", value=True)
    dedup_by_email = st.sidebar.checkbox("Deduplicate by email", value=False)
    explain_scores = st.sidebar.checkbox("Explain scores (why?)", value=True)
    
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
                with st.spinner('📋 Loading and validating your CSV...'):
                    df = pd.read_csv(uploaded_file)
                    
                    # Initialize column mapper
                    mapper = ColumnMapper()
                    
                    # Step 1: Auto-map columns
                    mapped_df, mapping_log, column_mapping = mapper.auto_map_columns(df)
                    
                    # Step 2: Check for missing columns after auto-mapping
                    missing_columns, available_columns = mapper.validate_required_columns(mapped_df)
                    
                    # Step 3: Show mapping results
                    if mapping_log:
                        show_column_mapping_results(mapping_log)
                    
                    # Step 4: Handle missing columns with manual mapping
                    if missing_columns:
                        st.warning(f"⚠️ **Missing columns after auto-mapping:** {', '.join(missing_columns)}")
                        
                        # Show manual mapping interface
                        manual_mapping = show_manual_column_mapping_interface(df, missing_columns, mapper)
                        
                        # Apply manual mapping button
                        if st.button("🔄 Apply Manual Mapping", type="primary"):
                            manual_mapped_df, manual_mapping_log = mapper.apply_manual_mapping(mapped_df, manual_mapping)
                            
                            # Validate again after manual mapping
                            final_missing, _ = mapper.validate_required_columns(manual_mapped_df)
                            
                            if final_missing:
                                st.error(f"😱 **Still missing required columns:** {', '.join(final_missing)}")
                                st.error("📝 **Please map all required columns to proceed.**")
                                st.stop()
                            else:
                                mapped_df = manual_mapped_df
                                if manual_mapping_log:
                                    show_column_mapping_results(manual_mapping_log)
                                st.success("✅ **All columns mapped successfully!**")
                        else:
                            st.info("👆 **Click 'Apply Manual Mapping' above to proceed with lead scoring.**")
                            st.stop()
                    
                    # Step 5: Enhanced validation on mapped data
                    issues, warnings, is_valid = validate_csv_data(mapped_df)
                    
                    # Display validation results
                    if issues:
                        st.error("😱 **Critical Issues Found:**")
                        for issue in issues:
                            st.error(issue)
                        st.error("📝 **Please fix these issues and re-upload your CSV.**")
                        st.stop()
                    
                    if warnings:
                        st.warning("⚠️ **Data Quality Warnings:**")
                        for warning in warnings:
                            st.warning(warning)
                        st.info("🚀 **Don't worry - we'll handle these automatically and proceed with scoring!**")
                    
                    # Step 6: Clean the data
                    df_clean = mapped_df.dropna(how='all')  # Remove completely empty rows
                    df_clean['name'] = df_clean['name'].fillna('Unknown')
                    df_clean['company'] = df_clean['company'].fillna('Unknown Company')
                    df_clean['job_title'] = df_clean['job_title'].fillna('Unknown')
                    
                    # Clean company_size
                    def clean_company_size(size):
                        if pd.isna(size):
                            return 0
                        try:
                            return int(size)
                        except (ValueError, TypeError):
                            return 0
                    
                    df_clean['company_size'] = df_clean['company_size'].apply(clean_company_size)

                    # Optional enrichment & deduplication (non-destructive to original)
                    df_to_score = df_clean.copy()
                    if enhance_enrichment:
                        df_to_score, enrich_report = enrich_leads(df_to_score)
                        st.info(f"🔎 Enriched data: {enrich_report['rows']} rows | Duplicate emails flagged: {enrich_report['duplicate_email_count']}")
                    if dedup_by_email:
                        before = len(df_to_score)
                        df_to_score = df_to_score.drop_duplicates(subset=['email'], keep='first')
                        st.info(f"🧹 Deduplicated by email: removed {before - len(df_to_score)} duplicates")
                
                with st.spinner('🎯 Scoring your leads...'):
                    # Apply scoring
                    if explain_scores:
                        scored_df = st.session_state.scorer.score_leads_batch_with_explain(df_to_score)
                    else:
                        scored_df = st.session_state.scorer.score_leads_batch(df_to_score)
                    
                st.success(f"✅ **Upload Complete!** Successfully processed {len(scored_df)} leads.")
                
                # Display stats
                total_leads = len(scored_df)
                high_count = len(scored_df[scored_df['score'] == 'High'])
                medium_count = len(scored_df[scored_df['score'] == 'Medium'])
                low_count = len(scored_df[scored_df['score'] == 'Low'])
                
                st.metric("Total Leads", total_leads)
                st.metric("🟢 High Priority", high_count)
                st.metric("🟡 Medium Priority", medium_count)
                st.metric("🔴 Low Priority", low_count)
                
            except pd.errors.EmptyDataError:
                st.error("😵 **File is empty** - Please upload a CSV file with lead data.")
                st.stop()
            except pd.errors.ParserError as e:
                st.error(f"😵 **CSV Format Error** - Unable to parse the file: {str(e)}")
                st.info("📝 **Tip:** Make sure your file is a valid CSV with proper formatting.")
                st.stop()
            except UnicodeDecodeError:
                st.error("😵 **Encoding Error** - Unable to read the file encoding.")
                st.info("📝 **Tip:** Save your CSV as UTF-8 encoding and try again.")
                st.stop()
            except Exception as e:
                st.error(f"😵 **Unexpected Error:** {str(e)}")
                st.error("📝 **Please check your CSV file and try again, or contact support.**")
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

        # Add compact "Why" summary if explanations are available
        if explain_scores and 'score_reasons' in display_df.columns:
            def _short_why(text):
                try:
                    s = str(text)
                except Exception:
                    return ''
                tags = []
                if 'senior title' in s or 'executive title' in s:
                    tags.append('Title')
                if 'corporate email' in s:
                    tags.append('Email')
                if 'company size' in s:
                    tags.append('Size')
                return ' | '.join(tags)
            display_df['Why'] = display_df['score_reasons'].apply(_short_why)
            # Hide verbose explanation columns in the table
            for col in ['score_reasons', 'score_points']:
                if col in display_df.columns:
                    display_df.drop(columns=[col], inplace=True)
        
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
            st.info("🎯 **Pro Tip:** Focus on high-priority leads first - they have the highest conversion potential!")
            
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
                st.info("📊 **No high-priority leads found.**")
                st.markdown("""
                **Tips to get high-priority leads:**
                - Look for leads with senior job titles (Manager, Director, VP, CEO)
                - Include leads from medium/large companies (25+ employees)
                - Use corporate email addresses rather than personal ones
                - Try the sample CSV to see how scoring works!
                """)
                
        # Export functionality
        st.markdown("---")
        st.subheader("📥 Export Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Export scored leads CSV
            csv_buffer = io.StringIO()
            scored_df.to_csv(csv_buffer, index=False)
            
            if st.download_button(
                label="📈 Download Scored Leads CSV",
                data=csv_buffer.getvalue(),
                file_name="scored_leads.csv",
                mime="text/csv",
                help="Download the complete dataset with scores",
                key="download_all"
            ):
                st.success("✅ **Complete dataset downloaded!** Ready for your sales team.")
        
        with col2:
            # Export high priority leads only
            high_priority_df = scored_df[scored_df['score'] == 'High']
            if len(high_priority_df) > 0:
                high_csv_buffer = io.StringIO()
                high_priority_df.to_csv(high_csv_buffer, index=False)
                if st.download_button(
                    label="⭐ Download High Priority Only",
                    data=high_csv_buffer.getvalue(),
                    file_name="high_priority_leads.csv",
                    mime="text/csv",
                    help="Download only high-priority leads",
                    key="download_high"
                ):
                    st.success(f"✅ **{len(high_priority_df)} high-priority leads downloaded!** Focus on these first.")
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
            if st.download_button(
                label="📉 Download Summary Report",
                data=summary_csv_buffer.getvalue(),
                file_name="lead_scoring_summary.csv",
                mime="text/csv",
                help="Download scoring summary metrics",
                key="download_summary"
            ):
                st.success("✅ **Summary report downloaded!** Great for stakeholder updates.")
    
    else:
        # Show sample data when no file is uploaded
        st.markdown("---")
        st.subheader("📋 Sample Lead Data (Demo)")
        st.info("Upload your CSV file above to see prioritized leads, or download our realistic 40-lead sample CSV to test all features.")
        
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
