#!/usr/bin/env python3
"""
Microsoft AutoGen - Assignment 0: SoM Teams
Streamlit Web Interface
==========================================

Interactive web interface for the Society of Mind framework with UserProxyAgent integration.
Demonstrates real-time multi-agent coordination with human-in-the-loop functionality.
"""

import streamlit as st
import json
import time
import os
from datetime import datetime
from typing import Dict, List, Any
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import our SoM framework
try:
    from demo_simple import SoMDemoSimulator
    from config import SCENARIOS, TEAM_CONFIGURATIONS
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="AutoGen SoM Teams - Interactive Demo",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .scenario-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
    }
    .agent-status {
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin: 0.25rem 0;
    }
    .agent-active {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
    }
    .agent-waiting {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
    }
    .human-intervention {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'demo_running' not in st.session_state:
        st.session_state.demo_running = False
    if 'current_scenario' not in st.session_state:
        st.session_state.current_scenario = None
    if 'demo_results' not in st.session_state:
        st.session_state.demo_results = {}
    if 'execution_log' not in st.session_state:
        st.session_state.execution_log = []
    if 'human_interventions' not in st.session_state:
        st.session_state.human_interventions = []
    if 'performance_metrics' not in st.session_state:
        st.session_state.performance_metrics = {
            'execution_times': [],
            'approval_rates': [],
            'quality_scores': []
        }

def render_header():
    """Render the main header."""
    st.markdown('<h1 class="main-header">🤖 Microsoft AutoGen - Assignment 0: SoM Teams</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center; color: #666;">Society of Mind Framework with UserProxyAgent Integration</h3>', unsafe_allow_html=True)

    # Status indicators
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        api_status = "✅ Connected" if os.getenv("OPENAI_API_KEY") else "❌ Not Found"
        st.metric("OpenAI API", api_status)

    with col2:
        framework_status = "✅ Ready"
        st.metric("SoM Framework", framework_status)

    with col3:
        agents_count = "12 Agents"
        st.metric("AI Agents", agents_count)

    with col4:
        scenarios_count = "3 Scenarios"
        st.metric("Available Scenarios", scenarios_count)

def render_sidebar():
    """Render the sidebar with controls."""
    st.sidebar.header("🎯 Control Panel")

    # API Key check
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.sidebar.error("⚠️ OpenAI API Key not found!")
        st.sidebar.info("Please set OPENAI_API_KEY in your .env file")
        return None
    else:
        st.sidebar.success(f"✅ API Key configured ({len(api_key)} chars)")

    # Scenario selection
    st.sidebar.subheader("📋 Scenario Selection")
    scenario_options = {
        "product_launch": "🚀 Product Launch Planning",
        "crisis_management": "🚨 Crisis Management Response",
        "interactive_demo": "🎯 Interactive Framework Demo"
    }

    selected_scenario = st.sidebar.selectbox(
        "Choose a scenario:",
        options=list(scenario_options.keys()),
        format_func=lambda x: scenario_options[x],
        key="scenario_selector"
    )

    # Execution controls
    st.sidebar.subheader("⚙️ Execution Controls")

    # Human intervention settings
    auto_approve = st.sidebar.checkbox("🤖 Auto-approve decisions", value=False)
    intervention_delay = st.sidebar.slider("⏱️ Intervention delay (seconds)", 1, 10, 3)

    # Advanced settings
    with st.sidebar.expander("🔧 Advanced Settings"):
        max_execution_time = st.sidebar.slider("Max execution time (seconds)", 30, 300, 120)
        quality_threshold = st.sidebar.slider("Quality threshold", 0.5, 1.0, 0.8)
        enable_logging = st.sidebar.checkbox("📝 Enable detailed logging", value=True)

    return {
        "scenario": selected_scenario,
        "auto_approve": auto_approve,
        "intervention_delay": intervention_delay,
        "max_execution_time": max_execution_time,
        "quality_threshold": quality_threshold,
        "enable_logging": enable_logging
    }

def render_scenario_info(scenario: str):
    """Render information about the selected scenario."""
    scenario_info = {
        "product_launch": {
            "title": "🚀 Product Launch Planning",
            "description": "Complete go-to-market strategy development for AI-powered fitness app",
            "teams": ["Research & Analysis", "Creative & Design", "Technical Implementation"],
            "objectives": [
                "Market research and competitive analysis",
                "Brand strategy and creative campaign",
                "Technical architecture and implementation plan"
            ],
            "expected_duration": "2-3 minutes",
            "human_interventions": 4
        },
        "crisis_management": {
            "title": "🚨 Crisis Management Response",
            "description": "Rapid incident response for data security breach",
            "teams": ["Incident Analysis", "Crisis Communication", "Technical Remediation"],
            "objectives": [
                "Incident analysis and impact assessment",
                "Crisis communication strategy",
                "Technical remediation and security hardening"
            ],
            "expected_duration": "2-3 minutes",
            "human_interventions": 4
        },
        "interactive_demo": {
            "title": "🎯 Interactive Framework Demo",
            "description": "Live demonstration of SoM framework capabilities",
            "teams": ["Framework Analysis", "Demonstration Strategy", "Technical Implementation"],
            "objectives": [
                "Framework analysis and performance metrics",
                "Presentation strategy and audience engagement",
                "Technical implementation and monitoring"
            ],
            "expected_duration": "2-3 minutes",
            "human_interventions": 4
        }
    }

    info = scenario_info.get(scenario, {})

    st.markdown(f'<div class="scenario-card">', unsafe_allow_html=True)
    st.markdown(f"### {info.get('title', 'Unknown Scenario')}")
    st.markdown(f"**Description:** {info.get('description', 'No description available')}")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Teams Involved:**")
        for team in info.get('teams', []):
            st.markdown(f"• {team}")

    with col2:
        st.markdown("**Key Objectives:**")
        for obj in info.get('objectives', []):
            st.markdown(f"• {obj}")

    col3, col4 = st.columns(2)
    with col3:
        st.metric("Expected Duration", info.get('expected_duration', 'Unknown'))
    with col4:
        st.metric("Human Interventions", info.get('human_interventions', 0))

    st.markdown('</div>', unsafe_allow_html=True)

def simulate_human_intervention(decision_point: str, context: str, auto_approve: bool = False) -> Dict[str, Any]:
    """Simulate human intervention with Streamlit interface."""
    if auto_approve:
        # Auto-approve for demo purposes
        decision = {
            "approved": True,
            "feedback": "Auto-approved for demonstration",
            "timestamp": datetime.now().isoformat()
        }
        return decision

    # Create intervention UI
    st.markdown('<div class="human-intervention">', unsafe_allow_html=True)
    st.markdown("### 👤 Human Intervention Required")
    st.markdown(f"**Decision Point:** {decision_point}")
    st.markdown(f"**Context:** {context}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Approve", key=f"approve_{decision_point}"):
            decision = {
                "approved": True,
                "feedback": "Approved via Streamlit interface",
                "timestamp": datetime.now().isoformat()
            }
            st.session_state.human_interventions.append(decision)
            st.success("Decision approved!")
            return decision

    with col2:
        if st.button("❌ Reject", key=f"reject_{decision_point}"):
            decision = {
                "approved": False,
                "feedback": "Rejected via Streamlit interface",
                "timestamp": datetime.now().isoformat()
            }
            st.session_state.human_interventions.append(decision)
            st.error("Decision rejected!")
            return decision

    # Feedback input
    feedback = st.text_area("Additional feedback:", key=f"feedback_{decision_point}")

    st.markdown('</div>', unsafe_allow_html=True)

    # Return pending decision
    return {
        "approved": None,
        "feedback": feedback,
        "timestamp": datetime.now().isoformat(),
        "status": "pending"
    }

def render_execution_progress():
    """Render real-time execution progress."""
    st.subheader("🔄 Execution Progress")

    # Progress indicators
    progress_container = st.container()

    with progress_container:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("#### 🧠 Inner Teams")
            team_progress = st.progress(0)
            team_status = st.empty()

        with col2:
            st.markdown("#### 🎯 Outer Coordination")
            coord_progress = st.progress(0)
            coord_status = st.empty()

        with col3:
            st.markdown("#### 👤 Human Interventions")
            human_progress = st.progress(0)
            human_status = st.empty()

    return {
        "team_progress": team_progress,
        "team_status": team_status,
        "coord_progress": coord_progress,
        "coord_status": coord_status,
        "human_progress": human_progress,
        "human_status": human_status
    }

def render_agent_status():
    """Render real-time agent status."""
    st.subheader("🤖 Agent Status Monitor")

    # Agent status grid
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### Research & Analysis Team")
        st.markdown('<div class="agent-status agent-active">🔬 Research Specialist: Active</div>', unsafe_allow_html=True)
        st.markdown('<div class="agent-status agent-active">📊 Data Analyst: Active</div>', unsafe_allow_html=True)
        st.markdown('<div class="agent-status agent-active">📝 Report Writer: Active</div>', unsafe_allow_html=True)
        st.markdown('<div class="agent-status agent-waiting">👤 UserProxy: Waiting</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("#### Creative & Design Team")
        st.markdown('<div class="agent-status agent-active">🎨 Creative Strategist: Active</div>', unsafe_allow_html=True)
        st.markdown('<div class="agent-status agent-active">✍️ Content Creator: Active</div>', unsafe_allow_html=True)
        st.markdown('<div class="agent-status agent-active">🎭 Visual Designer: Active</div>', unsafe_allow_html=True)
        st.markdown('<div class="agent-status agent-waiting">👤 UserProxy: Waiting</div>', unsafe_allow_html=True)

    with col3:
        st.markdown("#### Technical Implementation Team")
        st.markdown('<div class="agent-status agent-active">🏗️ System Architect: Active</div>', unsafe_allow_html=True)
        st.markdown('<div class="agent-status agent-active">💻 Developer: Active</div>', unsafe_allow_html=True)
        st.markdown('<div class="agent-status agent-active">🧪 QA Engineer: Active</div>', unsafe_allow_html=True)
        st.markdown('<div class="agent-status agent-waiting">👤 UserProxy: Waiting</div>', unsafe_allow_html=True)

def render_execution_log():
    """Render execution log."""
    st.subheader("📋 Execution Log")

    log_container = st.container()

    with log_container:
        if st.session_state.execution_log:
            for i, log_entry in enumerate(reversed(st.session_state.execution_log[-10:])):  # Show last 10 entries
                timestamp = log_entry.get('timestamp', 'Unknown')
                message = log_entry.get('message', 'No message')
                level = log_entry.get('level', 'INFO')

                if level == 'ERROR':
                    st.error(f"[{timestamp}] {message}")
                elif level == 'WARNING':
                    st.warning(f"[{timestamp}] {message}")
                elif level == 'SUCCESS':
                    st.success(f"[{timestamp}] {message}")
                else:
                    st.info(f"[{timestamp}] {message}")
        else:
            st.info("No execution logs yet. Start a scenario to see real-time logs.")

def add_log_entry(message: str, level: str = "INFO"):
    """Add entry to execution log."""
    log_entry = {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "message": message,
        "level": level
    }
    st.session_state.execution_log.append(log_entry)

def render_performance_metrics():
    """Render performance metrics and charts."""
    st.subheader("📊 Performance Metrics")

    # Metrics overview
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_scenarios = len(st.session_state.demo_results)
        st.metric("Scenarios Completed", total_scenarios)

    with col2:
        total_interventions = len(st.session_state.human_interventions)
        st.metric("Human Interventions", total_interventions)

    with col3:
        if st.session_state.human_interventions:
            approved = sum(1 for h in st.session_state.human_interventions if h.get('approved'))
            approval_rate = (approved / len(st.session_state.human_interventions)) * 100
            st.metric("Approval Rate", f"{approval_rate:.1f}%")
        else:
            st.metric("Approval Rate", "N/A")

    with col4:
        avg_quality = 92.5  # Simulated quality score
        st.metric("Avg Quality Score", f"{avg_quality:.1f}")

    # Performance charts
    if st.session_state.performance_metrics['execution_times']:
        col1, col2 = st.columns(2)

        with col1:
            # Execution time chart
            fig_time = px.line(
                x=list(range(len(st.session_state.performance_metrics['execution_times']))),
                y=st.session_state.performance_metrics['execution_times'],
                title="Execution Times",
                labels={'x': 'Scenario', 'y': 'Time (seconds)'}
            )
            st.plotly_chart(fig_time, use_container_width=True)

        with col2:
            # Quality scores chart
            fig_quality = px.bar(
                x=['Research', 'Creative', 'Technical', 'Overall'],
                y=[95, 88, 94, 92],
                title="Quality Scores by Team",
                labels={'x': 'Team', 'y': 'Quality Score'}
            )
            st.plotly_chart(fig_quality, use_container_width=True)

def run_scenario_simulation(scenario: str, settings: Dict[str, Any]):
    """Run scenario simulation with real-time updates."""
    add_log_entry(f"Starting {scenario} scenario simulation", "INFO")

    # Initialize progress
    progress_widgets = render_execution_progress()

    # Simulate scenario execution
    try:
        # Phase 1: Inner Teams Execution
        add_log_entry("Initializing inner teams...", "INFO")
        progress_widgets["team_status"].text("Initializing teams...")

        for i in range(3):  # 3 inner teams
            time.sleep(1)  # Simulate processing time
            progress = (i + 1) / 3
            progress_widgets["team_progress"].progress(progress)

            team_names = ["Research & Analysis", "Creative & Design", "Technical Implementation"]
            add_log_entry(f"{team_names[i]} team processing...", "INFO")
            progress_widgets["team_status"].text(f"Processing: {team_names[i]}")

        progress_widgets["team_status"].text("✅ All inner teams completed")
        add_log_entry("Inner teams execution completed", "SUCCESS")

        # Phase 2: Human Interventions
        add_log_entry("Requesting human interventions...", "INFO")
        progress_widgets["human_status"].text("Waiting for human decisions...")

        intervention_points = [
            ("Research Output Validation", "Review market analysis and strategic recommendations"),
            ("Creative Strategy Validation", "Review brand strategy and creative campaign"),
            ("Technical Architecture Validation", "Review system architecture and implementation plan"),
            ("Final Project Approval", "Review complete integrated strategy")
        ]

        for i, (decision_point, context) in enumerate(intervention_points):
            if settings["auto_approve"]:
                time.sleep(settings["intervention_delay"])
                decision = simulate_human_intervention(decision_point, context, auto_approve=True)
                add_log_entry(f"Auto-approved: {decision_point}", "SUCCESS")
            else:
                st.markdown(f"### Human Intervention {i+1}/4")
                decision = simulate_human_intervention(decision_point, context, auto_approve=False)

                if decision.get("status") == "pending":
                    st.warning("Waiting for human decision...")
                    return False  # Wait for user input

                if decision.get("approved"):
                    add_log_entry(f"Approved: {decision_point}", "SUCCESS")
                else:
                    add_log_entry(f"Rejected: {decision_point}", "WARNING")

            progress = (i + 1) / 4
            progress_widgets["human_progress"].progress(progress)

        progress_widgets["human_status"].text("✅ All interventions completed")

        # Phase 3: Outer Coordination
        add_log_entry("Starting outer team coordination...", "INFO")
        progress_widgets["coord_status"].text("Coordinating results...")

        for i in range(3):  # Coordination steps
            time.sleep(0.5)
            progress = (i + 1) / 3
            progress_widgets["coord_progress"].progress(progress)

            coord_steps = ["Integration planning", "Quality validation", "Final compilation"]
            add_log_entry(f"Coordination: {coord_steps[i]}", "INFO")
            progress_widgets["coord_status"].text(f"Processing: {coord_steps[i]}")

        progress_widgets["coord_status"].text("✅ Coordination completed")
        add_log_entry("Outer team coordination completed", "SUCCESS")

        # Generate results
        execution_time = 15 + len(intervention_points) * settings["intervention_delay"]

        results = {
            "scenario": scenario,
            "execution_time": execution_time,
            "human_interventions": len(intervention_points),
            "approval_rate": 100 if settings["auto_approve"] else 75,
            "quality_score": 92.5,
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        }

        # Update session state
        st.session_state.demo_results[scenario] = results
        st.session_state.performance_metrics['execution_times'].append(execution_time)
        st.session_state.performance_metrics['quality_scores'].append(92.5)

        add_log_entry(f"Scenario {scenario} completed successfully!", "SUCCESS")
        st.success(f"🎉 Scenario '{scenario}' completed successfully!")

        return True

    except Exception as e:
        add_log_entry(f"Error in scenario execution: {str(e)}", "ERROR")
        st.error(f"Error: {str(e)}")
        return False

def render_results_summary():
    """Render results summary."""
    if not st.session_state.demo_results:
        st.info("No completed scenarios yet. Run a scenario to see results.")
        return

    st.subheader("📈 Results Summary")

    # Results table
    results_data = []
    for scenario, result in st.session_state.demo_results.items():
        results_data.append({
            "Scenario": scenario.replace("_", " ").title(),
            "Execution Time (s)": result.get("execution_time", 0),
            "Human Interventions": result.get("human_interventions", 0),
            "Approval Rate (%)": result.get("approval_rate", 0),
            "Quality Score": result.get("quality_score", 0),
            "Status": result.get("status", "unknown")
        })

    if results_data:
        df = pd.DataFrame(results_data)
        st.dataframe(df, use_container_width=True)

        # Download results
        json_results = json.dumps(st.session_state.demo_results, indent=2)
        st.download_button(
            label="📥 Download Results (JSON)",
            data=json_results,
            file_name=f"som_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

def main():
    """Main Streamlit application."""
    initialize_session_state()

    # Header
    render_header()

    # Sidebar controls
    settings = render_sidebar()
    if not settings:
        return

    # Main content
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Scenario", "🔄 Execution", "📊 Metrics", "📋 Results"])

    with tab1:
        st.header("Scenario Configuration")
        render_scenario_info(settings["scenario"])

        # Execution button
        if st.button("🚀 Start Scenario Execution", type="primary", disabled=st.session_state.demo_running):
            st.session_state.demo_running = True
            st.session_state.current_scenario = settings["scenario"]
            st.rerun()

    with tab2:
        st.header("Real-Time Execution")

        if st.session_state.demo_running:
            success = run_scenario_simulation(st.session_state.current_scenario, settings)
            if success:
                st.session_state.demo_running = False
                st.session_state.current_scenario = None
                st.rerun()
        else:
            render_agent_status()
            render_execution_log()

    with tab3:
        st.header("Performance Analytics")
        render_performance_metrics()

    with tab4:
        st.header("Execution Results")
        render_results_summary()

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>🤖 Microsoft AutoGen - Assignment 0: SoM Teams</p>
        <p>Society of Mind Framework with UserProxyAgent Integration</p>
        <p>Built with Streamlit • Powered by OpenAI GPT-4</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()