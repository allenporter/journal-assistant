import datetime
from ical.calendar import Calendar
from ical.journal import Journal
from journal_assistant.tools.journal_tool import JournalTool

def test_read_entry() -> None:
    entry = Journal(
        summary="Test Entry",
        dtstart=datetime.date(2024, 1, 1),
        description="This is a test entry.\n- [ ] Task 1"
    )
    calendar = Calendar(journal=[entry])
    tool = JournalTool(calendar)

    result = tool.read_entry("2024-01-01")
    assert "Entry for 2024-01-01" in result
    assert "This is a test entry" in result
    assert "- [ ] Task 1" in result

def test_read_entry_not_found() -> None:
    calendar = Calendar(journal=[])
    tool = JournalTool(calendar)
    result = tool.read_entry("2024-01-01")
    assert "No entry found for 2024-01-01" in result

def test_read_entry_invalid_date() -> None:
    calendar = Calendar(journal=[])
    tool = JournalTool(calendar)
    result = tool.read_entry("invalid-date")
    assert "Invalid date format" in result

def test_search_entries() -> None:
    entry1 = Journal(
        summary="Entry 1",
        dtstart=datetime.date(2024, 1, 1),
        description="Meeting with Bob"
    )
    entry2 = Journal(
        summary="Entry 2",
        dtstart=datetime.date(2024, 1, 2),
        description="Buy milk"
    )
    calendar = Calendar(journal=[entry1, entry2])
    tool = JournalTool(calendar)

    result = tool.search_entries("Bob")
    assert "Date: 2024-01-01" in result
    assert "Meeting with Bob" in result
    assert "Buy milk" not in result

def test_search_entries_no_match() -> None:
    calendar = Calendar(journal=[])
    tool = JournalTool(calendar)
    result = tool.search_entries("xyz")
    assert "No matches found" in result
