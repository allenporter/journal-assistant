from ical.calendar import Calendar
from ical.journal import Journal
import datetime
from journal_assistant.context import journal_context, get_current_journal


def test_context_manager() -> None:
    """Test that the context manager sets and resets the context."""
    assert get_current_journal() is None

    j = Journal(summary="Test", dtstart=datetime.date(2025, 1, 1), description="Desc")
    c = Calendar()
    c.journal = [j]

    with journal_context(c):
        assert get_current_journal() == c

    assert get_current_journal() is None


def test_nested_context() -> None:
    """Test nested contexts."""
    j1 = Journal(
        summary="Test 1", dtstart=datetime.date(2025, 1, 1), description="Desc 1"
    )
    c1 = Calendar()
    c1.journal = [j1]

    j2 = Journal(
        summary="Test 2", dtstart=datetime.date(2025, 1, 2), description="Desc 2"
    )
    c2 = Calendar()
    c2.journal = [j2]

    assert get_current_journal() is None

    with journal_context(c1):
        assert get_current_journal() == c1

        with journal_context(c2):
            assert get_current_journal() == c2

        assert get_current_journal() == c1

    assert get_current_journal() is None
