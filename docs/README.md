# 🎯 Lead Prioritization Tool

## Caprae Capital AI-Readiness Challenge

### Overview
A lightweight lead prioritization tool that helps sales teams quickly identify and rank high-value leads from CSV uploads.

*Why I built this: After talking with sales teams, I realized they're drowning in leads but starving for priorities. This tool was designed to solve that specific pain point - transforming chaos into actionable insights in seconds.*

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
*Getting started is intentionally simple - I wanted anyone to be able to test this in under 2 minutes:*

1. Install dependencies:
   ```bash
   pip install pandas streamlit
   ```

2. Run the application (either of the following):
   ```bash
   # Recommended launcher
   python run_app.py

   # Or run Streamlit directly
   streamlit run src/app.py
   ```

*Pro tip: Try the sample CSV download first - it's designed with realistic, messy data that showcases the scoring logic.*

### File Structure
- `src/app.py` - Main Streamlit application
- `src/core/scoring_engine.py` - Lead scoring logic (modular)
- `src/modules/outreach_templates.py` - Email templates and openers  
- `src/modules/column_mapper.py` - CSV auto/ manual mapping
- `src/modules/industry_detector.py` - Industry classification
- `src/modules/industry_templates.py` - Industry-specific templates
- `tests/unit/` - Test suite
- `docs/` - Full documentation (see PROJECT_STRUCTURE.md for complete tree)

### Future Roadmap
- ML-based scoring model integration
- LinkedIn/CRM integrations
- SaaS deployment with authentication
