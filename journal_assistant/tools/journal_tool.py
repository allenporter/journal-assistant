import datetime
import os
from pathlib import Path
from typing import List

from ..processing.journal import journal_pages_from_markdown
from ..processing.model import JournalPage

class JournalTool:
    def __init__(self, root_dir: Path | None = None):
        if root_dir is None:
            env_path = os.environ.get("JOURNAL_DATA_DIR")
            if env_path:
                root_dir = Path(env_path)
        
        if root_dir is None:
            raise ValueError("root_dir must be provided or JOURNAL_DATA_DIR environment variable must be set.")

        self.root_dir = root_dir
        self._cache: dict[str, JournalPage] = {}
        self._loaded = False

    def _load_all(self):
        if self._loaded:
            return

        # Walk through all markdown files
        for file_path in self.root_dir.rglob("*.md"):
            pages = journal_pages_from_markdown(file_path)
            for page in pages:
                if page.date:
                    self._cache[page.date] = page
        self._loaded = True

    def read_entry(self, date: str) -> str:
        """
        Reads the journal entry for a specific date.

        Args:
            date (str): The date to read in YYYY-MM-DD format.

        Returns:
            str: The content of the journal entry, or a message if not found.
        """
        self._load_all()
        page = self._cache.get(date)
        if not page:
            return f"No entry found for {date}."

        # Format the output
        lines = [f"Entry for {date}:"]
        if page.records:
            for record in page.records:
                prefix = "- "
                if record.type == "task":
                    prefix = "[ ] " if record.status == "open" else "[x] "
                elif record.type == "event":
                    prefix = "o "

                lines.append(f"{prefix}{record.content}")

        return "\n".join(lines)

    def search_entries(self, query: str) -> str:
        """
        Searches journal entries for a query string.

        Args:
            query (str): The text to search for.

        Returns:
            str: A list of matching entries with their dates.
        """
        self._load_all()
        results = []
        query = query.lower()

        for date, page in self._cache.items():
            matches = []
            if page.records:
                for record in page.records:
                    if query in record.content.lower():
                        matches.append(record.content)

            if matches:
                results.append(f"Date: {date}")
                for match in matches:
                    results.append(f"  - {match}")

        if not results:
            return "No matches found."

        return "\n".join(results)
