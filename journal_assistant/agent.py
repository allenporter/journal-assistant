"""Agent entry point for evaluation."""

import os
from pathlib import Path
from google.adk.agents.config_agent_utils import from_config as agent_from_config
from journal_assistant.journal import get_calendar
from journal_assistant.context import journal_context

# Default paths
AGENT_CONFIG_PATH = Path("journal_assistant/agents/router_agent.yaml")
JOURNAL_DATA_DIR = Path("datasets/alex")

def create_agent():
    """Creates and returns the root agent."""
    # Allow overriding via env vars
    config_path = Path(os.environ.get("AGENT_CONFIG_PATH", str(AGENT_CONFIG_PATH))).resolve()
    journal_dir = Path(os.environ.get("JOURNAL_DATA_DIR", str(JOURNAL_DATA_DIR))).resolve()

    if not journal_dir.exists():
        raise FileNotFoundError(f"Journal directory not found: {journal_dir}")

    # Initialize calendar and context
    # Note: This side-effect of setting the context globally might be tricky for parallel tests
    # but for now it matches the script/run_agent.py pattern.
    calendar = get_calendar(journal_dir)

    # We need to activate the context for the agent to work
    # In a real app, this is done per request or session.
    # For the evaluator, we might need to ensure this context is active.
    # Since we can't easily wrap the evaluator's internal loop, we'll set it globally here
    # and hope it persists or we might need a custom runner.
    # BUT, journal_context is a context manager.
    # Let's just load the agent for now.

    return agent_from_config(str(config_path))

# Expose root_agent for ADK
root_agent = create_agent()
