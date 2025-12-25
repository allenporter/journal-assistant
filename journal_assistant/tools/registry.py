"""Registry for initializing and exposing tools for ADK config."""

import logging
from .journal_tool import JournalTool
from .calendar_tool import CalendarTool

_LOGGER = logging.getLogger(__name__)

# Singleton instances
_journal_tool: JournalTool | None = None
_calendar_tool: CalendarTool | None = None

def _get_journal_tool() -> JournalTool:
    global _journal_tool
    if _journal_tool is None:
        _LOGGER.info("Initializing JournalTool from registry")
        _journal_tool = JournalTool()
    return _journal_tool

def _get_calendar_tool() -> CalendarTool:
    global _calendar_tool
    if _calendar_tool is None:
        _LOGGER.info("Initializing CalendarTool from registry")
        _calendar_tool = CalendarTool()
    return _calendar_tool

# Exposed functions for ADK config
def read_entry(date: str) -> str:
    """Reads the journal entry for a specific date."""
    return _get_journal_tool().read_entry(date)

def search_entries(query: str) -> str:
    """Search for journal entries matching the query."""
    return _get_journal_tool().search_entries(query)

def get_events(start_date: str, end_date: str) -> str:
    """Get calendar events for a date range."""
    return _get_calendar_tool().get_events(start_date, end_date)
