# Test Data Generator Module
# Creates realistic, complex datasets for testing lead scoring system

import pandas as pd
import random
import numpy as np
from typing import List, Dict

class ComplexTestDataGenerator:
    """
    Generates realistic test datasets with various complexities and edge cases.
    Simulates real-world data quality issues for robust testing.
    """
    
    def __init__(self):
        # Industry distribution for realistic mix
        self.industry_companies = {
            'technology': [
                'TechInnovate Inc', 'DataCloud Solutions', 'AI Dynamics Corp', 'CodeStream Ltd',
                'DevOps Pro', 'CyberGuard Systems', 'CloudFirst Technologies', 'InnovateTech Co'
            ],
            'healthcare': [
                'MedCare Solutions', 'HealthTech Innovations', 'BioMed Research Corp', 'CareFirst Medical',
                'Pharma Dynamics Ltd', 'MedDevice Solutions', 'HealthSystem Pro', 'BioCare Inc'
            ],
            'finance': [
                'Capital Ventures LLC', 'FinTech Solutions', 'Investment Partners Inc', 'SecureBank Corp',
                'Financial Advisors Group', 'CreditFlow Systems', 'WealthManagement Pro', 'BankTech Ltd'
            ],
            'manufacturing': [
                'Industrial Solutions Corp', 'ManuTech Systems', 'Production Dynamics', 'Factory Innovations',
                'Assembly Line Pro', 'Manufacturing Excellence', 'Industrial Automation Inc', 'ProductionFirst'
            ],
            'retail': [
                'RetailPro Solutions', 'Commerce Dynamics', 'ShoppingTech Inc', 'Merchant Systems',
                'E-Commerce Partners', 'Retail Innovations Corp', 'StoreTech Solutions', 'MarketPlace Pro'
            ],
            'consulting': [
                'Strategic Advisors LLC', 'Business Excellence Corp', 'ConsultingPro Partners', 'Advisory Solutions',
                'Management Consultants Inc', 'Strategy Partners Ltd', 'Business Dynamics Group', 'Excellence Advisors'
            ],
            'education': [
                'EduTech Solutions', 'Learning Dynamics Corp', 'Academic Excellence Inc', 'Education Innovations',
                'SchoolTech Systems', 'Learning Partners LLC', 'EduSolutions Pro', 'Academic Advisors Group'
            ],
            'real_estate': [
                'Property Solutions Inc', 'RealEstate Dynamics', 'Housing Partners LLC', 'Property Pro Corp',
                'Real Estate Innovations', 'Development Partners', 'PropertyTech Solutions', 'Realty Advisors'
            ],
            'energy': [
                'Green Energy Corp', 'Renewable Solutions Inc', 'PowerTech Dynamics', 'Energy Innovations LLC',
                'SolarFirst Systems', 'EcoEnergy Partners', 'Sustainable Power Inc', 'CleanTech Solutions'
            ],
            'media': [
                'MediaTech Corp', 'Creative Solutions Inc', 'ContentFirst LLC', 'Digital Media Partners',
                'BrandTech Systems', 'Marketing Dynamics', 'Media Innovations Corp', 'Creative Partners Pro'
            ]
        }
        
        # Complex job title variations with abbreviations and regional differences
        self.complex_job_titles = [
            'Sr. VP Sales & Marketing', 'Chief Technology Officer', 'Marketing Dir., EMEA',
            'Head of Business Development', 'Senior Software Eng.', 'VP of Operations',
            'Director, Strategic Partnerships', 'Regional Sales Mgr', 'Principal Product Manager',
            'EVP, Global Sales', 'Asst. Director of Marketing', 'Lead Data Scientist',
            'Sr. Manager, Business Intelligence', 'Director of Customer Success', 'VP, Finance & Operations',
            'Chief Marketing Officer', 'Head of People & Culture', 'Principal Consultant',
            'Sr. Business Analyst', 'Director, Product Strategy', 'VP of Engineering',
            'Marketing Manager (APAC)', 'Head of Sales Operations', 'Senior Account Executive',
            'Director, Digital Marketing', 'VP, Strategic Accounts', 'Lead UX Designer',
            'Sr. Project Manager', 'Director of Business Operations', 'Chief Financial Officer',
            'Head of Customer Experience', 'Principal Software Architect', 'VP, Corporate Development',
            'Senior Marketing Specialist', 'Director, Human Resources', 'Chief Operating Officer',
            'Lead Business Development Rep', 'Sr. Financial Analyst', 'Director, Sales Enablement',
            'VP, Product Marketing', 'Head of Revenue Operations', 'Principal Data Engineer'
        ]
        
        # Realistic name combinations with international variety
        self.first_names = [
            'John', 'Sarah', 'Michael', 'Emily', 'David', 'Jessica', 'Robert', 'Ashley',
            'James', 'Amanda', 'Christopher', 'Melissa', 'Matthew', 'Michelle', 'Daniel', 'Lisa',
            'Anthony', 'Karen', 'Mark', 'Nancy', 'Paul', 'Betty', 'Steven', 'Helen',
            'Raj', 'Priya', 'Chen', 'Li', 'Ahmed', 'Fatima', 'Carlos', 'Maria',
            'Hans', 'Ingrid', 'Pierre', 'Sophie', 'Yuki', 'Akiko', 'Ivan', 'Olga'
        ]
        
        self.last_names = [
            'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
            'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas',
            'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson', 'White',
            'Patel', 'Kumar', 'Singh', 'Wang', 'Zhang', 'Chen', 'Al-Ahmad', 'Hassan',
            'Mueller', 'Schmidt', 'Dubois', 'Martin', 'Tanaka', 'Sato', 'Petrov', 'Volkov'
        ]
        
        # Company size variations (including text formats)
        self.company_sizes = [
            1, 5, 12, 25, 45, 67, 89, 120, 200, 350, 500, 750, 1000, 1500, 2500,
            'Startup', '50-100', 'Large', 'Enterprise', '1,200 employees', '25+', 'SMB',
            'Medium', '2,500+', 'Small Business', '100-500', '500+', 'Mid-size'
        ]
        
        # Email domain mix (corporate and personal)
        self.corporate_domains = ['corp.com', 'inc.com', 'solutions.com', 'tech.io', 'pro.biz', 'group.org', 'systems.net']
        self.personal_domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'aol.com']
        
    def generate_complex_dataset(self, num_leads: int = 40) -> pd.DataFrame:
        """
        Generate complex test dataset with realistic data quality issues.
        
        Args:
            num_leads (int): Number of leads to generate
            
        Returns:
            pd.DataFrame: Complex test dataset
        """
        leads_data = []
        
        # Ensure industry distribution
        industries = list(self.industry_companies.keys())
        leads_per_industry = num_leads // len(industries)
        extra_leads = num_leads % len(industries)
        
        lead_count = 0
        
        for i, industry in enumerate(industries):
            # Calculate leads for this industry
            industry_lead_count = leads_per_industry
            if i < extra_leads:
                industry_lead_count += 1
            
            # Generate leads for this industry
            for _ in range(industry_lead_count):
                lead = self._generate_single_lead(industry, lead_count)
                leads_data.append(lead)
                lead_count += 1
        
        # Create DataFrame
        df = pd.DataFrame(leads_data)
        
        # Apply data quality issues
        df = self._apply_data_quality_issues(df)
        
        return df
    
    def _generate_single_lead(self, industry: str, lead_index: int) -> Dict:
        """
        Generate a single lead with realistic data.
        
        Args:
            industry (str): Industry for the lead
            lead_index (int): Index for deterministic variation
            
        Returns:
            Dict: Lead data
        """
        # Generate name with some variations
        first_name = random.choice(self.first_names)
        last_name = random.choice(self.last_names)
        
        # Name format variations
        name_formats = [
            f"{first_name} {last_name}",
            f"{first_name.upper()} {last_name.upper()}",  # All caps
            f"{first_name.lower()} {last_name.lower()}",  # All lowercase
            f"{last_name}, {first_name}",  # Last, First format
            f"{first_name} {last_name[0]}.",  # First name + initial
        ]
        name = random.choice(name_formats)
        
        # Generate company
        company = random.choice(self.industry_companies[industry])
        
        # Add company variations
        if random.random() < 0.3:  # 30% chance of company suffix variation
            suffixes = [' Inc', ' Corp', ' LLC', ' Ltd', ' Co', ' Group']
            if not any(suffix in company for suffix in suffixes):
                company += random.choice(suffixes)
        
        # Generate job title
        job_title = random.choice(self.complex_job_titles)
        
        # Generate company size with variations
        company_size = random.choice(self.company_sizes)
        
        # Generate email with domain logic
        is_corporate_email = random.random() < 0.7  # 70% corporate emails
        
        if is_corporate_email:
            # Create corporate email
            domain_base = company.lower().replace(' ', '').replace(',', '').replace('.', '')
            domain_base = domain_base.split('inc')[0].split('corp')[0].split('llc')[0]
            
            if len(domain_base) > 15:
                domain_base = domain_base[:15]
            
            domain = f"{domain_base}.com"
            
            # Sometimes use predefined corporate domains
            if random.random() < 0.3:
                domain = random.choice(self.corporate_domains)
        else:
            domain = random.choice(self.personal_domains)
        
        # Create email with variations
        email_formats = [
            f"{first_name.lower()}.{last_name.lower()}@{domain}",
            f"{first_name.lower()}{last_name.lower()}@{domain}",
            f"{first_name[0].lower()}{last_name.lower()}@{domain}",
            f"{first_name.lower()}.{last_name[0].lower()}@{domain}",
            f"{first_name.lower()}_{last_name.lower()}@{domain}",
        ]
        email = random.choice(email_formats)
        
        return {
            'name': name,
            'email': email,
            'company': company,
            'job_title': job_title,
            'company_size': company_size
        }
    
    def _apply_data_quality_issues(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply realistic data quality issues to the dataset.
        
        Args:
            df (pd.DataFrame): Clean dataset
            
        Returns:
            pd.DataFrame: Dataset with quality issues
        """
        df_copy = df.copy()
        
        # 1. Missing data (5-10% of fields)
        missing_rate = 0.08  # 8% missing data
        
        for column in df_copy.columns:
            if column != 'email':  # Keep emails mostly intact
                missing_indices = np.random.choice(
                    df_copy.index, 
                    size=int(len(df_copy) * missing_rate), 
                    replace=False
                )
                df_copy.loc[missing_indices, column] = np.nan
        
        # 2. Add some 'N/A' and 'Unknown' values
        na_values = ['N/A', 'Unknown', '', 'TBD', 'Not Available']
        for column in ['company', 'job_title']:
            na_indices = np.random.choice(
                df_copy.index,
                size=int(len(df_copy) * 0.05),  # 5%
                replace=False
            )
            for idx in na_indices:
                df_copy.loc[idx, column] = random.choice(na_values)
        
        # 3. Email formatting issues
        email_issues_indices = np.random.choice(
            df_copy.index,
            size=int(len(df_copy) * 0.1),  # 10%
            replace=False
        )
        
        for idx in email_issues_indices:
            if pd.notna(df_copy.loc[idx, 'email']):
                email = df_copy.loc[idx, 'email']
                issue_type = random.choice(['extra_space', 'mixed_case', 'typo'])
                
                if issue_type == 'extra_space':
                    df_copy.loc[idx, 'email'] = f" {email} "
                elif issue_type == 'mixed_case':
                    df_copy.loc[idx, 'email'] = email.upper()
                elif issue_type == 'typo' and '@' in email:
                    # Introduce minor typo
                    df_copy.loc[idx, 'email'] = email.replace('.com', '.co')
        
        # 4. Inconsistent company size formats
        size_format_issues = np.random.choice(
            df_copy.index,
            size=int(len(df_copy) * 0.15),  # 15%
            replace=False
        )
        
        for idx in size_format_issues:
            if pd.notna(df_copy.loc[idx, 'company_size']):
                current_size = df_copy.loc[idx, 'company_size']
                if isinstance(current_size, (int, float)):
                    # Convert to text format
                    text_formats = [f"{int(current_size)} employees", f"{int(current_size)}+", f"~{int(current_size)}"]
                    df_copy.loc[idx, 'company_size'] = random.choice(text_formats)
        
        # 5. Add special characters and accents to names
        special_char_indices = np.random.choice(
            df_copy.index,
            size=int(len(df_copy) * 0.1),  # 10%
            replace=False
        )
        
        for idx in special_char_indices:
            if pd.notna(df_copy.loc[idx, 'name']):
                name = df_copy.loc[idx, 'name']
                # Add accent or special character
                special_replacements = {'a': 'á', 'e': 'é', 'i': 'í', 'o': 'ó', 'u': 'ú', 'n': 'ñ'}
                for normal, special in special_replacements.items():
                    if normal in name.lower():
                        df_copy.loc[idx, 'name'] = name.replace(normal, special)
                        break
        
        # 6. Inconsistent job title abbreviations
        title_abbrev_indices = np.random.choice(
            df_copy.index,
            size=int(len(df_copy) * 0.2),  # 20%
            replace=False
        )
        
        abbreviation_map = {
            'Senior': 'Sr.',
            'Vice President': 'VP',
            'Director': 'Dir.',
            'Manager': 'Mgr.',
            'Assistant': 'Asst.',
            'Chief': 'Chief',
        }
        
        for idx in title_abbrev_indices:
            if pd.notna(df_copy.loc[idx, 'job_title']):
                title = df_copy.loc[idx, 'job_title']
                for full, abbrev in abbreviation_map.items():
                    if full in title:
                        # Randomly choose between full and abbreviated
                        if random.choice([True, False]):
                            title = title.replace(full, abbrev)
                df_copy.loc[idx, 'job_title'] = title
        
        return df_copy
    
    def get_expected_score_distribution(self, df: pd.DataFrame) -> Dict[str, int]:
        """
        Calculate expected score distribution for validation.
        
        Args:
            df (pd.DataFrame): Dataset to analyze
            
        Returns:
            Dict[str, int]: Expected score counts
        """
        # This is a rough estimate based on the data generation logic
        total_leads = len(df)
        
        # Based on job title distribution and company sizes
        expected_high = int(total_leads * 0.30)  # ~30% high priority
        expected_medium = int(total_leads * 0.45)  # ~45% medium priority
        expected_low = total_leads - expected_high - expected_medium  # ~25% low priority
        
        return {
            'High': expected_high,
            'Medium': expected_medium,
            'Low': expected_low
        }

# Convenience function for easy import
def generate_complex_test_dataset(num_leads: int = 40, save_to_csv: bool = False, filename: str = 'complex_test_leads.csv') -> pd.DataFrame:
    """
    Generate complex test dataset with realistic data quality issues.
    
    Args:
        num_leads (int): Number of leads to generate
        save_to_csv (bool): Whether to save to CSV file
        filename (str): CSV filename if saving
        
    Returns:
        pd.DataFrame: Complex test dataset
    """
    generator = ComplexTestDataGenerator()
    df = generator.generate_complex_dataset(num_leads)
    
    if save_to_csv:
        df.to_csv(filename, index=False)
        print(f"Complex test dataset saved to {filename}")
    
    return df
