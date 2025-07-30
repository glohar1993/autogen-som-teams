#!/usr/bin/env python3
"""
Assignment 0: UserProxyAgent Integration in SoM Teams - Main Demo
================================================================

This script demonstrates the complete Society of Mind (SoM) framework
with UserProxyAgent integration for human-in-the-loop functionality.

Usage:
    python main.py --scenario product_launch
    python main.py --scenario crisis_management
    python main.py --interactive
"""

import os
import sys
import argparse
import json
from typing import Dict, List, Any
from datetime import datetime
import time

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.inner_team_agents import InnerTeamAgentFactory
from agents.outer_team_agents import OuterTeamAgentFactory
from agents.user_proxy_integration import UserProxyFactory
from som_framework.inner_teams import InnerTeamOrchestrator
from som_framework.outer_teams import OuterTeamCoordinator
from som_framework.coordination import SoMCoordinator

# Load environment variables
from dotenv import load_dotenv
load_dotenv()


class SoMDemonstration:
    """Main demonstration class for SoM Teams with UserProxyAgent integration."""
    
    def __init__(self, scenario: str = "product_launch"):
        self.scenario = scenario
        self.llm_config = self._setup_llm_config()
        self.demo_results = {
            "scenario": scenario,
            "start_time": datetime.now().isoformat(),
            "inner_teams": {},
            "outer_team": {},
            "human_interventions": [],
            "final_output": "",
            "performance_metrics": {}
        }
        
        # Initialize components
        self._initialize_components()
    
    def _setup_llm_config(self) -> Dict[str, Any]:
        """Setup LLM configuration."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("⚠️  Warning: OPENAI_API_KEY not found in environment variables")
            print("Please set your OpenAI API key in the .env file")
            api_key = input("Enter your OpenAI API key: ").strip()
        
        return {
            "config_list": [
                {
                    "model": "gpt-4-turbo-preview",
                    "api_key": api_key,
                    "temperature": 0.1,
                    "max_tokens": 2000
                }
            ],
            "timeout": 120,
        }
    
    def _initialize_components(self):
        """Initialize all SoM components."""
        print("🚀 Initializing Society of Mind Framework...")
        
        # Create inner team agents
        print("   📋 Creating inner team agents...")
        self.inner_team_agents = InnerTeamAgentFactory.create_all_teams(self.llm_config)
        
        # Create outer team agents
        print("   🎯 Creating outer team coordination agents...")
        self.outer_team_agents = OuterTeamAgentFactory.create_coordination_agents(self.llm_config)
        
        # Create UserProxyAgents
        print("   👤 Creating UserProxyAgents for human intervention...")
        self.user_proxies = UserProxyFactory.create_all_proxies(self.llm_config)
        
        # Create orchestrators
        print("   🎼 Setting up orchestrators...")
        self.inner_orchestrator = InnerTeamOrchestrator(
            self.inner_team_agents, 
            self.user_proxies["inner_teams"]
        )
        
        self.outer_coordinator = OuterTeamCoordinator(
            self.outer_team_agents,
            self.user_proxies["outer_team"]
        )
        
        self.som_coordinator = SoMCoordinator(
            self.inner_orchestrator,
            self.outer_coordinator
        )
        
        print("✅ SoM Framework initialized successfully!")
    
    def run_scenario(self):
        """Run the selected scenario demonstration."""
        print(f"\n🎬 Starting Scenario: {self.scenario.replace('_', ' ').title()}")
        print("=" * 60)
        
        if self.scenario == "product_launch":
            return self._run_product_launch_scenario()
        elif self.scenario == "crisis_management":
            return self._run_crisis_management_scenario()
        else:
            return self._run_interactive_scenario()
    
    def _run_product_launch_scenario(self):
        """Run product launch planning scenario."""
        print("📱 Scenario: Product Launch Planning")
        print("Objective: Plan comprehensive launch strategy for new mobile app")
        
        # Define project requirements
        project_requirements = {
            "product": "AI-powered fitness tracking mobile app",
            "target_market": "Health-conscious millennials and Gen Z",
            "launch_timeline": "3 months",
            "budget": "$500,000",
            "key_objectives": [
                "Market penetration analysis",
                "Brand positioning and messaging",
                "Technical launch infrastructure",
                "Marketing campaign strategy"
            ]
        }
        
        print(f"\n📋 Project Requirements:")
        for key, value in project_requirements.items():
            print(f"   {key}: {value}")
        
        # Step 1: Inner team execution
        print(f"\n🔄 Step 1: Inner Team Execution")
        inner_results = self._execute_inner_teams(project_requirements)
        
        # Step 2: Outer team coordination
        print(f"\n🔄 Step 2: Outer Team Coordination")
        coordination_results = self._execute_outer_coordination(inner_results)
        
        # Step 3: Final integration and validation
        print(f"\n🔄 Step 3: Final Integration and Human Validation")
        final_results = self._execute_final_integration(coordination_results)
        
        return final_results
    
    def _run_crisis_management_scenario(self):
        """Run crisis management response scenario."""
        print("🚨 Scenario: Crisis Management Response")
        print("Objective: Develop rapid response to data security incident")
        
        # Define crisis situation
        crisis_situation = {
            "incident": "Potential data breach affecting user accounts",
            "severity": "High",
            "affected_users": "~50,000 users",
            "discovery_time": "2 hours ago",
            "immediate_actions_needed": [
                "Incident assessment and containment",
                "Stakeholder communication strategy",
                "Technical remediation plan",
                "Legal and compliance response"
            ]
        }
        
        print(f"\n🚨 Crisis Situation:")
        for key, value in crisis_situation.items():
            print(f"   {key}: {value}")
        
        # Execute crisis response workflow
        print(f"\n🔄 Step 1: Rapid Assessment (Inner Teams)")
        inner_results = self._execute_inner_teams(crisis_situation)
        
        print(f"\n🔄 Step 2: Crisis Coordination (Outer Team)")
        coordination_results = self._execute_outer_coordination(inner_results)
        
        print(f"\n🔄 Step 3: Final Crisis Response Plan")
        final_results = self._execute_final_integration(coordination_results)
        
        return final_results
    
    def _execute_inner_teams(self, requirements: Dict[str, Any]) -> Dict[str, str]:
        """Execute inner team operations with human intervention."""
        print("\n👥 Executing Inner Teams...")
        
        inner_results = {}
        
        for team_name, agents in self.inner_team_agents.items():
            print(f"\n   🔸 Team: {team_name.replace('_', ' ').title()}")
            
            # Get team-specific requirements
            team_requirements = self._get_team_requirements(team_name, requirements)
            
            # Execute team workflow
            team_result = self.inner_orchestrator.execute_team_workflow(
                team_name, 
                team_requirements,
                agents
            )
            
            inner_results[team_name] = team_result
            
            # Human validation point
            user_proxy = self.user_proxies["inner_teams"][team_name]
            validation_result = user_proxy.validate_team_output(
                team_result, 
                [agent.name for agent in agents]
            )
            
            if not validation_result.approved:
                print(f"   ❌ Team output requires revision: {validation_result.feedback}")
                # In a real implementation, would iterate until approved
            else:
                print(f"   ✅ Team output approved")
            
            self.demo_results["human_interventions"].append({
                "team": team_name,
                "type": "output_validation",
                "approved": validation_result.approved,
                "feedback": validation_result.feedback
            })
        
        return inner_results
    
    def _execute_outer_coordination(self, inner_results: Dict[str, str]) -> Dict[str, Any]:
        """Execute outer team coordination with human oversight."""
        print("\n🎯 Executing Outer Team Coordination...")
        
        # Team coordination
        coordinator = self.outer_team_agents["team_coordinator"]
        integration_plan = coordinator.create_integration_plan(inner_results)
        
        print("   📋 Integration plan created")
        
        # Human coordination decision
        outer_proxy = self.user_proxies["outer_team"]
        coordination_decision = outer_proxy.coordinate_teams(inner_results, integration_plan)
        
        print(f"   👤 Human coordination decision: {coordination_decision.approved}")
        
        # Resource allocation
        resource_manager = self.outer_team_agents["resource_manager"]
        
        # Mock resource requests
        resource_requests = {
            team: {
                "budget": 50000 + (i * 25000),
                "time_weeks": 4 + i,
                "priority": ["high", "medium", "low"][i % 3],
                "description": f"Resources for {team} implementation"
            }
            for i, team in enumerate(inner_results.keys())
        }
        
        allocation_plan = resource_manager.create_allocation_plan(
            resource_requests,
            {"budget": 200000, "timeline_weeks": 12}
        )
        
        # Human resource allocation decision
        allocation_decision = outer_proxy.allocate_resources(resource_requests)
        
        print(f"   💰 Resource allocation decided")
        
        # Quality assurance
        qa_agent = self.outer_team_agents["quality_assurance"]
        quality_assessments = {}
        
        for team, output in inner_results.items():
            assessment = qa_agent.assess_team_output(team, output, {})
            quality_assessments[team] = assessment
        
        quality_report = qa_agent.create_quality_report(quality_assessments)
        
        print(f"   🔍 Quality assessment completed")
        
        return {
            "integration_plan": integration_plan,
            "coordination_decision": coordination_decision,
            "allocation_plan": allocation_plan,
            "allocation_decision": allocation_decision,
            "quality_report": quality_report,
            "quality_assessments": quality_assessments
        }
    
    def _execute_final_integration(self, coordination_results: Dict[str, Any]) -> Dict[str, Any]:
        """Execute final integration and validation."""
        print("\n🎯 Final Integration and Validation...")
        
        # Create consolidated output
        consolidated_output = self.som_coordinator.create_final_deliverable(
            self.demo_results,
            coordination_results
        )
        
        # Human final validation
        outer_proxy = self.user_proxies["outer_team"]
        final_validation = outer_proxy.validate_final_output(
            consolidated_output,
            {team: result for team, result in self.demo_results.get("inner_teams", {}).items()}
        )
        
        print(f"   👤 Final validation: {'✅ Approved' if final_validation.approved else '❌ Needs revision'}")
        
        # Compile final results
        final_results = {
            "consolidated_output": consolidated_output,
            "final_validation": final_validation,
            "coordination_results": coordination_results,
            "performance_summary": self._generate_performance_summary()
        }
        
        self.demo_results["final_output"] = consolidated_output
        self.demo_results["end_time"] = datetime.now().isoformat()
        
        return final_results
    
    def _get_team_requirements(self, team_name: str, overall_requirements: Dict[str, Any]) -> str:
        """Get team-specific requirements."""
        team_contexts = {
            "research_analysis": f"Conduct market research and analysis for: {overall_requirements}",
            "creative_design": f"Develop creative strategy and design for: {overall_requirements}",
            "technical_implementation": f"Plan technical implementation for: {overall_requirements}"
        }
        
        return team_contexts.get(team_name, str(overall_requirements))
    
    def _generate_performance_summary(self) -> Dict[str, Any]:
        """Generate performance summary."""
        return {
            "total_human_interventions": len(self.demo_results["human_interventions"]),
            "scenario_duration": "Calculated at runtime",
            "teams_executed": len(self.inner_team_agents),
            "coordination_agents": len(self.outer_team_agents),
            "success_metrics": {
                "inner_team_approvals": sum(
                    1 for intervention in self.demo_results["human_interventions"]
                    if intervention.get("approved", False)
                ),
                "coordination_success": True,  # Simplified
                "final_approval": True  # Would be based on actual validation
            }
        }
    
    def display_results(self, results: Dict[str, Any]):
        """Display demonstration results."""
        print("\n" + "="*60)
        print("🎉 DEMONSTRATION RESULTS")
        print("="*60)
        
        print(f"\n📊 Performance Summary:")
        perf = results["performance_summary"]
        print(f"   • Total Human Interventions: {perf['total_human_interventions']}")
        print(f"   • Teams Executed: {perf['teams_executed']}")
        print(f"   • Coordination Agents: {perf['coordination_agents']}")
        print(f"   • Inner Team Approvals: {perf['success_metrics']['inner_team_approvals']}")
        
        print(f"\n📋 Final Output Preview:")
        output = results["consolidated_output"]
        print(f"   {output[:200]}..." if len(output) > 200 else f"   {output}")
        
        print(f"\n👤 Human Interventions:")
        for intervention in self.demo_results["human_interventions"]:
            status = "✅" if intervention.get("approved", False) else "❌"
            print(f"   {status} {intervention['team']}: {intervention['type']}")
        
        print(f"\n🎯 Demonstration completed successfully!")
        print(f"   Scenario: {self.scenario.replace('_', ' ').title()}")
        print(f"   Duration: {datetime.now().isoformat()}")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="SoM Teams Demonstration")
    parser.add_argument(
        "--scenario", 
        choices=["product_launch", "crisis_management", "interactive"],
        default="product_launch",
        help="Scenario to demonstrate"
    )
    
    args = parser.parse_args()
    
    print("🤖 Microsoft AutoGen - Assignment 0: SoM Teams")
    print("UserProxyAgent Integration Demonstration")
    print("="*60)
    
    try:
        # Create and run demonstration
        demo = SoMDemonstration(args.scenario)
        results = demo.run_scenario()
        demo.display_results(results)
        
        # Save results
        results_file = f"demo_results_{args.scenario}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w') as f:
            json.dump(demo.demo_results, f, indent=2)
        
        print(f"\n💾 Results saved to: {results_file}")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demonstration interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during demonstration: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
