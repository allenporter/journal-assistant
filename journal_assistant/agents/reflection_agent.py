from google.adk.agents import Agent
from ..tools.journal_tool import JournalTool

def create_reflection_agent(model, journal_tool: JournalTool) -> Agent:
    return Agent(
        name="reflection_agent",
        description="Delegate to the Reflection Agent for reviewing past entries and generating summaries.",
        model=model,
        tools=[journal_tool.read_entry, journal_tool.search_entries],
        instruction="""You are a thoughtful Bullet Journal Reflection Assistant.
Your goal is to help the user review their past entries (Daily, Weekly, Monthly) and generate insights.
Use the `read_entry` tool to fetch specific days.
Use the `search_entries` tool to find themes or specific topics.
When asked to reflect on a period (e.g., "last week"), make sure to read the entries for those days first.
"""
    )
