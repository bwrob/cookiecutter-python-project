"""Automated 9-Pillar Repository Auditor and Maturity Scorecard Engine."""

import argparse
import subprocess
import sys
import tomllib
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path

from harvest_skills import format_harvest_markdown, harvest_repo


@dataclass(frozen=True)
class PillarAudit:
    """Evaluation result for an individual pillar."""

    name: str
    number: int
    level: int  # 1 to 4
    strengths: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class AuditReport:
    """Complete 9-pillar audit scorecard and report."""

    target_name: str
    target_path: Path
    pillars: list[PillarAudit]
    total_score: int
    max_score: int = 36

    @property
    def percentage(self) -> float:
        return (self.total_score / self.max_score) * 100


def load_toml(path: Path) -> dict[str, object]:
    """Safely parse a TOML file if it exists."""
    if not path.is_file():
        return {}
    try:
        return tomllib.loads(path.read_text(encoding="utf-8", errors="ignore"))
    except (OSError, tomllib.TOMLDecodeError):
        return {}


def audit_pillar_1_packaging(root: Path, pyproject: dict[str, object]) -> PillarAudit:
    """Pillar 1: Packaging & Build System."""
    strengths: list[str] = []
    gaps: list[str] = []
    level = 1

    build_system = pyproject.get("build-system")
    backend = ""
    if isinstance(build_system, dict):
        backend = str(build_system.get("build-backend", ""))

    has_src = (root / "src").is_dir()
    has_pytyped = bool(list(root.glob("**/py.typed")))
    project = pyproject.get("project")

    if backend:
        strengths.append(f"PEP 517 build backend: `{backend}`")
        if "uv_build" in backend:
            level = 4
        elif any(
            b in backend for b in ("hatchling", "flit_core", "maturin", "poetry.core")
        ):
            level = 3
        else:
            level = 2
    else:
        gaps.append("No declarative PEP 517 build backend found in pyproject.toml")

    if isinstance(project, dict):
        strengths.append("PEP 621 `[project]` metadata table standard")
        if project.get("scripts"):
            strengths.append("Exposes console entry points (`[project.scripts]`)")
    else:
        gaps.append("Missing PEP 621 `[project]` table")

    if has_src:
        strengths.append("Strict `src/` layout prevents accidental import collisions")
    else:
        gaps.append("Flat package layout instead of recommended `src/` layout")

    if has_pytyped:
        strengths.append("PEP 561 `py.typed` marker present for static consumers")
    else:
        gaps.append("No PEP 561 `py.typed` marker found")

    return PillarAudit(
        name="Packaging & Build System",
        number=1,
        level=level,
        strengths=strengths,
        gaps=gaps,
    )


def audit_pillar_2_dependencies(
    root: Path, pyproject: dict[str, object]
) -> PillarAudit:
    """Pillar 2: Dependency & Environment Management."""
    strengths: list[str] = []
    gaps: list[str] = []
    level = 1

    has_uv_lock = (root / "uv.lock").exists()
    has_poetry_lock = (root / "poetry.lock").exists()
    has_pdm_lock = (root / "pdm.lock").exists()

    if has_uv_lock:
        level = 4
        strengths.append(
            "Committed `uv.lock` for lightning-fast reproducible environments"
        )
    elif has_poetry_lock or has_pdm_lock:
        level = 3
        strengths.append("Committed lockfile present (Poetry / PDM)")
    else:
        gaps.append("No committed lockfile found (`uv.lock`)")

    dep_groups = pyproject.get("dependency-groups")
    if isinstance(dep_groups, dict):
        strengths.append(
            "PEP 735 `[dependency-groups]` used for modular dev/test/lint dependencies"
        )
        level = max(level, 4)
    else:
        gaps.append(
            "Lacks PEP 735 `[dependency-groups]`; uses legacy dev extras or unstructured dependencies"
        )

    tool_uv = pyproject.get("tool", {})
    if isinstance(tool_uv, dict) and "uv" in tool_uv:
        strengths.append("Configured `[tool.uv]` settings and default groups")

    return PillarAudit(
        name="Dependency & Environment Management",
        number=2,
        level=level,
        strengths=strengths,
        gaps=gaps,
    )


