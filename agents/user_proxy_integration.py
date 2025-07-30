"""
UserProxyAgent Integration for Assignment 0: SoM Teams
=====================================================

This module contains specialized UserProxyAgent implementations for both
inner and outer team configurations, enabling human-in-the-loop functionality.
"""

# Use the new AutoGen structure
try:
    from autogen_agentchat.agents import UserProxyAgent
    from autogen_agentchat import GroupChat, GroupChatManager
    import autogen_agentchat as autogen
except ImportError:
    # Fallback to old structure if available
    import autogen
    from autogen import UserProxyAgent, GroupChat, GroupChatManager

from typing import Dict, List, Any, Optional, Callable
import json
import time
from datetime import datetime
from enum import Enum


class InterventionType(Enum):
    """Types of human interventions."""
    APPROVAL = "approval"
    CONTEXT_ADDITION = "context_addition"
    CONSTRAINT_SETTING = "constraint_setting"
    DECISION_OVERRIDE = "decision_override"
    QUALITY_VALIDATION = "quality_validation"
    RESOURCE_ALLOCATION = "resource_allocation"
    PRIORITY_SETTING = "priority_setting"


class HumanInterventionResult:
    """Result of human intervention."""
    
    def __init__(self, approved: bool, feedback: str = "", additional_context: str = "", 
                 constraints: List[str] = None, override_decision: str = ""):
        self.approved = approved
        self.feedback = feedback
        self.additional_context = additional_context
        self.constraints = constraints or []
        self.override_decision = override_decision
        self.timestamp = datetime.now().isoformat()


class EnhancedUserProxyAgent(autogen.UserProxyAgent):
    """Enhanced UserProxyAgent with structured human intervention capabilities."""
    
    def __init__(self, name: str, role: str, team_context: str, **kwargs):
        # Configure for human input with structured prompts
        super().__init__(
            name=name,
            human_input_mode="ALWAYS",  # Always ask for human input
            max_consecutive_auto_reply=0,  # Don't auto-reply
            code_execution_config=False,  # Disable code execution for safety
            **kwargs
        )
        
        self.role = role
        self.team_context = team_context
        self.intervention_history = []
        self.decision_patterns = {}
        
    def get_human_input(self, prompt: str) -> str:
        """Enhanced human input with structured prompts."""
        # Add context and role information to the prompt
        enhanced_prompt = f"""
{'='*60}
HUMAN INTERVENTION REQUIRED
{'='*60}

Role: {self.role}
Team Context: {self.team_context}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{prompt}

{'='*60}
Please provide your response:
"""
        
        # Get human input
        human_response = input(enhanced_prompt)
        
        # Log the intervention
        self.intervention_history.append({
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "response": human_response,
            "role": self.role,
            "team_context": self.team_context
        })
        
        return human_response
    
    def request_approval(self, decision: str, context: str = "") -> HumanInterventionResult:
        """Request human approval for a decision."""
        prompt = f"""
DECISION APPROVAL REQUEST

Decision to approve: {decision}

Context: {context}

Options:
1. APPROVE - Type 'approve' or 'yes'
2. REJECT - Type 'reject' or 'no'
3. MODIFY - Type 'modify' followed by your changes

You can also provide additional feedback or context.
"""
        
        response = self.get_human_input(prompt)
        response_lower = response.lower().strip()
        
        if response_lower in ['approve', 'yes', 'y']:
            return HumanInterventionResult(approved=True, feedback=response)
        elif response_lower in ['reject', 'no', 'n']:
            return HumanInterventionResult(approved=False, feedback=response)
        elif response_lower.startswith('modify'):
            modification = response[6:].strip()  # Remove 'modify' prefix
            return HumanInterventionResult(
                approved=False, 
                feedback=response,
                override_decision=modification
            )
        else:
            # Treat as feedback with implicit approval
            return HumanInterventionResult(approved=True, feedback=response)
    
    def request_context_addition(self, current_context: str) -> HumanInterventionResult:
        """Request additional context from human."""
        prompt = f"""
CONTEXT ADDITION REQUEST

Current context: {current_context}

Please provide any additional context, constraints, or information
that should be considered:

Type 'none' if no additional context is needed.
"""
        
        response = self.get_human_input(prompt)
        
        if response.lower().strip() == 'none':
            return HumanInterventionResult(approved=True)
        else:
            return HumanInterventionResult(
                approved=True,
                additional_context=response
            )
    
    def request_constraint_setting(self, proposed_constraints: List[str]) -> HumanInterventionResult:
        """Request human to set or modify constraints."""
        constraints_text = "\n".join([f"- {c}" for c in proposed_constraints])
        
        prompt = f"""
CONSTRAINT SETTING REQUEST

Proposed constraints:
{constraints_text}

Please review and modify constraints as needed.
You can:
1. Accept all - Type 'accept'
2. Add constraints - Type 'add: [your constraint]'
3. Remove constraints - Type 'remove: [constraint to remove]'
4. Replace all - Type 'replace:' followed by new constraints

Separate multiple constraints with semicolons (;)
"""
        
        response = self.get_human_input(prompt)
        response_lower = response.lower().strip()
        
        if response_lower == 'accept':
            return HumanInterventionResult(approved=True, constraints=proposed_constraints)
        elif response_lower.startswith('add:'):
            new_constraint = response[4:].strip()
            updated_constraints = proposed_constraints + [new_constraint]
            return HumanInterventionResult(approved=True, constraints=updated_constraints)
        elif response_lower.startswith('remove:'):
            to_remove = response[7:].strip()
            updated_constraints = [c for c in proposed_constraints if c != to_remove]
            return HumanInterventionResult(approved=True, constraints=updated_constraints)
        elif response_lower.startswith('replace:'):
            new_constraints_text = response[8:].strip()
            new_constraints = [c.strip() for c in new_constraints_text.split(';')]
            return HumanInterventionResult(approved=True, constraints=new_constraints)
        else:
            # Treat as new constraints
            new_constraints = [c.strip() for c in response.split(';')]
            return HumanInterventionResult(approved=True, constraints=new_constraints)


