# journal-assistant

An agent based Journal Assistant, going deeper into https://github.com/allenporter/home-assistant-journal-assistant and https://github.com/allenporter/home-assistant-rulebook

## Local development

```shell
uv venv --python=3.14
source .venv/bin/activate
uv pip install -r ./requirements_dev.txt
```

## Run local agent

```shell
export GOOGLE_API_KEY=<api key>
export JOURNAL_DATA_DIR=datasets/alex
python3 -m script.run_agent
Enter a query (or 'exit' to quit):
> help me reflect on my life
Reflecting on your journey through 2024, there is a clear arc of transformation, resilience, and artistic growth.
...
```

## Testing

### Run Unit Tests
To run the standard unit tests (excluding expensive evaluations):

```shell
pytest
```

### Run Evaluations
To run the agent evaluations (requires `GOOGLE_API_KEY` and incurs LLM costs):

```shell
export GOOGLE_API_KEY=<your-api-key>
pytest -m eval
```

## Related Work

- https://github.com/allenporter/home-assistant-journal-assistant - LLM based Journal processor for Home Assistant
- https://github.com/allenporter/home-assistant-supernote-cloud - Home Assistant Media Source for the Supernote e-ink journal
- https://github.com/allenporter/supernote-lite - Private cloud server for Supernote e-ink journal and library for processing notebook entries
