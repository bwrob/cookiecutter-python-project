---
description: Authoritative guide for Tach modular architecture and layer boundary tool.
name: tool-tach
version: 1.0.0
---

# Tach Skill

`tach` is an ultra-fast architectural linter and dependency graph visualizer for
Python, written in Rust. It enforces strict modular boundaries, defines public
module interfaces, and guarantees that low-level domain layers never import
from high-level presentation or CLI layers.

In Zenith projects, `tach` enforces clean acyclic layer separation and blocks
circular imports.

---

## 1. Core CLI Commands

Use these commands to validate boundaries, show trees, and generate reports.

```bash
uv run tach check                  # Validate all module boundaries
uv run tach check --strict         # Fail on undeclared imports
uv run tach show                   # Print terminal architecture tree
uv run tach show --mermaid         # Export dependency graph in Mermaid
uv run tach sync                   # Sync tach.toml to existing imports
uv run tach report                 # Generate health report
```

---

## 2. Configuration & Where It Lives

Tach is configured via **`tach.toml`** at the project root:

```toml
# Source roots for Python import resolution
source_roots = ["src"]

# Strict import mode
strict = true

# Layer hierarchy (ordered from top to bottom)
# Higher layers can import from lower layers; lower cannot import upward.
layers = [
    "cli",
    "core",
]

# Module definitions and allowed dependencies
[[modules]]
path = "my_app.cli"
depends_on = ["my_app.core"]
layer = "cli"

[[modules]]
path = "my_app.core"
depends_on = []
layer = "core"
```

---

## 3. Most Common Configuration Changes During Development

Manage architectural layers, module dependencies, and public interfaces with
these patterns.

### A. Adding a New Architectural Layer

To introduce a new layer (such as `domain`, `adapters`, or `storage`):

1. Define the layer in the `layers` array in order of hierarchy:

   ```toml
   layers = [
       "cli",
       "services",
       "core",
   ]
   ```

2. Any module assigned to `cli` can import from `services` and `core`.
3. Modules in `services` can import from `core`, but never from `cli`.
4. Modules in `core` cannot import from `services` or `cli`.

### B. Adding a New Internal Module

When creating a new package or module inside `src/`:

```toml
[[modules]]
path = "my_app.storage"
depends_on = ["my_app.core"]
layer = "core"
```

### C. Declaring Public Interfaces (`[[modules.interfaces]]`)

To prevent external modules from importing private implementation details:

```toml
[[modules]]
path = "my_app.core"
depends_on = []
layer = "core"

[[modules.interfaces]]
expose = ["my_app.core.get_greeting", "my_app.core.GreetingConfig"]
```

Any attempt to import an unexposed symbol from outside `my_app.core` will
trigger a Tach interface violation error.

### D. Exporting Mermaid Architecture Diagrams to Documentation

Zenith defines a built-in task in `poe_tasks.toml` to export the current
dependency graph directly as a Mermaid diagram:

```bash
uv run poe dependency-graph
```

This generates `docs/dependency_graph.mmd`, which can be embedded in docs.

### E. Suppressing False Positives or Temporary Migration Exceptions

When transitioning legacy code or handling dynamic runtime imports:

```python
# tach-ignore
from my_app.cli import format_output
```

Or ignore a specific module path:

```python
from my_app.cli import format_output  # tach-ignore(my_app.cli)
```

---

## 4. Best Practices & Troubleshooting

Keep these architecture rules in mind:

- **Check boundaries with Poe**: Always run `uv run poe dependencies`
  before merging.
- **Top-Down Only**: Imports must flow downwards through layers (`cli` $\to$
  `services` $\to$ `core`). Never allow `core` to import anything from `cli`.
- **Acyclic Enforcement**: Tach mathematically prevents circular dependency
  cycles. If a cycle is detected, extract shared interfaces into a lower-level
  protocol module.
