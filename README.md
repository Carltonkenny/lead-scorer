# 🎯 Lead Prioritization Tool

## Caprae Capital AI-Readiness Challenge

### Overview
A lightweight lead prioritization tool that helps sales teams quickly identify and rank high-value leads from CSV uploads.

### Key Features
- **CSV Upload**: Import lead data from spreadsheets
- **Rule-based Scoring**: Automatic lead qualification and prioritization  
- **Color-coded Display**: Visual indicators for High/Medium/Low priority leads
- **Outreach Suggestions**: Mini templates and personalized openers
- **Export Functionality**: Download enriched lead data

### Business Value Proposition
- **Speed**: Quick lead assessment saves prospecting time
- **Relevance**: Rule-based filters focus on quality leads  
- **Usability**: Clean interface with actionable insights

### Tech Stack
- **Frontend**: Streamlit
- **Data Processing**: Pandas
- **Scoring Engine**: Rule-based (modular for future ML upgrade)

### Setup Instructions
1. Install dependencies:
   ```bash
   pip install pandas streamlit
   ```

2. Run the application:
   ```bash
   streamlit run app.py
   ```

### File Structure
- `app.py` - Main Streamlit application
- `scoring_engine.py` - Lead scoring logic (modular)
- `outreach_templates.py` - Email templates and openers  
- `logs.md` - Development progress log

### Future Roadmap
- ML-based scoring model integration
- LinkedIn scraping capabilities
- SaaS deployment with authentication