def audit_pillar_3_static_analysis(
    root: Path, pyproject: dict[str, object]
) -> PillarAudit:
    """Pillar 3: Linting, Formatting, & Static Analysis."""
    strengths: list[str] = []
    gaps: list[str] = []
    score = 0

    has_ruff = (root / "ruff.toml").exists() or (root / ".ruff.toml").exists()
    tool = pyproject.get("tool", {}) if isinstance(pyproject.get("tool"), dict) else {}
    if not has_ruff and "ruff" in tool:
        has_ruff = True

    if has_ruff:
        score += 2
        strengths.append("Ruff configured for high-performance linting and formatting")
    else:
        gaps.append("Ruff not configured")

    type_checkers: list[str] = []
    for tc, cfg in [
        ("pyrefly", "pyrefly.toml"),
        ("mypy", "mypy.ini"),
        ("pyright", "pyrightconfig.json"),
    ]:
        if (root / cfg).exists() or tc in tool:
            type_checkers.append(tc)

    if type_checkers:
        score += 1
        strengths.append(
            f"Static type checking: {', '.join(f'`{t}`' for t in type_checkers)}"
        )
    else:
        gaps.append("No dedicated static type checker configuration detected")

    if (root / "tach.toml").exists() or "tach" in tool:
        score += 1
        strengths.append("Tach modular architecture boundary enforcement (`tach.toml`)")

    if "complexipy" in tool or bool(list(root.glob("*.complexipy*"))):
        score += 1
        strengths.append("Complexipy cognitive complexity limits configured")

    if (root / ".typos.toml").exists() or (root / "_typos.toml").exists():
        strengths.append("Typos Rust-based source code spell checker")

    if (root / ".rumdl.toml").exists():
        strengths.append("Rumdl Markdown linter and formatter")

    if (root / ".pre-commit-config.yaml").exists():
        strengths.append("Pre-commit git hooks configured")

    level = 4 if score >= 4 else (3 if score >= 2 else (2 if score >= 1 else 1))
    return PillarAudit(
        name="Linting, Formatting, & Static Analysis",
        number=3,
        level=level,
        strengths=strengths,
        gaps=gaps,
    )


def audit_pillar_4_task_runner(root: Path, pyproject: dict[str, object]) -> PillarAudit:
    """Pillar 4: Task Runner & Developer Workflows."""
    strengths: list[str] = []
    gaps: list[str] = []
    level = 1

    tool = pyproject.get("tool", {}) if isinstance(pyproject.get("tool"), dict) else {}
    if (root / "poe_tasks.toml").exists() or "poe" in tool:
        level = 4
        strengths.append("Poe the Poet (`poethepoet`) orchestrates developer workflows")
    elif (root / "Justfile").exists() or (root / "justfile").exists():
        level = 3
        strengths.append("Justfile task orchestrator")
    elif (root / "Makefile").exists() or (root / "makefile").exists():
        level = 2
        strengths.append("Legacy Makefile for task automation")
    elif (root / "noxfile.py").exists() or (root / "tox.ini").exists():
        level = 3
        strengths.append("Matrix testing orchestrator (Nox / Tox)")
    else:
        gaps.append("No unified task runner (e.g. Poe or Just) detected")

    return PillarAudit(
        name="Task Runner & Developer Workflows",
        number=4,
        level=level,
        strengths=strengths,
        gaps=gaps,
    )


def audit_pillar_5_testing(root: Path, pyproject: dict[str, object]) -> PillarAudit:
    """Pillar 5: Testing Architecture & Quality Assurance."""
    strengths: list[str] = []
    gaps: list[str] = []
    level = 1

    test_dirs = [d for d in ("tests", "test", "testing") if (root / d).is_dir()]
    if test_dirs:
        level = 2
        strengths.append(
            f"Dedicated test directory: {', '.join(f'`{d}`' for d in test_dirs)}"
        )
    else:
        gaps.append("No test directory found")

    tool = pyproject.get("tool", {}) if isinstance(pyproject.get("tool"), dict) else {}
    has_pytest = (root / "pytest.ini").exists() or "pytest" in tool
    if has_pytest:
        level = max(level, 3)
        strengths.append("Pytest test framework configuration")

    dep_str = str(pyproject)
    if "hypothesis" in dep_str:
        strengths.append("Hypothesis property-based testing framework")
        level = 4
    if "syrupy" in dep_str:
        strengths.append("Syrupy snapshot testing library")
        level = 4
    if "pytest-cov" in dep_str:
        strengths.append("Coverage tracking with `pytest-cov`")
    if "pytest-xdist" in dep_str:
        strengths.append("Parallel test execution with `pytest-xdist`")

    return PillarAudit(
        name="Testing Architecture & Quality Assurance",
        number=5,
        level=level,
        strengths=strengths,
        gaps=gaps,
    )


