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

## Highlights

{% include "docs/_tool_stack.md" %}

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
