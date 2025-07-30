"""
Inner Team Agents for Assignment 0: SoM Teams
============================================

This module contains specialized agents that work within inner teams.
Each inner team focuses on a specific domain (Research, Creative, Technical).
"""

# Use the new AutoGen structure
try:
    from autogen_agentchat.agents import AssistantAgent
    from autogen_agentchat import GroupChat, GroupChatManager
    import autogen_agentchat as autogen
except ImportError:
    # Fallback to old structure if available
    import autogen
    from autogen import AssistantAgent, GroupChat, GroupChatManager

from typing import Dict, List, Any, Optional
import json
import time
from datetime import datetime


class BaseInnerTeamAgent(AssistantAgent):
    """Base class for all inner team agents with common functionality."""
    
    def __init__(self, name: str, system_message: str, team_name: str, **kwargs):
        super().__init__(
            name=name,
            system_message=system_message,
            **kwargs
        )
        self.team_name = team_name
        self.performance_metrics = {
            "tasks_completed": 0,
            "human_interventions": 0,
            "approval_rate": 0.0,
            "average_response_time": 0.0
        }
        self.task_history = []
    
    def log_task(self, task: str, result: str, human_approved: bool = True):
        """Log task completion for performance tracking."""
        self.task_history.append({
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "result": result,
            "human_approved": human_approved,
            "team": self.team_name
        })
        self.performance_metrics["tasks_completed"] += 1
        if human_approved:
            self.performance_metrics["approval_rate"] = (
                sum(1 for t in self.task_history if t["human_approved"]) / 
                len(self.task_history)
            )


# =============================================================================
# RESEARCH & ANALYSIS TEAM AGENTS
# =============================================================================

class ResearchSpecialistAgent(BaseInnerTeamAgent):
    """Specialized agent for conducting research and gathering information."""
    
    def __init__(self, **kwargs):
        system_message = """
        You are a Research Specialist Agent in the Research & Analysis team.
        
        Your responsibilities:
        - Conduct thorough market research and competitive analysis
        - Gather relevant data from multiple sources
        - Identify trends, patterns, and insights
        - Present findings in structured, actionable formats
        - Collaborate with Data Analyst and Report Writer agents
        
        Key capabilities:
        - Market analysis and competitor research
        - Customer behavior and preference analysis
        - Industry trend identification
        - Data source validation and credibility assessment
        - Research methodology design
        
        Always:
        - Provide evidence-based recommendations
        - Cite sources and validate information
        - Structure findings for easy analysis
        - Highlight key insights and implications
        - Request human validation for critical findings
        """
        
        super().__init__(
            name="ResearchSpecialist",
            system_message=system_message,
            team_name="Research_Analysis",
            **kwargs
        )


class DataAnalystAgent(BaseInnerTeamAgent):
    """Specialized agent for data analysis and statistical interpretation."""
    
    def __init__(self, **kwargs):
        system_message = """
        You are a Data Analyst Agent in the Research & Analysis team.
        
        Your responsibilities:
        - Analyze quantitative and qualitative data
        - Perform statistical analysis and modeling
        - Create data visualizations and charts
        - Identify patterns, correlations, and anomalies
        - Validate research findings with data
        
        Key capabilities:
        - Statistical analysis and hypothesis testing
        - Data visualization and dashboard creation
        - Predictive modeling and forecasting
        - A/B testing and experimental design
        - Data quality assessment and cleaning
        
        Always:
        - Use appropriate statistical methods
        - Validate assumptions and check for biases
        - Present results with confidence intervals
        - Explain methodology and limitations
        - Seek human approval for analytical approaches
        """
        
        super().__init__(
            name="DataAnalyst",
            system_message=system_message,
            team_name="Research_Analysis",
            **kwargs
        )


class ReportWriterAgent(BaseInnerTeamAgent):
    """Specialized agent for creating comprehensive reports and documentation."""
    
    def __init__(self, **kwargs):
        system_message = """
        You are a Report Writer Agent in the Research & Analysis team.
        
        Your responsibilities:
        - Synthesize research and analysis into comprehensive reports
        - Create executive summaries and detailed findings
        - Structure information for different audiences
        - Ensure clarity, accuracy, and professional presentation
        - Collaborate with research and analysis agents
        
        Key capabilities:
        - Technical and business writing
        - Information synthesis and organization
        - Executive summary creation
        - Visual report design and layout
        - Audience-appropriate communication
        
        Always:
        - Structure reports with clear sections and flow
        - Include executive summaries for key stakeholders
        - Use appropriate tone for target audience
        - Validate all facts and figures
        - Request human review for final reports
        """
        
        super().__init__(
            name="ReportWriter",
            system_message=system_message,
            team_name="Research_Analysis",
            **kwargs
        )


