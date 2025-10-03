# Industry-Specific Templates Module
# Contains tailored email templates for different industries

class IndustryTemplates:
    """
    Industry-specific email templates and messaging.
    Provides tailored outreach content based on industry characteristics.
    """
    
    def __init__(self):
        self.templates = {
            'technology': self._get_technology_templates(),
            'healthcare': self._get_healthcare_templates(),
            'finance': self._get_finance_templates(),
            'manufacturing': self._get_manufacturing_templates(),
            'retail': self._get_retail_templates(),
            'consulting': self._get_consulting_templates(),
            'education': self._get_education_templates(),
            'real_estate': self._get_real_estate_templates(),
            'energy': self._get_energy_templates(),
            'media': self._get_media_templates(),
            'general': self._get_general_templates()
        }
    
    def get_templates_for_industry(self, industry):
        """
        Get templates tailored for specific industry.
        
        Args:
            industry (str): Industry name
            
        Returns:
            list: Industry-specific templates
        """
        return self.templates.get(industry, self.templates['general'])
    
    def _get_technology_templates(self):
        """Technology industry templates focusing on innovation and scalability."""
        return [
            {
                "name": "Innovation Focus",
                "template": """Hi {Name},

I've been following {Company}'s innovative work in the tech space, and I'm impressed by your approach to {Goal}.

As the technology landscape evolves rapidly, staying ahead of scalability challenges while maintaining innovation velocity is crucial. We've helped similar tech companies achieve 40% faster deployment cycles while reducing technical debt.

Given your role and {Company}'s growth trajectory, I believe there's significant value we could deliver around {Goal}.

Would you be open to a brief 15-minute call to explore how we might accelerate {Company}'s technical innovation?

Best regards,
[Your Name]"""
            },
            {
                "name": "Scalability Solution",
                "template": """Hello {Name},

{Company} is clearly building something impressive in the technology sector. I imagine scaling {Goal} while maintaining system performance is a key priority for you.

We've developed a proven framework that's helped tech companies like yours achieve 3x scale without proportional infrastructure costs. The approach specifically addresses the challenges that come with rapid growth in the technology space.

I'd love to share some insights that might be valuable for {Company}'s scaling journey.

Are you available for a quick 10-minute conversation this week?

Thanks,
[Your Name]"""
            },
            {
                "name": "Digital Transformation",
                "template": """Hi {Name},

The pace of digital transformation is accelerating, and companies like {Company} are leading the charge. I wanted to reach out because {Goal} is becoming increasingly critical for sustainable tech growth.

We've helped technology companies navigate similar transformation challenges, resulting in 50% improved operational efficiency and faster time-to-market for new features.

Would you be interested in discussing how {Company} could leverage these proven strategies for {Goal}?

Best,
[Your Name]"""
            }
        ]
    
    def _get_healthcare_templates(self):
        """Healthcare industry templates emphasizing outcomes and compliance."""
        return [
            {
                "name": "Patient Outcomes Focus",
                "template": """Hello {Name},

Healthcare organizations like {Company} face the critical challenge of balancing excellent patient outcomes with operational efficiency. I imagine {Goal} is a significant priority for your team.

We've partnered with healthcare organizations to improve patient outcome metrics by 35% while ensuring full regulatory compliance. Our approach specifically addresses the unique challenges in healthcare delivery.

Given your leadership role at {Company}, I'd appreciate the opportunity to share some insights about {Goal} that might be valuable.

Would you have 15 minutes for a brief conversation?

Best regards,
[Your Name]"""
            },
            {
                "name": "Compliance & Efficiency",
                "template": """Hi {Name},

Regulatory compliance in healthcare continues to evolve, and I know organizations like {Company} must balance compliance requirements with {Goal}. 

We've developed solutions that help healthcare providers maintain 100% compliance while reducing administrative overhead by 40%. This directly supports better resource allocation toward patient care.

I'd love to discuss how these approaches might benefit {Company}'s objectives around {Goal}.

Are you available for a quick call this week?

Thank you,
[Your Name]"""
            },
            {
                "name": "Cost-Effective Care",
                "template": """Hello {Name},

The healthcare industry faces increasing pressure to deliver high-quality care while managing costs effectively. I suspect {Goal} is central to {Company}'s strategic priorities.

We've helped healthcare organizations achieve 25% cost reductions without compromising patient care quality. Our methodology focuses on operational optimization that directly supports better patient outcomes.

Would you be open to exploring how these strategies might enhance {Company}'s approach to {Goal}?

Best,
[Your Name]"""
            }
        ]
    
    def _get_finance_templates(self):
        """Finance industry templates emphasizing ROI and security."""
        return [
            {
                "name": "ROI-Focused Approach",
                "template": """Dear {Name},

Financial institutions like {Company} require solutions that deliver measurable ROI while maintaining the highest security standards. I understand {Goal} is likely a strategic priority requiring careful evaluation.

We've helped financial services companies achieve 300% ROI within 18 months while enhancing their security posture. Our approach includes comprehensive risk assessment and regulatory compliance measures.

Given your position at {Company}, I believe you'd find our proven methodology for {Goal} particularly relevant.

Would you be available for a brief 15-minute discussion about potential value creation opportunities?

Best regards,
[Your Name]"""
            },
            {
                "name": "Security & Compliance",
                "template": """Hello {Name},

Security and regulatory compliance are paramount in the financial sector. I imagine {Company} is focused on {Goal} while ensuring full adherence to industry regulations.

We've successfully helped financial institutions implement solutions that exceed compliance requirements while improving operational efficiency by 45%. Our track record includes working with organizations similar to {Company}.

I'd appreciate the opportunity to discuss how our proven approach might support {Company}'s objectives around {Goal}.

Are you available for a brief conversation?

Thank you,
[Your Name]"""
            },
            {
                "name": "Risk Mitigation",
                "template": """Dear {Name},

Risk management continues to be a critical focus for financial organizations. I suspect {Goal} requires careful balance between opportunity and risk for {Company}.

Our risk-adjusted approach has helped financial services companies reduce operational risk by 60% while achieving their strategic objectives. We understand the unique challenges facing organizations like {Company}.

Would you be interested in exploring how our methodology might enhance {Company}'s approach to {Goal}?

Best regards,
[Your Name]"""
            }
        ]
    
    def _get_manufacturing_templates(self):
        """Manufacturing industry templates focusing on efficiency and cost reduction."""
        return [
            {
                "name": "Operational Excellence",
                "template": """Hello {Name},

Manufacturing companies like {Company} are constantly seeking ways to optimize operations and reduce costs. I imagine {Goal} is a key focus for maintaining competitive advantage.

We've helped manufacturing organizations achieve 30% cost reduction while improving quality metrics through lean operational improvements. Our approach directly addresses the challenges facing today's manufacturing leaders.

Given your role at {Company}, I'd value the opportunity to discuss how these proven strategies might support your {Goal} initiatives.

Would you have 15 minutes available this week?

Best regards,
[Your Name]"""
            },
            {
                "name": "Supply Chain Optimization",
                "template": """Hi {Name},

Supply chain resilience has become critical for manufacturing success. I suspect {Goal} involves optimizing {Company}'s supply chain operations while managing costs effectively.

We've developed solutions that have helped manufacturing companies reduce supply chain costs by 25% while improving delivery reliability. Our methodology specifically addresses the complexities of modern manufacturing operations.

Would you be interested in discussing how these approaches might benefit {Company}'s {Goal} objectives?

Thank you,
[Your Name]"""
            },
            {
                "name": "Quality & Efficiency",
                "template": """Hello {Name},

Balancing quality control with operational efficiency is a constant challenge in manufacturing. I believe {Goal} is central to {Company}'s strategic priorities.

Our proven approach has helped manufacturing organizations improve quality metrics by 40% while reducing operational costs. We understand the unique pressures facing manufacturing leaders today.

I'd appreciate the opportunity to share insights that might be valuable for {Company}'s approach to {Goal}.

Are you available for a brief call?

Best,
[Your Name]"""
            }
        ]
    
    def _get_retail_templates(self):
        """Retail industry templates emphasizing customer experience and growth."""
        return [
            {
                "name": "Customer Experience Focus",
                "template": """Hi {Name},

Customer experience has become the key differentiator in retail. I imagine {Goal} is crucial for {Company}'s competitive positioning and growth strategy.

We've helped retail organizations increase customer satisfaction scores by 45% while driving 25% revenue growth through enhanced customer experience initiatives. Our approach understands the evolving retail landscape.

Given your leadership at {Company}, I'd love to discuss how these proven strategies might enhance your {Goal} efforts.

Would you be open to a 15-minute conversation?

Best regards,
[Your Name]"""
            },
            {
                "name": "Sales Growth Strategy",
                "template": """Hello {Name},

Retail growth requires balancing customer acquisition with retention strategies. I suspect {Goal} is central to {Company}'s revenue objectives and market expansion plans.

We've developed approaches that have helped retail companies achieve 35% sales growth while improving customer loyalty metrics. Our methodology addresses both online and offline retail challenges.

Would you be interested in exploring how these strategies might accelerate {Company}'s {Goal} initiatives?

Thank you,
[Your Name]"""
            },
            {
                "name": "Market Advantage",
                "template": """Hi {Name},

The retail landscape is increasingly competitive, and companies like {Company} need strategic advantages to thrive. I believe {Goal} is key to maintaining market leadership.

Our proven solutions have helped retail organizations gain 20% market share while optimizing operational costs. We understand the unique challenges facing retail leaders today.

I'd appreciate the opportunity to discuss how our approach might support {Company}'s {Goal} objectives.

Are you available for a brief call this week?

Best,
[Your Name]"""
            }
        ]
    
    def _get_consulting_templates(self):
        """Consulting industry templates emphasizing strategic value and client success."""
        return [
            {
                "name": "Strategic Advantage",
                "template": """Dear {Name},

Consulting firms like {Company} must constantly demonstrate clear value to clients while differentiating from competitors. I imagine {Goal} is essential for maintaining your competitive edge.

We've helped consulting organizations increase client satisfaction by 50% while improving project profitability. Our approach specifically addresses the challenges facing modern consulting practices.

Given your strategic role at {Company}, I'd value discussing how our proven methodology might enhance your {Goal} capabilities.

Would you be available for a 15-minute strategic conversation?

Best regards,
[Your Name]"""
            },
            {
                "name": "Client Success Focus",
                "template": """Hello {Name},

Client success is the foundation of consulting excellence. I suspect {Goal} is central to {Company}'s client satisfaction and retention strategies.

We've developed solutions that have helped consulting firms achieve 40% improvement in client outcomes while reducing project delivery time. Our methodology understands the unique demands of consulting work.

Would you be interested in exploring how these approaches might strengthen {Company}'s {Goal} initiatives?

Thank you,
[Your Name]"""
            },
            {
                "name": "Operational Excellence",
                "template": """Hi {Name},

Consulting efficiency directly impacts both client satisfaction and profitability. I believe {Goal} is crucial for {Company}'s operational excellence and growth.

Our proven strategies have helped consulting organizations improve operational efficiency by 35% while enhancing service delivery quality. We understand the balance consulting leaders must maintain.

I'd appreciate the opportunity to discuss how our approach might optimize {Company}'s {Goal} efforts.

Are you available for a brief conversation?

Best,
[Your Name]"""
            }
        ]
    
    def _get_education_templates(self):
        """Education industry templates emphasizing outcomes and accessibility."""
        return [
            {
                "name": "Student Success Focus",
                "template": """Hello {Name},

Educational institutions like {Company} are committed to improving student outcomes while managing resource constraints. I imagine {Goal} is central to your mission of educational excellence.

We've helped educational organizations improve student success rates by 30% while optimizing operational costs. Our approach specifically addresses the unique challenges facing education leaders today.

Given your role at {Company}, I'd value the opportunity to discuss how our proven strategies might support your {Goal} objectives.

Would you have 15 minutes available for a conversation?

Best regards,
[Your Name]"""
            },
            {
                "name": "Accessibility & Engagement",
                "template": """Hi {Name},

Accessibility and student engagement have become critical factors in educational success. I suspect {Goal} involves enhancing {Company}'s ability to reach and engage diverse student populations.

We've developed solutions that have helped educational institutions increase student engagement by 40% while improving accessibility across all demographics. Our methodology understands modern educational challenges.

Would you be interested in exploring how these approaches might enhance {Company}'s {Goal} initiatives?

Thank you,
[Your Name]"""
            },
            {
                "name": "Educational Innovation",
                "template": """Hello {Name},

Educational innovation requires balancing traditional excellence with modern learning approaches. I believe {Goal} is key to {Company}'s continued educational leadership.

Our proven strategies have helped educational organizations implement innovative programs that improved learning outcomes by 25% while maintaining academic standards. We understand the complexities of educational transformation.

I'd appreciate discussing how our approach might support {Company}'s {Goal} efforts.

Are you available for a brief call?

Best,
[Your Name]"""
            }
        ]
    
    def _get_real_estate_templates(self):
        """Real estate industry templates emphasizing relationships and market advantage."""
        return [
            {
                "name": "Market Leadership",
                "template": """Hello {Name},

Real estate success depends on market knowledge and client relationships. I imagine {Goal} is essential for {Company}'s continued market leadership and growth.

We've helped real estate organizations increase transaction volume by 35% while improving client satisfaction scores. Our approach addresses both market dynamics and relationship management.

Given your position at {Company}, I'd love to discuss how our proven strategies might enhance your {Goal} objectives.

Would you be open to a 15-minute conversation?

Best regards,
[Your Name]"""
            },
            {
                "name": "Client Satisfaction",
                "template": """Hi {Name},

Client satisfaction drives referrals and repeat business in real estate. I suspect {Goal} is central to {Company}'s client relationship and retention strategies.

We've developed approaches that have helped real estate firms achieve 90% client satisfaction while reducing transaction time by 20%. Our methodology understands the importance of client experience in real estate.

Would you be interested in exploring how these strategies might strengthen {Company}'s {Goal} initiatives?

Thank you,
[Your Name]"""
            },
            {
                "name": "Growth Opportunity",
                "template": """Hello {Name},

Real estate markets offer significant growth opportunities for well-positioned organizations. I believe {Goal} is crucial for {Company}'s market expansion and success.

Our proven solutions have helped real estate companies identify and capitalize on growth opportunities, resulting in 40% revenue increase while maintaining service quality.

I'd appreciate the opportunity to discuss how our approach might optimize {Company}'s {Goal} efforts.

Are you available for a brief conversation?

Best,
[Your Name]"""
            }
        ]
    
    def _get_energy_templates(self):
        """Energy industry templates emphasizing sustainability and innovation."""
        return [
            {
                "name": "Sustainability Focus",
                "template": """Dear {Name},

The energy sector is undergoing unprecedented transformation toward sustainability. I imagine {Goal} is central to {Company}'s strategic positioning in this evolving landscape.

We've helped energy organizations achieve 50% improvement in sustainability metrics while maintaining operational efficiency. Our approach addresses both environmental responsibilities and business objectives.

Given your leadership role at {Company}, I'd value discussing how our proven methodology might support your {Goal} initiatives.

Would you be available for a 15-minute strategic conversation?

Best regards,
[Your Name]"""
            },
            {
                "name": "Operational Innovation",
                "template": """Hello {Name},

Energy companies must balance innovation with reliable operations. I suspect {Goal} requires strategic approaches that enhance {Company}'s operational capabilities while embracing new technologies.

We've developed solutions that have helped energy organizations improve operational efficiency by 30% while successfully implementing innovative technologies. Our methodology understands the unique challenges in energy sector transformation.

Would you be interested in exploring how these approaches might accelerate {Company}'s {Goal} objectives?

Thank you,
[Your Name]"""
            },
            {
                "name": "Regulatory Compliance",
                "template": """Hi {Name},

Regulatory compliance continues to evolve in the energy sector. I believe {Goal} involves navigating these requirements while maintaining {Company}'s competitive advantage.

Our proven strategies have helped energy companies achieve 100% regulatory compliance while reducing compliance costs by 25%. We understand the balance energy leaders must maintain between regulation and innovation.

I'd appreciate the opportunity to discuss how our approach might optimize {Company}'s {Goal} efforts.

Are you available for a brief call?

Best,
[Your Name]"""
            }
        ]
    
    def _get_media_templates(self):
        """Media industry templates emphasizing creativity and audience engagement."""
        return [
            {
                "name": "Audience Engagement",
                "template": """Hi {Name},

Media companies like {Company} must constantly innovate to capture and maintain audience attention. I imagine {Goal} is crucial for your content strategy and audience growth.

We've helped media organizations increase audience engagement by 60% while improving content ROI. Our approach combines creative strategy with data-driven optimization for maximum impact.

Given your role at {Company}, I'd love to discuss how our proven strategies might enhance your {Goal} initiatives.

Would you be open to a 15-minute creative conversation?

Best regards,
[Your Name]"""
            },
            {
                "name": "Brand Growth",
                "template": """Hello {Name},

Brand differentiation is essential in today's competitive media landscape. I suspect {Goal} involves strengthening {Company}'s brand presence while expanding audience reach.

We've developed approaches that have helped media companies achieve 45% brand growth while maintaining authentic audience connections. Our methodology understands both creative excellence and business growth.

Would you be interested in exploring how these strategies might amplify {Company}'s {Goal} objectives?

Thank you,
[Your Name]"""
            },
            {
                "name": "Creative Innovation",
                "template": """Hello {Name},

Creative innovation drives success in the media industry. I believe {Goal} is key to {Company}'s continued creative leadership and market impact.

Our proven solutions have helped media organizations launch innovative campaigns that delivered 300% engagement improvement while maintaining brand integrity. We understand the creative challenges facing media leaders today.

I'd appreciate discussing how our approach might inspire {Company}'s {Goal} efforts.

Are you available for a brief conversation?

Best,
[Your Name]"""
            }
        ]
    
    def _get_general_templates(self):
        """General templates for industries not specifically categorized."""
        return [
            {
                "name": "Business Growth Focus",
                "template": """Hello {Name},

{Company} appears to be well-positioned for continued growth in your industry. I imagine {Goal} is a strategic priority for your organization's success.

We've helped similar companies achieve significant improvements in their core business objectives while optimizing operational efficiency. Our approach is tailored to each organization's unique challenges and opportunities.

Given your leadership role at {Company}, I'd value the opportunity to discuss how our proven strategies might support your {Goal} initiatives.

Would you be available for a 15-minute conversation?

Best regards,
[Your Name]"""
            },
            {
                "name": "Operational Excellence",
                "template": """Hi {Name},

Operational excellence is crucial for sustained business success. I suspect {Goal} requires strategic approaches that enhance {Company}'s operational capabilities while driving growth.

We've developed solutions that have helped organizations improve operational efficiency by 35% while achieving their strategic objectives. Our methodology addresses the common challenges facing business leaders today.

Would you be interested in exploring how these approaches might optimize {Company}'s {Goal} efforts?

Thank you,
[Your Name]"""
            },
            {
                "name": "Strategic Advantage",
                "template": """Hello {Name},

Competitive advantage requires continuous innovation and optimization. I believe {Goal} is essential for {Company}'s strategic positioning and market success.

Our proven strategies have helped organizations gain significant competitive advantages while improving overall business performance. We understand the balance leaders must maintain between growth and operational excellence.

I'd appreciate the opportunity to discuss how our approach might enhance {Company}'s {Goal} objectives.

Are you available for a brief call this week?

Best,
[Your Name]"""
            }
        ]

# Convenience function for easy import
def get_industry_templates(industry):
    """
    Get templates for specific industry.
    
    Args:
        industry (str): Industry name
        
    Returns:
        list: Industry-specific templates
    """
    templates = IndustryTemplates()
    return templates.get_templates_for_industry(industry)