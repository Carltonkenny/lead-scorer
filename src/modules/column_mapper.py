# Column Mapping Module
# Auto-detects and maps various CSV column name variations to standard format

import pandas as pd
import re
from typing import Dict, List, Tuple, Optional

class ColumnMapper:
    """
    Handles automatic detection and mapping of CSV columns to standard format.
    Supports 25+ column name variations for flexible CSV compatibility.
    """
    
    def __init__(self):
        # Standard column mappings with common variations
        self.column_mappings = {
            'name': [
                'name', 'full_name', 'fullname', 'contact_name', 'lead_name', 
                'person', 'first_name', 'last_name', 'full name', 'contact name',
                'lead name', 'person name', 'individual', 'prospect_name',
                'prospect name', 'client_name', 'client name', 'customer_name',
                'customer name', 'firstname', 'lastname', 'fname', 'lname'
            ],
            'email': [
                'email', 'email_address', 'contact_email', 'e_mail', 
                'mail', 'email address', 'e-mail', 'contact email',
                'e mail', 'electronic_mail', 'electronic mail', 'email_addr',
                'email addr', 'mailbox', 'mail_address', 'mail address',
                'contact_mail', 'contact mail', 'business_email', 'business email'
            ],
            'company': [
                'company', 'company_name', 'organization', 'business', 
                'firm', 'company name', 'org', 'corporation', 'enterprise',
                'employer', 'workplace', 'business_name', 'business name',
                'org_name', 'org name', 'organization_name', 'organization name',
                'client_company', 'client company', 'account', 'account_name'
            ],
            'job_title': [
                'job_title', 'title', 'position', 'role', 'job', 
                'designation', 'job title', 'job_role', 'work_title',
                'work title', 'position_title', 'position title', 'post',
                'occupation', 'function', 'job_function', 'job function',
                'work_role', 'work role', 'professional_title', 'professional title'
            ],
            'company_size': [
                'company_size', 'size', 'employees', 'team_size', 
                'staff_count', 'company size', 'employee_count', 'headcount',
                'staff_size', 'staff size', 'workforce', 'team_count',
                'team count', 'personnel', 'staff', 'employee_total',
                'employee total', 'total_employees', 'total employees', 'emp_count'
            ]
        }
        
        # Additional patterns for fuzzy matching
        self.fuzzy_patterns = {
            'name': [r'.*name.*', r'.*person.*', r'.*contact.*'],
            'email': [r'.*email.*', r'.*mail.*', r'.*@.*'],
            'company': [r'.*company.*', r'.*org.*', r'.*business.*', r'.*firm.*'],
            'job_title': [r'.*title.*', r'.*position.*', r'.*role.*', r'.*job.*'],
            'company_size': [r'.*size.*', r'.*employee.*', r'.*staff.*', r'.*team.*']
        }
    
    def auto_map_columns(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str], Dict[str, str]]:
        """
        Automatically detect and map column variations to standard format.
        
        Args:
            df (pd.DataFrame): Input DataFrame with various column names
            
        Returns:
            tuple: (mapped_df, mapping_log, column_mapping)
                - mapped_df: DataFrame with standardized column names
                - mapping_log: List of mapping descriptions
                - column_mapping: Dictionary of actual mappings applied
        """
        mapped_df = df.copy()
        mapping_log = []
        column_mapping = {}
        
        # Get original columns in lowercase for matching
        original_columns = df.columns.tolist()
        columns_lower = [col.lower().strip() for col in original_columns]
        
        for standard_name, variations in self.column_mappings.items():
            found_column = None
            original_column = None
            
            # First, try exact match (case-insensitive)
            for i, col_lower in enumerate(columns_lower):
                if col_lower in [var.lower() for var in variations]:
                    found_column = col_lower
                    original_column = original_columns[i]
                    break
            
            # If no exact match, try fuzzy pattern matching
            if not found_column:
                for pattern in self.fuzzy_patterns.get(standard_name, []):
                    for i, col_lower in enumerate(columns_lower):
                        if re.match(pattern, col_lower):
                            found_column = col_lower
                            original_column = original_columns[i]
                            break
                    if found_column:
                        break
            
            # Apply mapping if column found
            if found_column and original_column != standard_name:
                mapped_df = mapped_df.rename(columns={original_column: standard_name})
                mapping_log.append(f"Mapped '{original_column}' → '{standard_name}'")
                column_mapping[standard_name] = original_column
        
        return mapped_df, mapping_log, column_mapping
    
    def validate_required_columns(self, df: pd.DataFrame) -> Tuple[List[str], List[str]]:
        """
        Validate that all required columns are present after mapping.
        
        Args:
            df (pd.DataFrame): DataFrame to validate
            
        Returns:
            tuple: (missing_columns, available_columns)
        """
        required_columns = ['name', 'email', 'company', 'job_title', 'company_size']
        available_columns = df.columns.tolist()
        missing_columns = [col for col in required_columns if col not in available_columns]
        
        return missing_columns, available_columns
    
    def suggest_manual_mappings(self, df: pd.DataFrame, missing_columns: List[str]) -> Dict[str, List[str]]:
        """
        Suggest possible manual mappings for missing columns.
        
        Args:
            df (pd.DataFrame): DataFrame with unmapped columns
            missing_columns (List[str]): Columns that couldn't be auto-mapped
            
        Returns:
            Dict[str, List[str]]: Suggested mappings for each missing column
        """
        suggestions = {}
        available_columns = df.columns.tolist()
        
        for missing_col in missing_columns:
            suggestions[missing_col] = []
            
            # Look for columns that might match based on patterns
            for col in available_columns:
                col_lower = col.lower().strip()
                
                # Check against fuzzy patterns
                for pattern in self.fuzzy_patterns.get(missing_col, []):
                    if re.match(pattern, col_lower):
                        if col not in suggestions[missing_col]:
                            suggestions[missing_col].append(col)
                
                # Check for partial string matches
                if missing_col.lower() in col_lower or col_lower in missing_col.lower():
                    if col not in suggestions[missing_col]:
                        suggestions[missing_col].append(col)
        
        return suggestions
    
    def apply_manual_mapping(self, df: pd.DataFrame, manual_mapping: Dict[str, str]) -> Tuple[pd.DataFrame, List[str]]:
        """
        Apply manual column mappings specified by user.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            manual_mapping (Dict[str, str]): Manual mappings {standard_name: original_column}
            
        Returns:
            tuple: (mapped_df, mapping_log)
        """
        mapped_df = df.copy()
        mapping_log = []
        
        for standard_name, original_column in manual_mapping.items():
            if original_column and original_column != 'None' and original_column in df.columns:
                if original_column != standard_name:
                    mapped_df = mapped_df.rename(columns={original_column: standard_name})
                    mapping_log.append(f"Manual mapping: '{original_column}' → '{standard_name}'")
        
        return mapped_df, mapping_log
    
    def get_column_info(self, df: pd.DataFrame) -> Dict[str, Dict]:
        """
        Get information about columns for debugging and user feedback.
        
        Args:
            df (pd.DataFrame): DataFrame to analyze
            
        Returns:
            Dict[str, Dict]: Column information including data types and sample values
        """
        column_info = {}
        
        for col in df.columns:
            # Get basic info
            col_info = {
                'dtype': str(df[col].dtype),
                'non_null_count': df[col].count(),
                'null_count': df[col].isnull().sum(),
                'unique_count': df[col].nunique()
            }
            
            # Get sample values (non-null)
            sample_values = df[col].dropna().head(3).tolist()
            col_info['sample_values'] = [str(val) for val in sample_values]
            
            column_info[col] = col_info
        
        return column_info
    
    def detect_column_content_type(self, df: pd.DataFrame, column_name: str) -> str:
        """
        Analyze column content to help suggest appropriate mappings.
        
        Args:
            df (pd.DataFrame): DataFrame containing the column
            column_name (str): Name of column to analyze
            
        Returns:
            str: Detected content type (email, name, company, etc.)
        """
        if column_name not in df.columns:
            return 'unknown'
        
        col_data = df[column_name].dropna().astype(str)
        
        if len(col_data) == 0:
            return 'empty'
        
        # Check for email patterns
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        email_matches = col_data.str.contains(email_pattern, na=False).sum()
        if email_matches > len(col_data) * 0.5:  # 50% threshold
            return 'email'
        
        # Check for name patterns (contains space, common name patterns)
        space_count = col_data.str.contains(' ', na=False).sum()
        if space_count > len(col_data) * 0.3:  # 30% threshold
            return 'name'
        
        # Check for company patterns (contains common business words)
        company_words = ['inc', 'corp', 'ltd', 'llc', 'company', 'co', 'group', 'solutions', 'services']
        company_matches = 0
        for word in company_words:
            company_matches += col_data.str.contains(word, case=False, na=False).sum()
        
        if company_matches > len(col_data) * 0.2:  # 20% threshold
            return 'company'
        
        # Check for job title patterns
        title_words = ['manager', 'director', 'ceo', 'president', 'vice', 'senior', 'lead', 'head', 'officer']
        title_matches = 0
        for word in title_words:
            title_matches += col_data.str.contains(word, case=False, na=False).sum()
        
        if title_matches > len(col_data) * 0.2:  # 20% threshold
            return 'job_title'
        
        # Check for numeric patterns (company size)
        try:
            numeric_convertible = pd.to_numeric(col_data, errors='coerce').count()
            if numeric_convertible > len(col_data) * 0.5:  # 50% threshold
                return 'company_size'
        except:
            pass
        
        return 'text'

# Convenience functions for easy import
def auto_map_csv_columns(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str], Dict[str, str]]:
    """
    Convenience function to auto-map columns without instantiating class.
    
    Args:
        df (pd.DataFrame): Input DataFrame
        
    Returns:
        tuple: (mapped_df, mapping_log, column_mapping)
    """
    mapper = ColumnMapper()
    return mapper.auto_map_columns(df)

def validate_csv_columns(df: pd.DataFrame) -> Tuple[List[str], List[str]]:
    """
    Convenience function to validate required columns.
    
    Args:
        df (pd.DataFrame): DataFrame to validate
        
    Returns:
        tuple: (missing_columns, available_columns)
    """
    mapper = ColumnMapper()
    return mapper.validate_required_columns(df)