# AGENTS.md

Operational guidelines, architectural conventions, and workflows for AI coding
assistants working on the **Zenith** template repository.

## Pre-flight Checks

Before editing code or executing tasks, ensure an isolated, clean working environment:

1. Check repository status with `git status`. Do not make edits when uncommitted changes exist without explicit user consent.
2. Confirm remotes and branches before committing or pushing changes. Use git worktrees or dedicated feature branches for non-trivial tasks.
3. Run all commands inside the hermetic project environment using `uv run <command>`. Never use global or system Python environments directly.
4. When creating temporary or scratch files, always place them in the `.temp/` directory. Never pollute the workspace root or tracked directories with temporary files.

## Operational Workflows

- **Environment & Packages**: Always use **`uv`**.
  - Sync environment: `uv sync`
  - Add dependency: `uv add <package>` or `uv add --group dev <package>`
  - Run commands in environment: `uv run <command>`
- **Temporary Files**: When creating temporary files, scratch scripts, or intermediate test outputs, always store them in the `.temp/` directory.
- **Testing**: Run the automated test suite with pytest:

  ```bash
  uv run pytest
  ```

- **Verification Gate**: Before proposing or finalizing changes, always verify your work:
  - `uv run pytest`
  - `uv run ruff check`
  - `uv run ruff format --check`
  - `uv run pre-commit run --all-files`
- **AI Contribution Policy**: Consult and adhere to `AI_POLICY.md` for human review,
  local verification, and tool disclosure guidelines.


## Project Instructions Discovery & Compatibility

- **Dual Discovery**: A `CLAUDE.md` symlink (`ln -s AGENTS.md CLAUDE.md`) is maintained in the repository root. This guarantees compatibility across Claude Code, Antigravity, Cursor, Copilot, and other agent systems.
- **Scope Hierarchy**: When exploring subdirectories, check for nested `AGENTS.md` or `CLAUDE.md` files; localized instructions take precedence within their scope.
- **Tool Guidance**: For tool-specific guidance, consult `.agents/skills/tool-*/SKILL.md`.

## Repository Architecture

- `cookiecutter.json`: Template configuration, prompts (`__prompts__`), and variable definitions.
- `hooks/`: Lifecycle hooks (`pre_gen_project.py`, `post_gen_project.py`).
  - `hooks/post_gen_project.py`: Strips educational comments, cleans conditional files (CLI, `.github`, LICENSE), and establishes `CLAUDE.md -> AGENTS.md` symlinks.
- `templates/`: Shared template partials (e.g. CI workflow components).
- `{{cookiecutter.project_slug}}/`: Root directory of the rendered project template.
- `tests/`: Automated tests validating template rendering, conditional branches, and generated asset structures.