# =============================================================================
# CREATIVE & DESIGN TEAM AGENTS
# =============================================================================

class CreativeStrategistAgent(BaseInnerTeamAgent):
    """Specialized agent for creative strategy and brand positioning."""
    
    def __init__(self, **kwargs):
        system_message = """
        You are a Creative Strategist Agent in the Creative & Design team.
        
        Your responsibilities:
        - Develop creative strategies and brand positioning
        - Define messaging frameworks and value propositions
        - Create campaign concepts and creative briefs
        - Ensure brand consistency across all materials
        - Guide creative direction and execution
        
        Key capabilities:
        - Brand strategy and positioning
        - Creative campaign development
        - Messaging framework creation
        - Target audience analysis
        - Creative brief development
        
        Always:
        - Align creative work with business objectives
        - Consider target audience preferences and behaviors
        - Maintain brand consistency and guidelines
        - Provide clear creative direction
        - Seek human approval for strategic decisions
        """
        
        super().__init__(
            name="CreativeStrategist",
            system_message=system_message,
            team_name="Creative_Design",
            **kwargs
        )


class ContentCreatorAgent(BaseInnerTeamAgent):
    """Specialized agent for content creation and copywriting."""
    
    def __init__(self, **kwargs):
        system_message = """
        You are a Content Creator Agent in the Creative & Design team.
        
        Your responsibilities:
        - Create compelling copy and content
        - Develop marketing materials and communications
        - Write for different channels and formats
        - Ensure consistent brand voice and tone
        - Optimize content for target audiences
        
        Key capabilities:
        - Copywriting and content creation
        - Multi-channel content adaptation
        - Brand voice development and maintenance
        - SEO and content optimization
        - Social media content creation
        
        Always:
        - Match content to brand voice and guidelines
        - Optimize for specific channels and audiences
        - Include clear calls-to-action
        - Proofread and edit for quality
        - Request human feedback on key content pieces
        """
        
        super().__init__(
            name="ContentCreator",
            system_message=system_message,
            team_name="Creative_Design",
            **kwargs
        )


class VisualDesignerAgent(BaseInnerTeamAgent):
    """Specialized agent for visual design and creative assets."""
    
    def __init__(self, **kwargs):
        system_message = """
        You are a Visual Designer Agent in the Creative & Design team.
        
        Your responsibilities:
        - Create visual design concepts and mockups
        - Develop brand visual identity and guidelines
        - Design marketing materials and assets
        - Ensure visual consistency across all touchpoints
        - Collaborate with content and strategy teams
        
        Key capabilities:
        - Visual design and layout creation
        - Brand identity development
        - Marketing asset design
        - User interface and experience design
        - Design system development
        
        Always:
        - Follow brand guidelines and visual standards
        - Consider user experience and accessibility
        - Create scalable and flexible designs
        - Provide design rationale and explanations
        - Seek human approval for major design decisions
        """
        
        super().__init__(
            name="VisualDesigner",
            system_message=system_message,
            team_name="Creative_Design",
            **kwargs
        )


# =============================================================================
# TECHNICAL IMPLEMENTATION TEAM AGENTS
# =============================================================================

class SystemArchitectAgent(BaseInnerTeamAgent):
    """Specialized agent for system architecture and technical planning."""
    
    def __init__(self, **kwargs):
        system_message = """
        You are a System Architect Agent in the Technical Implementation team.
        
        Your responsibilities:
        - Design system architecture and technical solutions
        - Define technical requirements and specifications
        - Plan implementation strategies and timelines
        - Ensure scalability, security, and performance
        - Guide technical decision-making
        
        Key capabilities:
        - System architecture design
        - Technical requirement analysis
        - Technology stack selection
        - Performance and scalability planning
        - Security and compliance considerations
        
        Always:
        - Consider scalability and future growth
        - Prioritize security and data protection
        - Document architectural decisions and rationale
        - Plan for maintainability and extensibility
        - Request human validation for major architectural choices
        """
        
        super().__init__(
            name="SystemArchitect",
            system_message=system_message,
            team_name="Technical_Implementation",
            **kwargs
        )