def audit_pillar_6_docs(root: Path) -> PillarAudit:
    """Pillar 6: Documentation & Specification Engineering."""
    strengths: list[str] = []
    gaps: list[str] = []
    level = 1

    if (root / "zensical.toml").exists():
        level = 4
        strengths.append("Zensical TOML-native static documentation engine")
    elif (root / "mkdocs.yml").exists() or (root / "mkdocs.yaml").exists():
        level = 3
        strengths.append("MkDocs / MkDocs Material documentation system")
    elif (root / "docs" / "conf.py").exists():
        level = 3
        strengths.append("Sphinx documentation pipeline")
    elif (root / "docs").is_dir():
        level = 2
        strengths.append("Docs directory with Markdown files")
    else:
        gaps.append(
            "No dedicated documentation configuration found (e.g. Zensical or MkDocs)"
        )

    if bool(list(root.glob("**/*.typ"))):
        strengths.append("Typst vector layout engine for docs/logos")

    return PillarAudit(
        name="Documentation & Specification Engineering",
        number=6,
        level=level,
        strengths=strengths,
        gaps=gaps,
    )


def audit_pillar_7_cicd(root: Path) -> PillarAudit:
    """Pillar 7: CI/CD & Supply Chain Security."""
    strengths: list[str] = []
    gaps: list[str] = []
    workflows_dir = root / ".github" / "workflows"
    level = 1

    if not workflows_dir.is_dir():
        gaps.append("No GitHub Actions workflows found")
        return PillarAudit(
            name="CI/CD & Supply Chain Security",
            number=7,
            level=1,
            strengths=strengths,
            gaps=gaps,
        )

    level = 2
    workflows = list(workflows_dir.glob("*.yml")) + list(workflows_dir.glob("*.yaml"))
    strengths.append(f"{len(workflows)} GitHub Actions workflow(s) detected")

    combined_content = ""
    for w in workflows:
        try:
            combined_content += w.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            pass

    if "astral-sh/setup-uv" in combined_content:
        strengths.append("Astral `setup-uv` high-velocity action with caching")
        level = max(level, 3)

    if (
        "id-token: write" in combined_content
        and "pypa/gh-action-pypi-publish" in combined_content
    ):
        strengths.append("PyPI Trusted Publishing via OIDC cryptographic tokens")
        level = 4

    if "attest-build-provenance" in combined_content:
        strengths.append("PEP 740 build provenance attestations")
        level = 4

    if "zizmor" in combined_content or (root / ".zizmor.yml").exists():
        strengths.append("Zizmor GitHub Actions security static analyzer")

    return PillarAudit(
        name="CI/CD & Supply Chain Security",
        number=7,
        level=level,
        strengths=strengths,
        gaps=gaps,
    )


def audit_pillar_8_governance(root: Path) -> PillarAudit:
    """Pillar 8: Governance, Security, & Open Source Health."""
    strengths: list[str] = []
    gaps: list[str] = []
    level = 1

    health_files = {
        "LICENSE": "Open source license file",
        "SECURITY.md": "Security disclosure policy (`SECURITY.md`)",
        "CONTRIBUTING.md": "Contributor guidelines (`CONTRIBUTING.md`)",
        "CODE_OF_CONDUCT.md": "Community code of conduct",
    }
    found_count = 0
    for filename, desc in health_files.items():
        if (root / filename).exists():
            found_count += 1
            strengths.append(desc)
        else:
            gaps.append(f"Missing `{filename}`")

    if (root / ".github" / "PULL_REQUEST_TEMPLATE.md").exists():
        strengths.append("PR template with contributor checklist")
    if (root / ".github" / "ISSUE_TEMPLATE").is_dir():
        strengths.append("Issue template schemas")

    level = (
        4
        if found_count >= 3
        else (3 if found_count >= 2 else (2 if found_count >= 1 else 1))
    )
    return PillarAudit(
        name="Governance, Security, & Open Source Health",
        number=8,
        level=level,
        strengths=strengths,
        gaps=gaps,
    )


