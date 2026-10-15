# AGENTS.md

Operational guidelines, architectural conventions, and workflows for AI coding
assistants working in **{{ cookiecutter.project_name }}**.

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

## Architecture & Code Design

Refer to `.agents/skills/python-style-guide/SKILL.md` for complete guidelines.

- **Python Version**: Python {{ cookiecutter.python_version }}+.
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
{% if cookiecutter.include_cli == "yes" -%}
- **Layer Boundaries**: The application follows strict layer boundaries:
  `cli` -> `core` -> external dependencies. The `core` module must never import
  from `cli`.
{%- else -%}
- **Layer Boundaries**: The application follows strict layer boundaries:
  `core` -> external dependencies.
{%- endif %}

## Testing & Documentation

- **Testing**: Write unit tests with `pytest`. Use `hypothesis` for property-based
  exploration and `syrupy` for snapshot assertions.
- **Documentation**: Site is built with Zensical. API references are generated
  automatically from docstrings with `mkdocstrings`.
- **Diagrams**: Use Mermaid code blocks (```mermaid) for architecture and sequence
  diagrams.
