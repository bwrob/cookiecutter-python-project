---
description: >
  Performs an authoritative pre-flight code review against Zenith engineering,
  architecture, and AI policy standards before submitting changes or opening a PR.
  Use when asked to review code, conduct pre-PR audits, check compliance with
  AI_POLICY.md, verify architectural boundaries, or check typing precision.
name: code-review
version: 1.0.0
---

# Pre-Flight Code Review (`code-review`)

This workflow skill defines the comprehensive code review protocol for Zenith
Python repositories. It establishes the mandatory quality gates that all code
changes, whether authored by humans or AI coding assistants, must satisfy prior
to merging.

---

## 1. The 6-Point Review Matrix

Review candidate changes systematically across the following six dimensions:

### 1. AI Governance & Accountability (`AI_POLICY.md`)

- [ ] **Human Understanding**: Does the change reflect clear intent and complete
  comprehension rather than unvetted model generation?
- [ ] **Concise Implementation**: Is the code free of AI slop, redundant docstrings,
  excessive conversational comments, or narrative change logs?
- [ ] **Disclosure Ready**: Are the scope of AI assistance and tools used clearly
  identified for inclusion in the pull request description?

### 2. Architectural Boundaries & Layering (`tach.toml`)

- [ ] **Layer Hierarchy**: Does code respect the unidirectional dependency graph:
  `cli` ➔ `core` ➔ external dependencies?
- [ ] **No Inversion**: Does `core` remain strictly isolated from `cli` and user
  interface logic?
- [ ] **Encapsulation**: Are internal implementation details encapsulated into
  private modules or functions with appropriate visibility?

### 3. Type Precision & Python 3.12+ Standards (`python-style-guide`)

- [ ] **PEP 695 Generics**: Does code use modern `def func[T]()` and `type Alias = ...`
  syntax instead of legacy `TypeVar` or `TypeAlias`?
- [ ] **Standard Collections**: Are collection protocols imported from
  `collections.abc` (`Sequence`, `Mapping`, `Iterable`), never from `typing`?
- [ ] **Immutable Data Models**: Are data entities modeled as frozen, slotted
  dataclasses (`@dataclass(frozen=True, slots=True)`)?
- [ ] **Pyrefly Strict**: Does static type checking pass without suppressions or
  unjustified `type: ignore` comments?

### 4. Cognitive Complexity (`complexipy.toml`)

- [ ] **Cognitive Score**: Does every function maintain a cognitive complexity score
  of 10 or less?
- [ ] **Composability**: Are complex conditional branches, nested loops, or deep
  matching clauses decomposed into small, pure helper functions?

### 5. Testing & Quality Assurance (`pytest.ini`)

- [ ] **Behavioral Coverage**: Are new features and bug fixes accompanied by
  automated pytest test cases?
- [ ] **Snapshot Stability**: Are syrupy snapshot files updated cleanly if outputs
  intentionally changed?
- [ ] **Coverage Threshold**: Does test coverage satisfy project thresholds (80%+
  branch coverage)?

### 6. Packaging & Hermetic Dependencies (`pyproject.toml`)

- [ ] **Declared Dependencies**: Are all third-party imports declared in
  `[project.dependencies]` or appropriate dependency groups?
- [ ] **Wheel Import Verification**: Does the package build and pass pre-flight
  wheel import verification via `uv run poe verify-wheel`?

---

## 2. Review Execution Workflow

When conducting a pre-flight review, run the automated verification suite:

```bash
# 1. Run all static quality gates (linting, types, complexity, architecture)
uv run poe code-quality

# 2. Run automated test suite with coverage
uv run poe test

# 3. Verify wheel packaging in isolated virtual environment
uv run poe verify-wheel

# 4. Verify all git pre-commit hooks pass
uv run pre-commit run --all-files
```

---

## 3. Output Review Template

Format code review feedback using the following structured template:

```markdown
### Pre-Flight Code Review Summary

- **Verdict**: [APPROVE / CHANGES REQUESTED]
- **Verification Gates**:
  - `poe code-quality`: [PASSED / FAILED]
  - `poe test`: [PASSED / FAILED]
  - `poe verify-wheel`: [PASSED / FAILED]

#### Key Findings & Observations
- **Architecture & Boundaries**: [Observations or ✓ Clean]
- **Typing & Style (PEP 695)**: [Observations or ✓ Clean]
- **Test Coverage**: [Observations or ✓ Clean]

#### Required Action Items
1. [Action item with file and line reference]
```
