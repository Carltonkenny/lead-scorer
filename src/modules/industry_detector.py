# Industry Detection Module
# Detects company industry from company names and email domains

class IndustryDetector:
    """
    Modular industry detection system.
    Analyzes company names and email domains to classify industries.
    """
    
    def __init__(self):
        # Technology industry indicators
        self.tech_indicators = [
            'tech', 'software', 'app', 'digital', 'data', 'cloud', 'ai', 'ml',
            'startup', 'saas', 'platform', 'dev', 'code', 'cyber', 'analytics',
            'innovation', 'solutions', 'systems', 'technologies', 'computing'
        ]
        
        self.tech_domains = [
            '.io', '.ly', '.co', '.dev', '.app', '.tech', '.ai'
        ]
        
        # Healthcare industry indicators  
        self.healthcare_indicators = [
            'health', 'medical', 'pharma', 'bio', 'clinic', 'hospital', 'care',
            'wellness', 'medicine', 'therapeutic', 'diagnostics', 'device',
            'pharmaceutical', 'biotech', 'medtech', 'healthcare'
        ]
        
        # Finance industry indicators
        self.finance_indicators = [
            'bank', 'finance', 'capital', 'invest', 'fund', 'credit', 'loan',
            'insurance', 'wealth', 'financial', 'asset', 'trading', 'fintech',
            'payment', 'money', 'fiscal', 'equity', 'securities'
        ]
        
        # Manufacturing industry indicators
        self.manufacturing_indicators = [
            'manufacturing', 'industrial', 'factory', 'production', 'assembly',
            'automotive', 'aerospace', 'chemical', 'materials', 'machinery',
            'equipment', 'tools', 'engineering', 'fabrication', 'supply'
        ]
        
        # Retail/E-commerce indicators
        self.retail_indicators = [
            'retail', 'store', 'shop', 'market', 'commerce', 'ecommerce', 'sales',
            'fashion', 'clothing', 'apparel', 'consumer', 'brand', 'merchandise',
            'outlet', 'marketplace', 'shopping'
        ]
        
        # Consulting indicators
        self.consulting_indicators = [
            'consulting', 'advisory', 'services', 'consultant', 'strategy',
            'management', 'business', 'professional', 'expertise', 'guidance',
            'optimization', 'transformation', 'improvement'
        ]
        
        # Education indicators
        self.education_indicators = [
            'education', 'school', 'university', 'college', 'academy', 'learning',
            'training', 'institute', 'educational', 'academic', 'student'
        ]
        
        # Real Estate indicators
        self.real_estate_indicators = [
            'real estate', 'property', 'realty', 'housing', 'construction',
            'development', 'building', 'architecture', 'land'
        ]
        
        # Energy indicators
        self.energy_indicators = [
            'energy', 'oil', 'gas', 'renewable', 'solar', 'wind', 'electric',
            'power', 'utility', 'petroleum', 'utilities'
        ]
        
        # Media/Marketing indicators
        self.media_indicators = [
            'media', 'marketing', 'advertising', 'communications', 'pr', 'creative',
            'agency', 'branding', 'design', 'content', 'publishing', 'broadcast'
        ]
    
    def detect_industry(self, company_name, email_domain=None):
        """
        Detect industry from company name and optional email domain.
        
        Args:
            company_name (str): Company name to analyze
            email_domain (str): Email domain (optional, for additional context)
            
        Returns:
            str: Detected industry or 'general' if no clear match
        """
        if not company_name or str(company_name).lower().strip() in ['', 'unknown', 'nan', 'none']:
            return 'general'
            
        company_lower = str(company_name).lower().strip()
        domain_lower = str(email_domain).lower().strip() if email_domain else ''
        
        # Combine company name and domain for analysis
        combined_text = f"{company_lower} {domain_lower}"
        
        # Check each industry with weighted scoring
        industry_scores = {
            'technology': self._calculate_industry_score(combined_text, self.tech_indicators, self.tech_domains),
            'healthcare': self._calculate_industry_score(combined_text, self.healthcare_indicators),
            'finance': self._calculate_industry_score(combined_text, self.finance_indicators),
            'manufacturing': self._calculate_industry_score(combined_text, self.manufacturing_indicators),
            'retail': self._calculate_industry_score(combined_text, self.retail_indicators),
            'consulting': self._calculate_industry_score(combined_text, self.consulting_indicators),
            'education': self._calculate_industry_score(combined_text, self.education_indicators),
            'real_estate': self._calculate_industry_score(combined_text, self.real_estate_indicators),
            'energy': self._calculate_industry_score(combined_text, self.energy_indicators),
            'media': self._calculate_industry_score(combined_text, self.media_indicators)
        }
        
        # Find industry with highest score
        max_score = max(industry_scores.values())
        
        # Require minimum confidence threshold
        if max_score < 1:
            return 'general'
            
        # Return industry with highest score
        for industry, score in industry_scores.items():
            if score == max_score:
                return industry
                
        return 'general'
    
    def _calculate_industry_score(self, text, indicators, domain_indicators=None):
        """
        Calculate confidence score for industry match.
        
        Args:
            text (str): Combined company name and domain text
            indicators (list): Industry keyword indicators
            domain_indicators (list): Domain-specific indicators (optional)
            
        Returns:
            int: Confidence score (higher = better match)
        """
        score = 0
        
        # Check for keyword matches
        for indicator in indicators:
            if indicator in text:
                # Exact word match gets higher score
                if f" {indicator} " in f" {text} " or text.startswith(indicator) or text.endswith(indicator):
                    score += 2
                else:
                    score += 1
        
        # Check domain indicators if provided
        if domain_indicators:
            for domain_indicator in domain_indicators:
                if domain_indicator in text:
                    score += 3  # Domain indicators are strong signals
        
        return score
    
    def get_industry_characteristics(self, industry):
        """
        Get characteristics and messaging approach for each industry.
        
        Args:
            industry (str): Industry name
            
        Returns:
            dict: Industry characteristics for personalization
        """
        characteristics = {
            'technology': {
                'tone': 'innovative',
                'focus_areas': ['scalability', 'innovation', 'digital transformation', 'efficiency'],
                'pain_points': ['rapid growth challenges', 'technical scalability', 'competitive advantage'],
                'value_props': ['cutting-edge solutions', 'competitive edge', 'future-ready technology'],
                'terminology': ['innovation', 'disruption', 'scalability', 'optimization']
            },
            'healthcare': {
                'tone': 'professional',
                'focus_areas': ['patient outcomes', 'compliance', 'efficiency', 'cost reduction'],
                'pain_points': ['regulatory compliance', 'patient care quality', 'operational efficiency'],
                'value_props': ['improved outcomes', 'compliance assurance', 'cost-effective solutions'],
                'terminology': ['outcomes', 'compliance', 'quality', 'efficiency']
            },
            'finance': {
                'tone': 'formal',
                'focus_areas': ['ROI', 'security', 'compliance', 'risk management'],
                'pain_points': ['regulatory requirements', 'security concerns', 'market volatility'],
                'value_props': ['measurable ROI', 'enhanced security', 'regulatory compliance'],
                'terminology': ['ROI', 'security', 'compliance', 'risk mitigation']
            },
            'manufacturing': {
                'tone': 'results_focused',
                'focus_areas': ['operational efficiency', 'cost reduction', 'quality control', 'supply chain'],
                'pain_points': ['production costs', 'supply chain disruptions', 'quality consistency'],
                'value_props': ['cost savings', 'operational excellence', 'quality improvement'],
                'terminology': ['efficiency', 'lean operations', 'cost reduction', 'optimization']
            },
            'retail': {
                'tone': 'customer_focused',
                'focus_areas': ['customer experience', 'sales growth', 'inventory management', 'market reach'],
                'pain_points': ['customer acquisition', 'inventory optimization', 'market competition'],
                'value_props': ['customer satisfaction', 'sales increase', 'market advantage'],
                'terminology': ['customer experience', 'growth', 'engagement', 'conversion']
            },
            'consulting': {
                'tone': 'strategic',
                'focus_areas': ['client success', 'expertise', 'strategic advantage', 'efficiency'],
                'pain_points': ['client expectations', 'competitive differentiation', 'service delivery'],
                'value_props': ['strategic insights', 'competitive advantage', 'client success'],
                'terminology': ['strategy', 'optimization', 'transformation', 'excellence']
            },
            'education': {
                'tone': 'supportive',
                'focus_areas': ['student outcomes', 'efficiency', 'engagement', 'accessibility'],
                'pain_points': ['budget constraints', 'student engagement', 'outcome measurement'],
                'value_props': ['improved outcomes', 'cost-effective solutions', 'enhanced engagement'],
                'terminology': ['outcomes', 'engagement', 'accessibility', 'efficiency']
            },
            'real_estate': {
                'tone': 'relationship_focused',
                'focus_areas': ['client satisfaction', 'market advantage', 'efficiency', 'growth'],
                'pain_points': ['market competition', 'client acquisition', 'operational efficiency'],
                'value_props': ['competitive edge', 'client satisfaction', 'operational improvement'],
                'terminology': ['growth', 'opportunity', 'advantage', 'success']
            },
            'energy': {
                'tone': 'sustainability_focused',
                'focus_areas': ['sustainability', 'efficiency', 'cost reduction', 'innovation'],
                'pain_points': ['regulatory changes', 'sustainability requirements', 'operational costs'],
                'value_props': ['sustainable solutions', 'cost efficiency', 'regulatory compliance'],
                'terminology': ['sustainability', 'efficiency', 'innovation', 'optimization']
            },
            'media': {
                'tone': 'creative',
                'focus_areas': ['audience engagement', 'brand growth', 'creativity', 'reach'],
                'pain_points': ['audience acquisition', 'content creation', 'brand differentiation'],
                'value_props': ['enhanced engagement', 'brand growth', 'creative solutions'],
                'terminology': ['engagement', 'creativity', 'growth', 'impact']
            },
            'general': {
                'tone': 'professional',
                'focus_areas': ['business growth', 'efficiency', 'success', 'optimization'],
                'pain_points': ['operational challenges', 'growth obstacles', 'competitive pressure'],
                'value_props': ['business improvement', 'operational excellence', 'competitive advantage'],
                'terminology': ['growth', 'success', 'optimization', 'excellence']
            }
        }
        
        return characteristics.get(industry, characteristics['general'])

# Convenience function for easy import
def detect_company_industry(company_name, email_domain=None):
    """
    Convenience function to detect industry without instantiating class.
    
    Args:
        company_name (str): Company name
        email_domain (str): Email domain (optional)
        
    Returns:
        str: Detected industry
    """
    detector = IndustryDetector()
    return detector.detect_industry(company_name, email_domain)