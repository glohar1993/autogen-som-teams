#!/usr/bin/env python3
"""
Test Setup for Assignment 0: SoM Teams
======================================

This script tests the basic setup and imports for the SoM Teams implementation.
"""

import sys
import os
from datetime import datetime

def test_imports():
    """Test all required imports."""
    print("🧪 Testing imports...")
    
    try:
        # Test basic Python imports
        import json
        import time
        from typing import Dict, List, Any
        print("   ✅ Basic Python imports successful")
        
        # Test AutoGen imports
        import autogen
        print("   ✅ AutoGen import successful")
        
        # Test environment loading
        from dotenv import load_dotenv
        load_dotenv()
        print("   ✅ Environment loading successful")
        
        # Test project imports
        from agents.inner_team_agents import InnerTeamAgentFactory
        from agents.outer_team_agents import OuterTeamAgentFactory
        from agents.user_proxy_integration import UserProxyFactory
        print("   ✅ Agent imports successful")
        
        from som_framework.inner_teams import InnerTeamOrchestrator
        from som_framework.outer_teams import OuterTeamCoordinator
        from som_framework.coordination import SoMCoordinator
        print("   ✅ SoM framework imports successful")
        
        from config import SoMConfig
        print("   ✅ Configuration import successful")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def test_configuration():
    """Test configuration setup."""
    print("\n🔧 Testing configuration...")
    
    try:
        from config import SoMConfig
        
        # Test basic config
        team_config = SoMConfig.get_team_config()
        print(f"   ✅ Team config loaded: {len(team_config)} settings")
        
        # Test scenario config
        scenario_config = SoMConfig.get_scenario_config("product_launch")
        print(f"   ✅ Scenario config loaded: {scenario_config['name']}")
        
        # Test available scenarios
        scenarios = SoMConfig.AVAILABLE_SCENARIOS
        print(f"   ✅ Available scenarios: {', '.join(scenarios)}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Configuration error: {e}")
        return False

def test_agent_factories():
    """Test agent factory creation (without LLM config)."""
    print("\n🤖 Testing agent factories...")
    
    try:
        from agents.inner_team_agents import InnerTeamAgentFactory
        from agents.outer_team_agents import OuterTeamAgentFactory
        from agents.user_proxy_integration import UserProxyFactory
        
        # Test factory class availability
        inner_teams = InnerTeamAgentFactory.AGENT_CLASSES
        print(f"   ✅ Inner team types: {', '.join(inner_teams.keys())}")
        
        # Count total agent types
        total_agent_types = sum(len(agents) for agents in inner_teams.values())
        print(f"   ✅ Total inner agent types: {total_agent_types}")
        
        # Test outer team factory (class methods)
        print("   ✅ Outer team factory available")
        print("   ✅ UserProxy factory available")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Agent factory error: {e}")
        return False

def test_som_framework():
    """Test SoM framework classes."""
    print("\n🎯 Testing SoM framework...")
    
    try:
        from som_framework.inner_teams import InnerTeamOrchestrator
        from som_framework.outer_teams import OuterTeamCoordinator
        from som_framework.coordination import SoMCoordinator
        
        print("   ✅ InnerTeamOrchestrator class available")
        print("   ✅ OuterTeamCoordinator class available")
        print("   ✅ SoMCoordinator class available")
        
        return True
        
    except Exception as e:
        print(f"   ❌ SoM framework error: {e}")
        return False

def test_environment_variables():
    """Test environment variable setup."""
    print("\n🌍 Testing environment variables...")
    
    try:
        import os
        
        # Check for API key (don't print the actual key)
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            print("   ✅ OPENAI_API_KEY found")
        else:
            print("   ⚠️  OPENAI_API_KEY not found (will need to be provided)")
        
        # Check other optional environment variables
        optional_vars = [
            "MAX_INNER_TEAMS",
            "MAX_AGENTS_PER_TEAM", 
            "HUMAN_INTERVENTION_TIMEOUT",
            "AUTO_APPROVE_THRESHOLD"
        ]
        
        found_vars = []
        for var in optional_vars:
            if os.getenv(var):
                found_vars.append(var)
        
        if found_vars:
            print(f"   ✅ Optional vars found: {', '.join(found_vars)}")
        else:
            print("   ℹ️  No optional environment variables set (using defaults)")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Environment error: {e}")
        return False

def test_file_structure():
    """Test project file structure."""
    print("\n📁 Testing file structure...")
    
    try:
        required_files = [
            "main.py",
            "config.py",
            "agents/inner_team_agents.py",
            "agents/outer_team_agents.py", 
            "agents/user_proxy_integration.py",
            "som_framework/inner_teams.py",
            "som_framework/outer_teams.py",
            "som_framework/coordination.py"
        ]
        
        missing_files = []
        for file_path in required_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
        
        if missing_files:
            print(f"   ❌ Missing files: {', '.join(missing_files)}")
            return False
        else:
            print(f"   ✅ All {len(required_files)} required files present")
        
        # Check directories
        required_dirs = ["agents", "som_framework", "diagrams", "tests"]
        missing_dirs = []
        for dir_path in required_dirs:
            if not os.path.exists(dir_path):
                missing_dirs.append(dir_path)
        
        if missing_dirs:
            print(f"   ⚠️  Missing directories: {', '.join(missing_dirs)}")
        else:
            print(f"   ✅ All {len(required_dirs)} required directories present")
        
        return True
        
    except Exception as e:
        print(f"   ❌ File structure error: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Assignment 0: SoM Teams - Setup Test")
    print("=" * 50)
    print(f"Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_configuration),
        ("Agent Factories", test_agent_factories),
        ("SoM Framework", test_som_framework),
        ("Environment Variables", test_environment_variables),
        ("File Structure", test_file_structure)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"   ❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Setup is ready.")
        print("\nNext steps:")
        print("1. Set OPENAI_API_KEY in .env file")
        print("2. Run: python main.py --scenario product_launch")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
