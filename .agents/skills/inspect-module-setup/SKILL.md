---
description: >
  Authoritative workflow for inspecting, auditing, and benchmarking mature
  Python project setups to extract best practices and propose improvements.
name: inspect-module-setup
version: 1.0.0
---

# Inspect Module Setup (`inspect-module-setup`)

This skill defines the structured workflow for auditing, benchmarking, and
reverse-engineering the architecture, configuration, toolchains, and CI/CD
practices of mature Python projects.

Use this skill whenever benchmarking Zenith against best-in-class repositories,
evaluating modern tooling shifts in the Python ecosystem, or preparing
actionable improvement proposals.

---

## 1. The 8-Pillar Audit Framework

Inspect target projects across eight foundational dimensions of modern Python
engineering.

### Pillar 1: Packaging & Build System

Examine how the package defines metadata, builds artifacts, and exposes APIs:

- **Build Backend**: Identify the PEP 517/518 backend (`uv_build`, `hatchling`,
  `flit-core`, `maturin`, `poetry-core`, or `setuptools`).
- **Metadata Standard**: Check for PEP 621 compliance (`[project]` table in
  `pyproject.toml`), dynamic versioning (`hatch-vcs`), and classifiers.
- **Layout**: Check for `src/` layout vs flat layout, PEP 561 typing marker
  (`py.typed`), namespace packages, and internal encapsulation (`_internal/`).
- **Entry Points**: Inspect console script entry points (`[project.scripts]`)
  and plugin entry points (`[project.entry-points]`).

### Pillar 2: Dependency & Environment Management

Analyze dependency classification, pin strategies, and locking mechanics:

- **Dependency Separation**: Check separation between core runtime dependencies
  (`dependencies`), optional extras (`[project.optional-dependencies]`), and
  development groups (PEP 735 `[dependency-groups]`).
- **Tooling & Locks**: Inspect environment management tools (`uv`, `poetry`,
  `pdm`) and lockfiles (`uv.lock`). Verify if locks are committed.
- **Pinning Strategy**: Check whether libraries use open lower bounds
  (`package>=1.0.0`) or restrictive upper bounds (`package>=1.0.0,<2.0.0`).

### Pillar 3: Linting, Formatting, & Static Analysis

Evaluate static verification engines, rule selections, and enforcement gates:

- **Linter & Formatter**: Inspect Ruff configuration (`ruff.toml` or
  `[tool.ruff]`), enabled rule prefixes, and per-file ignores.
- **Type Checking**: Identify the type checker (`pyrefly`, `mypy`, `pyright`),
  strictness preset, custom plugins, and stub packages.
- **Cognitive Complexity**: Check for complexity gates (`complexipy`,
  `flake8-cognitive-complexity`, or Ruff `C901`).
- **Architecture Boundaries**: Check for modular boundary checkers (`tach`,
  `import-linter`).
- **Linters for Non-Code Assets**: Check spell-checkers (`typos`), markdown
  linters (`rumdl`, `markdownlint`), and config validators.
- **Git Hooks**: Inspect `.pre-commit-config.yaml` or fast native runners
  (`prek`).

### Pillar 4: Task Runner & Developer Workflows

Review developer automation, command discoverability, and local ergonomics:

- **Task Runner**: Identify the task orchestrator (`poethepoet`, `just`, `nox`,
  `tox`, `make`).
- **Standard Tasks**: Look for consistent task naming (`lint`, `format`,
  `type-check`, `test`, `test-fast`, `coverage`, `fix`, `code-quality`).
- **Execution Engine**: Verify whether commands execute inside hermetic virtual
  environments (e.g. `uv run`).

### Pillar 5: Testing Architecture & Quality Assurance

Inspect test framework integration, plugins, and coverage requirements:

- **Framework & Plugins**: Review `pytest` configuration, test discovery
  patterns, and plugins (`pytest-cov`, `pytest-xdist`, `pytest-randomly`,
  `syrupy`, `hypothesis`).
- **Test Organization**: Examine directory layout (`tests/unit/`,
  `tests/integration/`, `tests/fixtures/`, `conftest.py`).
- **Coverage Configuration**: Inspect branch coverage settings, coverage
  fail-under thresholds, and exclusion patterns (`.coveragerc` or
  `pyproject.toml`).
- **Property & Snapshot Testing**: Identify use of property-based testing
  (`hypothesis`) and snapshot assertions (`syrupy`).

### Pillar 6: Documentation & Specification Engineering

Analyze technical documentation generation and asset pipelines:

- **Static Doc Generator**: Identify the engine (`zensical`, `mkdocs-material`,
  `sphinx`). Both `zensical` and `mkdocs` (especially `mkdocs-material`) are
  first-class targets to learn from. Note that `zensical` is compatible with
  `mkdocstrings` plugins (`mkdocstrings[python]`, Griffe, docstring options,
  and signature cross-references), allowing patterns from mature `mkdocs.yml`
  setups to be directly adapted into `zensical.toml`.
