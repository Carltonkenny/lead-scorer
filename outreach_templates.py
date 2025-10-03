# Outreach Templates and Personalized Openers
# For lead engagement and sales outreach

def get_templates():
    """
    Returns list of mini outreach email templates with placeholders.
    Uses {Name}, {Company}, {Goal} placeholders for personalization.
    """
    templates = [
        {
            "name": "Professional Introduction",
            "template": """Hi {Name},

I hope this message finds you well. I came across {Company} and was impressed by your work in the industry.

As someone in your position, I imagine you're focused on {Goal}. We've helped similar companies achieve significant results in this area.

Would you be open to a brief 15-minute call this week to discuss how we might support {Company}'s objectives?

Best regards,
[Your Name]"""
        },
        {
            "name": "Value Proposition Approach", 
            "template": """Hello {Name},

I noticed {Company} is in a growth phase, and I wanted to reach out with a quick idea.

We've helped companies like yours increase {Goal} by 25-40% through strategic optimization. Given your role and {Company}'s trajectory, this might be relevant.

Would you be interested in a brief conversation about potential opportunities?

Thanks for your time,
[Your Name]"""
        },
        {
            "name": "Problem-Solving Opener",
            "template": """Hi {Name},

I've been researching {Company} and the challenges facing your industry. Many leaders in similar positions are struggling with {Goal}.

We've developed a proven approach that's helped companies overcome these exact challenges. I'd love to share some insights that might be valuable for {Company}.

Would you have 10 minutes for a quick call?

Best,
[Your Name]"""
        }
    ]
    return templates

def get_openers():
    """
    Returns list of personalized one-liner openers.
    Perfect for LinkedIn messages or brief email intros.
    """
    openers = [
        "Hi {Name}, saw your recent work at {Company} and thought you might be interested in how we've helped similar companies with {Goal}.",
        "Hello {Name}, quick question - is {Goal} a priority for {Company} right now?",
        "Hi {Name}, impressed by {Company}'s growth. Would love to share some insights about {Goal} that might be valuable.",
        "Hello {Name}, I've been following {Company} and think there's a great opportunity to discuss {Goal}.",
        "Hi {Name}, reaching out because {Company} seems like it would benefit from our approach to {Goal}."
    ]
    return openers

def generate_personalized_content(lead_data, content_type="both"):
    """
    Generate personalized outreach content for a specific lead.
    
    Args:
        lead_data (dict): Lead information with name, company, job_title, etc.
        content_type (str): "templates", "openers", or "both"
        
    Returns:
        dict: Personalized templates and/or openers
    """
    name = lead_data.get('name', 'there')
    company = lead_data.get('company', 'your company')
    job_title = lead_data.get('job_title', '')
    
    # Determine appropriate goal based on job title
    goal = determine_goal_from_title(job_title)
    
    result = {}
    
    if content_type in ["templates", "both"]:
        templates = get_templates()
        personalized_templates = []
        
        for template in templates:
            personalized = {
                "name": template["name"],
                "content": template["template"].format(
                    Name=name,
                    Company=company,
                    Goal=goal
                )
            }
            personalized_templates.append(personalized)
        
        result["templates"] = personalized_templates
    
    if content_type in ["openers", "both"]:
        openers = get_openers()
        personalized_openers = [
            opener.format(Name=name, Company=company, Goal=goal)
            for opener in openers
        ]
        
        result["openers"] = personalized_openers
    
    return result

def determine_goal_from_title(job_title):
    """
    Determine appropriate outreach goal based on job title.
    
    Args:
        job_title (str): The person's job title
        
    Returns:
        str: Suggested goal/focus area for outreach
    """
    if not job_title:
        return "operational efficiency"
        
    job_title_lower = job_title.lower()
    
    # Sales-focused roles
    if any(word in job_title_lower for word in ['sales', 'revenue', 'business development', 'account']):
        return "revenue growth"
    
    # Marketing-focused roles  
    elif any(word in job_title_lower for word in ['marketing', 'brand', 'digital', 'content']):
        return "lead generation"
    
    # Operations/Management roles
    elif any(word in job_title_lower for word in ['operations', 'manager', 'director', 'head']):
        return "operational efficiency"
    
    # Technology roles
    elif any(word in job_title_lower for word in ['tech', 'it', 'engineer', 'developer', 'cto']):
        return "technical optimization"
    
    # Executive roles
    elif any(word in job_title_lower for word in ['ceo', 'president', 'founder', 'chief']):
        return "strategic growth"
    
    # Default
    else:
        return "business objectives"
