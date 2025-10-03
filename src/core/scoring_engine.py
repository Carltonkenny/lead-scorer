# Scoring Engine - Rule-based Lead Prioritization
# Modular design for future ML upgrade

class LeadScorer:
    """
    Rule-based lead scoring engine.
    Future upgrade path: replace rule-based logic with ML model.
    """
    
    def __init__(self):
        self.scoring_mode = "rule"
        # Normalize common job title variations
        self.job_title_mappings = {
            'mgr': 'manager',
            'sr': 'senior',
            'sr.': 'senior', 
            'jr': 'junior',
            'jr.': 'junior',
            'vp': 'vice president',
            'v.p.': 'vice president',
            'ceo': 'chief executive officer',
            'cto': 'chief technology officer',
            'cfo': 'chief financial officer',
            'cmo': 'chief marketing officer',
            'coo': 'chief operating officer',
            'evp': 'executive vice president',
            'svp': 'senior vice president',
            'avp': 'assistant vice president',
            'dir': 'director',
            'dir.': 'director',
            'asst': 'assistant',
            'assoc': 'associate',
            'coord': 'coordinator',
            'rep': 'representative',
            'dev': 'developer',
            'eng': 'engineer',
            'admin': 'administrator'
        }
    
    def normalize_job_title(self, job_title):
        """
        Normalize job title variations for consistent scoring.
        
        Args:
            job_title (str): Raw job title from CSV
            
        Returns:
            str: Normalized job title
        """
        if not job_title or str(job_title).lower().strip() in ['nan', 'none', '']:
            return 'unknown'
            
        title = str(job_title).lower().strip()
        
        # Remove common punctuation and extra spaces
        title = title.replace(',', ' ').replace('.', ' ').replace('/', ' ')
        title = ' '.join(title.split())  # Normalize whitespace
        
        # Apply mappings for common abbreviations
        words = title.split()
        normalized_words = []
        for word in words:
            # Check if word (without punctuation) is in our mappings
            clean_word = word.strip('.,!?;:')
            if clean_word in self.job_title_mappings:
                normalized_words.append(self.job_title_mappings[clean_word])
            else:
                normalized_words.append(word)
        
        return ' '.join(normalized_words)
    
    def normalize_email_domain(self, email):
        """
        Extract and normalize email domain for corporate vs personal classification.
        
        Args:
            email (str): Email address
            
        Returns:
            str: Normalized domain or empty string if invalid
        """
        if not email or str(email).lower().strip() in ['nan', 'none', '']:
            return ''
            
        email_str = str(email).lower().strip()
        
        if '@' not in email_str:
            return ''
            
        try:
            domain = email_str.split('@')[1]
            # Remove common variations
            domain = domain.replace('www.', '')
            return domain
        except (IndexError, AttributeError):
            return ''
    
    def normalize_company_size(self, company_size):
        """
        Normalize company size to handle various input formats.
        
        Args:
            company_size: Raw company size (could be int, str, float)
            
        Returns:
            int: Normalized company size (0 if invalid)
        """
        if company_size is None or str(company_size).lower().strip() in ['nan', 'none', '', 'unknown']:
            return 0
            
        # Handle string representations
        size_str = str(company_size).lower().strip()
        
        # Handle common text representations
        size_mappings = {
            'startup': 5,
            'small': 10,
            'medium': 50,
            'large': 200,
            'enterprise': 1000,
            'freelance': 1,
            'freelancer': 1,
            'individual': 1,
            'solo': 1,
            'self-employed': 1
        }
        
        if size_str in size_mappings:
            return size_mappings[size_str]
            
        # Handle ranges like "50-100", "10+", "100-500"
        if '-' in size_str:
            try:
                # Take the lower bound of ranges
                parts = size_str.split('-')
                return int(parts[0].strip())
            except (ValueError, IndexError):
                return 0
                
        if '+' in size_str:
            try:
                return int(size_str.replace('+', '').strip())
            except ValueError:
                return 0
        
        # Handle numeric values
        try:
            # Remove common suffixes and convert
            size_clean = size_str.replace(',', '').replace('employees', '').replace('people', '').strip()
            return max(0, int(float(size_clean)))  # Convert via float to handle "50.0"
        except (ValueError, TypeError):
            return 0
    
    def score_lead(self, lead: dict, mode="rule"):
        """
        Score a single lead based on specified mode.
        
        Args:
            lead (dict): Lead data containing name, email, company, job_title, company_size
            mode (str): Scoring mode - "rule" for rule-based, "ml" for future ML model
            
        Returns:
            str: Score level - "High", "Medium", or "Low"
        """
        if mode == "rule":
            return self._rule_based_score(lead)
        elif mode == "ml":
            # Placeholder for future ML model integration
            return "Medium"
        else:
            return "Medium"

    def score_lead_with_explain(self, lead: dict):
        """
        Score a single lead and return explanation details.
        Returns: (level, points, reasons_list)
        """
        points = 0
        reasons = []

        normalized_title = self.normalize_job_title(lead.get('job_title', ''))
        email_domain = self.normalize_email_domain(lead.get('email', ''))
        normalized_size = self.normalize_company_size(lead.get('company_size', 0))

        senior_titles = [
            'manager', 'head', 'director', 'vice president', 'vp',
            'lead', 'principal', 'senior', 'supervisor', 'coordinator'
        ]
        executive_titles = [
            'chief executive officer', 'ceo', 'chief technology officer', 'cto',
            'chief financial officer', 'cfo', 'chief marketing officer', 'cmo',
            'chief operating officer', 'coo', 'president', 'founder',
            'executive vice president', 'evp', 'senior vice president', 'svp'
        ]

        if any(t in normalized_title for t in senior_titles):
            points += 2
            reasons.append("+2 senior title")
        if any(t in normalized_title for t in executive_titles):
            points += 1
            reasons.append("+1 executive title")

        if email_domain:
            personal_domains = [
                'gmail.com','yahoo.com','hotmail.com','outlook.com','aol.com',
                'icloud.com','live.com','msn.com','mail.com','protonmail.com',
                'yandex.com','qq.com','sina.com','zoho.com'
            ]
            if email_domain not in personal_domains:
                points += 1
                reasons.append(f"+1 corporate email ({email_domain})")

        if normalized_size > 100:
            points += 2
            reasons.append("+2 company size > 100")
        elif normalized_size > 25:
            points += 1
            reasons.append("+1 company size > 25")
        elif normalized_size > 5:
            reasons.append("±0 company size > 5")
        else:
            reasons.append("±0 very small company")

        if points >= 5:
            level = "High"
        elif points >= 3:
            level = "Medium"
        elif points >= 1:
            level = "Medium"
        else:
            level = "Low"

        return level, points, reasons

    def score_leads_batch_with_explain(self, leads_df):
        """
        Batch scoring with explanations.
        Returns DataFrame with 'score', 'score_points', 'score_reasons' columns.
        """
        import pandas as pd
        scored_df = leads_df.copy()
        levels = []
        points_list = []
        reasons_list = []
        for _, row in scored_df.iterrows():
            level, pts, reasons = self.score_lead_with_explain(row.to_dict())
            levels.append(level)
            points_list.append(pts)
            reasons_list.append('; '.join(reasons))
        scored_df['score'] = levels
        scored_df['score_points'] = points_list
        scored_df['score_reasons'] = reasons_list
        priority_order = {'High': 3, 'Medium': 2, 'Low': 1}
        scored_df['_sort_priority'] = scored_df['score'].map(priority_order)
        scored_df = scored_df.sort_values('_sort_priority', ascending=False)
        scored_df = scored_df.drop('_sort_priority', axis=1)
        return scored_df
    
    def _rule_based_score(self, lead: dict):
        """
        Enhanced rule-based scoring logic with normalization.
        
        Rules:
        1. If job title contains senior roles (Manager, Director, VP, etc.) → +2 points
        2. If email domain is corporate (not personal) → +1 point
        3. If company size > 50 → +2 points, > 10 → +1 point
        4. Bonus points for C-level titles → +1 point
        
        Returns:
            str: Score level - "High", "Medium", or "Low"
        """
        score = 0
        
        # Rule 1: Job Title Check (with normalization)
        normalized_title = self.normalize_job_title(lead.get('job_title', ''))
        
        # Senior titles (enhanced list)
        senior_titles = [
            'manager', 'head', 'director', 'vice president', 'vp', 
            'lead', 'principal', 'senior', 'supervisor', 'coordinator'
        ]
        
        # C-level and executive titles get extra points
        executive_titles = [
            'chief executive officer', 'ceo', 'chief technology officer', 'cto',
            'chief financial officer', 'cfo', 'chief marketing officer', 'cmo',
            'chief operating officer', 'coo', 'president', 'founder', 
            'executive vice president', 'evp', 'senior vice president', 'svp'
        ]
        
        # Check for senior titles
        if any(title in normalized_title for title in senior_titles):
            score += 2
            
        # Bonus for executive titles
        if any(title in normalized_title for title in executive_titles):
            score += 1
        
        # Rule 2: Corporate Email Domain Check (with normalization)
        email_domain = self.normalize_email_domain(lead.get('email', ''))
        
        if email_domain:
            # Expanded list of personal domains
            personal_domains = [
                'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com',
                'icloud.com', 'live.com', 'msn.com', 'mail.com', 'protonmail.com',
                'yandex.com', 'qq.com', 'sina.com', 'zoho.com'
            ]
            
            if not any(personal_domain == email_domain for personal_domain in personal_domains):
                score += 1  # Corporate email bonus
        
        # Rule 3: Company Size Check (with normalization)
        normalized_size = self.normalize_company_size(lead.get('company_size', 0))
        
        if normalized_size > 100:  # Large company
            score += 2
        elif normalized_size > 25:  # Medium company
            score += 1
        elif normalized_size > 5:   # Small but established company
            score += 0  # Neutral
        # Freelancers, students, etc. get no bonus (could be negative in future)
        
        # Convert score to priority level with refined thresholds
        if score >= 5:  # High bar for high priority
            return "High"
        elif score >= 3:  # Medium priority
            return "Medium"
        elif score >= 1:  # Some positive signals
            return "Medium"
        else:
            return "Low"
    
    def score_leads_batch(self, leads_df):
        """
        Score multiple leads in batch.
        
        Args:
            leads_df: pandas DataFrame with lead data
            
        Returns:
            pandas DataFrame with added 'score' column
        """
        import pandas as pd
        
        # Create a copy to avoid modifying original DataFrame
        scored_df = leads_df.copy()
        
        # Apply scoring to each row
        scores = []
        for index, row in scored_df.iterrows():
            lead_dict = row.to_dict()
            score = self.score_lead(lead_dict, mode="rule")
            scores.append(score)
        
        # Add score column
        scored_df['score'] = scores
        
        # Sort by priority (High > Medium > Low)
        priority_order = {'High': 3, 'Medium': 2, 'Low': 1}
        scored_df['_sort_priority'] = scored_df['score'].map(priority_order)
        scored_df = scored_df.sort_values('_sort_priority', ascending=False)
        scored_df = scored_df.drop('_sort_priority', axis=1)
        
        return scored_df
