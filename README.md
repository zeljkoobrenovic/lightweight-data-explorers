# Lightweight Data Explorers

Lightweight Data Explorers is a static-site toolkit for small dashboards, data explorers, controls pages, and standards references.

The repository uses local JSON/CSV files plus simple HTML templates. Python scripts wire those inputs into standalone HTML pages under `docs/`. There is no frontend framework, no npm build, and no server-side runtime requirement.

## What Is Included

Current generated areas include:

- Start page launcher
- AWS usage and cost explorer
- GCP usage and cost explorer
- Brand landscape explorer
- Budget explorer
- Company history explorer
- Incidents explorer
- Business scorecard
- Slack activity explorer
- Workday people explorer
- Controls dashboards
- Standards pages for golden paths, job architecture, rituals, checklists, and principles

## Repository Layout

```text
_config/      Source data and source-owned assets
_templates/   HTML templates and template-owned assets
_wiring/      Python generators
docs/         Generated static site output
```

The main rule is:

```text
_config + _templates + _wiring -> docs
```

## Quick Start

Open the generated launcher:

```text
docs/start/index.html
```

Most generated pages are plain HTML and can be opened directly in a browser. If a browser blocks local assets, serve the repo locally:

```bash
python3 -m http.server 8000
```

Then open:

```text
http://localhost:8000/docs/start/index.html
```

## Requirements

- Python 3
- A browser

No npm install, package manager, database, application server, or bundled frontend build is required.

## Regenerating Pages

Run a generator from the repository root:

```bash
python3 _wiring/generate-start-docs.py
python3 _wiring/data-explorers/generate-scorecard-docs.py
python3 _wiring/controls/generate-controls-docs.py
```

To check that a generator is syntactically valid before running it:

```bash
python3 -B -m py_compile _wiring/data-explorers/generate-scorecard-docs.py
```

To regenerate all current wiring outputs:

```bash
python3 _wiring/controls/generate-controls-docs.py
python3 _wiring/data-explorers/generate-aws-docs.py
python3 _wiring/data-explorers/generate-brands-docs.py
python3 _wiring/data-explorers/generate-budget-docs.py
python3 _wiring/data-explorers/generate-gcp-docs.py
python3 _wiring/data-explorers/generate-history-docs.py
python3 _wiring/data-explorers/generate-incidents-docs.py
python3 _wiring/data-explorers/generate-scorecard-docs.py
python3 _wiring/data-explorers/generate-slack-docs.py
python3 _wiring/data-explorers/generate-workday-docs.py
python3 _wiring/generate-start-docs.py
python3 _wiring/standards/checklists/generate-docs.py
python3 _wiring/standards/generate-golden-paths-docs.py
python3 _wiring/standards/generate-job-architecture-docs.py
python3 _wiring/standards/generate-rituals-docs.py
python3 _wiring/standards/principles/generate-docs.py
```

## Editing Data

For data changes, edit `_config/`.

Examples:

- Start page apps: `_config/start/apps.json`
- Business scorecard: `_config/data/scorecard/scorecard.json`
- Control catalogs: `_config/controls/*.json`
- Standards data: `_config/standards/**`
- Explorer data: `_config/data/<explorer>/...`

After editing data, run the matching generator under `_wiring/`.

## Editing Presentation

For layout, styling, or client-side behavior, edit `_templates/`.

Examples:

- Start page template: `_templates/start/index.html`
- Scorecard template: `_templates/scorecard/index.html`
- Data explorer templates: `_templates/data-explorers/**`
- Shared tabs and breadcrumbs snippets: `_templates/_imports/**`

After editing a template, run every generator that uses it.

## Generated Output

`docs/` is generated output. It is useful for publishing and inspection, but source changes should normally happen in `_config/`, `_templates/`, or `_wiring/`.

Some generators clean their output directories before writing fresh files so stale pages do not remain after source data changes.

## Design Constraints

Keep the project lightweight:

- Use plain HTML, CSS, and vanilla JavaScript.
- Keep generated pages static and publishable as files.
- Embed generated data directly in HTML unless there is a clear reason not to.
- Do not add React, npm tooling, bundlers, or external JavaScript libraries unless the project explicitly changes direction.

## Agent Notes

Machine-oriented working instructions live in `AGENTS.md`. Humans should start here; coding agents should also read `AGENTS.md` before making repository changes.
