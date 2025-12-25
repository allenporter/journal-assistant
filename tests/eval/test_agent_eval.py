"""Evaluation tests for the journal assistant agent using ADK AgentEvaluator."""

import os
import pytest
from pathlib import Path
from google.adk.evaluation.agent_evaluator import AgentEvaluator
from google.adk.evaluation.config import EvalConfig
from journal_assistant.journal import get_calendar
from journal_assistant.context import journal_context

# Constants
JOURNAL_DATA_DIR = Path("datasets/alex")
TEST_DATA_FILE = Path("tests/eval/retrieval_adk.test.json")

@pytest.fixture(autouse=True)
def setup_env():
    """Sets up environment variables for the test."""
    if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = "dummy_test_key"
    os.environ["JOURNAL_DATA_DIR"] = str(JOURNAL_DATA_DIR)

@pytest.mark.asyncio
async def test_retrieval_eval():
    """Runs the retrieval evaluation set."""
    if not TEST_DATA_FILE.exists():
        pytest.skip(f"Test data not found at {TEST_DATA_FILE}")

    if not JOURNAL_DATA_DIR.exists():
        pytest.skip(f"Journal data not found at {JOURNAL_DATA_DIR}")

    # Setup context
    calendar = get_calendar(JOURNAL_DATA_DIR)

    # Run evaluation within the journal context
    with journal_context(calendar):
        await AgentEvaluator.evaluate(
            agent_module="journal_assistant.agent",
            eval_dataset_file_path_or_dir=str(TEST_DATA_FILE),
            eval_config=EvalConfig(
                criteria={
                    "response_match_score": 0.8,
                }
            )
        )
