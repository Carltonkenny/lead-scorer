# Lightweight enrichment utilities (no external dependencies)
# Adds useful context for prioritization without altering required inputs

from typing import Tuple, Dict
import pandas as pd
from industry_detector import IndustryDetector


def _extract_email_domain(email: str) -> str:
    if not isinstance(email, str):
        try:
            email = str(email)
        except Exception:
            return ''
    email = email.strip().lower()
    if '@' not in email:
        return ''
    try:
        domain = email.split('@')[1].strip()
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain
    except Exception:
        return ''


def _is_corporate_domain(domain: str) -> bool:
    if not domain:
        return False
    personal = {
        'gmail.com','yahoo.com','hotmail.com','outlook.com','aol.com','icloud.com','live.com','msn.com','mail.com','protonmail.com','yandex.com','qq.com','sina.com','zoho.com'
    }
    return domain not in personal


def _guess_website(domain: str) -> str:
    if not domain:
        return ''
    # Very simple guess (kept offline-friendly)
    return f"https://{domain}"


def enrich_leads(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, int]]:
    """
    Add light enrichment columns:
    - email_domain
    - is_corporate_email (bool)
    - website_guess (https://domain)
    - industry (via IndustryDetector using company + domain)
    - duplicate_email (bool)
    - duplicate_name_company (bool)

    Returns the enriched DataFrame and a small report dict.
    """
    detector = IndustryDetector()

    enriched = df.copy()

    # Email domain and corporate flag
    enriched['email_domain'] = enriched['email'].apply(_extract_email_domain)
    enriched['is_corporate_email'] = enriched['email_domain'].apply(_is_corporate_domain)

    # Website guess
    enriched['website_guess'] = enriched['email_domain'].apply(_guess_website)

    # Industry detection
    def _detect(row):
        company = row.get('company', '')
        domain = row.get('email_domain', '')
        return detector.detect_industry(company, domain)
    enriched['industry'] = enriched.apply(_detect, axis=1)

    # Duplicates
    enriched['duplicate_email'] = enriched.duplicated(subset=['email'], keep='first')
    # Name+company duplicate marker (normalized to lower + stripped)
    def _name_company_key(row):
        name = str(row.get('name', '') or '').strip().lower()
        company = str(row.get('company', '') or '').strip().lower()
        return f"{name}|{company}"
    enriched['_name_company_key'] = enriched.apply(_name_company_key, axis=1)
    enriched['duplicate_name_company'] = enriched.duplicated(subset=['_name_company_key'], keep='first')
    enriched.drop(columns=['_name_company_key'], inplace=True)

    report = {
        'rows': len(enriched),
        'duplicate_email_count': int(enriched['duplicate_email'].sum()),
        'duplicate_name_company_count': int(enriched['duplicate_name_company'].sum())
    }

    return enriched, report