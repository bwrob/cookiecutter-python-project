---
description: Authoritative guide for pytest testing stack (xdist, syrupy, hypothesis).
name: tool-pytest
version: 1.0.0
---

# pytest Testing Stack Skill

Zenith equips `pytest` with a modern, high-speed testing toolchain:

- **Parallel Execution**: `pytest-xdist` (`-n auto`) for multi-core speed.
- **Flakiness Detection**: `pytest-randomly` for randomized execution order.
- **Snapshot Testing**: `syrupy` for clean, declarative snapshot assertions.
- **Property-Based Testing**: `hypothesis` for generative edge-case discovery.
- **Branch Coverage**: `pytest-cov` enforcing an 80%+ coverage threshold.

---

## 1. Core CLI Commands

Execute tests across the suite, single files, or in parallel.

```bash
uv run pytest                         # Run all tests with coverage
uv run pytest -n auto                 # Run tests in parallel across cores
uv run pytest path/to/test_file.py    # Run a specific test file
uv run pytest -k "test_greeting"      # Run tests matching expression
uv run pytest -m "not slow"           # Run tests excluding markers
uv run pytest --snapshot-update       # Update syrupy snapshot files (.ambr)
uv run pytest --cov --cov-report=html # Generate HTML coverage in htmlcov/
```

In Zenith, task aliases are managed via Poe:

```bash
uv run poe test                       # Run tests with coverage and doctests
uv run poe test-fast                  # Run tests in parallel with xdist
uv run poe test-snapshot-update       # Update Syrupy snapshots
uv run poe coverage                   # Generate HTML coverage report
```

---

## 2. Configuration Files

Pytest and coverage behavior are configured through root configuration files.

### `pytest.ini`

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --doctest-modules
    --strict-markers
    -ra
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: external or integration tests
```

### `.coveragerc`

```ini
[run]
source = src
branch = true
omit =
    */tests/*
    */__snapshots__/*

[report]
fail_under = 80
show_missing = true
exclude_lines =
    pragma: no cover
    def __repr__
    if TYPE_CHECKING:
    raise NotImplementedError
    if __name__ == .__main__.:
```

---

## 3. Testing Paradigms in Zenith

Zenith integrates snapshot, property-based, and randomized testing patterns.

### A. Snapshot Testing with `syrupy`

Use snapshot assertions for complex data structures, rendered strings, or
payloads:

```python
def test_greeting_snapshot(snapshot):
    result = get_greeting("Developer")
    assert result == snapshot
```

Snapshots are stored in `tests/__snapshots__/<test_file>.ambr`.
To update snapshots after intentional code changes:

```bash
uv run poe test-snapshot-update
```

### B. Property-Based Testing with `hypothesis`

Use `hypothesis` to test mathematical invariants across hundreds of random
inputs:

```python
from hypothesis import given
from hypothesis import strategies as st


@given(st.text(min_size=1))
def test_greeting_always_contains_name(name: str):
    clean = name.strip()
    result = get_greeting(name)
    if clean:
        assert clean in result
    else:
        assert result == "Hello, World!"
```

### C. Randomized Execution (`pytest-randomly`)

`pytest-randomly` runs tests in a different order on every invocation. If a test
fails only when run after another test, they share state (e.g. global variables,
un-reset caches, or dirty file systems).

To reproduce a specific randomized run:

```bash
uv run pytest --randomly-seed=12345
```

---

## 4. Most Common Configuration Changes During Development

Register markers, tune coverage thresholds, or exclude lines with these
settings.

### A. Registering Custom Test Markers

When adding markers (e.g. `@pytest.mark.integration`), register them in
`pytest.ini` to avoid warnings under `--strict-markers`:

```ini
[pytest]
markers =
    integration: External network or integration tests
    gpu: Hardware-dependent GPU tests
```

### B. Adjusting Coverage Thresholds

To adjust minimum branch coverage requirement in `.coveragerc`:

```ini
[report]
fail_under = 85
```

### C. Ignoring Untestable Lines from Coverage

Add exclusion regex patterns under `exclude_lines` in `.coveragerc`:

```ini
exclude_lines =
    pragma: no cover
    if self\.debug:
    raise AssertionError
```
