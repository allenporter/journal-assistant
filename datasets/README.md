# Evaluation Datasets

This directory contains synthetic journal data designed for evaluating the Journal Assistant agent. The data simulates the personal journals of two distinct personas over a multi-year period, providing a rich context for testing the agent's ability to understand narrative, track tasks, and infer correlations.

## Structure

The data is organized by persona and year:

```
datasets/
├── ground_truth/       # Source-of-truth files for evaluation
│   ├── alex_profile.yaml
│   ├── alex_timeline.yaml
│   ├── sarah_profile.yaml
│   └── sarah_timeline.yaml
├── alex/               # Persona: Creative / Art Student
│   ├── 2024/
│   │   ├── 2024-01.md ... 2024-12.md  # Full daily logs
│   │   └── summary.md
│   └── 2025/
│       └── 2025-01.md
└── sarah/              # Persona: Professional / Project Manager
    ├── 2024/
    │   ├── 2024-01.md ... 2024-12.md  # Full daily logs
    │   └── summary.md
    └── 2025/
        └── 2025-01.md
```

## Personas

### Sarah (The Professional)
*   **Role**: Senior Project Manager at TechCorp.
*   **Themes**: Career progression (promotion), health tracking (migraines, running), family life (husband Mark, daughter Lily).
*   **Journal Style**: Structured, task-oriented, uses rapid logging symbols extensively.

### Alex (The Creative)
*   **Role**: Art Student / Freelance Illustrator.
*   **Themes**: Creative struggles, financial stress, moving cities (CA to Portland), social life.
*   **Journal Style**: Expressive, mood-focused, less rigid structure.

## Journal Format

The journals use a rapid logging format:
*   `• Task`: An open task.
*   `x Task`: A completed task.
*   `> Task`: A task migrated to a future date.
*   `o Event`: An event or appointment.
*   `- Note`: A note, observation, or thought.

## Usage

This dataset is intended to be used for:
1.  **Context Retrieval**: Testing if the agent can find specific past events (e.g., "When did Sarah go to Hawaii?").
2.  **Inference**: Testing if the agent can connect dots (e.g., "Does Alex's sleep affect their art?" or "What triggers Sarah's migraines?").
3.  **Task Management**: Evaluating how the agent handles task migration and completion across days/months.
4.  **Summarization**: Generating summaries of weeks, months, or years based on the raw logs.

## Ground Truth

The `ground_truth/` directory contains YAML files that define the "facts" of the simulation. These can be used to programmatically verify the agent's outputs. For example, `sarah_timeline.yaml` lists key events that *should* be reflected in the markdown journals.
