# Outreach Templates and Personalized Openers
# For lead engagement and sales outreach
# Enhanced with industry detection and company size-based messaging

from industry_detector import IndustryDetector
from industry_templates import IndustryTemplates

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
    Enhanced with industry detection and company size-based messaging.
    
    Args:
        lead_data (dict): Lead information with name, company, job_title, etc.
        content_type (str): "templates", "openers", or "both"
        
    Returns:
        dict: Personalized templates and/or openers
    """
    name = lead_data.get('name', 'there')
    company = lead_data.get('company', 'your company')
    job_title = lead_data.get('job_title', '')
    email = lead_data.get('email', '')
    company_size = lead_data.get('company_size', 0)
    
    # Initialize industry detection and templates
    industry_detector = IndustryDetector()
    industry_templates = IndustryTemplates()
    
    # Extract email domain for industry detection
    email_domain = ''
    if email and '@' in str(email):
        try:
            email_domain = str(email).split('@')[1]
        except IndexError:
            email_domain = ''
    
    # Detect industry
    industry = industry_detector.detect_industry(company, email_domain)
    
    # Determine appropriate goal based on job title (enhanced)
    goal = determine_goal_from_title(job_title)
    
    # Get company size context for messaging tone
    size_context = get_company_size_context(company_size)
    
    result = {}
    
    if content_type in ["templates", "both"]:
        # Use industry-specific templates when available
        if industry != 'general':
            templates = industry_templates.get_templates_for_industry(industry)
            # Add some general templates for variety
            general_templates = get_templates()
            templates.extend(general_templates[:1])  # Add one general template
        else:
            # Fall back to general templates
            templates = get_templates()
            
        personalized_templates = []
        
        for template in templates:
            # Enhanced personalization with size context
            personalized_content = template["template"].format(
                Name=name,
                Company=company,
                Goal=enhance_goal_with_context(goal, size_context, industry)
            )
            
            personalized = {
                "name": template["name"],
                "content": personalized_content,
                "industry": industry,  # Add industry info for reference
                "size_context": size_context["tone"]  # Add size context for reference
            }
            personalized_templates.append(personalized)
        
        result["templates"] = personalized_templates
    
    if content_type in ["openers", "both"]:
        # Enhanced openers with industry and size context
        base_openers = get_openers()
        industry_enhanced_openers = get_industry_enhanced_openers(industry)
        
        # Combine base openers with industry-enhanced ones
        all_openers = base_openers + industry_enhanced_openers
        
        personalized_openers = []
        enhanced_goal = enhance_goal_with_context(goal, size_context, industry)
        
        for opener in all_openers:
            personalized_opener = opener.format(
                Name=name, 
                Company=company, 
                Goal=enhanced_goal
            )
            personalized_openers.append(personalized_opener)
        
        result["openers"] = personalized_openers
        result["industry"] = industry  # Add industry info
        result["company_size_tone"] = size_context["tone"]  # Add size context
    
    return result

def get_company_size_context(company_size):
    """
    Get messaging context based on company size.
    
    Args:
        company_size (int): Number of employees
        
    Returns:
        dict: Context information for messaging tone
    """
    try:
        size = int(company_size) if company_size else 0
    except (ValueError, TypeError):
        size = 0
    
    if size > 1000:
        return {
            'tone': 'formal',
            'focus': 'enterprise-scale challenges',
            'approach': 'proven enterprise solutions',
            'urgency': 'strategic priorities'
        }
    elif size > 100:
        return {
            'tone': 'professional',
            'focus': 'growth and scalability',
            'approach': 'scalable solutions',
            'urgency': 'competitive advantage'
        }
    elif size > 25:
        return {
            'tone': 'collaborative',
            'focus': 'operational optimization',
            'approach': 'efficient and practical solutions',
            'urgency': 'resource optimization'
        }
    else:
        return {
            'tone': 'entrepreneurial',
            'focus': 'agility and growth',
            'approach': 'cost-effective solutions that scale',
            'urgency': 'competitive positioning'
        }

def enhance_goal_with_context(base_goal, size_context, industry):
    """
    Enhance goal description with company size and industry context.
    
    Args:
        base_goal (str): Basic goal from job title analysis
        size_context (dict): Company size context
        industry (str): Detected industry
        
    Returns:
        str: Enhanced goal description
    """
    # Industry-specific goal enhancements
    industry_enhancements = {
        'technology': f"{base_goal} with technical innovation",
        'healthcare': f"{base_goal} while ensuring compliance",
        'finance': f"{base_goal} with measurable ROI",
        'manufacturing': f"{base_goal} through operational excellence",
        'retail': f"{base_goal} and customer satisfaction",
        'consulting': f"{base_goal} and client success",
        'education': f"{base_goal} and student outcomes",
        'real_estate': f"{base_goal} and client relationships",
        'energy': f"{base_goal} with sustainability focus",
        'media': f"{base_goal} and audience engagement"
    }
    
    enhanced_goal = industry_enhancements.get(industry, base_goal)
    
    # Add size-specific context
    if size_context['tone'] == 'formal':
        return f"enterprise-level {enhanced_goal}"
    elif size_context['tone'] == 'entrepreneurial':
        return f"agile {enhanced_goal}"
    else:
        return enhanced_goal

def get_industry_enhanced_openers(industry):
    """
    Get industry-specific opener variations.
    
    Args:
        industry (str): Industry name
        
    Returns:
        list: Industry-enhanced openers
    """
    industry_openers = {
        'technology': [
            "Hi {Name}, noticed {Company}'s innovative tech approach - curious about your {Goal} strategy?",
            "Hello {Name}, {Company}'s tech growth is impressive. How are you handling {Goal} challenges?"
        ],
        'healthcare': [
            "Hi {Name}, healthcare compliance and {Goal} - would love to share some insights for {Company}.",
            "Hello {Name}, patient outcomes and {Goal} are critical - {Company} might benefit from our approach."
        ],
        'finance': [
            "Dear {Name}, ROI-focused solutions for {Goal} - {Company} might find this valuable.",
            "Hello {Name}, financial sector {Goal} requires proven approaches - interested in discussing?"
        ],
        'manufacturing': [
            "Hi {Name}, operational efficiency in {Goal} is crucial for {Company}'s competitive edge.",
            "Hello {Name}, manufacturing excellence and {Goal} - we've helped similar companies significantly."
        ],
        'retail': [
            "Hi {Name}, customer experience drives {Goal} success - {Company} might benefit from our insights.",
            "Hello {Name}, retail growth through {Goal} - would love to share proven strategies with {Company}."
        ],
        'consulting': [
            "Dear {Name}, client success and {Goal} - {Company} might appreciate our strategic approach.",
            "Hello {Name}, consulting excellence in {Goal} - interested in discussing methodologies?"
        ],
        'education': [
            "Hello {Name}, student success and {Goal} - {Company} might benefit from our proven approaches.",
            "Hi {Name}, educational innovation in {Goal} - would love to share insights with {Company}."
        ],
        'real_estate': [
            "Hello {Name}, client relationships and {Goal} drive success - {Company} might find this valuable.",
            "Hi {Name}, market advantage through {Goal} - interested in discussing strategies for {Company}?"
        ],
        'energy': [
            "Dear {Name}, sustainability and {Goal} are key priorities - {Company} might benefit from our approach.",
            "Hello {Name}, energy sector {Goal} requires innovative solutions - interested in exploring options?"
        ],
        'media': [
            "Hi {Name}, audience engagement and {Goal} - {Company}'s creative approach could benefit from our insights.",
            "Hello {Name}, brand growth through {Goal} - would love to discuss creative strategies with {Company}."
        ]
    }
    
    return industry_openers.get(industry, [])

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
