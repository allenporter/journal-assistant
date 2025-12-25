"""Module for parsing journal entries into an iCal Calendar."""

import datetime
from pathlib import Path
import logging

from ical.calendar import Calendar
from ical.journal import Journal

_LOGGER = logging.getLogger(__name__)

__all__ = [
    "get_calendar",
]


def _parse_date_from_filename(filename: Path) -> datetime.date | None:
    """Parse a date from a filename in YYYY-MM-DD.md or YYYY-MM.md format."""
    if len(filename.stem) == 10:
        try:
            return datetime.date.fromisoformat(filename.stem)
        except ValueError:
            _LOGGER.debug(f"Filename {filename} does not match YYYY-MM-DD format.")
            return None

    if len(filename.stem) == 7:
        try:
            year, month = map(int, filename.stem.split("-"))
            return datetime.date(year, month, 1)
        except ValueError:
            _LOGGER.debug(f"Filename {filename} does not match YYYY-MM format.")
            return None

    _LOGGER.debug(f"Filename {filename} does not match expected date formats.")
    return None


def _parse_title(content: str) -> str | None:
    """Parse a title from the markdown content."""
    for i, line in enumerate(content.splitlines()):
        if i >= 4:
            break
        if line.startswith("#"):
            return line.lstrip("#").strip()
    return None


def get_calendar(directory: Path) -> Calendar:
    """Parse markdown journal entries from a directory into an iCal Calendar.

    Args:
        directory: The root directory containing journal entries (e.g. datasets/alex).

    Returns:
        A Calendar object containing journal entries for each journal entry.
    """
    # Walk through the directory to find markdown files
    entries = []
    for file_path in directory.rglob("*.md"):
        date = _parse_date_from_filename(file_path)
        content = file_path.read_text()
        title = _parse_title(content)
        if not title:
            title = f"Journal Entry {date}" if date else "Journal Entry"

        entries.append(
            Journal(
                summary=title,
                dtstart=date,
                description=content,
            )
        )
    return Calendar(journal=entries)
