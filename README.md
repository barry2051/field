# Field Codex

Field Codex is a minimal knowledge graph CLI for exploring the field, General Nature Intelligence (GNI), and related ideas. Data lives in a single `universe.json` file at the repository root. The tool loads seed data on first run and keeps the design intentionally simple for future extensions.

## Project structure

```
.
├── README.md
├── universe.json        # created on first run with seed nodes/edges
└── src/
    └── field_codex/
        ├── __init__.py
        └── __main__.py  # CLI entrypoint
```

## Requirements

- Python 3.10+
- No external dependencies

## Installation

Run commands from the repository root. You can execute the CLI with `python -m field_codex` using the `src` directory on the module path:

```bash
python -m field_codex --help
```

If you prefer, you can set `PYTHONPATH` for convenience:

```bash
PYTHONPATH=src python -m field_codex list
```

## Commands

- `python -m field_codex list` — list all nodes
- `python -m field_codex list-questions` — list only nodes tagged as `question`
- `python -m field_codex show <node_id>` — view a node and its incoming/outgoing links
- `python -m field_codex search "<text>"` — search for text in ids, titles, summaries, or tags
- `python -m field_codex add-node` — interactively add a node (prompts for id, title, node_type, summary, tags)
- `python -m field_codex add-link` — interactively add a link (prompts for source, relation, target)

Changes made via `add-node` or `add-link` are persisted back to `universe.json` immediately.

## Notes

- The CLI writes `universe.json` with formatted JSON for readability.
- You can extend the data model later with timestamps, provenance fields, or export routines without changing the storage layout.
