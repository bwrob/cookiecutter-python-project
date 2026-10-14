<p align="center">
  <img src="assets/opinionated-snake.svg" alt="Zenith Opinionated Snake Emblem" width="180">
</p>

# 🥋 Zenith (cookiecutter-zenith)

[![Template: Cookiecutter](https://img.shields.io/badge/template-cookiecutter-D4B830.svg)](https://github.com/cookiecutter/cookiecutter)
[![Python: 3.12+](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14%20%7C%203.15-blue.svg)](https://www.python.org/)
[![Package Manager: uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Code Style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Type Checked: Pyrefly](https://img.shields.io/badge/types-pyrefly%20strict-blueviolet.svg)](https://github.com/facebook/pyrefly)
[![Documentation: Zensical](https://img.shields.io/badge/docs-zensical-teal.svg)](https://github.com/zensical/zensical)
[![Markdown: rumdl](https://img.shields.io/badge/markdown-rumdl-orange.svg)](https://github.com/rvben/rumdl)
[![Complexity: complexipy](https://img.shields.io/badge/complexity-complexipy-crimson.svg)](https://github.com/rohaquinlop/complexipy)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**Zenith** is a modern, opinionated, and strict Cookiecutter template for high-craftsmanship Python projects.

Distilled from real-world, battle-tested setups in [`debug-dojo`](https://github.com/bwrob/debug-dojo), [`sus-inspector`](https://github.com/bwrob/sus-inspector), and [`bwrob.github.io`](https://github.com/bwrob/bwrob.github.io), Zenith brings together the fastest Rust-powered tools in the Python ecosystem into a cohesive, zero-friction developer experience.

---

## 🎯 Elevator Pitch

> **Tired of spending the first two days of every Python project stitching together
> slow tools, fragmented linters, and brittle config files?**
>
> **Zenith** scaffolds a production-grade, zero-compromise Python project in
> seconds. Built for developers who care about speed and rigor, it gives you
> sub-second workflows, uncompromising type safety, modular architecture
> boundaries, and automated task pipelines out of the box — so you can stop
> configuring and start shipping.

---

## ⚡ The Zenith Philosophy

Modern Python development doesn't need slow package managers, fragmented linting tools, or loose typing. Zenith enforces a disciplined, high-velocity standard:

1. **Lightning Speed**: Powered by **uv** for dependency resolution and standard PEP 517 builds (`uv_build`).
2. **Zero-Tolerance Quality**: **Ruff** in preview mode with comprehensive rules (`select = ["ALL"]`) and automatic docstring formatting.
3. **Uncompromising Static Typing**: Exclusively powered by Meta's **Pyrefly** type checker configured in `strict` preset mode.
4. **Cognitive Complexity Guards**: **complexipy** keeps methods readable, maintainable, and modular (`max-complexity-allowed = 10`).
5. **Modern Static Documentation**: **Zensical** delivers beautiful, fast documentation with dark/light theme toggles, Lucide icons, full **LaTeX math notation** via MathJax, and **markdown-exec** for executable docs.
6. **Strict Markdown Standards**: **rumdl** formats and lints documentation, including embedded Python code blocks via Ruff.
7. **Architectural Boundaries**: **Tach** guarantees modular separation between layers (e.g. `core` vs `cli`) and forbids circular dependencies.
8. **Enforced Test Coverage**: **pytest** paired with **pytest-cov** and `.coveragerc` guarantees that running tests measures and enforces coverage thresholds.
9. **Unified Task Automation**: Every workflow (lint, fix, test, type-check, docs, publish) is codified via **Poe the Poet** with uv executor support.

---

## 🚀 How to Use

### 1. Generate Your New Project

Generate your project directly from GitHub using `uvx`:

```bash
uvx cookiecutter https://github.com/bwrob/cookiecutter-python-project.git
```

Or using an existing local `cookiecutter` installation:

```bash
cookiecutter gh:bwrob/cookiecutter-python-project
```

### 2. Answer the Interactive Prompts

```text
project_name [My Python Project]: Quantum Inspector
project_slug [quantum-inspector]:
package_name [quantum_inspector]:
description [An opinionated Python project powered by uv, ruff, pyrefly, and zensical.]: High precision object inspector.
author_name [Bartosz Marcin Wróblewski]:
author_email [bartosz.marcin.wroblewski@gmail.com]:
github_username [bwrob]:
version [0.1.0]:
Select python_version:
1 - 3.13
2 - 3.12
3 - 3.14
4 - 3.15
Choose from [1, 2, 3, 4] [1]: 1
Select license:
1 - MIT
2 - Apache-2.0
3 - BSD-3-Clause
4 - None
Choose from [1, 2, 3, 4] [1]: 1
Select include_cli:
1 - yes
2 - no
Choose from [1, 2] [1]: 1
Select include_github_actions:
1 - yes
2 - no
Choose from [1, 2] [1]: 1
```

### 3. Initialize & Verify

Step into your new project, sync the virtual environment, and run the verification suite:

```bash
# 1. Enter the project
cd quantum-inspector

# 2. Sync all dev dependencies using uv
uv sync --group dev

# 3. Run unit tests with pytest-cov
uv run poe test

# 4. Run the complete quality suite (Ruff, Pyrefly, complexipy, Tach, rumdl)
uv run poe code-quality

# 5. Launch the live documentation server with LaTeX support
uv run poe docs-serve
```

---

## 📋 Template Variables

| Variable | Default | Purpose |
|---|---|---|
| `project_name` | `My Python Project` | Human-friendly name displayed in docs and READMEs |
| `project_slug` | *derived from name* | Distribution slug used for PyPI and repository URLs |
| `package_name` | *derived from slug* | Python package import name (`import <package_name>`) |
| `description` | *modern description* | One-line summary of project |
| `author_name` | `Bartosz Marcin Wróblewski` | Primary author or organization name |
| `author_email` | `bartosz.marcin.wroblewski@gmail.com` | Author email for packaging metadata |
| `github_username`| `bwrob` | GitHub handle used for repository and Pages URLs |
| `version` | `0.1.0` | Initial release version |
| `python_version` | `3.13` | Minimum Python version (`3.12` - `3.15`) |
| `license` | `MIT` | Chosen open-source license (`MIT`, `Apache-2.0`, `BSD-3-Clause`, `None`) |
| `include_cli` | `yes` | Scaffold Typer CLI with Rich terminal output (`yes`/`no`) |
| `include_github_actions` | `yes` | Scaffold multi-OS test matrix, docs deploy, & PyPI publishing (`yes`/`no`) |

---

## 🏗️ Generated Project Structure

```text
<project-slug>/
├── .github/
│   └── workflows/
│       ├── python_tests.yaml      # Multi-platform matrix (Linux, macOS, Windows)
│       ├── docs.yaml              # Zensical docs deployment to GitHub Pages
│       └── publish.yml            # Trusted PyPI / TestPyPI publishing via OIDC
├── docs/
│   ├── index.md                   # Documentation landing page with Mermaid & LaTeX
│   ├── getting-started.md         # Onboarding and development instructions
│   ├── reference.md               # API & CLI reference
│   └── javascripts/
│       └── mathjax.js             # MathJax setup enabling full LaTeX rendering
├── src/
│   └── <package_name>/
│       ├── __init__.py            # Package root, docstring, and version export
│       ├── py.typed               # PEP 561 static typing marker
│       ├── core.py                # Core functions with docstrings and doctests
│       └── cli.py                 # Typer + Rich CLI interface (if enabled)
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Reusable pytest fixtures
│   ├── test_core.py               # Unit tests for core functions
│   └── test_cli.py                # Tests for CLI interface (if enabled)
├── .coveragerc                    # Coverage settings, exclusions, & 80%+ threshold
├── .gitignore                     # Comprehensive ignores for uv, ruff, rumdl, etc.
├── .pre-commit-config.yaml        # Pre-commit hook configurations
├── .python-version                # Pin active Python version
├── .taplo.toml                    # Opinionated TOML formatting
├── complexipy.toml                # Cognitive complexity threshold rules (max = 10)
├── LICENSE                        # Selected project license
├── poe_tasks.toml                 # Declarative task runner workflows
├── pyproject.toml                 # PEP 621 metadata + uv_build build system
├── pyrefly.toml                   # Strict Pyrefly type checking configuration
├── pytest.ini                     # Doctests & verbose pytest settings
├── README.md                      # Detailed project README
├── ruff.toml                      # Strict Ruff preview rules & docstring formatting
├── rumdl.toml                     # Rigid markdown rules + embedded code linting
└── tach.toml                      # Modular architecture layer boundaries
```

---

## 🧮 LaTeX in Zensical Documentation

Zensical includes first-class support for mathematical formulas. Zenith pre-configures MathJax 3 with `pymdownx.arithmatex` so that LaTeX formulas render in the browser:

- **Inline equations**: `$E = mc^2$` or `\(\mathcal{O}(n \log n)\)`
- **Display equations**:

$$
\mathcal{L}(\theta) = \frac{1}{N} \sum_{i=1}^N \ell\left(f(x_i; \theta), y_i\right)
$$

The client-side loader in `docs/javascripts/mathjax.js` ensures that equations re-render upon page navigation without requiring full page reloads.

---

## 🧪 Testing with pytest-cov & Coverage Config

In Zenith, tests and coverage are tightly integrated:

1. **Integrated Test Command**: `uv run poe test` automatically executes `pytest` with coverage collection, generating terminal missing-lines reporting and XML reports.
2. **Dedicated HTML Coverage**: `uv run poe coverage` generates an interactive HTML report in `htmlcov/`.
3. **Dedicated Configuration**: [`.coveragerc`](file:///Users/bwrob/dev/cookiecutter-python-project/{{cookiecutter.project_slug}}/.coveragerc) specifies branch coverage, exclusion regexes (e.g. `pragma: no cover`, `if TYPE_CHECKING:`, `raise NotImplementedError`), and enforces a strict `fail_under = 80` minimum coverage threshold.

---

## 🛠️ Complete Task Reference

The generated project includes these commands out of the box via [Poe the Poet](https://github.com/nat-n/poethepoet):

| Task | Command | Description |
|---|---|---|
| **Quality** | `uv run poe code-quality` | Runs full suite: auto-fix, format, lint, type-check, complexity, tach |
| **Test** | `uv run poe test` | Executes unit tests and doctests with coverage reporting |
| **Coverage** | `uv run poe coverage` | Generates HTML, XML, and terminal coverage reports |
| **Lint** | `uv run poe lint` | Checks Python code against all Ruff rules |
| **Format** | `uv run poe format` | Formats Python code with Ruff |
| **Markdown Lint** | `uv run poe lint-md` | Lints markdown files with rumdl |
| **Markdown Format** | `uv run poe format-md` | Formats markdown and embedded snippets with rumdl |
| **Type Check** | `uv run poe type-check` | Type checks code with Pyrefly in strict preset mode |
| **Complexity** | `uv run poe complexity` | Evaluates cognitive complexity with complexipy |
| **Dependencies** | `uv run poe dependencies` | Enforces architecture layers with Tach |
| **Dependency Graph** | `uv run poe dependency-graph` | Exports Mermaid diagram of architecture layers |
| **Docs Live Preview** | `uv run poe docs-serve` | Starts local Zensical live-reload documentation server |
| **Docs Build** | `uv run poe docs-build` | Builds production-ready documentation into `site/` |
| **Docs Publish** | `uv run poe publish-docs` | Deploys docs to GitHub Pages via protected-branch-safe orphan branch |
| **Publish** | `uv run poe publish` | Runs quality checks, builds wheels with `uv build`, and publishes |

---

## 🧪 Testing the Zenith Template

The Zenith template includes an automated test suite verifying all combinations of flags:

```bash
uv run --with pytest,cookiecutter pytest tests
```

---

## 📄 License

Distributed under the [MIT License](LICENSE).
