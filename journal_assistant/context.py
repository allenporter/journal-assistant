from contextvars import ContextVar
from contextlib import contextmanager
from typing import Generator
from ical.calendar import Calendar

_CURRENT_JOURNAL: ContextVar[Calendar | None] = ContextVar(
    "current_journal", default=None
)


@contextmanager
def journal_context(journal: Calendar) -> Generator[None, None, None]:
    """Context manager to set the current journal."""
    token = _CURRENT_JOURNAL.set(journal)
    try:
        yield
    finally:
        _CURRENT_JOURNAL.reset(token)


def get_current_journal() -> Calendar | None:
    """Get the current journal from context."""
    return _CURRENT_JOURNAL.get()
