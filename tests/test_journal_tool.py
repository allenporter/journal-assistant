import datetime
from ical.calendar import Calendar
from ical.journal import Journal
from journal_assistant.tools.journal_tool import JournalTool, read_entry, search_entries
from journal_assistant.context import journal_context


def test_read_entry() -> None:
    entry = Journal(
        summary="Test Entry",
        dtstart=datetime.date(2024, 1, 1),
        description="This is a test entry.\n- [ ] Task 1",
    )
    calendar = Calendar()
    calendar.journal = [entry]
    tool = JournalTool(calendar)

    result = tool.read_entry("2024-01-01")
    assert "Entry for 2024-01-01" in result
    assert "This is a test entry" in result
    assert "- [ ] Task 1" in result


def test_read_entry_not_found() -> None:
    calendar = Calendar()
    tool = JournalTool(calendar)
    result = tool.read_entry("2024-01-01")
    assert "No entry found for 2024-01-01" in result


def test_read_entry_invalid_date() -> None:
    calendar = Calendar()
    tool = JournalTool(calendar)
    result = tool.read_entry("invalid-date")
    assert "Invalid date format" in result


def test_search_entries() -> None:
    entry1 = Journal(
        summary="Entry 1",
        dtstart=datetime.date(2024, 1, 1),
        description="Meeting with Bob",
    )
    entry2 = Journal(
        summary="Entry 2", dtstart=datetime.date(2024, 1, 2), description="Buy milk"
    )
    calendar = Calendar()
    calendar.journal = [entry1, entry2]
    tool = JournalTool(calendar)

    result = tool.search_entries("Bob")
    assert "Date: 2024-01-01" in result
    assert "Meeting with Bob" in result
    assert "Buy milk" not in result


def test_search_entries_no_match() -> None:
    calendar = Calendar()
    tool = JournalTool(calendar)
    result = tool.search_entries("xyz")
    assert "No matches found" in result


def test_context_based_tool_calls() -> None:
    """Test the standalone functions that use the context."""
    entry = Journal(
        summary="Context Entry",
        dtstart=datetime.date(2024, 1, 1),
        description="Context test",
    )
    calendar = Calendar()
    calendar.journal = [entry]

    # Test without context
    assert read_entry("2024-01-01") == "No journal context is set."
    assert search_entries("Context") == "No journal context is set."

    # Test with context
    with journal_context(calendar):
        result = read_entry("2024-01-01")
        assert "Entry for 2024-01-01" in result
        assert "Context test" in result

        search_result = search_entries("Context")
        assert "Date: 2024-01-01" in search_result
        assert "Context test" in search_result