- **API Reference Generator**: Inspect docstring parsing tools (`mkdocstrings`,
  `griffe`), docstring style (Google, NumPy), and inventory cross-references
  (`objects.inv`).
- **Executable Snippets & Doc Validation**: Check for code-block execution
  tools (`markdown-exec`) or test runner validation (`pytest-examples`).
- **Vector Assets & Diagrams**: Check for diagram tools (Mermaid, Typst vector
  layouts for logos and figures).

### Pillar 7: CI/CD & Supply Chain Security

Examine automation pipelines, matrix tests, and publication security:

- **Matrix CI**: Check GitHub Actions workflows for Python versions (3.12, 3.13,
  3.14, 3.15, free-threading), operating systems (Ubuntu, macOS, Windows).
- **Fast Caching**: Review caching mechanisms (Astral `setup-uv`, cache keys).
- **Publication Security**: Verify PyPI Trusted Publishing (OIDC tokens),
  PEP 740 digital attestations, and provenance generation.
- **Automation**: Check automated release tools (`release-please`,
  `semantic-release`, `changesets`).

### Pillar 8: Governance, Security, & Open Source Health

Review project health, contributor onboarding, and community policies:

- **Issue & PR Templates**: Inspect `.github/ISSUE_TEMPLATE/` and
  `PULL_REQUEST_TEMPLATE.md`.
- **Security & Contributing**: Inspect `SECURITY.md`, `CONTRIBUTING.md`, and
  `CODE_OF_CONDUCT.md`.
- **Dependency Automation**: Inspect Renovate or Dependabot configurations.

---

## 2. Ingestion & Extraction Workflow

Follow this procedure when auditing an external repository or local project.

### Step 1: Shallow Clone or Inspect

Fetch repository files quickly without downloading full git history:

```bash
# Shallow clone target repository into temporary scratch directory
git clone --depth 1 https://github.com/<org>/<repo>.git /tmp/inspect-<repo>
```

### Step 2: Audit Configuration Files

Inspect the core setup files in order:

```bash
cd /tmp/inspect-<repo>

# Packaging, dependencies, and tools
cat pyproject.toml

# Tool-specific configurations
ls -la ruff.toml .ruff.toml pyrefly.toml mypy.ini tach.toml \
  .pre-commit-config.yaml 2>/dev/null

# Documentation configs (Zensical / MkDocs / Sphinx)
ls -la zensical.toml mkdocs.yml mkdocs.yaml docs/ 2>/dev/null

# Task runner definitions
ls -la poe_tasks.toml Justfile Makefile noxfile.py tox.ini 2>/dev/null

# CI/CD pipelines
ls -la .github/workflows/
```

### Step 3: Extract Notable Patterns

Identify non-obvious configurations, clever flags, and patterns worthy of
adoption or adaptation.

---

## 3. Golden Reference Projects

Use these mature, high-leverage Python repositories as benchmarks:

| Project | Repository | Key Benchmark Strengths |
| --- | --- | --- |
| **uv** | `astral-sh/uv` | Modern packaging, workspace layouts, ultra-fast CI |
| **Pydantic** | `pydantic/pydantic` | PEP 695 typing, MkDocs/mkdocstrings, test matrix |
| **HTTPX** | `encode/httpx` | Strict typing, async testing, clean architecture |
| **Textual / Rich** | `Textualize/rich` | Modern CLI design, snapshot testing, packaging |
| **Structlog** | `hynek/structlog` | Modern packaging by Hynek Schlawack, hatchling, docs |
| **FastAPI** | `fastapi/fastapi` | Multi-version testing, docs workflow, API design |

---

## 4. Proposal Synthesis Template

When proposing template improvements based on an audit, structure the output as
follows:

```markdown
# Improvement Proposal: [Area / Feature] (Learned from [Project Name])

## 1. Executive Summary
Brief summary of the discovered pattern and why Zenith benefits from it.

## 2. Benchmark Source & Context
- Target Project: `[org/repo]`
- Discovered Pattern: `[e.g., Trusted Publishing OIDC / PEP 735 groups]`

## 3. Gap Analysis (Target vs. Zenith)
| Capability | Target Repo Pattern | Zenith Current State | Advantage |
| --- | --- | --- | --- |

## 4. Proposed Changes
- Exact configuration diffs or new template files.
- Updates to `cookiecutter.json`, hooks, or `{{cookiecutter.project_slug}}`.

## 5. Verification Plan
- Unit tests (`uv run pytest`).
- End-to-end template generation & smoke tests (`uv run poe code-quality`).
```
