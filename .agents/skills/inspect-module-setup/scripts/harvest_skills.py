"""Agent skill harvester: extracts and benchmarks AI agent capabilities."""

import re
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class DiscoveredSkill:
    """Represents an agent skill found in a repository."""

    name: str
    location: str
    description: str = ""
    is_novel: bool = True


@dataclass(frozen=True)
class HarvestResult:
    """Consolidated harvest analysis of agent skills and instructions."""

    target_name: str
    target_path: Path
    instructions: list[str] = field(default_factory=list)
    novel_skills: list[DiscoveredSkill] = field(default_factory=list)
    shared_skills: list[DiscoveredSkill] = field(default_factory=list)
    ai_policy_present: bool = False
    notes: list[str] = field(default_factory=list)


def extract_skill_metadata(skill_path: Path) -> tuple[str, str]:
    """Extract skill name and description from a SKILL.md or directory."""
    skill_md = skill_path if skill_path.is_file() else (skill_path / "SKILL.md")
    name = skill_path.parent.name if skill_path.is_file() else skill_path.name
    desc = ""

    if skill_md.exists():
        try:
            content = skill_md.read_text(encoding="utf-8", errors="ignore")
            name_match = re.search(r"^name:\s*([^\n]+)", content, re.MULTILINE)
            if name_match:
                name = name_match.group(1).strip().strip("'\"")

            desc_match = re.search(
                r"^description:\s*(?:>|\|)?\s*\n?([^\n]+)", content, re.MULTILINE
            )
            if desc_match:
                desc = desc_match.group(1).strip().strip("'\"")
        except OSError:
            pass

    return name, desc


def resolve_zenith_skills() -> set[str]:
    """Retrieve known Zenith skill names from .agents/skills."""
    zenith_root = Path(__file__).resolve().parent.parent.parent
    if not zenith_root.exists():
        return set()
    return {
        path.name
        for path in zenith_root.iterdir()
        if path.is_dir() and not path.name.startswith(".")
    }


def scan_agent_instructions(root: Path) -> list[str]:
    """Detect instruction files and agent configuration entrypoints."""
    candidates = [
        "AGENTS.md",
        "CLAUDE.md",
        ".cursorrules",
        ".windsurfrules",
        ".github/copilot-instructions.md",
        ".claude/settings.json",
        ".codex/config.toml",
        ".gemini/settings.json",
        ".aider.conf.yml",
    ]
    found: list[str] = []
    for rel_path in candidates:
        if (root / rel_path).exists():
            found.append(rel_path)
    return found


def scan_agent_skills(
    root: Path, known_skills: set[str]
) -> tuple[list[DiscoveredSkill], list[DiscoveredSkill]]:
    """Scan directory trees for agent skills and classify them against Zenith."""
    skill_dirs = [
        root / ".agents" / "skills",
        root / ".agent" / "skills",
        root / ".cursor" / "skills",
        root / ".cursor" / "rules",
        root / ".gemini" / "skills",
    ]

    novel: list[DiscoveredSkill] = []
    shared: list[DiscoveredSkill] = []
    seen_names: set[str] = set()

    for base_dir in skill_dirs:
        if not base_dir.exists() or not base_dir.is_dir():
            continue

        for item in base_dir.iterdir():
            if item.name.startswith("."):
                continue

            name, desc = extract_skill_metadata(item)
            if name in seen_names:
                continue
            seen_names.add(name)

            rel_loc = str(item.relative_to(root))
            is_novel = name not in known_skills
            skill = DiscoveredSkill(
                name=name, location=rel_loc, description=desc, is_novel=is_novel
            )

            if is_novel:
                novel.append(skill)
            else:
                shared.append(skill)

    return novel, shared


def harvest_repo(target_path: Path) -> HarvestResult:
    """Run full agent skill harvest on a target directory."""
    known_zenith_skills = resolve_zenith_skills()
    instructions = scan_agent_instructions(target_path)
    novel_skills, shared_skills = scan_agent_skills(target_path, known_zenith_skills)

    ai_policy_present = (target_path / "AI_POLICY.md").exists()
    notes: list[str] = []

    if (target_path / "CLAUDE.md").is_symlink():
        target = (target_path / "CLAUDE.md").readlink()
        notes.append(f"Symlink CLAUDE.md -> {target}")

    return HarvestResult(
        target_name=target_path.name,
        target_path=target_path,
        instructions=instructions,
        novel_skills=novel_skills,
        shared_skills=shared_skills,
        ai_policy_present=ai_policy_present,
        notes=notes,
    )


def format_harvest_markdown(result: HarvestResult) -> str:
    """Format harvest results into clean GitHub-flavored markdown."""
    lines: list[str] = [
        f"### Agent Skills & AI Workflow Harvest: `{result.target_name}`",
        "",
        f"- **AI Policy**: {'✅ Present (`AI_POLICY.md`)' if result.ai_policy_present else '❌ None detected'}",
        f"- **Agent Instructions**: {', '.join(f'`{i}`' for i in result.instructions) if result.instructions else 'None detected'}",
        "",
    ]

    if result.novel_skills:
        lines.append("#### Novel Skills Discovered (Potential Zenith Additions)")
        lines.append("| Skill Name | Location | Description |")
        lines.append("| :--- | :--- | :--- |")
        for s in result.novel_skills:
            desc = s.description or "No description provided in frontmatter"
            lines.append(f"| **`{s.name}`** | `{s.location}` | {desc} |")
        lines.append("")
    else:
        lines.append("> [!NOTE]")
        lines.append(
            "> No novel agent skills detected beyond Zenith's existing skill library."
        )
        lines.append("")

    if result.shared_skills:
        lines.append("#### Shared / Overlapping Skills")
        for s in result.shared_skills:
            lines.append(f"- `{s.name}` (`{s.location}`)")
        lines.append("")

    if result.notes:
        lines.append("#### Structural Notes")
        for note in result.notes:
            lines.append(f"- {note}")
        lines.append("")

    return "\n".join(lines)


def ensure_target_dir(target_arg: str) -> Path:
    """Resolve target path or clone shallow repo into .temp/ if remote."""
    path = Path(target_arg)
    if path.exists():
        return path

    # Check if target is a GitHub repo slug or URL
    url = target_arg
    if not url.startswith(("https://", "git@")):
        url = f"https://github.com/{target_arg.strip('/')}.git"

    repo_name = target_arg.rstrip("/").split("/")[-1].removesuffix(".git")
    dest = Path(".temp") / f"inspect-{repo_name}"

    if dest.exists():
        return dest

    dest.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["git", "clone", "--depth", "1", url, str(dest)]
    print(f"Cloning {url} into {dest}...", file=sys.stderr)
    subprocess.run(cmd, check=True)
    return dest


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entrypoint for skill harvesting."""
    args = sys.argv[1:] if argv is None else argv
    if not args or not args[0].strip():
        print(
            "Usage: uv run python .agents/skills/inspect-module-setup/scripts/harvest_skills.py <target_path_or_repo>",
            file=sys.stderr,
        )
        return 1

    try:
        target_dir = ensure_target_dir(args[0])
        result = harvest_repo(target_dir)
        print(format_harvest_markdown(result))
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f"Error harvesting skills: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
