import datetime
from typing import List

from ical.calendar import Calendar

class JournalTool:
    def __init__(self, calendar: Calendar):
        self.calendar = calendar

    def read_entry(self, date: str) -> str:
        """
        Reads the journal entry for a specific date.

        Args:
            date (str): The date to read in YYYY-MM-DD format.

        Returns:
            str: The content of the journal entry, or a message if not found.
        """
        try:
            target_date = datetime.date.fromisoformat(date)
        except ValueError:
            return f"Invalid date format: {date}. Please use YYYY-MM-DD."

        for entry in self.calendar.journal:
            if entry.dtstart == target_date:
                return f"Entry for {date}:\n{entry.description}"

        return f"No entry found for {date}."

    def search_entries(self, query: str) -> str:
        """
        Searches journal entries for a query string.

        Args:
            query (str): The text to search for.

        Returns:
            str: A list of matching entries with their dates.
        """
        results = []
        query = query.lower()

        for entry in self.calendar.journal:
            if not entry.description:
                continue

            matches = []
            for line in entry.description.splitlines():
                if query in line.lower():
                    matches.append(line.strip())

            if matches:
                results.append(f"Date: {entry.dtstart}")
                for match in matches:
                    results.append(f"  - {match}")

        if not results:
            return "No matches found."

        return "\n".join(results)
