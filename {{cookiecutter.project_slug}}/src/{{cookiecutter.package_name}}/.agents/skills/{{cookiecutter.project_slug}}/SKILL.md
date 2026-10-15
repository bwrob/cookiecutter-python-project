---
description: Authoritative usage guidelines, patterns, and conventions for {{ cookiecutter.project_name }}. Use when writing, refactoring, or reviewing code using {{ cookiecutter.project_name }}.
name: {{ cookiecutter.project_slug }}
version: 1.0.0
---

# {{ cookiecutter.project_name }} Developer Guidelines

Authoritative engineering guidelines for working with `{{ cookiecutter.package_name }}`.

## API Conventions

- Import primary public interfaces directly from `{{ cookiecutter.package_name }}`:
  ```python
  from {{ cookiecutter.package_name }} import get_greeting
  ```
- Use strict typing across all function boundaries.
- Adhere to the core architectural patterns defined in `AGENTS.md`.

## Integration with AI Coding Assistants

This library bundles official agent skills directly inside its package distribution.
To discover and synchronize skills from this and other installed dependencies in your project:

```bash
uvx library-skills --all -y
```
