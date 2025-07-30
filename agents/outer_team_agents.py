"""
Outer Team Agents for Assignment 0: SoM Teams
============================================

This module contains coordination agents that manage multiple inner teams
and facilitate communication, resource allocation, and quality assurance
at the outer team level.
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


class BaseOuterTeamAgent(AssistantAgent):
    """Base class for outer team coordination agents."""
    
    def __init__(self, name: str, system_message: str, **kwargs):
        super().__init__(
            name=name,
            system_message=system_message,
            **kwargs
        )
        self.coordination_history = []
        self.performance_metrics = {
            "coordination_tasks": 0,
            "successful_integrations": 0,
            "conflict_resolutions": 0,
            "resource_allocations": 0
        }
    
    def log_coordination_task(self, task_type: str, details: Dict[str, Any], success: bool = True):
        """Log coordination task for performance tracking."""
        self.coordination_history.append({
            "timestamp": datetime.now().isoformat(),
            "task_type": task_type,
            "details": details,
            "success": success
        })
        
        self.performance_metrics["coordination_tasks"] += 1
        if success:
            if task_type == "integration":
                self.performance_metrics["successful_integrations"] += 1
            elif task_type == "conflict_resolution":
                self.performance_metrics["conflict_resolutions"] += 1
            elif task_type == "resource_allocation":
                self.performance_metrics["resource_allocations"] += 1


class TeamCoordinatorAgent(BaseOuterTeamAgent):
    """Agent responsible for coordinating between multiple inner teams."""
    
    def __init__(self, **kwargs):
        system_message = """
        You are the Team Coordinator Agent in the outer coordination layer.
        
        Your primary responsibilities:
        - Coordinate communication between inner teams
        - Identify dependencies and integration points
        - Resolve conflicts between team outputs
        - Ensure alignment with overall project objectives
        - Facilitate knowledge sharing between teams
        
        Key capabilities:
        - Inter-team communication facilitation
        - Dependency mapping and management
        - Conflict identification and resolution
        - Integration planning and execution
        - Progress tracking and reporting
        
        Coordination principles:
        - Maintain clear communication channels
        - Identify and resolve conflicts early
        - Ensure all teams work toward common goals
        - Facilitate knowledge and resource sharing
        - Escalate critical issues to human oversight
        
        Always:
        - Map dependencies between team deliverables
        - Identify potential conflicts before they occur
        - Propose integration strategies for team outputs
        - Request human intervention for critical decisions
        - Document all coordination activities
        """
        
        super().__init__(
            name="TeamCoordinator",
            system_message=system_message,
            **kwargs
        )
        self.team_dependencies = {}
        self.active_conflicts = []
        self.integration_plans = {}
    
    def analyze_team_dependencies(self, team_outputs: Dict[str, str]) -> Dict[str, List[str]]:
        """Analyze dependencies between team outputs."""
        dependencies = {}
        
        # Simple dependency analysis based on content overlap
        teams = list(team_outputs.keys())
        for i, team1 in enumerate(teams):
            dependencies[team1] = []
            for j, team2 in enumerate(teams):
                if i != j:
                    # Check for potential dependencies (simplified)
                    output1 = team_outputs[team1].lower()
                    output2 = team_outputs[team2].lower()
                    
                    # Look for common keywords that suggest dependencies
                    common_keywords = ['data', 'requirements', 'design', 'implementation', 
                                     'strategy', 'analysis', 'content', 'technical']
                    
                    overlap_score = sum(1 for keyword in common_keywords 
                                      if keyword in output1 and keyword in output2)
                    
                    if overlap_score >= 2:  # Threshold for dependency
                        dependencies[team1].append(team2)
        
        self.team_dependencies = dependencies
        return dependencies
    
    def create_integration_plan(self, team_outputs: Dict[str, str]) -> str:
        """Create a plan for integrating team outputs."""
        dependencies = self.analyze_team_dependencies(team_outputs)
        
        integration_plan = f"""
        TEAM INTEGRATION PLAN
        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        TEAM DEPENDENCIES:
        {json.dumps(dependencies, indent=2)}
        
        INTEGRATION STRATEGY:
        1. Sequential Integration:
           - Start with teams that have no dependencies
           - Integrate dependent teams in dependency order
           
        2. Conflict Resolution:
           - Identify overlapping responsibilities
           - Merge complementary outputs
           - Resolve contradictory recommendations
           
        3. Quality Assurance:
           - Validate integrated output against requirements
           - Ensure consistency across all team contributions
           - Verify completeness of final deliverable
        
        RECOMMENDED INTEGRATION ORDER:
        """
        
        # Determine integration order based on dependencies
        integration_order = self._calculate_integration_order(dependencies)
        for i, team in enumerate(integration_order, 1):
            integration_plan += f"\n        {i}. {team}"
        
        integration_plan += f"""
        
        HUMAN INTERVENTION POINTS:
        - Approve dependency analysis
        - Validate integration strategy
        - Resolve complex conflicts
        - Approve final integrated output
        """
        
        self.integration_plans[datetime.now().isoformat()] = integration_plan
        return integration_plan
    
    def _calculate_integration_order(self, dependencies: Dict[str, List[str]]) -> List[str]:
        """Calculate optimal integration order based on dependencies."""
        # Simple topological sort for integration order
        teams = list(dependencies.keys())
        in_degree = {team: 0 for team in teams}
        
        # Calculate in-degrees
        for team, deps in dependencies.items():
            for dep in deps:
                if dep in in_degree:
                    in_degree[dep] += 1
        
        # Sort by in-degree (teams with fewer dependencies first)
        return sorted(teams, key=lambda x: in_degree[x])


class ResourceManagerAgent(BaseOuterTeamAgent):
    """Agent responsible for managing resources across teams."""
    
    def __init__(self, **kwargs):
        system_message = """
        You are the Resource Manager Agent in the outer coordination layer.
        
        Your primary responsibilities:
        - Allocate resources (time, budget, personnel) across teams
        - Monitor resource utilization and efficiency
        - Identify resource conflicts and bottlenecks
        - Optimize resource distribution for project success
        - Provide resource recommendations to human oversight
        
        Key capabilities:
        - Resource requirement analysis
        - Allocation optimization algorithms
        - Utilization monitoring and reporting
        - Bottleneck identification and resolution
        - Cost-benefit analysis for resource decisions
        
        Resource management principles:
        - Prioritize critical path activities
        - Balance resource utilization across teams
        - Minimize idle time and resource waste
        - Consider both current and future resource needs
        - Escalate resource conflicts to human decision-makers
        
        Always:
        - Analyze resource requirements objectively
        - Consider project priorities and deadlines
        - Identify potential resource conflicts early
        - Provide data-driven allocation recommendations
        - Request human approval for major resource decisions
        """
        
        super().__init__(
            name="ResourceManager",
            system_message=system_message,
            **kwargs
        )
        self.resource_allocations = {}
        self.utilization_metrics = {}
        self.resource_conflicts = []
    
    def analyze_resource_requirements(self, team_requests: Dict[str, Dict]) -> Dict[str, Any]:
        """Analyze resource requirements from all teams."""
        analysis = {
            "total_budget_requested": 0,
            "total_time_requested": 0,
            "personnel_requests": {},
            "priority_analysis": {},
            "conflict_areas": []
        }
        
        for team, request in team_requests.items():
            # Extract resource requirements
            budget = request.get('budget', 0)
            time = request.get('time_weeks', 0)
            personnel = request.get('personnel', [])
            priority = request.get('priority', 'medium')
            
            analysis["total_budget_requested"] += budget
            analysis["total_time_requested"] += time
            analysis["priority_analysis"][team] = priority
            
            # Track personnel requests
            for person in personnel:
                if person not in analysis["personnel_requests"]:
                    analysis["personnel_requests"][person] = []
                analysis["personnel_requests"][person].append(team)
        
        # Identify conflicts (same person requested by multiple teams)
        for person, requesting_teams in analysis["personnel_requests"].items():
            if len(requesting_teams) > 1:
                analysis["conflict_areas"].append({
                    "type": "personnel_conflict",
                    "resource": person,
                    "conflicting_teams": requesting_teams
                })
        
        return analysis
    
    def create_allocation_plan(self, team_requests: Dict[str, Dict], 
                             available_resources: Dict[str, Any]) -> str:
        """Create resource allocation plan."""
        analysis = self.analyze_resource_requirements(team_requests)
        
        allocation_plan = f"""
        RESOURCE ALLOCATION PLAN
        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        RESOURCE ANALYSIS:
        - Total Budget Requested: ${analysis['total_budget_requested']:,}
        - Available Budget: ${available_resources.get('budget', 0):,}
        - Total Time Requested: {analysis['total_time_requested']} weeks
        - Available Timeline: {available_resources.get('timeline_weeks', 0)} weeks
        
        PRIORITY-BASED ALLOCATION:
        """
        
        # Sort teams by priority
        priority_order = {'high': 3, 'medium': 2, 'low': 1}
        sorted_teams = sorted(
            team_requests.items(),
            key=lambda x: priority_order.get(x[1].get('priority', 'medium'), 2),
            reverse=True
        )
        
        allocated_budget = 0
        allocated_time = 0
        
        for team, request in sorted_teams:
            team_budget = request.get('budget', 0)
            team_time = request.get('time_weeks', 0)
            priority = request.get('priority', 'medium')
            
            # Check if allocation is possible
            budget_available = (allocated_budget + team_budget) <= available_resources.get('budget', 0)
            time_available = (allocated_time + team_time) <= available_resources.get('timeline_weeks', 0)
            
            if budget_available and time_available:
                status = "APPROVED"
                allocated_budget += team_budget
                allocated_time += team_time
            else:
                status = "REQUIRES_HUMAN_DECISION"
            
            allocation_plan += f"""
        {team.upper()}:
        - Priority: {priority}
        - Budget Request: ${team_budget:,}
        - Time Request: {team_time} weeks
        - Status: {status}
        """
        
        allocation_plan += f"""
        
        CONFLICT RESOLUTION NEEDED:
        {json.dumps(analysis['conflict_areas'], indent=2)}
        
        HUMAN DECISIONS REQUIRED:
        - Approve high-priority allocations
        - Resolve personnel conflicts
        - Decide on over-budget requests
        - Set final timeline constraints
        """
        
        return allocation_plan


class QualityAssuranceAgent(BaseOuterTeamAgent):
    """Agent responsible for quality assurance across all teams."""
    
    def __init__(self, **kwargs):
        system_message = """
        You are the Quality Assurance Agent in the outer coordination layer.
        
        Your primary responsibilities:
        - Establish quality standards and criteria
        - Review outputs from all inner teams
        - Identify quality issues and improvement opportunities
        - Ensure consistency across team deliverables
        - Validate final integrated outputs
        
        Key capabilities:
        - Quality criteria definition and validation
        - Multi-dimensional quality assessment
        - Consistency checking across deliverables
        - Gap analysis and improvement recommendations
        - Final output validation and approval
        
        Quality assurance principles:
        - Define clear, measurable quality criteria
        - Apply consistent standards across all teams
        - Identify issues early in the process
        - Provide constructive feedback for improvement
        - Ensure final output meets all requirements
        
        Always:
        - Establish quality criteria before review
        - Provide specific, actionable feedback
        - Check for consistency across team outputs
        - Validate against original requirements
        - Request human validation for quality decisions
        """
        
        super().__init__(
            name="QualityAssurance",
            system_message=system_message,
            **kwargs
        )
        self.quality_criteria = {}
        self.quality_assessments = {}
        self.improvement_recommendations = {}
    
    def establish_quality_criteria(self, project_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Establish quality criteria based on project requirements."""
        criteria = {
            "completeness": {
                "description": "All required elements are present",
                "weight": 0.25,
                "measurement": "percentage_of_requirements_met"
            },
            "accuracy": {
                "description": "Information is correct and validated",
                "weight": 0.25,
                "measurement": "error_rate_percentage"
            },
            "consistency": {
                "description": "Consistent style, format, and messaging",
                "weight": 0.20,
                "measurement": "consistency_score"
            },
            "clarity": {
                "description": "Clear, understandable communication",
                "weight": 0.15,
                "measurement": "readability_score"
            },
            "alignment": {
                "description": "Aligned with project objectives",
                "weight": 0.15,
                "measurement": "objective_alignment_score"
            }
        }
        
        self.quality_criteria = criteria
        return criteria
    
    def assess_team_output(self, team_name: str, output: str, 
                          requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Assess quality of team output against established criteria."""
        if not self.quality_criteria:
            self.establish_quality_criteria(requirements)
        
        assessment = {
            "team": team_name,
            "timestamp": datetime.now().isoformat(),
            "scores": {},
            "overall_score": 0.0,
            "issues": [],
            "recommendations": []
        }
        
        # Simplified quality scoring (in real implementation, would use more sophisticated methods)
        for criterion, details in self.quality_criteria.items():
            # Mock scoring based on output length and content
            if criterion == "completeness":
                score = min(100, len(output) / 10)  # Simplified completeness check
            elif criterion == "accuracy":
                score = 85  # Would need fact-checking in real implementation
            elif criterion == "consistency":
                score = 90  # Would check against style guide
            elif criterion == "clarity":
                score = 80  # Would use readability metrics
            elif criterion == "alignment":
                score = 88  # Would check against objectives
            else:
                score = 85
            
            assessment["scores"][criterion] = score
            
            # Identify issues if score is below threshold
            if score < 80:
                assessment["issues"].append(f"Low {criterion} score: {score}")
                assessment["recommendations"].append(f"Improve {criterion}: {details['description']}")
        
        # Calculate overall score
        total_weighted_score = sum(
            assessment["scores"][criterion] * details["weight"]
            for criterion, details in self.quality_criteria.items()
        )
        assessment["overall_score"] = total_weighted_score
        
        self.quality_assessments[f"{team_name}_{datetime.now().isoformat()}"] = assessment
        return assessment
    
    def create_quality_report(self, team_assessments: Dict[str, Dict]) -> str:
        """Create comprehensive quality report."""
        report = f"""
        QUALITY ASSURANCE REPORT
        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        QUALITY CRITERIA:
        {json.dumps(self.quality_criteria, indent=2)}
        
        TEAM ASSESSMENTS:
        """
        
        overall_scores = []
        all_issues = []
        all_recommendations = []
        
        for team, assessment in team_assessments.items():
            overall_scores.append(assessment["overall_score"])
            all_issues.extend(assessment["issues"])
            all_recommendations.extend(assessment["recommendations"])
            
            report += f"""
        {team.upper()}:
        - Overall Score: {assessment['overall_score']:.1f}/100
        - Individual Scores: {assessment['scores']}
        - Issues: {len(assessment['issues'])}
        - Status: {'PASS' if assessment['overall_score'] >= 80 else 'NEEDS_IMPROVEMENT'}
        """
        
        avg_score = sum(overall_scores) / len(overall_scores) if overall_scores else 0
        
        report += f"""
        
        SUMMARY:
        - Average Quality Score: {avg_score:.1f}/100
        - Teams Passing (≥80): {sum(1 for score in overall_scores if score >= 80)}
        - Teams Needing Improvement: {sum(1 for score in overall_scores if score < 80)}
        - Total Issues Identified: {len(all_issues)}
        
        CRITICAL ISSUES:
        {chr(10).join(f"- {issue}" for issue in all_issues[:10])}  # Top 10 issues
        
        IMPROVEMENT RECOMMENDATIONS:
        {chr(10).join(f"- {rec}" for rec in set(all_recommendations)[:10])}  # Top 10 unique recommendations
        
        HUMAN VALIDATION REQUIRED:
        - Review quality criteria and weights
        - Approve teams with borderline scores
        - Prioritize improvement recommendations
        - Make final quality acceptance decision
        """
        
        return report


# =============================================================================
# OUTER TEAM FACTORY AND UTILITIES
# =============================================================================

class OuterTeamAgentFactory:
    """Factory for creating outer team coordination agents."""
    
    @staticmethod
    def create_coordination_agents(llm_config: Dict) -> Dict[str, BaseOuterTeamAgent]:
        """Create all outer team coordination agents."""
        return {
            "team_coordinator": TeamCoordinatorAgent(llm_config=llm_config),
            "resource_manager": ResourceManagerAgent(llm_config=llm_config),
            "quality_assurance": QualityAssuranceAgent(llm_config=llm_config)
        }


def get_coordination_summary(agents: Dict[str, BaseOuterTeamAgent]) -> Dict[str, Any]:
    """Get summary of coordination activities."""
    summary = {
        "total_coordination_tasks": 0,
        "successful_integrations": 0,
        "conflict_resolutions": 0,
        "resource_allocations": 0,
        "agent_performance": {}
    }
    
    for agent_name, agent in agents.items():
        metrics = agent.performance_metrics
        summary["total_coordination_tasks"] += metrics["coordination_tasks"]
        summary["successful_integrations"] += metrics["successful_integrations"]
        summary["conflict_resolutions"] += metrics["conflict_resolutions"]
        summary["resource_allocations"] += metrics["resource_allocations"]
        
        summary["agent_performance"][agent_name] = {
            "coordination_tasks": metrics["coordination_tasks"],
            "success_rate": (
                metrics["successful_integrations"] / max(1, metrics["coordination_tasks"])
            ),
            "specialization": agent_name.replace("_", " ").title()
        }
    
    return summary
