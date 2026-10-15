---
description: >
  Manages git branches, conventional commits, and pull requests in Zenith
  projects. Enforces AI disclosure checklists, testing plans, and clean commit
  hygiene. Use when creating branches, preparing commits, staging files, authoring
  commit messages, or creating pull requests.
name: git-workflow
version: 1.0.0
---

# Git Workflow & Pull Request Standards (`git-workflow`)

This workflow skill establishes the git branch management, conventional commit
formatting, and pull request submission standards for Zenith repositories.

---

## 1. Branch Conventions

Maintain clean, dedicated feature branches for non-trivial tasks:

- **Main Branch**: `main` remains protected and always deployable.
- **Feature Branches**: Prefix with purpose:
  - `feat/<short-description>`: New features or capabilities.
  - `fix/<short-description>`: Bug fixes or issue resolutions.
  - `refactor/<short-description>`: Internal code refactoring.
  - `docs/<short-description>`: Documentation additions or updates.
  - `chore/<short-description>`: Dependency updates, CI, or tool configuration.

---

## 2. Conventional Commit Standards

Every commit message must follow the Conventional Commits specification:

```
<type>(<scope>): <short imperative summary>

[optional body explaining problem and solution rationale]

[optional footer, e.g. Closes #123]
```

### Commit Types

- **`feat`**: A new user-facing feature or library capability.
- **`fix`**: A bug fix.
- **`docs`**: Documentation changes only.
- **`refactor`**: Code changes that neither fix bugs nor add features.
- **`test`**: Adding or correcting test cases.
- **`chore`**: Maintenance, build system, or dependency updates.

### Rules for Commit Messages

1. **Imperative Mood**: Use imperative present tense in the subject ("add feature",
   not "added feature" or "adds feature").
2. **Lowercase Subject**: Start summary with a lowercase letter and no trailing period.
3. **Concise Body**: Explain *why* the change was made, not merely *what* code
   lines were modified.

### AI Co-Authorship & Attribution Trailers

When AI coding assistants help generate code or commit diffs, credit them in the commit footer using standard Git `Co-authored-by` trailers:

```git
feat(auth): add token refresh endpoint

Implement automatic token rotation on expiry with sliding window validation.

Co-authored-by: Claude <noreply@anthropic.com>
```

---

## 3. Pre-Commit Verification Gate

Never commit unverified changes. Execute the verification pipeline locally:

```bash
# Verify static analysis, types, and architecture
uv run poe code-quality

# Verify unit tests and coverage
uv run poe test

# Verify all pre-commit hooks pass
uv run pre-commit run --all-files
```

---

## 4. Pull Request Preparation & AI Disclosure

When opening a pull request, adhere to the project's `PULL_REQUEST_TEMPLATE.md`
and `AI_POLICY.md`:

> [!IMPORTANT]
> **Unsupervised agentic contributions are not accepted**. Every contribution must be reviewed,
> understood, and tested by a human contributor who can substantively explain and defend the changes.
> See `AI_POLICY.md` for full requirements.

### Pull Request Structure

1. **Problem & Solution**:
   - Provide a concise description of the underlying problem.
   - Summarize the chosen solution and architectural rationale.
2. **Testing Plan**:
   - Report passed `pytest` results and coverage status.
   - Document any manual testing performed.
3. **AI Assistance Disclosure (Mandatory)**:
   - Identify AI coding assistants utilized (e.g., Antigravity, Claude Code, Cursor).
   - Summarize the scope of assistance (e.g., initial draft, refactoring, test generation).
   - Confirm human review and full accountability for all submitted changes.
   - Confirm that AI assistants are credited in commit messages via `Co-authored-by` trailers.
