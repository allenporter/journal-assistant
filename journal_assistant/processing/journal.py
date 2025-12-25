"""Converter from markdown journal files to JournalPage objects."""

import re
import logging
import datetime
from pathlib import Path
from typing import Iterator

from .model import JournalPage, RapidLogEntry

_LOGGER = logging.getLogger(__name__)

def parse_line(line: str) -> RapidLogEntry | None:
    """Parse a single line of markdown into a RapidLogEntry."""
    line = line.strip()
    if not line:
        return None

    entry = RapidLogEntry()

    # Check for critical task
    if line.startswith("*"):
        entry.critical = True
        line = line[1:].strip()

    # Check type based on bullet point
    if line.startswith("o "):
        entry.type = "event"
        entry.content = line[2:]
    elif line.startswith("• "):
        entry.type = "task"
        entry.status = "open"
        entry.content = line[2:]
    elif line.startswith("X "):
        entry.type = "task"
        entry.status = "completed"
        entry.content = line[2:]
    elif line.startswith("- "):
        entry.type = "note"
        entry.content = line[2:]
    elif line.startswith("< "):
        entry.type = "task"
        entry.status = "migrated_future"
        entry.content = line[2:]
    elif line.startswith("> "):
        entry.type = "task"
        entry.status = "migrated"
        entry.content = line[2:]
    else:
        # If it doesn't start with a known bullet, ignore or treat as note?
        # For now, ignore lines that don't look like log entries (e.g. headers, empty lines)
        return None

    return entry

def journal_pages_from_markdown(file_path: Path) -> list[JournalPage]:
    """Parse a markdown file into a list of JournalPage objects (one per day)."""
    content = file_path.read_text()
    lines = content.splitlines()

    pages = []
    current_date = None
    current_records = []

    # Try to infer year/month from filename (e.g., "2024-01.md")
    try:
        stem = file_path.stem
        year_str, month_str = stem.split("-")
        year = int(year_str)
        month = int(month_str)
    except ValueError:
        # Fallback or log warning
        _LOGGER.warning(f"Could not parse date from filename: {file_path.name}")
        return []

    # Regex for date headers like "### Jan 1 (Mon)"
    # We assume the month in the header matches the file's month or is consistent.
    date_header_re = re.compile(r"^###\s+(\w{3})\s+(\d+)\s+\(\w+\)")

    for line in lines:
        match = date_header_re.match(line)
        if match:
            # If we were processing a day, save it
            if current_date:
                pages.append(JournalPage(
                    filename=str(file_path),
                    created_at=current_date.isoformat(),
                    date=current_date.isoformat(),
                    records=current_records
                ))
                current_records = []

            # Start new day
            day = int(match.group(2))
            try:
                current_date = datetime.date(year, month, day)
            except ValueError:
                _LOGGER.warning(f"Invalid date encountered: {year}-{month}-{day}")
                current_date = None

        elif current_date:
            # We are inside a day section
            # Stop if we hit another header level that isn't a day header (e.g. ## Week 2)
            if line.startswith("## "):
                 # Save and close current day
                if current_records:
                    pages.append(JournalPage(
                        filename=str(file_path),
                        created_at=current_date.isoformat(),
                        date=current_date.isoformat(),
                        records=current_records
                    ))
                current_date = None
                current_records = []
                continue

            entry = parse_line(line)
            if entry:
                entry.date = current_date.isoformat()
                current_records.append(entry)

    # Add the last page if exists
    if current_date and current_records:
        pages.append(JournalPage(
            filename=str(file_path),
            created_at=current_date.isoformat(),
            date=current_date.isoformat(),
            records=current_records
        ))

    return pages
