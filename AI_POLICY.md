# AI Usage & Contribution Policy

The **Zenith** project welcomes the responsible use of AI coding assistants (such as Claude Code, Antigravity, Cursor, and GitHub Copilot) to augment development. To preserve template reliability, strict tooling standards, and maintainer time, all contributors must adhere to the following principles:

## 1. Human-in-the-Loop & Full Accountability

- **Human Ownership**: All AI-assisted code, template files, and documentation must be thoroughly understood, reviewed, and edited by a human contributor before submission.
- **Full Accountability**: Contributors accept full responsibility for all changes, including template hooks, test coverage, and documentation consistency.

## 2. Verification Gate Before Submitting

- **Mandatory Local Verification**: Before submitting a PR, verify all template tests, linting, formatting, and pre-commit checks locally:
  ```bash
  uv run pytest
  uv run ruff check
  uv run ruff format --check
  uv run pre-commit run --all-files
  ```
- **Hermetic Testing**: Never submit untested template Jinja2 modifications or hook changes. Always verify that both default and edge-case project renderings succeed cleanly.

## 3. No Unattended Bots or PR Floods

- **Automated Agents Restricted**: Unattended bot scripts are strictly forbidden from directly opening pull requests or creating automated issue spam.
- **Targeted Contributions**: AI-assisted PRs must address accepted issues or coordinated feature requests.

## 4. Transparent Disclosure

- **PR Disclosure**: State the AI tools used and the general scope of assistance in the pull request description.
- **Commit Attribution**: When AI coding assistants contribute directly to code generation or commits, credit them in Git commit messages using standard `Co-authored-by` trailers (e.g. `Co-authored-by: Claude <noreply@anthropic.com>`).
- **Protecting Newcomer Issues**: Issues labeled `good first issue` are reserved for human contributors learning the codebase.

## 5. Concise Code & Clean Comments

- **No AI Slop**: Trim excessive, chatty comments, redundant docstrings, or obsolete narrative change logs before submitting.
- **Adhere to AGENTS.md**: Respect architectural boundaries, hermetic `uv` usage, and tool guidance documented in `.agents/skills/`.
