# Plan: Design Bullet Journal Assistant with Google ADK

This plan outlines the design and implementation of a modular agent system using the Google Agent Development Kit (ADK) to handle bullet journal tasks like reflection, planning, and image generation. The system will be built in the `journal-assistant` repository, reusing logic from the Home Assistant integration where applicable.

## Goals
- Create a standalone agentic application using Google ADK.
- Support core Bullet Journal tasks: Reflection (Daily/Weekly/Monthly), Planning, and Image Generation.
- Ensure modularity for future integration back into Home Assistant.
- Establish a robust evaluation pipeline using existing ground truth data.

## Architecture

### 1. Data Layer
- **Journal Reader**: A component to parse markdown-based journal files.
  - *Source*: Adapt `JournalPage` and YAML parsing logic from `home-assistant-journal-assistant/custom_components/journal_assistant/processing/journal.py`.
  - *Extension*: Add support for pure Markdown parsing (parsing headers as dates/sections) to match `tests/testdata` format.
- **Vector Database**: (Optional for V1) Reuse `local_vectordb.py` for semantic search over past entries.

### 2. Tools (ADK Components)
- **`JournalTool`**:
  - `read_entry(date)`: Retrieve specific journal entries.
  - `search_entries(query)`: Find relevant past notes.
  - `append_entry(date, text)`: (Future) Add new notes.
- **`CalendarTool`**:
  - `get_events(start_date, end_date)`: Look ahead for upcoming events (mocked or connected to `.ics`/CalDAV).
- **`ImageGenTool`**:
  - `generate_image(prompt)`: Wrapper for an image generation model (e.g., Imagen).

### 3. Agents
- **`ReflectionAgent`**:
  - *Role*: Reviews past entries and generates summaries/reflections.
  - *Prompts*: Reuse `dynamic_prompts/` (e.g., `daily.yaml`, `monthly-01.yaml`).
- **`PlanningAgent`**:
  - *Role*: Looks at the calendar and previous tasks to suggest a schedule or focus for the day/week.
- **`RouterAgent`**:
  - *Role*: The entry point that decides which specialized agent to call based on the user's request (e.g., "Help me reflect on last month" vs. "What's on my plate today?").

## Implementation Steps

### Step 1: Project Initialization
1.  Initialize a new ADK project in `journal-assistant`.
2.  Configure `pyproject.toml` with `google-adk` dependencies.
3.  Set up the directory structure: `agents/`, `tools/`, `processing/`.

### Step 2: Core Logic Migration
1.  Copy relevant processing logic from `home-assistant-journal-assistant`:
    - `processing/journal.py` (adapt for Markdown)
    - `processing/dynamic_prompts/` (copy YAML templates)
2.  Implement `MarkdownJournalReader` in `journal_assistant/processing/`.

### Step 3: Tool Implementation
1.  Create `JournalTool` class implementing the ADK Tool interface.
2.  Create `CalendarTool` class.
3.  Create `ImageGenTool` class.

### Step 4: Agent Configuration
1.  Define `ReflectionAgent` using ADK's configuration (system instructions + tools).
2.  Define `PlanningAgent`.
3.  Set up the `RouterAgent` or a main entry loop.

### Step 5: Evaluation Pipeline
1.  Create an evaluation script `scripts/eval_agents.py`.
2.  Use `tests/testdata/alex` as input.
3.  Compare agent outputs against `tests/testdata/ground_truth` (e.g., `alex_profile.yaml`, `alex_timeline.yaml`).
4.  Implement metrics: Semantic similarity of reflections, accuracy of extracted tasks.

## Future Considerations
- **Home Assistant Integration**: Expose the ADK agents as a service in HA.
- **State Management**: Decide if agents need conversation history (Memory) or just context from files.
- **Model Config**: Allow users to swap LLMs (Gemini, local models) via configuration.
