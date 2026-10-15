---
description: Authoritative guide for Meta Pyrefly static type checker in Python 3.12+.
name: pyrefly
version: 1.0.0
---

# Pyrefly Skill

`pyrefly` is Meta's next-generation, high-performance static type checker and
Language Server Protocol (LSP) for Python, written in Rust. It enforces strict
type safety, full generic verification, and zero implicit `Any` types with
exceptional speed.

In Zenith projects, `pyrefly` is configured with the `strict` preset mode to
guarantee complete type coverage across the codebase.

---

## 1. Core CLI Commands

Use these commands to verify static typing across the project or in single
modules.

```bash
uv run pyrefly check                      # Check entire project config
uv run pyrefly check path/to/file.py      # Check a specific file or module
uv run pyrefly check --output-format json # Output machine-readable JSON
uv run pyrefly init                       # Generate pyrefly.toml config
```

---

## 2. Configuration & Where It Lives

Pyrefly is configured through **`pyrefly.toml`** at the project root:

```toml
# Preset modes: "strict", "recommended", or "lenient"
preset = "strict"

# Root paths for project source code
project_roots = ["src", "tests"]

# Extra module search paths (e.g. stubs)
search_path = ["stubs"]

# Untyped library behavior
untyped_def_behavior = "error"
```

---

## 3. Most Common Configuration Changes During Development

Adjust type checking rules and module search paths using these standard
patterns.

### A. Suppressing Type Errors on a Specific Line

When interfacing with untyped C-extensions or external APIs where type
inference cannot be satisfied:

```python
# Suppress a specific error code
result = untyped_library.call()  # pyrefly: ignore[unknown-attribute]

# Suppress multiple errors
data = legacy_payload.parse()  # pyrefly: ignore[bad-arg, missing-attribute]
```

> [!NOTE]
> Always specify the exact error code inside brackets. Never use bare
> ignores.

### B. Configuring Custom Type Stubs

When a third-party dependency does not ship with inline type annotations:

1. Create a `stubs/` directory at the project root.
2. Create the stub file (e.g., `stubs/untyped_pkg/__init__.pyi`).
3. Add `stubs` to `search_path` in `pyrefly.toml`:

   ```toml
   search_path = ["src", "stubs"]
   ```

### C. Adding a New Directory to Type Checking

When adding a new directory such as `scripts/` or `benchmarks/`:

```toml
project_roots = ["src", "tests", "scripts"]
```

### D. Toggling Presets

While Zenith defaults to `strict`, projects during active prototyping can
adjust the preset level:

- **`strict`**: Requires full type coverage, disallows implicit `Any`,
  enforces exhaustive matching and protocol variance.
- **`recommended`**: Balanced enforcement suitable for general applications.
- **`lenient`**: Minimal barrier to entry, warnings only for overt mismatches.

```toml
preset = "recommended"
```

---

## 4. Modern Python 3.12+ Typing Patterns for Pyrefly

Write idiomatically typed code using modern standard library features.

### Native Generics (PEP 695)

Always use Python 3.12+ type parameter syntax instead of legacy `TypeVar`:

```python
# Correct (PEP 695)
type Matrix[T] = list[list[T]]


def first[T](items: list[T]) -> T | None:
    return items[0] if items else None
```

```python
# Legacy syntax to avoid
from typing import Optional, TypeVar

T = TypeVar("T")
```

### Protocol Contracts over Nominal Inheritance

Define interfaces with structural typing:

```python
from typing import Protocol


class Greeter(Protocol):
    def greet(self, name: str) -> str: ...
```

---

## 5. Best Practices & Troubleshooting

Keep the following tips in mind when type checking code:

- **Check frequently with Poe**: Run `uv run poe type-check` before
  committing code.
- **Avoid `typing.Any`**: Use specific union types, generics, or `object`
  with narrowing (`isinstance`).
- **Missing `py.typed`**: If an installed library warns of missing types,
  install its stub package (e.g., `uv add --dev types-requests`).
