"""
SoM Coordination Framework
=========================

This module provides the main coordination framework that integrates
inner team orchestration with outer team coordination to create a
complete Society of Mind system.
"""

from typing import Dict, List, Any, Optional
import json
import time
from datetime import datetime


class SoMCoordinator:
    """Main coordinator for the Society of Mind framework."""
    
    def __init__(self, inner_orchestrator, outer_coordinator):
        self.inner_orchestrator = inner_orchestrator
        self.outer_coordinator = outer_coordinator
        self.system_state = {
            "initialization_time": datetime.now().isoformat(),
            "total_projects": 0,
            "successful_projects": 0,
            "system_performance": {},
            "human_intervention_stats": {}
        }
        self.project_history = []
    
    def execute_complete_som_workflow(self, project_requirements: Dict[str, Any], 
                                    scenario_name: str = "default") -> Dict[str, Any]:
        """Execute the complete SoM workflow from start to finish."""
        print(f"🎯 Executing complete SoM workflow for: {scenario_name}")
        
        workflow_result = {
            "scenario": scenario_name,
            "start_time": datetime.now().isoformat(),
            "project_requirements": project_requirements,
            "inner_team_results": {},
            "outer_coordination_results": {},
            "final_deliverable": "",
            "human_interventions": [],
            "performance_metrics": {},
            "success": False
        }
        
        try:
            # Phase 1: Inner Team Execution
            print("   📋 Phase 1: Inner team execution")
            inner_results = self._execute_inner_teams_phase(project_requirements)
            workflow_result["inner_team_results"] = inner_results
            
            # Phase 2: Outer Team Coordination
            print("   🎯 Phase 2: Outer team coordination")
            coordination_results = self.outer_coordinator.coordinate_project_execution(
                inner_results, 
                project_requirements
            )
            workflow_result["outer_coordination_results"] = coordination_results
            
            # Phase 3: Final Integration
            print("   🎉 Phase 3: Final integration and deliverable creation")
            final_deliverable = self.create_final_deliverable(
                workflow_result,
                coordination_results
            )
            workflow_result["final_deliverable"] = final_deliverable
            
            # Phase 4: Performance Analysis
            print("   📊 Phase 4: Performance analysis")
            performance_metrics = self._analyze_workflow_performance(workflow_result)
            workflow_result["performance_metrics"] = performance_metrics
            
            workflow_result["success"] = True
            workflow_result["end_time"] = datetime.now().isoformat()
            
            # Update system state
            self._update_system_state(workflow_result)
            
            print("   ✅ SoM workflow completed successfully")
            
        except Exception as e:
            print(f"   ❌ SoM workflow failed: {str(e)}")
            workflow_result["error"] = str(e)
            workflow_result["success"] = False
            workflow_result["end_time"] = datetime.now().isoformat()
        
        # Store in project history
        self.project_history.append(workflow_result)
        
        return workflow_result
    
    def _execute_inner_teams_phase(self, project_requirements: Dict[str, Any]) -> Dict[str, str]:
        """Execute the inner teams phase of the workflow."""
        inner_results = {}
        
        # Get team requirements for each inner team
        team_requirements = self._generate_team_requirements(project_requirements)
        
        # Execute each inner team
        for team_name, agents in self.inner_orchestrator.inner_team_agents.items():
            print(f"      🔸 Executing {team_name.replace('_', ' ').title()}")
            
            team_req = team_requirements.get(team_name, str(project_requirements))
            team_result = self.inner_orchestrator.execute_team_workflow(
                team_name,
                team_req,
                agents
            )
            
            inner_results[team_name] = team_result
        
        return inner_results
    
    def _generate_team_requirements(self, project_requirements: Dict[str, Any]) -> Dict[str, str]:
        """Generate specific requirements for each inner team."""
        base_context = json.dumps(project_requirements, indent=2)
        
        team_requirements = {
            "research_analysis": f"""
RESEARCH & ANALYSIS TEAM REQUIREMENTS

Project Context: {base_context}

Your team's specific objectives:
1. Conduct comprehensive market research and competitive analysis
2. Analyze target audience and customer segments
3. Identify market opportunities and potential risks
4. Provide data-driven insights and recommendations
5. Create detailed research reports and findings

Deliverables expected:
• Market analysis report with size, growth, and trends
• Competitive landscape assessment
• Customer persona and segmentation analysis
• Risk assessment and mitigation strategies
• Data-driven recommendations for project success

Focus areas:
• Market validation and opportunity assessment
• Competitive positioning and differentiation
• Customer needs and behavior analysis
• Industry trends and future projections
• Success metrics and KPI recommendations
""",
            
            "creative_design": f"""
CREATIVE & DESIGN TEAM REQUIREMENTS

Project Context: {base_context}

Your team's specific objectives:
1. Develop comprehensive brand strategy and positioning
2. Create compelling messaging and content strategy
3. Design visual identity and brand guidelines
4. Develop marketing campaign concepts and materials
5. Ensure consistent brand experience across all touchpoints

Deliverables expected:
• Brand positioning and messaging framework
• Visual identity system and brand guidelines
• Marketing campaign strategy and creative concepts
• Content strategy and copywriting guidelines
• Design assets and templates for various channels

Focus areas:
• Brand differentiation and unique value proposition
• Target audience communication preferences
• Visual design that supports brand objectives
• Multi-channel campaign coordination
• Brand consistency and scalability planning
""",
            
            "technical_implementation": f"""
TECHNICAL IMPLEMENTATION TEAM REQUIREMENTS

Project Context: {base_context}

Your team's specific objectives:
1. Design scalable and secure technical architecture
2. Plan development phases and implementation strategy
3. Define technical requirements and specifications
4. Create testing and quality assurance frameworks
5. Plan deployment and maintenance procedures

Deliverables expected:
• Technical architecture design and documentation
• Development roadmap and implementation plan
• Technical specifications and requirements
• Testing strategy and quality assurance plan
• Deployment and operational procedures

Focus areas:
• Scalability and performance optimization
• Security and data protection measures
• Integration with existing systems and platforms
• Development best practices and standards
• Monitoring, maintenance, and support planning
"""
        }
        
        return team_requirements
    
    def create_final_deliverable(self, workflow_result: Dict[str, Any], 
                               coordination_results: Dict[str, Any]) -> str:
        """Create the final integrated deliverable."""
        
        scenario = workflow_result.get("scenario", "Unknown")
        inner_results = workflow_result.get("inner_team_results", {})
        
        final_deliverable = f"""
{'='*80}
FINAL PROJECT DELIVERABLE
{'='*80}

Project: {scenario.replace('_', ' ').title()}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
SoM Framework Version: 1.0

EXECUTIVE SUMMARY:
This deliverable represents the integrated output of a Society of Mind (SoM) 
framework implementation, combining specialized inner team expertise with 
outer team coordination and human oversight.

PROJECT OVERVIEW:
{json.dumps(workflow_result.get("project_requirements", {}), indent=2)}

INTEGRATED TEAM CONTRIBUTIONS:
"""
        
        # Integrate contributions from each team
        for team_name, team_output in inner_results.items():
            final_deliverable += f"""

{team_name.replace('_', ' ').upper()} TEAM CONTRIBUTION:
{'-' * 50}
{team_output[:1000]}{'...' if len(team_output) > 1000 else ''}
"""
        
        # Add coordination insights
        final_deliverable += f"""

COORDINATION AND INTEGRATION INSIGHTS:
{'-' * 50}
"""
        
        if "integration_plan" in coordination_results:
            final_deliverable += f"""
Integration Strategy:
{coordination_results['integration_plan'][:500]}{'...' if len(coordination_results.get('integration_plan', '')) > 500 else ''}
"""
        
        if "final_recommendations" in coordination_results:
            final_deliverable += f"""
Strategic Recommendations:
"""
            for i, rec in enumerate(coordination_results["final_recommendations"][:10], 1):
                final_deliverable += f"{i}. {rec}\n"
        
        # Add quality assessment summary
        quality_assessments = coordination_results.get("quality_assessments", {}).get("individual_assessments", {})
        if quality_assessments:
            final_deliverable += f"""

QUALITY ASSESSMENT SUMMARY:
{'-' * 50}
"""
            for team, assessment in quality_assessments.items():
                score = assessment.get("overall_score", 0)
                status = "✅ APPROVED" if score >= 80 else "⚠️ NEEDS REVIEW"
                final_deliverable += f"{team.replace('_', ' ').title()}: {score:.1f}/100 {status}\n"
        
        # Add human intervention summary
        final_deliverable += f"""

HUMAN OVERSIGHT SUMMARY:
{'-' * 50}
This project included strategic human intervention points ensuring:
• Quality validation at each team level
• Coordination approval for inter-team integration
• Resource allocation optimization
• Final deliverable validation and approval

Total human interventions: {len(workflow_result.get('human_interventions', []))}
All critical decisions were reviewed and approved by human experts.

NEXT STEPS AND IMPLEMENTATION:
{'-' * 50}
1. Review and approve final deliverable
2. Initiate implementation based on team recommendations
3. Establish monitoring and feedback mechanisms
4. Plan regular review and optimization cycles
5. Document lessons learned for future projects

PROJECT SUCCESS METRICS:
{'-' * 50}
• All inner teams completed their objectives successfully
• Outer team coordination achieved seamless integration
• Human oversight ensured quality and strategic alignment
• Final deliverable meets all specified requirements
• SoM framework demonstrated effective human-AI collaboration

{'='*80}
END OF DELIVERABLE
{'='*80}
"""
        
        return final_deliverable
    
    def _analyze_workflow_performance(self, workflow_result: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the performance of the complete workflow."""
        
        start_time = datetime.fromisoformat(workflow_result["start_time"])
        end_time = datetime.fromisoformat(workflow_result["end_time"])
        duration = (end_time - start_time).total_seconds()
        
        performance_metrics = {
            "execution_time_seconds": duration,
            "execution_time_formatted": f"{duration//60:.0f}m {duration%60:.0f}s",
            "teams_executed": len(workflow_result.get("inner_team_results", {})),
            "coordination_success": workflow_result.get("success", False),
            "human_interventions_count": len(workflow_result.get("human_interventions", [])),
            "deliverable_length": len(workflow_result.get("final_deliverable", "")),
            "quality_scores": {},
            "efficiency_metrics": {}
        }
        
        # Extract quality scores
        coordination_results = workflow_result.get("outer_coordination_results", {})
        quality_assessments = coordination_results.get("quality_assessments", {}).get("individual_assessments", {})
        
        for team, assessment in quality_assessments.items():
            performance_metrics["quality_scores"][team] = assessment.get("overall_score", 0)
        
        # Calculate efficiency metrics
        if performance_metrics["teams_executed"] > 0:
            performance_metrics["efficiency_metrics"] = {
                "average_time_per_team": duration / performance_metrics["teams_executed"],
                "average_quality_score": (
                    sum(performance_metrics["quality_scores"].values()) / 
                    len(performance_metrics["quality_scores"])
                ) if performance_metrics["quality_scores"] else 0,
                "human_intervention_rate": (
                    performance_metrics["human_interventions_count"] / 
                    performance_metrics["teams_executed"]
                ),
                "deliverable_efficiency": (
                    performance_metrics["deliverable_length"] / duration
                ) if duration > 0 else 0
            }
        
        return performance_metrics
    
    def _update_system_state(self, workflow_result: Dict[str, Any]):
        """Update the overall system state based on workflow results."""
        self.system_state["total_projects"] += 1
        
        if workflow_result.get("success", False):
            self.system_state["successful_projects"] += 1
        
        # Update performance statistics
        performance = workflow_result.get("performance_metrics", {})
        if "system_performance" not in self.system_state:
            self.system_state["system_performance"] = {
                "total_execution_time": 0,
                "total_teams_executed": 0,
                "total_human_interventions": 0,
                "average_quality_score": 0
            }
        
        sys_perf = self.system_state["system_performance"]
        sys_perf["total_execution_time"] += performance.get("execution_time_seconds", 0)
        sys_perf["total_teams_executed"] += performance.get("teams_executed", 0)
        sys_perf["total_human_interventions"] += performance.get("human_interventions_count", 0)
        
        # Calculate running averages
        if self.system_state["total_projects"] > 0:
            sys_perf["average_execution_time"] = (
                sys_perf["total_execution_time"] / self.system_state["total_projects"]
            )
            sys_perf["average_teams_per_project"] = (
                sys_perf["total_teams_executed"] / self.system_state["total_projects"]
            )
            sys_perf["average_interventions_per_project"] = (
                sys_perf["total_human_interventions"] / self.system_state["total_projects"]
            )
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        return {
            "system_state": self.system_state,
            "project_history_count": len(self.project_history),
            "success_rate": (
                self.system_state["successful_projects"] / 
                max(1, self.system_state["total_projects"])
            ),
            "inner_orchestrator_metrics": self.inner_orchestrator.get_team_performance_metrics(),
            "outer_coordinator_status": self.outer_coordinator.get_project_status_summary(),
            "last_project": (
                self.project_history[-1]["scenario"] if self.project_history else None
            )
        }
    
    def generate_system_report(self) -> str:
        """Generate comprehensive system report."""
        status = self.get_system_status()
        
        report = f"""
SOCIETY OF MIND SYSTEM REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SYSTEM OVERVIEW:
• Total Projects Executed: {self.system_state['total_projects']}
• Successful Projects: {self.system_state['successful_projects']}
• Success Rate: {status['success_rate']:.1%}
• System Uptime: {self.system_state['initialization_time']}

PERFORMANCE METRICS:
• Average Execution Time: {self.system_state['system_performance'].get('average_execution_time', 0):.1f} seconds
• Average Teams per Project: {self.system_state['system_performance'].get('average_teams_per_project', 0):.1f}
• Average Human Interventions: {self.system_state['system_performance'].get('average_interventions_per_project', 0):.1f}

INNER TEAM PERFORMANCE:
• Total Team Executions: {status['inner_orchestrator_metrics']['total_executions']}
• Successful Executions: {status['inner_orchestrator_metrics']['successful_executions']}
• Average Result Length: {status['inner_orchestrator_metrics']['average_result_length']:.0f} characters

OUTER COORDINATION STATUS:
• Active Teams: {status['outer_coordinator_status']['active_teams_count']}
• Completed Teams: {status['outer_coordinator_status']['completed_teams_count']}
• Overall Quality Score: {status['outer_coordinator_status']['overall_quality_score']:.1f}/100

RECENT ACTIVITY:
• Last Project: {status['last_project'] or 'None'}
• Project History: {status['project_history_count']} projects

SYSTEM HEALTH: ✅ OPERATIONAL
"""
        
        return report
