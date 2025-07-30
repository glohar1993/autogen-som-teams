"""
Outer Team Coordination for SoM Framework
=========================================

This module handles the coordination between inner teams and manages
the overall project orchestration at the outer team level.
"""

from typing import Dict, List, Any, Optional
import json
import time
from datetime import datetime


class OuterTeamCoordinator:
    """Coordinates multiple inner teams and manages project-level decisions."""
    
    def __init__(self, outer_team_agents: Dict[str, Any], user_proxy: Any):
        self.outer_team_agents = outer_team_agents
        self.user_proxy = user_proxy
        self.coordination_history = []
        self.project_state = {
            "active_teams": [],
            "completed_teams": [],
            "pending_decisions": [],
            "resource_allocations": {},
            "quality_status": {}
        }
    
    def coordinate_project_execution(self, inner_team_results: Dict[str, str], 
                                   project_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate the execution of the overall project."""
        print("      🎯 Coordinating project execution...")
        
        coordination_result = {
            "timestamp": datetime.now().isoformat(),
            "coordination_steps": [],
            "decisions_made": [],
            "resource_allocations": {},
            "quality_assessments": {},
            "integration_plan": "",
            "final_recommendations": []
        }
        
        # Step 1: Team Coordination
        print("         📋 Step 1: Team coordination and integration planning")
        team_coordinator = self.outer_team_agents["team_coordinator"]
        integration_plan = team_coordinator.create_integration_plan(inner_team_results)
        coordination_result["integration_plan"] = integration_plan
        coordination_result["coordination_steps"].append("Integration plan created")
        
        # Human intervention for coordination approval
        coordination_decision = self.user_proxy.coordinate_teams(
            inner_team_results, 
            integration_plan
        )
        coordination_result["decisions_made"].append({
            "type": "coordination_approval",
            "approved": coordination_decision.approved,
            "feedback": coordination_decision.feedback
        })
        
        # Step 2: Resource Management
        print("         💰 Step 2: Resource allocation and management")
        resource_manager = self.outer_team_agents["resource_manager"]
        
        # Generate resource requests based on team results
        resource_requests = self._generate_resource_requests(inner_team_results)
        
        allocation_plan = resource_manager.create_allocation_plan(
            resource_requests,
            project_requirements.get("resources", {"budget": 500000, "timeline_weeks": 12})
        )
        
        # Human intervention for resource allocation
        allocation_decision = self.user_proxy.allocate_resources(resource_requests)
        coordination_result["resource_allocations"] = {
            "plan": allocation_plan,
            "human_decision": allocation_decision.feedback,
            "approved": allocation_decision.approved
        }
        coordination_result["coordination_steps"].append("Resource allocation completed")
        
        # Step 3: Quality Assurance
        print("         🔍 Step 3: Quality assurance and validation")
        qa_agent = self.outer_team_agents["quality_assurance"]
        
        # Assess quality of each team's output
        quality_assessments = {}
        for team_name, team_output in inner_team_results.items():
            assessment = qa_agent.assess_team_output(
                team_name, 
                team_output, 
                project_requirements
            )
            quality_assessments[team_name] = assessment
        
        # Generate comprehensive quality report
        quality_report = qa_agent.create_quality_report(quality_assessments)
        coordination_result["quality_assessments"] = {
            "individual_assessments": quality_assessments,
            "comprehensive_report": quality_report
        }
        coordination_result["coordination_steps"].append("Quality assessment completed")
        
        # Step 4: Final Integration and Recommendations
        print("         🎯 Step 4: Final integration and recommendations")
        final_recommendations = self._generate_final_recommendations(
            inner_team_results,
            coordination_result,
            project_requirements
        )
        coordination_result["final_recommendations"] = final_recommendations
        coordination_result["coordination_steps"].append("Final recommendations generated")
        
        # Log coordination activity
        self.coordination_history.append(coordination_result)
        
        # Update project state
        self._update_project_state(inner_team_results, coordination_result)
        
        return coordination_result
    
    def _generate_resource_requests(self, inner_team_results: Dict[str, str]) -> Dict[str, Dict]:
        """Generate resource requests based on team outputs."""
        resource_requests = {}
        
        base_budgets = {
            "research_analysis": 75000,
            "creative_design": 100000,
            "technical_implementation": 200000
        }
        
        base_timelines = {
            "research_analysis": 4,
            "creative_design": 6,
            "technical_implementation": 10
        }
        
        priorities = {
            "research_analysis": "high",
            "creative_design": "medium", 
            "technical_implementation": "high"
        }
        
        for team_name, team_output in inner_team_results.items():
            # Adjust resource requests based on output complexity
            complexity_factor = min(2.0, len(team_output) / 1000)  # Simple complexity measure
            
            resource_requests[team_name] = {
                "budget": int(base_budgets.get(team_name, 50000) * complexity_factor),
                "time_weeks": int(base_timelines.get(team_name, 4) * complexity_factor),
                "priority": priorities.get(team_name, "medium"),
                "description": f"Resources for {team_name.replace('_', ' ')} implementation",
                "personnel": self._get_personnel_requirements(team_name),
                "justification": f"Based on output complexity and scope: {len(team_output)} chars"
            }
        
        return resource_requests
    
    def _get_personnel_requirements(self, team_name: str) -> List[str]:
        """Get personnel requirements for each team."""
        personnel_map = {
            "research_analysis": ["Senior Researcher", "Data Analyst", "Research Coordinator"],
            "creative_design": ["Creative Director", "Content Strategist", "Visual Designer"],
            "technical_implementation": ["Tech Lead", "Senior Developer", "QA Engineer", "DevOps Engineer"]
        }
        
        return personnel_map.get(team_name, ["Team Lead", "Specialist"])
    
    def _generate_final_recommendations(self, inner_team_results: Dict[str, str],
                                      coordination_result: Dict[str, Any],
                                      project_requirements: Dict[str, Any]) -> List[str]:
        """Generate final project recommendations."""
        recommendations = []
        
        # Analyze team outputs for key insights
        all_outputs = " ".join(inner_team_results.values()).lower()
        
        # Strategic recommendations based on content analysis
        if "ai" in all_outputs and "personalization" in all_outputs:
            recommendations.append(
                "Prioritize AI-powered personalization as core differentiator"
            )
        
        if "market" in all_outputs and "growth" in all_outputs:
            recommendations.append(
                "Focus on rapid market entry to capitalize on growth opportunity"
            )
        
        if "user" in all_outputs and "experience" in all_outputs:
            recommendations.append(
                "Invest heavily in user experience optimization and testing"
            )
        
        if "technical" in all_outputs and "scalability" in all_outputs:
            recommendations.append(
                "Implement scalable architecture from launch to support growth"
            )
        
        # Resource-based recommendations
        total_budget = sum(
            req.get("budget", 0) 
            for req in coordination_result.get("resource_allocations", {}).get("plan", "").split("$")
            if req.replace(",", "").replace(":", "").strip().isdigit()
        )
        
        if total_budget > project_requirements.get("budget", 500000):
            recommendations.append(
                "Consider phased implementation to manage budget constraints"
            )
        
        # Quality-based recommendations
        quality_assessments = coordination_result.get("quality_assessments", {}).get("individual_assessments", {})
        low_quality_teams = [
            team for team, assessment in quality_assessments.items()
            if assessment.get("overall_score", 100) < 80
        ]
        
        if low_quality_teams:
            recommendations.append(
                f"Provide additional support and review for: {', '.join(low_quality_teams)}"
            )
        
        # Timeline recommendations
        if "crisis" in str(project_requirements).lower():
            recommendations.append(
                "Implement rapid response protocols with 24/7 monitoring"
            )
        else:
            recommendations.append(
                "Establish regular milestone reviews and progress checkpoints"
            )
        
        # Integration recommendations
        recommendations.extend([
            "Establish cross-team communication protocols",
            "Implement shared project management and tracking systems",
            "Create integrated testing and validation procedures",
            "Plan for post-launch monitoring and optimization"
        ])
        
        return recommendations
    
    def _update_project_state(self, inner_team_results: Dict[str, str], 
                            coordination_result: Dict[str, Any]):
        """Update the overall project state."""
        self.project_state["active_teams"] = list(inner_team_results.keys())
        self.project_state["completed_teams"].extend(
            team for team in inner_team_results.keys()
            if team not in self.project_state["completed_teams"]
        )
        
        # Update resource allocations
        if "resource_allocations" in coordination_result:
            self.project_state["resource_allocations"].update(
                coordination_result["resource_allocations"]
            )
        
        # Update quality status
        if "quality_assessments" in coordination_result:
            quality_data = coordination_result["quality_assessments"]["individual_assessments"]
            for team, assessment in quality_data.items():
                self.project_state["quality_status"][team] = {
                    "score": assessment.get("overall_score", 0),
                    "status": "PASS" if assessment.get("overall_score", 0) >= 80 else "NEEDS_IMPROVEMENT",
                    "last_assessed": datetime.now().isoformat()
                }
    
    def get_project_status_summary(self) -> Dict[str, Any]:
        """Get comprehensive project status summary."""
        return {
            "project_state": self.project_state,
            "coordination_history_count": len(self.coordination_history),
            "last_coordination": (
                self.coordination_history[-1]["timestamp"] 
                if self.coordination_history else None
            ),
            "active_teams_count": len(self.project_state["active_teams"]),
            "completed_teams_count": len(self.project_state["completed_teams"]),
            "overall_quality_score": (
                sum(
                    status["score"] for status in self.project_state["quality_status"].values()
                ) / max(1, len(self.project_state["quality_status"]))
            ),
            "resource_allocation_status": (
                "ALLOCATED" if self.project_state["resource_allocations"] else "PENDING"
            )
        }
    
    def generate_project_dashboard(self) -> str:
        """Generate a project dashboard summary."""
        status = self.get_project_status_summary()
        
        dashboard = f"""
PROJECT COORDINATION DASHBOARD
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

PROJECT OVERVIEW:
• Active Teams: {status['active_teams_count']}
• Completed Teams: {status['completed_teams_count']}
• Overall Quality Score: {status['overall_quality_score']:.1f}/100
• Resource Status: {status['resource_allocation_status']}

TEAM STATUS:
"""
        
        for team, quality_info in self.project_state["quality_status"].items():
            dashboard += f"• {team.replace('_', ' ').title()}: {quality_info['status']} ({quality_info['score']:.1f}/100)\n"
        
        dashboard += f"""
COORDINATION ACTIVITIES:
• Total Coordination Sessions: {status['coordination_history_count']}
• Last Coordination: {status['last_coordination'] or 'None'}

RESOURCE ALLOCATIONS:
"""
        
        if self.project_state["resource_allocations"]:
            dashboard += "• Resource allocation plan approved and active\n"
        else:
            dashboard += "• Resource allocation pending\n"
        
        dashboard += f"""
NEXT ACTIONS:
• Monitor team progress and quality metrics
• Review resource utilization and adjust as needed
• Prepare for final integration and delivery
• Conduct stakeholder updates and reviews
"""
        
        return dashboard
    
    def reset_coordination_state(self):
        """Reset coordination state for new project."""
        self.coordination_history = []
        self.project_state = {
            "active_teams": [],
            "completed_teams": [],
            "pending_decisions": [],
            "resource_allocations": {},
            "quality_status": {}
        }
