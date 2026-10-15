---
description: Authoritative guide for maintaining, testing, and developing Cookiecutter templates.
name: tool-cookiecutter
version: 1.0.0
---

# Cookiecutter Skill

`cookiecutter` is a command-line utility and Python library that scaffolds
projects from file templates using the Jinja templating engine.

In this repository, Cookiecutter defines the core generation pipeline for the
**Zenith** modern Python template.

---

## 1. Repository Layout & Template Architecture

This repository consists of three distinct components:

- **`cookiecutter.json`**: The template interface defining user variables,
  choice prompts, default values, and copy rules.
- **`hooks/`**: Python lifecycle scripts executed before (`pre_gen_project.py`)
  and after (`post_gen_project.py`) template rendering.
- **`{{cookiecutter.project_slug}}/`**: The template source root. Both
  directory names and file contents contain Jinja template syntax.

---

## 2. Core CLI & Testing Commands

Use these commands to test template generation and validate rendered projects.

```bash
uv run cookiecutter .                          # Interactive generation test
uv run cookiecutter . --no-input               # Generate with default values
uv run cookiecutter . --no-input -o /tmp/test  # Render into specific output dir
uv run pytest                                  # Run template unit test suite
```

### End-to-End Smoke Test Workflow

Validate that a generated project satisfies all quality gates:

```bash
# 1. Render template to a temporary directory
uv run cookiecutter . --no-input -o /tmp/smoke-test

# 2. Sync dependencies and run full quality and test suite
cd /tmp/smoke-test/zenith-python-project
uv sync
uv run poe code-quality
uv run poe test
uv run poe docs-build
```

---

## 3. Most Common Configuration Changes During Development

Follow these patterns when modifying template variables, files, or logic.

### A. Adding a New Variable to `cookiecutter.json`

1. Declare the key, default value, or list of choices in `cookiecutter.json`:

   ```json
   {
     "database_backend": ["sqlite", "postgresql", "none"]
   }
   ```

2. Reference the variable in Jinja templates:

   ```jinja
   {% if cookiecutter.database_backend == "postgresql" %}
   psycopg = ">=3.2.0"
   {% endif %}
   ```

3. Update tests in `tests/test_template.py` to assert correct rendering across
   all options.

### B. Adding Conditional Files & Cleanup in Hooks

When a file should only exist if a user selects an optional feature:

1. Create the template file inside `{{cookiecutter.project_slug}}/`.
2. Add removal logic to `hooks/post_gen_project.py`:

   ```python
   def main() -> None:
       include_feature = "{{ cookiecutter.include_feature }}"
       if include_feature.lower() != "yes":
           remove_file("src", package_name, "feature.py")
           remove_file("tests", "test_feature.py")
   ```

### C. Escaping Jinja Syntax in Template Files

When template files must contain literal `{{ ... }}` or `{% ... %}` (such as
GitHub Actions workflows or docs):

```jinja
{% raw %}
steps:
  - name: Echo SHA
    run: echo "Commit: ${{ github.sha }}"
{% endraw %}
```

### D. Preventing Jinja Rendering on Binary Assets (`_copy_without_render`)

Static assets like images, fonts, or SVGs must not be processed as text.
Register glob patterns in `_copy_without_render` inside `cookiecutter.json`:

```json
{
  "_copy_without_render": [
    "docs/assets/*",
    "*.svg",
    "*.png",
    "*.ico"
  ]
}
```

---

## 4. Best Practices & Pitfalls

Keep these principles in mind when developing the template:

- **Edit template, never rendered output**: Always make changes inside
  `{{cookiecutter.project_slug}}/`, not in a temporary test directory.
- **Test all permutations**: When adding boolean or choice toggles, add test
  cases verifying both enabled and disabled states.
- **Maintain formatting resilience**: Template expressions like
  `{{ cookiecutter.project_slug }}` vary in character length. Break or
  parenthesize lines in Python template code so `ruff format` does not fail on
  longer project names.
- **Config header stripping**: Zenith includes educational comments in config
  files that `hooks/post_gen_project.py` strips out. Keep
  `CONFIG_FILES_WITH_HEADERS` in sync when adding new root configs.
