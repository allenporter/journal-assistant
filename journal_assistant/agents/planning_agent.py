from google.adk.agents import Agent
from ..tools.journal_tool import JournalTool
from ..tools.calendar_tool import CalendarTool

def create_planning_agent(model, journal_tool: JournalTool, calendar_tool: CalendarTool) -> Agent:
    return Agent(
        name="planning_agent",
        description="Delegate to the Planning Agent for scheduling and future task management.",
        model=model,
        tools=[
            journal_tool.read_entry,
            journal_tool.search_entries,
            calendar_tool.get_events
        ],
        instruction="""You are a proactive Bullet Journal Planning Assistant.
Your goal is to help the user plan their upcoming days or weeks.
Check for open tasks in previous entries using `read_entry` or `search_entries`.
Check for upcoming events using `get_events`.
Suggest a schedule or a list of priorities based on this information.
"""
    )
