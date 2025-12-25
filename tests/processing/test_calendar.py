"""Tests for the calendar processing module."""

import datetime
from pathlib import Path

from journal_assistant.processing.calendar import get_calendar

TEST_DATA_DIR = Path("datasets/alex")

def test_get_calendar_alex() -> None:
    """Test parsing the Alex dataset."""
    calendar = get_calendar(TEST_DATA_DIR)

    # Verify we have journal entries
    assert len(calendar.journal) > 0

    # Check a specific date: 2024-01-01
    target_date = datetime.date(2024, 1, 1)
    found_entry = None
    for entry in calendar.journal:
        if entry.dtstart == target_date:
            found_entry = entry
            break

    assert found_entry is not None
    assert found_entry.summary == "Journal Entry 2024-01-01"
    assert found_entry.dtstart == target_date
    assert "### Jan 1 (Mon)" in found_entry.description
    assert "o Work 10-6" in found_entry.description

def test_get_calendar_empty(tmp_path: Path) -> None:
    """Test parsing an empty directory."""
    calendar = get_calendar(tmp_path)
    assert len(calendar.journal) == 0

def test_get_calendar_ignores_non_date_files(tmp_path: Path) -> None:
    """Test that files not matching YYYY-MM-DD.md are ignored."""
    (tmp_path / "2024-01.md").write_text("Monthly summary")
    (tmp_path / "random.md").write_text("Random note")
    (tmp_path / "2024-01-01.md").write_text("Daily entry")

    calendar = get_calendar(tmp_path)
    assert len(calendar.journal) == 1
    assert calendar.journal[0].dtstart == datetime.date(2024, 1, 1)
