# ADK Reference

This document describes how to use the Google Agent Development Kit (ADK) configuration format and how to run agents with different personas.

## Agent Configuration

Agents are defined in YAML files located in `journal_assistant/agents/`.

### Structure

```yaml
name: agent_name
model: gemini-2.0-flash-exp
description: Description of the agent.
instruction: |
  System instructions for the agent.
tools:
  - name: package.module.function_name
sub_agents:
  - config_path: sub_agent.yaml
```

## Tool Registration

Tools are Python functions that the agent can call. In the YAML config, tools are referenced by their full import path (e.g., `journal_assistant.tools.registry.read_entry`).

To support class-based tools (like `JournalTool`) that require initialization, we use a **registry pattern**. The `journal_assistant.tools.registry` module initializes the tool instances (singletons) and exposes their methods as module-level functions.

## Running Agents

You can run an agent using the ADK CLI or a Python script that loads the config.

### Environment Variables

To switch between different datasets (personas), use the `JOURNAL_DATA_DIR` environment variable.

```bash
# Run as Alex
export JOURNAL_DATA_DIR=$(pwd)/datasets/alex
python script/run_agent.py

# Run as Sarah
export JOURNAL_DATA_DIR=$(pwd)/datasets/sarah
python script/run_agent.py
```