# =============================================================================
# INNER TEAM USER PROXY AGENTS
# =============================================================================

class InnerTeamUserProxy(EnhancedUserProxyAgent):
    """UserProxyAgent for inner team human intervention."""
    
    def __init__(self, team_name: str, domain_expertise: str, **kwargs):
        super().__init__(
            name=f"{team_name}_HumanExpert",
            role=f"{domain_expertise} Expert",
            team_context=f"Inner Team: {team_name}",
            **kwargs
        )
        self.team_name = team_name
        self.domain_expertise = domain_expertise
    
    def validate_team_output(self, output: str, agents_involved: List[str]) -> HumanInterventionResult:
        """Validate output from the inner team."""
        prompt = f"""
INNER TEAM OUTPUT VALIDATION

Team: {self.team_name}
Agents involved: {', '.join(agents_involved)}
Domain: {self.domain_expertise}

Output to validate:
{output}

As a {self.domain_expertise} expert, please review this output and:
1. Validate accuracy and quality
2. Identify any missing elements
3. Suggest improvements if needed

Type 'approve' to accept, or provide feedback for improvements.
"""
        
        response = self.get_human_input(prompt)
        
        if response.lower().strip() in ['approve', 'approved', 'good', 'ok']:
            return HumanInterventionResult(approved=True, feedback=response)
        else:
            return HumanInterventionResult(approved=False, feedback=response)


class ResearchTeamUserProxy(InnerTeamUserProxy):
    """UserProxyAgent for Research & Analysis team."""
    
    def __init__(self, **kwargs):
        super().__init__(
            team_name="Research_Analysis",
            domain_expertise="Research & Data Analysis",
            **kwargs
        )


class CreativeTeamUserProxy(InnerTeamUserProxy):
    """UserProxyAgent for Creative & Design team."""
    
    def __init__(self, **kwargs):
        super().__init__(
            team_name="Creative_Design",
            domain_expertise="Creative Strategy & Design",
            **kwargs
        )


class TechnicalTeamUserProxy(InnerTeamUserProxy):
    """UserProxyAgent for Technical Implementation team."""
    
    def __init__(self, **kwargs):
        super().__init__(
            team_name="Technical_Implementation",
            domain_expertise="Technical Architecture & Development",
            **kwargs
        )


# =============================================================================
# OUTER TEAM USER PROXY AGENT
# =============================================================================

