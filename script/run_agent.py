"""Script to run the agent from config."""

import argparse
import asyncio
import logging
import os
import sys
from pathlib import Path

from google.adk.apps import App
from google.adk.runners import InMemoryRunner
from google.genai.types import Content, Part

from journal_assistant.agent import create_agent
from journal_assistant.context import journal_context
from journal_assistant.journal import get_calendar

_LOGGER = logging.getLogger(__name__)

APP_NAME = "journal_assistant"


async def main() -> None:
    parser = argparse.ArgumentParser(description="Run the journal assistant agent.")
    parser.add_argument(
        "--log-level",
        default=None,
        help="Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )
    args = parser.parse_args()

    if args.log_level:
        logging.basicConfig(level=getattr(logging, args.log_level.upper()))

    if not (journal_dir := os.environ.get("JOURNAL_DATA_DIR", "")):
        print("Error: JOURNAL_DATA_DIR environment variable not set.")
        sys.exit(1)

    print(f"Loading journal from {journal_dir}...")
    calendar = get_calendar(Path(journal_dir))

    print("Loading agent...")

    agent = create_agent()
    print(f"Agent loaded: {agent.name}")

    app = App(
        name=APP_NAME,
        root_agent=agent,
        # Optionally include App-level features:
        # plugins, context_cache_config, resumability_config
    )
    runner = InMemoryRunner(app=app)
    user_id = "test_user"
    session_id = "test_session"
    await runner.session_service.create_session(
        app_name=app.name, user_id=user_id, session_id=session_id
    )

    # Simple interaction loop
    print("Enter a query (or 'exit' to quit):")
    with journal_context(calendar):
        while True:
            query = input("> ")
            if query.lower() in ("exit", "quit"):
                break

            try:
                async for event in runner.run_async(
                    user_id=user_id,
                    session_id=session_id,
                    new_message=Content(parts=[Part(text=query)]),
                ):
                    if event.content and event.content.parts:
                        for part in event.content.parts:
                            if part.text:
                                print(part.text, end="", flush=True)
                            else:
                                _LOGGER.debug("Received part: %s", part)
                print("\n")
            except Exception as e:  # noqa: BLE001
                print(f"Error running agent: {e}")


if __name__ == "__main__":
    asyncio.run(main())
