"""Script to run the agent from config."""

import os
import sys
from pathlib import Path
from google.adk.agents.config_agent_utils import from_config as agent_from_config

# Add workspace root to python path
sys.path.append(str(Path(__file__).parent.parent))

def main():
    print(f"sys.path: {sys.path}")
    try:
        import journal_assistant.processing
        print("Successfully imported journal_assistant.processing")
    except ImportError as e:
        print(f"Failed to import journal_assistant.processing: {e}")

    if not os.environ.get("JOURNAL_DATA_DIR"):
        print("Error: JOURNAL_DATA_DIR environment variable not set.")
        sys.exit(1)

    config_path = Path("journal_assistant/agents/router_agent.yaml").resolve()
    print(f"Loading agent from {config_path}...")

    try:
        agent = agent_from_config(str(config_path))
    except Exception as e:
        print(f"Failed to load agent: {e}")
        sys.exit(1)

    print(f"Agent loaded: {agent.name}")

    # Simple interaction loop
    print("Enter a query (or 'exit' to quit):")
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
