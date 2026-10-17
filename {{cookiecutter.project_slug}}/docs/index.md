# {{ cookiecutter.project_name }}

<p align="center">
  <img src="assets/python-logo.svg" alt="Python Logotype" width="120">
</p>

Welcome to the documentation for **{{ cookiecutter.project_name }}**.

{{ cookiecutter.description }}

```mermaid
flowchart LR
    A["Developer"] -->|uv run| B["{{ cookiecutter.project_slug }}"]
    B --> C["Core Engine"]
    B --> D["Zensical Docs"]
```
{% if cookiecutter.include_cli in [True, "yes", "true", "True", "1"] %}

## Quick Start CLI

<div class="termy">

```console
$ uv run {{ cookiecutter.project_slug }} greet "World"

✨ Hello, World!

// Inspect CLI options and help
$ uv run {{ cookiecutter.project_slug }} --help

<b>Usage: </b><b>{{ cookiecutter.project_slug }} [OPTIONS] COMMAND [ARGS]...</b>

╭─ Options ─────────────────────────────────────────╮
│ --version  -v        Show version and exit.       │
│ --help               Show this message and exit.  │
╰───────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────╮
│ greet                Display a personalized       │
│                      greeting.                    │
╰───────────────────────────────────────────────────╯
```

</div>
{% endif %}

## Installation

=== "uv (Recommended)"

    ```bash
    uv add {{ cookiecutter.project_slug }}
    ```

=== "pip"

    ```bash
    pip install {{ cookiecutter.project_slug }}
    ```

> [!TIP]
> Always run project commands via `uv run poe <task>` or `uv run <command>`.
> This guarantees hermetic execution inside the managed virtual environment without manual activation.

## Highlights

{% include "docs/_tool_stack.md" %}

## Architecture & Project Layout

```tree
./
├── pyproject.toml
├── poe_tasks.toml
├── zensical.toml
├── src/
│   └── {{ cookiecutter.package_name }}/
│       ├── __init__.py
│       └── core.py
├── tests/
│   └── test_core.py
└── docs/
    ├── index.md
    ├── getting-started.md
    ├── reference.md
    └── changelog.md
```

> [!NOTE]
> The directory tree above is rendered dynamically at documentation build time using
> the `markdown-exec` plugin with the ` ```tree ` fence.

## Mathematical Notation

LaTeX equations are fully supported via MathJax:

$$
f(x) = \int_{-\infty}^\infty \hat{f}(\xi)\,e^{2 \pi i \xi x}\,d\xi
$$

Inline equations such as $E = mc^2$ and $\mathcal{O}(n \log n)$ render smoothly.

## Dynamic Code Execution

Execute embedded Python and shell snippets at documentation build time:

```python exec="on"
import sys

print(f"Docs built with Python {sys.version.split()[0]} via markdown-exec!")
```

## Next Steps

- Explore the [Guide](getting-started.md) to set up your environment.
- Review the [API Reference](reference.md) for module details.
- Review the [Changelog](changelog.md) for release history.
