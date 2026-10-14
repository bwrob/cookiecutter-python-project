<p align="center">
  <img src="assets/zenith-star.svg" alt="Zenith Emblem" width="160">
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

An opinionated Cookiecutter template for modern Python 3.12+ projects, configured
with `uv`, `ruff`, `pyrefly`, `complexipy`, `tach`, `rumdl`, and `zensical`.

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

## Usage

Generate a new project with `uvx`:

```bash
uvx cookiecutter https://github.com/bwrob/cookiecutter-python-project.git
```

Or using a local `cookiecutter` install:

```bash
cookiecutter gh:bwrob/cookiecutter-python-project
```

### Initializing the Project

```bash
cd <project-slug>
uv sync --group dev
uv run poe test
uv run poe code-quality
uv run poe docs-serve
```

---

## Tooling

| Tool | Role | Configuration |
|---|---|---|
| [uv](https://github.com/astral-sh/uv) | Package manager & builds | Standard PEP 517 via `uv_build`, `dev` dependency group |
| [ruff](https://github.com/astral-sh/ruff) | Linter & formatter | Preview rules enabled (`select = ["ALL"]`), docstring format |
| [pyrefly](https://github.com/facebook/pyrefly) | Static type checker | Strict preset mode (`preset = "strict"`) |
| [complexipy](https://github.com/rohaquinlop/complexipy) | Complexity guard | Max cognitive complexity per function <= 10 |
| [tach](https://github.com/gauge-sh/tach) | Modular boundaries | Enforces module layering, blocks circular dependencies |
| [zensical](https://github.com/zensical/zensical) | Documentation | TOML-based static docs with MathJax LaTeX and `markdown-exec` |
| [rumdl](https://github.com/rvben/rumdl) | Markdown linter | Strict GFM markdown rules + embedded Python code linting |
| [pytest](https://pytest.org) | Test runner & coverage | Branch coverage with `.coveragerc` enforcing 80% threshold |
| [poethepoet](https://github.com/nat-n/poethepoet) | Task automation | Declarative tasks executed with `uv` (`poe_tasks.toml`) |

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
| `version` | `0.1.0` | Initial release version |
| `python_version` | `3.13` | Target Python version (`3.12`, `3.13`, `3.14`, `3.15`) |
| `license` | `MIT` | Chosen license (`MIT`, `Apache-2.0`, `BSD-3-Clause`, `None`) |
| `include_cli` | `yes` | Scaffolds Typer CLI with Rich output (`yes`/`no`) |
| `include_github_actions` | `yes` | Test matrix, Pages deploy, & PyPI publish workflows |

---

## Tasks

Run tasks via `uv run poe <task>`:

| Task | Command | What it does |
|---|---|---|
| `test` | `pytest --cov --cov-report=term-missing --cov-report=xml` | Runs tests with coverage |
| `coverage` | `pytest --cov --cov-report=html` | Generates HTML report in `htmlcov/` |
| `lint` | `ruff check --config ruff.toml` | Lints Python source code |
| `format` | `ruff format` | Formats Python code |
| `lint-md` | `rumdl check` | Lints markdown documentation |
| `format-md` | `rumdl fmt` | Formats markdown and code snippets |
| `type-check` | `pyrefly check` | Performs strict type analysis |
| `complexity` | `complexipy src tests` | Checks cognitive complexity |
| `dependencies` | `tach check` | Validates architecture boundaries |
| `dependency-graph` | `tach show --mermaid -o docs/dependency_graph.mmd` | Generates Mermaid diagram |
| `fix` | `ruff check --fix && ruff format && rumdl fmt` | Auto-fixes lint and format issues |
| `code-quality` | Runs `fix`, `lint`, `lint-md`, `type-check`, `complexity`, `dependencies` | Full quality check sequence |
| `docs-serve` | `zensical serve` | Starts local documentation server |
| `docs-build` | `zensical build` | Builds static site into `site/` |
| `publish-docs` | Deploys docs to GitHub Pages | Deploys docs to `gh-pages` branch |
| `publish` | Runs checks, builds with `uv build`, publishes with `uv publish` | Release package to PyPI |

---

## Testing the Template

Run the automated Cookiecutter test suite:

```bash
uv run --with pytest,cookiecutter pytest tests
```

---

## License

Distributed under the [MIT License](LICENSE).