def audit_pillar_9_agent_skills(root: Path) -> PillarAudit:
    """Pillar 9: Agent Skills & AI Development Workflows."""
    strengths: list[str] = []
    gaps: list[str] = []
    harvest = harvest_repo(root)
    level = 1

    if harvest.instructions:
        level = 3
        strengths.append(
            f"Agent instructions: {', '.join(f'`{i}`' for i in harvest.instructions)}"
        )
    else:
        gaps.append(
            "No agent instruction files (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`)"
        )

    if harvest.novel_skills or harvest.shared_skills:
        level = 4
        total_skills = len(harvest.novel_skills) + len(harvest.shared_skills)
        strengths.append(
            f"Repository agent skills library ({total_skills} skills found)"
        )
    else:
        gaps.append("No repository agent skills directory (`.agents/skills/`)")

    if harvest.ai_policy_present:
        strengths.append("AI contribution policy present (`AI_POLICY.md`)")
        level = max(level, 4)

    return PillarAudit(
        name="Agent Skills & AI Development Workflows",
        number=9,
        level=level,
        strengths=strengths,
        gaps=gaps,
    )


def run_full_audit(target_path: Path) -> AuditReport:
    """Execute complete 9-pillar audit against a target directory."""
    pyproject = load_toml(target_path / "pyproject.toml")

    pillars = [
        audit_pillar_1_packaging(target_path, pyproject),
        audit_pillar_2_dependencies(target_path, pyproject),
        audit_pillar_3_static_analysis(target_path, pyproject),
        audit_pillar_4_task_runner(target_path, pyproject),
        audit_pillar_5_testing(target_path, pyproject),
        audit_pillar_6_docs(target_path),
        audit_pillar_7_cicd(target_path),
        audit_pillar_8_governance(target_path),
        audit_pillar_9_agent_skills(target_path),
    ]

    total_score = sum(p.level for p in pillars)
    return AuditReport(
        target_name=target_path.name,
        target_path=target_path,
        pillars=pillars,
        total_score=total_score,
    )


def format_audit_markdown(report: AuditReport) -> str:
    """Format audit scorecard and detailed breakdown as markdown."""
    lines: list[str] = [
        f"# 9-Pillar Benchmark Audit: `{report.target_name}`",
        "",
        f"- **Maturity Score**: **{report.total_score} / {report.max_score}** ({report.percentage:.1f}%)",
        f"- **Target Directory**: `{report.target_path}`",
        "",
        "## 1. 9-Pillar Maturity Scorecard & Gap Radar",
        "",
        "| Pillar | Target Level | Zenith Baseline | Discovered Strengths | Gaps vs. Zenith |",
        "| :--- | :---: | :---: | :--- | :--- |",
    ]

    for p in report.pillars:
        s_str = "<br>".join(f"• {s}" for s in p.strengths) if p.strengths else "None"
        g_str = "<br>".join(f"• {g}" for g in p.gaps) if p.gaps else "None"
        lines.append(
            f"| **Pillar {p.number}: {p.name}** | **L{p.level} / 4** | **L4 / 4** | {s_str} | {g_str} |"
        )

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 2. Agent Skills & AI Workflow Breakdown")
    lines.append("")

    harvest_result = harvest_repo(report.target_path)
    lines.append(format_harvest_markdown(harvest_result))

    return "\n".join(lines)


def parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Audit a Python repository across the 9 Zenith Pillars."
    )
    parser.add_argument(
        "target", help="Local directory path or GitHub URL/slug (org/repo)"
    )
    parser.add_argument("--output", "-o", help="Optional output markdown file path")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entrypoint."""
    args = parse_arguments(argv)
    try:
        from harvest_skills import ensure_target_dir

        target_dir = ensure_target_dir(args.target)
        report = run_full_audit(target_dir)
        md = format_audit_markdown(report)

        if args.output:
            out_path = Path(args.output)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(md, encoding="utf-8")
            print(f"Audit report saved to: {out_path}")
        else:
            print(md)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f"Error executing audit: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
