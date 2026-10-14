<p align="center">
  <img src="assets/opinionated-snake.svg" alt="Zenith Emblem" width="180">
</p>

# Zenith

[![Template: Cookiecutter](https://img.shields.io/badge/template-cookiecutter-D4B830.svg)](https://github.com/cookiecutter/cookiecutter)
[![Python: 3.12+](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14%20%7C%203.15-blue.svg)](https://www.python.org/)
[![Package Manager: uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Code Style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Type Checked: Pyrefly](https://img.shields.io/badge/types-pyrefly%20strict-blueviolet.svg)](https://github.com/facebook/pyrefly)
[![Documentation: Zensical](https://img.shields.io/badge/docs-zensical-teal.svg)](https://github.com/zensical/zensical)
[![Markdown: rumdl](https://img.shields.io/badge/markdown-rumdl-orange.svg)](https://github.com/rvben/rumdl)
[![Complexity: complexipy](https://img.shields.io/badge/complexity-complexipy-crimson.svg)](https://github.com/rohaquinlop/complexipy)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

An opinionated Cookiecutter template for Python 3.12+ projects, based on tooling
and configurations used in [debug-dojo](https://github.com/bwrob/debug-dojo),
[sus-inspector](https://github.com/bwrob/sus-inspector), and
[bwrob.github.io](https://github.com/bwrob/bwrob.github.io).

Zenith wires up a modern toolchain (`uv`, `ruff`, `pyrefly`, `complexipy`,
`tach`, `rumdl`, `zensical`) with unified tasks defined in `poe_tasks.toml`.

---

## Elevator Pitch

Starting a new Python project usually means spending hours wiring up linters,
formatters, type checkers, test coverage, and documentation generators — or
copying config files from older repos and fixing whatever broke.

Zenith scaffolds a ready-to-use repository in seconds. You get fast package
management with `uv`, strict typing with Meta's `pyrefly`, linting and
formatting with `ruff`, modular boundary checks with `tach`, complexity limits
with `complexipy`, and documentation with `zensical`. Every check runs through
`poe`, giving you identical workflows locally and in CI.

---

## Toolchain & Defaults

| Concern | Tool | Configuration |
|---|---|---|
| **Package Manager & Build** | [uv](https://github.com/astral-sh/uv) | PEP 517 build via `uv_build`, dependency groups (`dev`) |
| **Linter & Formatter** | [ruff](https://github.com/astral-sh/ruff) | Preview mode enabled, `select = ["ALL"]`, docstring formatting |
| **Static Type Checker** | [pyrefly](https://github.com/facebook/pyrefly) | Strict preset mode (`preset = "strict"`) |
| **Complexity Analysis** | [complexipy](https://github.com/rohaquinlop/complexipy) | Cognitive complexity threshold (`max-complexity-allowed = 10`) |
| **Architecture Boundaries**| [tach](https://github.com/gauge-sh/tach) | Enforces module layers (`cli` -> `core`), blocks circular imports |
| **Documentation** | [zensical](https://github.com/zensical/zensical) | TOML-based static docs with MathJax (LaTeX) and `markdown-exec` |
| **Markdown Linting** | [rumdl](https://github.com/rvben/rumdl) | Strict GFM markdown rules + embedded Python code block linting |
| **Testing & Coverage** | [pytest](https://pytest.org) + [pytest-cov](https://pytest-cov.readthedocs.io) | Branch coverage with `.coveragerc` enforcing `fail_under = 80` |
| **Task Runner** | [poethepoet](https://github.com/nat-n/poethepoet) | Declarative tasks executed directly in `uv` (`poe_tasks.toml`) |

---

## Quickstart

Generate a new project with `uvx`:

```bash
uvx cookiecutter https://github.com/bwrob/cookiecutter-python-project.git
```

Or using a local `cookiecutter` install:

```bash
cookiecutter gh:bwrob/cookiecutter-python-project
```

### Next Steps

```bash
# 1. Enter the generated repository
cd <project-slug>

# 2. Sync virtual environment and dependencies
uv sync --group dev

# 3. Run tests with coverage
uv run poe test

# 4. Run the code quality checks
uv run poe code-quality

# 5. Start the local documentation server
uv run poe docs-serve
```

---

## Template Variables

| Variable | Default | Description |
|---|---|---|
| `project_name` | `Zenith Python Project` | Project title used in docs and README |
| `project_slug` | *derived from name* | Repository and PyPI package name |
| `package_name` | *derived from slug* | Python import name (`import <package_name>`) |
| `description` | *default description* | Package summary string |
| `author_name` | `Bartosz Marcin Wróblewski` | Package author |
| `author_email` | `bartosz.marcin.wroblewski@gmail.com` | Author email |
| `github_username`| `bwrob` | GitHub handle for repo and GitHub Pages URLs |
| `version` | `0.1.0` | Initial version |
| `python_version` | `3.13` | Minimum Python version (`3.12`, `3.13`, `3.14`, `3.15`) |
| `license` | `MIT` | License (`MIT`, `Apache-2.0`, `BSD-3-Clause`, `None`) |
| `include_cli` | `yes` | Scaffolds Typer CLI with Rich output (`yes`/`no`) |
| `include_github_actions` | `yes` | Multi-OS test matrix, docs deploy, & PyPI publish workflows |

---

## Project Structure

```text
<project-slug>/
├── .github/
│   └── workflows/
│       ├── python_tests.yaml      # Multi-platform matrix (Linux, macOS, Windows)
│       ├── docs.yaml              # Zensical docs deployment to GitHub Pages
│       └── publish.yml            # PyPI / TestPyPI publishing via OIDC
├── docs/
│   ├── index.md                   # Documentation home with Mermaid & LaTeX
│   ├── getting-started.md         # Installation and usage walkthrough
│   ├── reference.md               # API & CLI reference
│   └── javascripts/
│       └── mathjax.js             # MathJax 3 configuration for client-side LaTeX
├── src/
│   └── <package_name>/
│       ├── __init__.py            # Exports and PEP 561 marker
│       ├── py.typed               # Marker file for type distribution
│       ├── core.py                # Core functions with doctests
│       └── cli.py                 # CLI interface (if include_cli=yes)
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Pytest fixtures
│   ├── test_core.py               # Unit tests
│   └── test_cli.py                # CLI tests (if include_cli=yes)
├── .coveragerc                    # Branch coverage settings and 80% threshold
├── .gitignore                     # Git ignore rules for uv, Python, caches
├── .pre-commit-config.yaml        # Pre-commit hook configuration
├── .python-version                # Pinned Python version
├── .taplo.toml                    # TOML formatter settings
├── complexipy.toml                # Cognitive complexity config
├── LICENSE                        # Project license
├── poe_tasks.toml                 # Tasks for poethepoet
├── pyproject.toml                 # PEP 621 packaging metadata and dependencies
├── pyrefly.toml                   # Pyrefly strict type-check config
├── pytest.ini                     # Pytest defaults and doctest options
├── README.md                      # Project README
├── ruff.toml                      # Ruff lint and format rules
├── rumdl.toml                     # rumdl markdown linting config
└── tach.toml                      # Architecture boundary rules
```

---

## Documentation Features

Zensical documentation includes:

- **LaTeX math notation**: Rendered via MathJax 3 and `pymdownx.arithmatex`:
  - Inline: `$E = mc^2$`
  - Block:
  $$
  f(x) = \int_{-\infty}^{\infty} \hat{f}(\xi)\,e^{2\pi i \xi x}\,d\xi
  $$
- **Executable code blocks**: `markdown-exec` executes Python and shell snippets at build time using ````python exec="on"`.
- **Mermaid diagrams**: Native flowchart, sequence, and architecture diagrams via `pymdownx.superfences`.

---

## Tasks

Defined in `poe_tasks.toml` and runnable via `uv run poe <task>`:

| Task | Command | What it does |
|---|---|---|
| `test` | `pytest --cov --cov-report=term-missing --cov-report=xml` | Runs tests and prints coverage |
| `coverage` | `pytest --cov --cov-report=html` | Generates HTML coverage report in `htmlcov/` |
| `lint` | `ruff check --config ruff.toml` | Lints Python code |
| `format` | `ruff format` | Formats Python code |
| `lint-md` | `rumdl check` | Lints markdown files |
| `format-md` | `rumdl fmt` | Formats markdown and embedded code snippets |
| `type-check` | `pyrefly check` | Type checks code in strict preset mode |
| `complexity` | `complexipy src tests` | Verifies cognitive complexity <= 10 |
| `dependencies` | `tach check` | Checks layer boundaries |
| `dependency-graph` | `tach show --mermaid -o docs/dependency_graph.mmd` | Generates architecture diagram |
| `fix` | `ruff check --fix --unsafe-fixes && ruff format && rumdl fmt` | Auto-fixes linting and formatting issues |
| `code-quality` | Runs `fix`, `lint`, `lint-md`, `type-check`, `complexity`, `dependencies` | Full quality check sequence |
| `docs-serve` | `zensical serve` | Starts live-reloading docs server |
| `docs-build` | `zensical build` | Builds static site into `site/` |
| `publish-docs` | Deploys docs to GitHub Pages | Deploys docs from `site/` to `gh-pages` |
| `publish` | Runs checks, builds with `uv build`, publishes with `uv publish` | Full release pipeline |

---

## Testing the Template

Run the Cookiecutter test suite:

```bash
uv run --with pytest,cookiecutter pytest tests
```

---

## License

Distributed under the [MIT License](LICENSE).