class OuterTeamUserProxy(EnhancedUserProxyAgent):
    """UserProxyAgent for outer team coordination and oversight."""
    
    def __init__(self, **kwargs):
        super().__init__(
            name="ProjectDirector_Human",
            role="Project Director",
            team_context="Outer Team: Project Coordination",
            **kwargs
        )
        self.team_coordination_history = []
        self.resource_allocation_decisions = []
    
    def coordinate_teams(self, team_outputs: Dict[str, str], 
                        coordination_plan: str) -> HumanInterventionResult:
        """Coordinate between multiple inner teams."""
        teams_summary = "\n".join([
            f"{team}: {output[:200]}..." 
            for team, output in team_outputs.items()
        ])
        
        prompt = f"""
INTER-TEAM COORDINATION DECISION

Team Outputs Summary:
{teams_summary}

Proposed Coordination Plan:
{coordination_plan}

As Project Director, please:
1. Review the coordination plan
2. Identify any conflicts or gaps
3. Approve or suggest modifications
4. Set priorities for team interactions

Your decision:
"""
        
        response = self.get_human_input(prompt)
        
        # Log coordination decision
        self.team_coordination_history.append({
            "timestamp": datetime.now().isoformat(),
            "team_outputs": team_outputs,
            "coordination_plan": coordination_plan,
            "human_decision": response
        })
        
        return HumanInterventionResult(approved=True, feedback=response)
    
    def allocate_resources(self, resource_requests: Dict[str, Dict]) -> HumanInterventionResult:
        """Make resource allocation decisions between teams."""
        requests_summary = "\n".join([
            f"{team}: {req.get('description', 'No description')} "
            f"(Priority: {req.get('priority', 'Not specified')})"
            for team, req in resource_requests.items()
        ])
        
        prompt = f"""
RESOURCE ALLOCATION DECISION

Resource Requests:
{requests_summary}

Please make resource allocation decisions:
1. Approve/deny each request
2. Set priorities if resources are limited
3. Suggest alternatives if needed

Format your response as:
Team_Name: APPROVE/DENY - [reason/alternative]

Your allocation decisions:
"""
        
        response = self.get_human_input(prompt)
        
        # Log resource allocation decision
        self.resource_allocation_decisions.append({
            "timestamp": datetime.now().isoformat(),
            "requests": resource_requests,
            "allocation_decision": response
        })
        
        return HumanInterventionResult(approved=True, feedback=response)
    
    def validate_final_output(self, consolidated_output: str, 
                             team_contributions: Dict[str, str]) -> HumanInterventionResult:
        """Validate the final consolidated output from all teams."""
        contributions_summary = "\n".join([
            f"{team}: {contrib[:150]}..."
            for team, contrib in team_contributions.items()
        ])
        
        prompt = f"""
FINAL OUTPUT VALIDATION

Consolidated Output:
{consolidated_output}

Team Contributions:
{contributions_summary}

As Project Director, please provide final validation:
1. Does the output meet project objectives?
2. Are all team contributions properly integrated?
3. Is the quality acceptable for delivery?
4. Any final modifications needed?

Your final decision:
"""
        
        response = self.get_human_input(prompt)
        
        if any(word in response.lower() for word in ['approve', 'accept', 'good', 'ready']):
            return HumanInterventionResult(approved=True, feedback=response)
        else:
            return HumanInterventionResult(approved=False, feedback=response)


# =============================================================================
# USER PROXY FACTORY AND UTILITIES
# =============================================================================

class UserProxyFactory:
    """Factory for creating UserProxyAgent instances."""
    
    @staticmethod
    def create_inner_team_proxies(llm_config: Dict) -> Dict[str, InnerTeamUserProxy]:
        """Create UserProxyAgents for all inner teams."""
        return {
            "research_analysis": ResearchTeamUserProxy(llm_config=llm_config),
            "creative_design": CreativeTeamUserProxy(llm_config=llm_config),
            "technical_implementation": TechnicalTeamUserProxy(llm_config=llm_config)
        }
    
    @staticmethod
    def create_outer_team_proxy(llm_config: Dict) -> OuterTeamUserProxy:
        """Create UserProxyAgent for outer team coordination."""
        return OuterTeamUserProxy(llm_config=llm_config)
    
    @staticmethod
    def create_all_proxies(llm_config: Dict) -> Dict[str, Any]:
        """Create all UserProxyAgent instances."""
        return {
            "inner_teams": UserProxyFactory.create_inner_team_proxies(llm_config),
            "outer_team": UserProxyFactory.create_outer_team_proxy(llm_config)
        }


def get_intervention_summary(user_proxies: Dict[str, Any]) -> Dict[str, Any]:
    """Get summary of all human interventions."""
    summary = {
        "total_interventions": 0,
        "inner_team_interventions": {},
        "outer_team_interventions": 0,
        "intervention_types": {},
        "timeline": []
    }
    
    # Process inner team interventions
    if "inner_teams" in user_proxies:
        for team_name, proxy in user_proxies["inner_teams"].items():
            team_interventions = len(proxy.intervention_history)
            summary["inner_team_interventions"][team_name] = team_interventions
            summary["total_interventions"] += team_interventions
            
            # Add to timeline
            for intervention in proxy.intervention_history:
                summary["timeline"].append({
                    "timestamp": intervention["timestamp"],
                    "team": team_name,
                    "type": "inner_team",
                    "role": intervention["role"]
                })
    
    # Process outer team interventions
    if "outer_team" in user_proxies:
        outer_proxy = user_proxies["outer_team"]
        outer_interventions = len(outer_proxy.intervention_history)
        summary["outer_team_interventions"] = outer_interventions
        summary["total_interventions"] += outer_interventions
        
        # Add to timeline
        for intervention in outer_proxy.intervention_history:
            summary["timeline"].append({
                "timestamp": intervention["timestamp"],
                "team": "outer_coordination",
                "type": "outer_team",
                "role": intervention["role"]
            })
    
    # Sort timeline by timestamp
    summary["timeline"].sort(key=lambda x: x["timestamp"])
    
    return summary
