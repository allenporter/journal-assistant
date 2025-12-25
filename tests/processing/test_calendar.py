"""Tests for the calendar processing module."""

import datetime
from pathlib import Path

from journal_assistant.processing.calendar import get_calendar

TEST_DATA_DIR = Path("datasets/alex")

def test_get_calendar_alex() -> None:
    """Test parsing the Alex dataset."""
    calendar = get_calendar(TEST_DATA_DIR)

    # Verify we have events
    assert len(calendar.events) > 0

    # Check a specific date: 2024-01-01
    target_date = datetime.date(2024, 1, 1)
    found_event = None
    for event in calendar.events:
        if event.dtstart == target_date:
            found_event = event
            break

    assert found_event is not None
    assert found_event.summary == "Journal Entry 2024-01-01"
    assert found_event.dtstart == target_date
    assert found_event.dtend == target_date + datetime.timedelta(days=1)
    assert "### Jan 1 (Mon)" in found_event.description
    assert "o Work 10-6" in found_event.description

def test_get_calendar_empty(tmp_path: Path) -> None:
    """Test parsing an empty directory."""
    calendar = get_calendar(tmp_path)
    assert len(calendar.events) == 0

def test_get_calendar_ignores_non_date_files(tmp_path: Path) -> None:
    """Test that files not matching YYYY-MM-DD.md are ignored."""
    (tmp_path / "2024-01.md").write_text("Monthly summary")
    (tmp_path / "random.md").write_text("Random note")
    (tmp_path / "2024-01-01.md").write_text("Daily entry")

    calendar = get_calendar(tmp_path)
    assert len(calendar.events) == 1
    assert calendar.events[0].dtstart == datetime.date(2024, 1, 1)
