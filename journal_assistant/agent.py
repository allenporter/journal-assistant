"""Agent entry point for evaluation."""

import os
from pathlib import Path
from google.adk.agents.config_agent_utils import from_config as agent_from_config

# Default paths
AGENT_CONFIG_PATH = Path("journal_assistant/agents/router_agent.yaml")


def create_agent():
    """Creates and returns the root agent."""
    # Allow overriding via env vars
    config_path = Path(
        os.environ.get("AGENT_CONFIG_PATH", str(AGENT_CONFIG_PATH))
    ).resolve()

    # Note: The agent relies on the journal context being set by the runner (e.g. script/run_agent.py or tests)
    # The tools will fail if context.get_current_journal() returns None.

    return agent_from_config(str(config_path))


# Expose root_agent for ADK
root_agent = create_agent()
