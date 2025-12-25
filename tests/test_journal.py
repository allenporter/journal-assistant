"""Tests for the calendar processing module."""

import datetime
from pathlib import Path

import pytest

from journal_assistant.journal import get_calendar

TEST_DATA_DIR = Path("datasets/alex")


@pytest.mark.parametrize(
    "data_dir",
    [
        Path("datasets/alex"),
        Path("datasets/sarah"),
    ],
)
def test_get_calendar_sarah(data_dir: Path) -> None:
    """Test parsing the Sarah dataset."""
    calendar = get_calendar(data_dir)
    assert len(calendar.journal) > 0


def test_get_calendar_alex() -> None:
    """Test parsing the Alex dataset."""
    calendar = get_calendar(TEST_DATA_DIR)

    # Verify we have journal entries
    assert len(calendar.journal) > 0

    # Check a specific date: 2024-01-01
    target_date = datetime.date(2024, 1, 1)
    found_entry = None
    for entry in calendar.journal:
        if entry.dtstart == target_date and "### Jan 1 (Mon)" in entry.description:
            found_entry = entry
            break

    assert found_entry is not None
    assert found_entry.summary == "Jan 1 (Mon)"
    assert found_entry.dtstart == target_date
    assert "o Work 10-6" in found_entry.description

    # Check monthly summary
    monthly_entry = None
    for entry in calendar.journal:
        if entry.dtstart == target_date and "# January 2024" in entry.description:
            monthly_entry = entry
            break

    assert monthly_entry is not None
    assert monthly_entry.summary == "January 2024"


def test_get_calendar_empty(tmp_path: Path) -> None:
    """Test parsing an empty directory."""
    calendar = get_calendar(tmp_path)
    assert len(calendar.journal) == 0


def test_get_calendar_includes_non_date_files(tmp_path: Path) -> None:
    """Test that files not matching YYYY-MM-DD.md are included as non-dated entries."""
    (tmp_path / "2024-01.md").write_text("Monthly summary")
    (tmp_path / "random.md").write_text("Random note")
    (tmp_path / "2024-01-01.md").write_text("Daily entry")

    calendar = get_calendar(tmp_path)
    # All 3 files should be parsed
    assert len(calendar.journal) == 3

    # Verify random.md
    random_entry = next(
        (
            e
            for e in calendar.journal
            if e.summary == "Journal Entry" and e.dtstart is None
        ),
        None,
    )
    assert random_entry is not None
    assert random_entry.description == "Random note"
