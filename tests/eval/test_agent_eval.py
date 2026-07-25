"""Evaluation tests for the journal assistant agent using ADK AgentEvaluator."""

import os
from pathlib import Path

import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator

from journal_assistant.context import journal_context
from journal_assistant.journal import get_calendar

pytestmark = pytest.mark.eval

# Constants
JOURNAL_DIR = Path("datasets/alex")
RETRIEVAL_EVAL_FILE = Path("tests/eval/retrieval_adk.test.json")
REFLECTION_EVAL_FILE = Path("tests/eval/reflection_adk.test.json")
NUM_RUNS = 1


@pytest.fixture(autouse=True)
def setup_env():
    """Sets up environment variables for the test."""
    if "GOOGLE_API_KEY" not in os.environ:
        raise ValueError("GOOGLE_API_KEY environment variable is not set")


@pytest.mark.asyncio
async def test_retrieval_eval():
    """Runs the retrieval evaluation set."""
    if not RETRIEVAL_EVAL_FILE.exists():
        pytest.skip(f"Test data not found at {RETRIEVAL_EVAL_FILE}")

    if not JOURNAL_DIR.exists():
        pytest.skip(f"Journal data not found at {JOURNAL_DIR}")

    # Setup context
    calendar = get_calendar(JOURNAL_DIR)

    # Run evaluation within the journal context
    with journal_context(calendar):
        await AgentEvaluator.evaluate(
            agent_module="journal_assistant.agent",
            eval_dataset_file_path_or_dir=str(RETRIEVAL_EVAL_FILE),
            num_runs=NUM_RUNS,
        )


@pytest.mark.asyncio
async def test_reflection_eval():
    """Runs the reflection evaluation set."""
    if not REFLECTION_EVAL_FILE.exists():
        pytest.skip(f"Test data not found at {REFLECTION_EVAL_FILE}")

    if not JOURNAL_DIR.exists():
        pytest.skip(f"Journal data not found at {JOURNAL_DIR}")

    # Setup context
    calendar = get_calendar(JOURNAL_DIR)

    # Run evaluation within the journal context
    with journal_context(calendar):
        await AgentEvaluator.evaluate(
            agent_module="journal_assistant.agent",
            eval_dataset_file_path_or_dir=str(REFLECTION_EVAL_FILE),
            num_runs=NUM_RUNS,
        )
