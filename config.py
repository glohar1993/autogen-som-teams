"""
Configuration settings for Assignment 0: SoM Teams
=================================================

This module contains configuration settings for the Society of Mind
framework implementation.
"""

import os
from typing import Dict, Any


class SoMConfig:
    """Configuration class for SoM Teams implementation."""
    
    # LLM Configuration
    DEFAULT_MODEL = "gpt-4-turbo-preview"
    DEFAULT_TEMPERATURE = 0.1
    DEFAULT_MAX_TOKENS = 2000
    DEFAULT_TIMEOUT = 120
    
    # Team Configuration
    MAX_INNER_TEAMS = int(os.getenv("MAX_INNER_TEAMS", "5"))
    MAX_AGENTS_PER_TEAM = int(os.getenv("MAX_AGENTS_PER_TEAM", "10"))
    
    # Human Intervention Configuration
    HUMAN_INTERVENTION_TIMEOUT = int(os.getenv("HUMAN_INTERVENTION_TIMEOUT", "300"))
    AUTO_APPROVE_THRESHOLD = float(os.getenv("AUTO_APPROVE_THRESHOLD", "0.8"))
    
    # Performance Configuration
    MAX_PROCESSING_TIME = 300  # seconds
    MAX_COORDINATION_TIME = 180  # seconds
    
    # Scenario Configuration
    AVAILABLE_SCENARIOS = [
        "product_launch",
        "crisis_management",
        "interactive"
    ]
    
    @classmethod
    def get_llm_config(cls, api_key: str = None) -> Dict[str, Any]:
        """Get LLM configuration."""
        if not api_key:
            api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            raise ValueError("OpenAI API key is required")
        
        return {
            "config_list": [
                {
                    "model": cls.DEFAULT_MODEL,
                    "api_key": api_key,
                    "temperature": cls.DEFAULT_TEMPERATURE,
                    "max_tokens": cls.DEFAULT_MAX_TOKENS
                }
            ],
            "timeout": cls.DEFAULT_TIMEOUT,
        }
    
    @classmethod
    def get_team_config(cls) -> Dict[str, Any]:
        """Get team configuration."""
        return {
            "max_inner_teams": cls.MAX_INNER_TEAMS,
            "max_agents_per_team": cls.MAX_AGENTS_PER_TEAM,
            "human_intervention_timeout": cls.HUMAN_INTERVENTION_TIMEOUT,
            "auto_approve_threshold": cls.AUTO_APPROVE_THRESHOLD
        }
    
    @classmethod
    def get_scenario_config(cls, scenario: str) -> Dict[str, Any]:
        """Get scenario-specific configuration."""
        scenario_configs = {
            "product_launch": {
                "name": "Product Launch Planning",
                "description": "Plan comprehensive launch strategy for new product",
                "expected_duration": 1800,  # 30 minutes
                "complexity": "medium",
                "human_interventions_expected": 8
            },
            "crisis_management": {
                "name": "Crisis Management Response",
                "description": "Develop rapid response to business crisis",
                "expected_duration": 1200,  # 20 minutes
                "complexity": "high",
                "human_interventions_expected": 12
            },
            "interactive": {
                "name": "Interactive Demonstration",
                "description": "Custom interactive demonstration",
                "expected_duration": 2400,  # 40 minutes
                "complexity": "variable",
                "human_interventions_expected": 10
            }
        }
        
        return scenario_configs.get(scenario, scenario_configs["interactive"])


# Global configuration instance
config = SoMConfig()
