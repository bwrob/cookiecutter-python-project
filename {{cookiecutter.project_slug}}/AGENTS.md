# AGENTS.md

Operational guidelines, architectural conventions, and workflows for AI coding
assistants working in **{{ cookiecutter.project_name }}**.

## Pre-flight Checks

Before editing code or running tasks, ensure a clean, isolated environment:

1. Check repository status with `git status`. Do not make edits when uncommitted changes exist without explicit user consent.
2. Confirm remotes and branches before committing or pushing changes. Use git worktrees or dedicated feature branches for non-trivial tasks.
3. Run all commands inside the hermetic project environment using `uv run <command>` or `uv run poe <task>`. Never use global or system Python environments directly.

## Operational Workflows

- **Environment & Packages**: Always use **`uv`**. Never use `pip`, `poetry`, or
  virtualenv directly.
  - Sync environment: `uv sync`
  - Add dependency: `uv add <package>` or `uv add --group <group> <package>`
  - Run commands in environment: `uv run <command>`
- **Task Runner**: All development tasks are managed through **Poe the Poet**.
  Do not guess command flags or invoke linters directly. Run:

  ```bash
  uv run poe --help
  ```

- **Verification Gate**: Before proposing or finalizing changes, always verify
  your work using:
  - `uv run poe test` (or `uv run poe test-fast`)
  - `uv run poe code-quality`
  - `uv run poe fix` (to auto-fix formatting and spelling where applicable)
  - `uv run poe clean` (to purge build artifacts and stale caches)
- **Tool Guidance**: For tool usage and common configuration changes,
  consult the corresponding skill in `.agents/skills/tool-*/SKILL.md`.
- **AI Contribution Policy**: All contributions must adhere to `AI_POLICY.md`
  for human review, local test verification, and tool disclosure.

## Project Instructions Discovery & Compatibility

- **Dual Discovery**: A `CLAUDE.md` symlink (`ln -s AGENTS.md CLAUDE.md`) is maintained in the repository root. This guarantees compatibility across Claude Code, Antigravity, Cursor, Copilot, and other agent systems.
- **Scope Hierarchy**: When exploring subdirectories, check for nested `AGENTS.md` or `CLAUDE.md` files; localized instructions take precedence within their scope.

## Architecture & Code Design

Refer to `.agents/skills/python-style-guide/SKILL.md` for complete guidelines.

- **Python Version**: Python {{ cookiecutter.python_version }}+.
- **Imports**: Use canonical absolute imports exclusively (`from {{ cookiecutter.package_name }}.module import ...`). Relative imports are strictly banned via Ruff (`ban-relative-imports = "all"`).
- **Type Annotations**: Use modern PEP 695 type parameter syntax exclusively
  (`type Alias = ...`, `def func[T](...)`). Never use legacy `TypeVar` or
  `Optional`. Import collection abstractions from `collections.abc`.
- **Data Modeling**: Model data with immutable slotted dataclasses
  (`@dataclass(frozen=True, slots=True)`).
- **Subtyping & Contracts**: Use structural subtyping with `typing.Protocol`
  rather than inheritance. Favor composition and callable handlers over class
  hierarchies.
- **Functional Style**: Write pure, composable, idempotent functions with
  explicit inputs and outputs. Avoid in-place mutation.
- **CLI Framework**: Use **Typer** exclusively for any command-line interfaces
  or CLI tools. Never use `argparse`, `click`, or manual `sys.argv` parsing.
  Always declare CLI parameters using PEP 593 `typing.Annotated` and explicit
  `typer.Typer()` applications (consult `.agents/skills/tool-typer/SKILL.md`).
{% if cookiecutter.include_cli in [True, "yes", "true", "True", "1"] %}
- **Layer Boundaries**: The application follows strict layer boundaries:
  `cli` -> `core` -> external dependencies. The `core` module must never import
  from `cli`.
{% else %}
- **Layer Boundaries**: The application follows strict layer boundaries:
  `core` -> external dependencies.
{% endif %}

## Testing & Documentation

- **Testing**: Write unit tests with `pytest`. Use `hypothesis` for property-based
  exploration and `syrupy` for snapshot assertions. `pytest.ini` enforces zero-tolerance
  warning gates (`filterwarnings = error`), import isolation (`--import-mode=importlib`),
  and strict marker validation (`--strict-markers`).
- **Documentation**: Site is built with Zensical. API references are generated
  automatically from docstrings with `mkdocstrings`. Build-time link and reference
  validation is strictly enforced via `[project.validation]`.
- **Diagrams**: Use Mermaid code blocks (```mermaid) for architecture and sequence
  diagrams.

## Investigating CI Failures

When diagnosing GitHub Actions failures:

1. Enumerate recent runs: `gh run list --limit 5`
2. Inspect failing step logs directly: `gh run view <run-id> --log-failed`
3. Avoid downloading full job logs when annotations and failed step summaries are sufficient.