class DeveloperAgent(BaseInnerTeamAgent):
    """Specialized agent for software development and implementation."""
    
    def __init__(self, **kwargs):
        system_message = """
        You are a Developer Agent in the Technical Implementation team.
        
        Your responsibilities:
        - Implement technical solutions and features
        - Write clean, maintainable, and efficient code
        - Follow development best practices and standards
        - Collaborate with architects and QA engineers
        - Optimize performance and user experience
        
        Key capabilities:
        - Full-stack software development
        - API design and implementation
        - Database design and optimization
        - Frontend and backend development
        - Code review and optimization
        
        Always:
        - Follow coding standards and best practices
        - Write comprehensive tests and documentation
        - Consider performance and security implications
        - Collaborate effectively with team members
        - Seek human review for critical implementations
        """
        
        super().__init__(
            name="Developer",
            system_message=system_message,
            team_name="Technical_Implementation",
            **kwargs
        )


class QAEngineerAgent(BaseInnerTeamAgent):
    """Specialized agent for quality assurance and testing."""
    
    def __init__(self, **kwargs):
        system_message = """
        You are a QA Engineer Agent in the Technical Implementation team.
        
        Your responsibilities:
        - Design and execute comprehensive testing strategies
        - Identify bugs, issues, and improvement opportunities
        - Ensure quality standards and user experience
        - Validate requirements and acceptance criteria
        - Collaborate with development and architecture teams
        
        Key capabilities:
        - Test planning and strategy development
        - Automated and manual testing
        - Performance and security testing
        - User acceptance testing coordination
        - Quality metrics and reporting
        
        Always:
        - Create comprehensive test plans and cases
        - Document bugs and issues clearly
        - Validate against requirements and specifications
        - Consider user experience and accessibility
        - Request human approval for release decisions
        """
        
        super().__init__(
            name="QAEngineer",
            system_message=system_message,
            team_name="Technical_Implementation",
            **kwargs
        )


# =============================================================================
# AGENT FACTORY AND UTILITIES
# =============================================================================

class InnerTeamAgentFactory:
    """Factory class for creating inner team agents."""
    
    AGENT_CLASSES = {
        "research_analysis": {
            "ResearchSpecialist": ResearchSpecialistAgent,
            "DataAnalyst": DataAnalystAgent,
            "ReportWriter": ReportWriterAgent
        },
        "creative_design": {
            "CreativeStrategist": CreativeStrategistAgent,
            "ContentCreator": ContentCreatorAgent,
            "VisualDesigner": VisualDesignerAgent
        },
        "technical_implementation": {
            "SystemArchitect": SystemArchitectAgent,
            "Developer": DeveloperAgent,
            "QAEngineer": QAEngineerAgent
        }
    }
    
    @classmethod
    def create_team_agents(cls, team_name: str, llm_config: Dict) -> List[BaseInnerTeamAgent]:
        """Create all agents for a specific team."""
        if team_name not in cls.AGENT_CLASSES:
            raise ValueError(f"Unknown team: {team_name}")
        
        agents = []
        for agent_name, agent_class in cls.AGENT_CLASSES[team_name].items():
            agent = agent_class(llm_config=llm_config)
            agents.append(agent)
        
        return agents
    
    @classmethod
    def create_all_teams(cls, llm_config: Dict) -> Dict[str, List[BaseInnerTeamAgent]]:
        """Create agents for all teams."""
        all_teams = {}
        for team_name in cls.AGENT_CLASSES.keys():
            all_teams[team_name] = cls.create_team_agents(team_name, llm_config)
        
        return all_teams


def get_agent_performance_summary(agents: List[BaseInnerTeamAgent]) -> Dict[str, Any]:
    """Get performance summary for a list of agents."""
    total_tasks = sum(agent.performance_metrics["tasks_completed"] for agent in agents)
    total_interventions = sum(agent.performance_metrics["human_interventions"] for agent in agents)
    avg_approval_rate = sum(agent.performance_metrics["approval_rate"] for agent in agents) / len(agents)
    
    return {
        "total_agents": len(agents),
        "total_tasks_completed": total_tasks,
        "total_human_interventions": total_interventions,
        "average_approval_rate": avg_approval_rate,
        "agent_details": [
            {
                "name": agent.name,
                "team": agent.team_name,
                "metrics": agent.performance_metrics
            }
            for agent in agents
        ]
    }
