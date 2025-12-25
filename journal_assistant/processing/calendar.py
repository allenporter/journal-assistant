"""Module for parsing journal entries into an iCal Calendar."""

import datetime
from pathlib import Path
import logging

from ical.calendar import Calendar
from ical.journal import Journal

_LOGGER = logging.getLogger(__name__)

def get_calendar(directory: Path) -> Calendar:
    """Parse markdown journal entries from a directory into an iCal Calendar.

    Args:
        directory: The root directory containing journal entries (e.g. datasets/alex).

    Returns:
        A Calendar object containing journal entries for each journal entry.
    """
    calendar = Calendar()

    # Walk through the directory to find markdown files
    for file_path in directory.rglob("*.md"):
        # Check if filename matches YYYY-MM-DD.md format
        if not len(file_path.stem) == 10:
            continue

        try:
            date = datetime.date.fromisoformat(file_path.stem)
        except ValueError:
            continue

        # Read content
        content = file_path.read_text()

        # Create a journal entry
        journal = Journal(
            summary=f"Journal Entry {date}",
            dtstart=date,
            description=content,
        )
        calendar.journal.append(journal)
    return calendar
