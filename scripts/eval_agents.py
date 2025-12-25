import logging
import sys
from pathlib import Path
from typing import Any, List, AsyncIterator, Iterator

# Add the workspace root to the path so we can import journal_assistant
sys.path.append(str(Path(__file__).parent.parent))

# Import ADK components
try:
    from google.adk.models.base_llm import BaseLlm
    from google.adk.models.llm_request import LlmRequest
    from google.adk.models.llm_response import LlmResponse
    from google.genai.types import Content, Part
    from google.adk.runners import InMemoryRunner
except ImportError:
    # Fallback for debugging if imports fail
    print("Failed to import ADK models. Ensure google-adk is installed.")
    class BaseLlm: pass
    class LlmResponse:
        def __init__(self, text): self.text = text
    class InMemoryRunner: pass

from journal_assistant.tools.journal_tool import JournalTool
from journal_assistant.tools.calendar_tool import CalendarTool
from journal_assistant.agents.reflection_agent import create_reflection_agent
from journal_assistant.agents.planning_agent import create_planning_agent
from journal_assistant.agents.router_agent import create_router_agent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MockModel(BaseLlm):
    """A mock model for testing purposes."""

    def generate_content(self, request: LlmRequest, **kwargs) -> LlmResponse:
        # Extract prompt from request
        prompt = ""
        if request.messages:
            for msg in request.messages:
                if hasattr(msg, 'content'):
                     # This is a simplification, actual content might be complex
                     prompt += str(msg.content)
                else:
                     prompt += str(msg)

        logger.info(f"MockModel received prompt: {prompt[:100]}...")

        text_response = "I am a mock agent."
        if "Reflect" in prompt or "reflection" in prompt.lower():
            text_response = "Based on your journal entries, January was a busy month with a focus on work and art."
        elif "Plan" in prompt or "planning" in prompt.lower():
            text_response = "You have a few deadlines coming up. I suggest focusing on your portfolio."

        return LlmResponse(text=text_response)

    async def generate_content_async(self, request: LlmRequest, **kwargs) -> LlmResponse:
        print("DEBUG: generate_content_async called")
        return self.generate_content(request, **kwargs)

    async def generate_content_stream_async(self, request: LlmRequest, **kwargs) -> AsyncIterator[LlmResponse]:
        print("DEBUG: generate_content_stream_async called")
        await asyncio.sleep(0)
        yield self.generate_content(request, **kwargs)

def main():
    # Setup paths
    root_dir = Path(__file__).parent.parent
    test_data_dir = root_dir / "tests" / "testdata" / "alex"

    if not test_data_dir.exists():
        logger.error(f"Test data directory not found: {test_data_dir}")
        return

    logger.info(f"Using test data from: {test_data_dir}")

    # Initialize Tools
    journal_tool = JournalTool(root_dir=test_data_dir)
    calendar_tool = CalendarTool()

    # Initialize Model (Mock for now)
    model = MockModel(model="mock-model")

    # Initialize Agents
    reflection_agent = create_reflection_agent(model, journal_tool)
    planning_agent = create_planning_agent(model, journal_tool, calendar_tool)
    router_agent = create_router_agent(model, reflection_agent, planning_agent)

    # Test Query
    query = "Reflect on my January 2024 entries."
    logger.info(f"Running query: {query}")

    # Run the agent
    try:
        runner = InMemoryRunner(agent=router_agent, app_name="journal-assistant")
        # Create session first
        runner.session_service.create_session_sync(session_id="test_session", user_id="test_user", app_name="journal-assistant")

        # run() returns a generator of events
        # Wrap query in Content object
        content = Content(role="user", parts=[Part(text=query)])
        events = runner.run(user_id="test_user", session_id="test_session", new_message=content)

        print("\n=== Agent Response ===")
        for event in events:
            # Print event for debugging/verification
            print(event)
        print("======================\n")
    except Exception as e:
        logger.error(f"Error running agent: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
