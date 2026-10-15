import os
import re
import shutil

PROJECT_DIR = os.path.realpath(os.path.curdir)

CONFIG_FILES_WITH_HEADERS = [
    "pyproject.toml",
    "poe_tasks.toml",
    "ruff.toml",
    "pyrefly.toml",
    "complexipy.toml",
    "zensical.toml",
    "rumdl.toml",
    "tach.toml",
    ".coveragerc",
    "pytest.ini",
    ".taplo.toml",
    "typos.toml",
    ".pre-commit-config.yaml",
    ".prettierrc.yaml",
    ".editorconfig",
]


def remove_file(*filepath_parts: str) -> None:
    path = os.path.join(PROJECT_DIR, *filepath_parts)
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)


def remove_dir(*dirpath_parts: str) -> None:
    path = os.path.join(PROJECT_DIR, *dirpath_parts)
    if os.path.isdir(path):
        shutil.rmtree(path)


def strip_config_headers() -> None:
    """Strip explanatory template comments from generated configuration files."""
    pattern = re.compile(r"^# =+[^\n]*\n(?:#[^\n]*\n)*# =+[^\n]*\n+")
    for filename in CONFIG_FILES_WITH_HEADERS:
        filepath = os.path.join(PROJECT_DIR, filename)
        if not os.path.isfile(filepath):
            continue
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        new_content = pattern.sub("", content)
        if new_content != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)


def to_bool(val: object) -> bool:
    if isinstance(val, bool):
        return val
    return str(val).lower() in ("true", "yes", "1", "t", "y", "on")


def setup_agent_instructions() -> None:
    """Ensure CLAUDE.md points to AGENTS.md for dual agent compatibility."""
    agents_path = os.path.join(PROJECT_DIR, "AGENTS.md")
    claude_path = os.path.join(PROJECT_DIR, "CLAUDE.md")
    if os.path.isfile(agents_path) and not os.path.lexists(claude_path):
        try:
            os.symlink("AGENTS.md", claude_path)
        except (OSError, NotImplementedError):
            # Fallback for platforms or environments without symlink privileges
            shutil.copyfile(agents_path, claude_path)


def main() -> None:
    include_cli = to_bool("{{ cookiecutter.include_cli }}")
    include_github_actions = to_bool("{{ cookiecutter.include_github_actions }}")
    license_type = "{{ cookiecutter.license }}"
    package_name = "{{ cookiecutter.package_name }}"

    # Strip template educational header comments from generated project configs
    strip_config_headers()

    if not include_cli:
        remove_file("src", package_name, "cli.py")
        remove_file("tests", "test_cli.py")
        remove_file("docs", "javascripts", "termynal.js")
        remove_file("docs", "stylesheets", "termynal.css")
        remove_dir("docs", "stylesheets")

    if not include_github_actions:
        remove_dir(".github")

    if license_type.lower() == "none":
        remove_file("LICENSE")

    setup_agent_instructions()


if __name__ == "__main__":
    main()
