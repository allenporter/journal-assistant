"""Agent entry point for evaluation."""

from dataclasses import dataclass, field
import importlib
import os
from pathlib import Path
from typing import Any, List, Optional
from mashumaro.mixins.yaml import DataClassYAMLMixin

from google.adk import Agent
from google.adk.agents.base_agent import BaseAgent

# Default paths
AGENT_CONFIG_PATH = Path("journal_assistant/agents/router_agent.yaml")


@dataclass
class ToolRef:
    name: str


@dataclass
class SubAgentRef:
    config_path: str


@dataclass
class LocalAgentConfig(DataClassYAMLMixin):
    name: str
    model: str
    description: Optional[str] = None
    instruction: Optional[str] = None
    tools: List[ToolRef] = field(default_factory=list)
    sub_agents: List[SubAgentRef] = field(default_factory=list)


def load_agent_from_yaml(config_path: Path) -> Agent:
    """Helper to parse agent yaml config and build Agent dynamically."""
    config_path = config_path.resolve()
    with open(config_path, "r", encoding="utf-8") as f:
        config = LocalAgentConfig.from_yaml(f.read())

    # Resolve tools by importing functions
    resolved_tools: List[Any] = []
    for tool_ref in config.tools:
        module_name, func_name = tool_ref.name.rsplit(".", 1)
        module = importlib.import_module(module_name)
        resolved_tools.append(getattr(module, func_name))

    # Resolve sub-agents recursively
    resolved_sub_agents: List[BaseAgent] = []
    for sub_agent_ref in config.sub_agents:
        sub_config_path = config_path.parent / sub_agent_ref.config_path
        resolved_sub_agents.append(load_agent_from_yaml(sub_config_path))

    return Agent(
        name=config.name,
        model=config.model,
        description=config.description or "",
        instruction=config.instruction or "",
        tools=resolved_tools,
        sub_agents=resolved_sub_agents,
    )


def create_agent() -> Agent:
    """Creates and returns the root agent."""
    # Allow overriding via env vars
    config_path = Path(
        os.environ.get("AGENT_CONFIG_PATH", str(AGENT_CONFIG_PATH))
    ).resolve()

    # Note: The agent relies on the journal context being set by the runner (e.g. script/run_agent.py or tests)
    # The tools will fail if context.get_current_journal() returns None.

    return load_agent_from_yaml(config_path)


# Expose root_agent for ADK
root_agent = create_agent()
