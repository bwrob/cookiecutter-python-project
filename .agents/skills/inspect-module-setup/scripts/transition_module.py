"""Transition a benchmark module from candidates.log to inspected.log."""

import sys
from collections.abc import Sequence
from pathlib import Path

DEFAULT_SKILL_DIR = Path(__file__).resolve().parent.parent


def transition_module(module: str, skill_dir: Path = DEFAULT_SKILL_DIR) -> None:
    """Move a target module from candidates.log to inspected.log.

    Ensures the target module is recorded in inspected.log and removed from
    candidates.log within the skill directory without duplicate entries or
    blank lines.
    """
    clean_module = module.strip()
    if not clean_module:
        raise ValueError("Module name cannot be empty.")

    skill_dir.mkdir(parents=True, exist_ok=True)
    inspected_log = skill_dir / "inspected.log"
    candidates_log = skill_dir / "candidates.log"

    # Append to inspected.log if not already present
    inspected: list[str] = []
    if inspected_log.exists():
        inspected = [
            line.strip()
            for line in inspected_log.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    if clean_module not in inspected:
        inspected.append(clean_module)
        inspected_log.write_text(
            "\n".join(inspected) + "\n",
            encoding="utf-8",
        )
        print(f"Recorded '{clean_module}' in {inspected_log}")
    else:
        print(f"'{clean_module}' was already recorded in {inspected_log}")

    # Remove from candidates.log if present
    if candidates_log.exists():
        candidates = [
            line.strip()
            for line in candidates_log.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        if clean_module in candidates:
            updated_candidates = [c for c in candidates if c != clean_module]
            content = "\n".join(updated_candidates) + "\n" if updated_candidates else ""
            candidates_log.write_text(content, encoding="utf-8")
            print(f"Removed '{clean_module}' from {candidates_log}")


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entrypoint for module transition."""
    args = sys.argv[1:] if argv is None else argv
    if not args or not args[0].strip():
        print(
            "Usage: uv run python .agents/skills/inspect-module-setup/scripts/transition_module.py <module_name>",
            file=sys.stderr,
        )
        return 1

    try:
        transition_module(args[0])
    except (ValueError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
