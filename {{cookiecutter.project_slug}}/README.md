# {{ cookiecutter.project_name }}

<p align="center">
  <img src="docs/assets/python-logo.svg" alt="Python Logo" width="100">
</p>

{% if cookiecutter.include_github_actions == "yes" -%}
[![CI](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/actions/workflows/python_tests.yaml/badge.svg)](https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/actions/workflows/python_tests.yaml)
{%- endif %}
[![Python: {{ cookiecutter.python_version }}+](https://img.shields.io/badge/python-{{ cookiecutter.python_version }}+-blue.svg)](https://www.python.org/downloads/)
[![Code Style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Type Checked: Pyrefly](https://img.shields.io/badge/types-pyrefly-blueviolet.svg)](https://github.com/facebook/pyrefly)
[![Coverage: pytest-cov](https://img.shields.io/badge/coverage-80%25%2B-brightgreen.svg)](.coveragerc)
{% if cookiecutter.license != "None" -%}
[![License: {{ cookiecutter.license }}](https://img.shields.io/badge/license-{{ cookiecutter.license }}-green.svg)](LICENSE)
{%- endif %}

{{ cookiecutter.description }}

## 🎯 Elevator Pitch

> **{{ cookiecutter.project_name }}** is a high-velocity, production-grade
> Python project built for developers who refuse to compromise on speed,
> typing rigor, or architectural cleanliness. Engineered for rapid iteration and
> zero-regression craftsmanship, it couples strict static typing and automated
> modular boundaries with instant verification pipelines and live-reloading
> documentation.

## Overview

**{{ cookiecutter.project_name }}** is built with a modern, strict Python
stack designed for reliability, speed, and clean architecture:

- **uv**: Next-generation package manager and PEP 517 build backend.
- **Ruff**: Comprehensive linting and formatting with preview rules.
- **Pyrefly**: Meta's high-performance static type checker in strict mode.
- **complexipy**: Cognitive complexity limits preventing spaghetti logic.
- **Zensical**: Modern static site documentation with MathJax LaTeX support and
  markdown-exec.
- **rumdl**: Rigid markdown formatting and embedded code block linting.
- **Tach**: Architecture boundary enforcement preventing circular imports.
- **Poe the Poet**: Declarative task automation.

## Quick Start

Get started with **{{ cookiecutter.project_name }}** in moments.

### 1. Installation

Install via `uv`:

```bash
uv add {{ cookiecutter.project_slug }}
```

Or install with pip:

```bash
pip install {{ cookiecutter.project_slug }}
```

### 2. Library Usage

```python
from {{ cookiecutter.package_name }} import get_greeting

message = get_greeting("World")
print(message)
```

{%- if cookiecutter.include_cli == "yes" %}

### 3. Command Line Interface

Execute the CLI commands via `uv run`:

```bash
# Display help and available commands
uv run {{ cookiecutter.project_slug }} --help

# Run greet command
uv run {{ cookiecutter.project_slug }} greet "Developer"
```
{%- endif %}

## Development Setup

Get your local development environment ready in three steps:

### 1. Install Dependencies

```bash
git clone https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.git
cd {{ cookiecutter.project_slug }}
uv sync --group dev
```

### 2. Run Tests with Coverage

Run unit tests and verify code coverage:

```bash
uv run poe test
```

Generate an interactive HTML coverage report in `htmlcov/`:

```bash
uv run poe coverage
```

### 3. Run Quality Checks

Verify that the codebase satisfies all strict linting, typing, complexity,
and architectural rules:

```bash
uv run poe code-quality
```

### 4. Serve Documentation

Preview the documentation locally with live reload and MathJax rendering:

```bash
uv run poe docs-serve
```

## Architecture & Boundaries

Architecture rules are defined and enforced with **Tach**:

{% if cookiecutter.include_cli == "yes" -%}
```mermaid
flowchart TD
    CLI["CLI Layer"]
    CORE["Core Layer"]
    CLI --> CORE
    CORE --> EXT["External Dependencies"]
```
{%- else -%}
```mermaid
flowchart TD
    CORE["Core Layer"]
    CORE --> EXT["External Dependencies"]
```
{%- endif %}

Run `uv run poe dependencies` to validate that no layer violations or circular
dependencies occur.

## Mathematical Specifications

Documentation formulas are rendered via **Zensical** and **MathJax**:

$$
\mathcal{L}(\theta) = \frac{1}{N} \sum_{i=1}^N \ell\left(f(x_i; \theta), y_i\right)
$$

Inline equations like $E = mc^2$ and $\Omega(n)$ are supported out of the box.

## Available Poe Tasks

| Task | Command | Description |
|---|---|---|
| **Quality** | `uv run poe code-quality` | Runs lint, format-check, lint-md, type-check, complexity, tach |
| **Test** | `uv run poe test` | Executes pytest with doctests and coverage thresholds |
| **Coverage** | `uv run poe coverage` | Creates detailed HTML coverage report |
| **Lint** | `uv run poe lint` | Checks code against all Ruff rules |
| **Format** | `uv run poe format` | Formats code with Ruff |
| **Format Check** | `uv run poe format-check` | Verifies code format with Ruff without modifying files |
| **Markdown** | `uv run poe lint-md` | Lints markdown files with rumdl |
| **Types** | `uv run poe type-check` | Performs strict type analysis with Pyrefly |
| **Complexity** | `uv run poe complexity` | Evaluates cognitive complexity with complexipy |
| **Boundaries** | `uv run poe dependencies` | Validates modular boundaries with Tach |
| **Docs** | `uv run poe docs-serve` | Starts local Zensical documentation server |
| **Build Docs** | `uv run poe docs-build` | Compiles documentation into `site/` |

## Configuration Blueprint

| File | Purpose |
|---|---|
| `pyproject.toml` | Project metadata, dependencies, and `uv_build` backend |
| `poe_tasks.toml` | Task runner configuration with `uv` executor |
| `ruff.toml` | Strict Ruff linter and formatter configuration |
| `pyrefly.toml` | Pyrefly strict preset and project path definitions |
| `complexipy.toml` | Cognitive complexity threshold rules (`max = 10`) |
| `zensical.toml` | Zensical documentation layout, themes, and MathJax |
| `rumdl.toml` | Rigid markdown rules and embedded code block checkers |
| `tach.toml` | Modular architecture layer hierarchy |
| `.coveragerc` | Coverage thresholds (80%+ target) and exclusions |
| `pytest.ini` | Test paths and verbose output options |

## License

{% if cookiecutter.license != "None" -%}
Distributed under the {{ cookiecutter.license }} License. See [LICENSE](LICENSE) for details.
{%- else -%}
All rights reserved.
{%- endif %}
