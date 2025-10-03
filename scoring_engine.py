# Scoring Engine - Rule-based Lead Prioritization
# Modular design for future ML upgrade

class LeadScorer:
    """
    Rule-based lead scoring engine.
    Future upgrade path: replace rule-based logic with ML model.
    """
    
    def __init__(self):
        self.scoring_mode = "rule"
    
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
    
    def _rule_based_score(self, lead: dict):
        """
        Rule-based scoring logic.
        
        Rules:
        1. If job title contains "Manager", "Head", "Director" → High priority
        2. If email domain is corporate (not Gmail/Yahoo) → +1 tier up
        3. If company size > 50 → High, else Medium or Low
        
        Returns:
            str: Score level - "High", "Medium", or "Low"
        """
        score = 0
        
        # Rule 1: Job Title Check
        job_title = str(lead.get('job_title', '')).lower()
        senior_titles = ['manager', 'head', 'director', 'vp', 'vice president', 'chief', 'lead']
        if any(title in job_title for title in senior_titles):
            score += 2
        
        # Rule 2: Corporate Email Domain Check
        email = str(lead.get('email', '')).lower()
        personal_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com']
        if email and '@' in email:
            domain = email.split('@')[1]
            if not any(personal_domain in domain for personal_domain in personal_domains):
                score += 1  # Corporate email bonus
        
        # Rule 3: Company Size Check
        company_size = lead.get('company_size', 0)
        try:
            company_size = int(company_size)
            if company_size > 50:
                score += 2
            elif company_size > 10:
                score += 1
        except (ValueError, TypeError):
            pass  # Invalid company size, no bonus
        
        # Convert score to priority level
        if score >= 4:
            return "High"
        elif score >= 2:
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
