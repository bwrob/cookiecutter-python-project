---
description: Run and manage project tasks with poethepoet (poe) in uv projects.
name: tool-poethepoet
---

# Poethepoet (poe) Task Runner

Poethepoet (`poe`) is a task runner for Python projects. It defines and
documents project commands inside `pyproject.toml` or standalone config files.

## 1. Quick Start and Execution

Run tasks using `uv run poe`. Poe runs each command inside the project
virtual environment automatically.

```bash
uv run poe                       # List all available tasks with descriptions
uv run poe --help                # Show usage help and options
uv run poe <task>                # Execute a specific task
uv run poe <task> -v             # Execute with verbose output
uv run poe -d <task>             # Dry run: print command without executing
uv run poe <task> -- -x          # Pass free arguments directly to underlying tool
```

> [!IMPORTANT]
> Always prefer running poe tasks instead of invoking tools directly.
> Poe tasks inherit project defaults, environment variables, and flags.

## 2. Core Task Types

Poe supports multiple task types defined under `[tool.poe.tasks]`.

### Command Tasks (`cmd`)

Runs a shell binary or executable command:

```toml
[tool.poe.tasks.test]
cmd = "pytest tests/"
help = "Run unit and functional test suite"
```

### Script Tasks (`script`)

Calls a Python function directly from a project module:

```toml
[tool.poe.tasks.generate]
script = "scripts.codegen:main"
help = "Run code generator script"
```

### Shell Tasks (`shell`)

Executes POSIX shell pipelines or multi-command scripts:

```toml
[tool.poe.tasks.clean]
shell = "rm -rf dist/ build/ *.egg-info"
help = "Remove build artifacts and caches"
```

### Sequence Tasks (`sequence`)

Executes multiple subtasks in sequential order:

```toml
[tool.poe.tasks.check]
sequence = ["lint", "type-check", "test"]
help = "Run linting, type-checking, and tests sequentially"
```

### Parallel Tasks (`parallel`)

Executes subtasks concurrently:

```toml
[tool.poe.tasks.all-checks]
parallel = ["lint", "type-check"]
help = "Run independent checks concurrently"
```

## 3. Most Common Configuration Changes During Development

All poe tasks are configured in `pyproject.toml` under `[tool.poe.tasks]`.

### Adding CLI Arguments to a Task

Define named CLI options that users can pass when invoking `uv run poe`:

```toml
[tool.poe.tasks.test]
cmd = "pytest ${markers}"
help = "Run tests with optional markers"
args = [
  { name = "markers", options = ["-m"], default = "", help = "Marker filter" },
]
```

### Forwarding Arguments in Sequence Tasks

Use `$POE_EXTRA_ARGS` to forward CLI flags to subtasks in a sequence:

```toml
[tool.poe.tasks.check]
sequence = ["lint $POE_EXTRA_ARGS", "test $POE_EXTRA_ARGS"]
help = "Run checks and forward extra flags"
```

### Defining Task Dependencies (`deps`)

Ensure prerequisites run before the target task:

```toml
[tool.poe.tasks.build]
cmd = "uv build"
deps = ["check"]
help = "Build packages after running all checks"
```

### Setting Task Environment Variables

Inject environment variables into a task process:

```toml
[tool.poe.tasks.test-ci]
cmd = "pytest"
env = { CI = "1", PYTHONUNBUFFERED = "1" }
help = "Run tests with CI environment variables"
```

### Creating Internal Tasks (`_` Prefix)

Prefix tasks with an underscore `_` to hide them from the task list:

```toml
[tool.poe.tasks._internal_check]
cmd = "ruff check src/"

[tool.poe.tasks.lint]
sequence = ["_internal_check"]
help = "Run public linting suite"
```

## 4. Best Practices and Rules

Keep the following conventions in mind when editing poe tasks:

- **Compose, don't recurse**: Use `sequence`, `parallel`, or `deps` to
  chain tasks. Never shell out using `cmd = "poe other-task"`.
- **Always provide `help`**: Every public task must include a concise
  `help` string for self-documentation.
- **Never hand-edit dependencies**: Use `uv add --dev <package>` rather
  than modifying dependency tables manually.
- **Inspect discovery**: Run `uv run poe --help` to confirm tasks parse
  and documentation displays properly.
