"""Script to run the agent from config."""

import os
import sys
from pathlib import Path

from google.adk.agents.config_agent_utils import from_config as agent_from_config
from journal_assistant.journal import get_calendar
from journal_assistant.context import journal_context


AGENT_CONFIG = Path("journal_assistant/agents/router_agent.yaml")


def main() -> None:
    if not (journal_dir := os.environ.get("JOURNAL_DATA_DIR", "")):
        print("Error: JOURNAL_DATA_DIR environment variable not set.")
        sys.exit(1)

    config_path = Path(os.environ.get("AGENT_CONFIG_PATH", str(AGENT_CONFIG))).resolve()
    if not config_path.is_file():
        print(f"Error: Config file {config_path} does not exist.")
        sys.exit(1)

    print(f"Loading journal from {journal_dir}...")
    calendar = get_calendar(Path(journal_dir))

    print(f"Loading agent from {config_path}...")

    agent = agent_from_config(str(config_path))
    print(f"Agent loaded: {agent.name}")

    # Simple interaction loop
    print("Enter a query (or 'exit' to quit):")
    with journal_context(calendar):
        while True:
            query = input("> ")
            if query.lower() in ("exit", "quit"):
                break

            try:
                response = agent.run(query)
                print(f"\nResponse: {response}\n")
            except Exception as e:
                print(f"Error running agent: {e}")


if __name__ == "__main__":
    main()
