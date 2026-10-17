"""Tests for the Zenith template."""

import tempfile
from pathlib import Path

import pytest
from cookiecutter.exceptions import FailedHookException
from cookiecutter.main import cookiecutter

TEMPLATE_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def temp_output_dir():
    """Create a temporary directory for cookiecutter output."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


def test_default_generation(temp_output_dir: Path) -> None:
    """Test generating a project with default configuration."""
    project_dir = Path(
        cookiecutter(
            str(TEMPLATE_ROOT),
            no_input=True,
            output_dir=str(temp_output_dir),
            extra_context={
                "project_name": "Demo App",
                "python_version": "3.13",
                "include_cli": "yes",
            },
        )
    )

    assert project_dir.exists()
    assert (project_dir / "pyproject.toml").exists()
    assert (project_dir / "poe_tasks.toml").exists()
    assert (project_dir / "ruff.toml").exists()
    assert (project_dir / "pyrefly.toml").exists()
    assert (project_dir / "complexipy.toml").exists()
    assert (project_dir / "zensical.toml").exists()
    assert (project_dir / "rumdl.toml").exists()
    assert (project_dir / "tach.toml").exists()
    assert (project_dir / "typos.toml").exists()
    assert (project_dir / "AGENTS.md").exists()
    assert (project_dir / "CLAUDE.md").exists()
    assert (project_dir / "AI_POLICY.md").exists()
    assert (project_dir / "pytest.ini").exists()
    assert (project_dir / ".coveragerc").exists()
    assert (project_dir / ".gitattributes").exists()
    assert (project_dir / ".prettierrc.yaml").exists()
    assert (project_dir / ".pre-commit-config.yaml").exists()
    assert (project_dir / ".editorconfig").exists()
    assert (project_dir / ".zizmor.yml").exists()
    assert (project_dir / ".gemini" / "settings.json").exists()
    assert (
        '"contextFileName": "AGENTS.md"'
        in (project_dir / ".gemini" / "settings.json").read_text()
    )
    assert (project_dir / ".claude" / "settings.json").exists()
    assert (project_dir / ".codex" / "config.toml").exists()
    assert (project_dir / ".aider.conf.yml").exists()
    assert (project_dir / ".cursorrules").exists()
    assert (project_dir / ".windsurfrules").exists()
    assert (project_dir / ".github" / "copilot-instructions.md").exists()
    assert (project_dir / ".github" / "codecov.yml").exists()
    for skill in [
        "code-review",
        "git-workflow",
        "project-setup",
        "python-style-guide",
        "tool-complexipy",
        "tool-poethepoet",
        "tool-pyrefly",
        "tool-pytest",
        "tool-ruff",
        "tool-rumdl",
        "tool-tach",
        "tool-typer",
        "tool-typos",
        "tool-typst",
        "tool-uv",
        "tool-zensical",
        "tool-zizmor",
    ]:
        assert (project_dir / ".agents" / "skills" / skill / "SKILL.md").exists()
    setup_skill_text = (
        project_dir / ".agents" / "skills" / "project-setup" / "SKILL.md"
    ).read_text()
    assert "disable-model-invocation: true" in setup_skill_text
    poe_text = (project_dir / "poe_tasks.toml").read_text()
    assert "[tasks.zizmor]" in poe_text
    assert '"zizmor"' in poe_text
    assert (
        "zizmor --config .zizmor.yml --pedantic --min-severity informational .github/workflows"
        in poe_text
    )
    for ref in [
        "hypothesis.md",
        "pytest-cov.md",
        "pytest-randomly.md",
        "pytest-sugar.md",
        "pytest-xdist.md",
        "syrupy.md",
    ]:
        assert (
            project_dir / ".agents" / "skills" / "tool-pytest" / "references" / ref
        ).exists()
    assert (project_dir / "src" / "demo_app" / "__init__.py").exists()
    assert (project_dir / "src" / "demo_app" / "_lazy.py").exists()
    assert (project_dir / "src" / "demo_app" / "cli.py").exists()
    assert (project_dir / "src" / "demo_app" / "__main__.py").exists()
    init_text = (project_dir / "src" / "demo_app" / "__init__.py").read_text()
    assert "_lazy" in init_text
    assert "_LAZY_MEMBERS" in init_text
    assert "accessors(globals(), _LAZY_MEMBERS)" in init_text
    assert (
        project_dir
        / "src"
        / "demo_app"
        / ".agents"
        / "skills"
        / "demo-app"
        / "SKILL.md"
    ).exists()
    assert (project_dir / "tests" / "test_core.py").exists()
    assert (project_dir / "tests" / "__snapshots__" / "test_core.ambr").exists()
    assert (project_dir / "tests" / "test_cli.py").exists()
    assert (project_dir / "docs" / "index.md").exists()
    assert (project_dir / "docs" / "javascripts" / "mathjax.js").exists()
    assert (project_dir / "docs" / "javascripts" / "termynal.js").exists()
    assert (project_dir / "docs" / "stylesheets" / "termynal.css").exists()
    assert (project_dir / "docs" / "assets" / "python-logo.svg").exists()
    assert (project_dir / "docs" / "assets" / "python-logo.typ").exists()
    assert (project_dir / "scripts" / "verify_wheel.py").exists()
    assert (project_dir / ".github" / "workflows" / "python_tests.yaml").exists()
    assert (project_dir / ".github" / "workflows" / "guard-dependencies.yaml").exists()
    assert (
        "timeout-minutes: 5"
        in (
            project_dir / ".github" / "workflows" / "guard-dependencies.yaml"
        ).read_text()
    )
    assert (project_dir / ".github" / "workflows" / "docs.yaml").exists()
    assert (project_dir / ".github" / "workflows" / "publish.yaml").exists()
    assert (project_dir / ".github" / "workflows" / "test_redistribute.yaml").exists()
    assert (
        "UV_EXCLUDE_NEWER"
        in (project_dir / ".github" / "workflows" / "publish.yaml").read_text()
    )
    assert (
        "python scripts/verify_wheel.py"
        in (project_dir / ".github" / "workflows" / "publish.yaml").read_text()
    )
    assert (
        "python scripts/verify_wheel.py"
        in (
            project_dir / ".github" / "workflows" / "test_redistribute.yaml"
        ).read_text()
    )
    assert (project_dir / ".github" / "dependabot.yml").exists()
    dependabot_text = (project_dir / ".github" / "dependabot.yml").read_text()
    assert 'package-ecosystem: "uv"' in dependabot_text
    assert '"github_actions"' in dependabot_text
    assert '"python"' in dependabot_text
    assert (project_dir / ".github" / "PULL_REQUEST_TEMPLATE.md").exists()
    assert (project_dir / ".github" / "ISSUE_TEMPLATE" / "bug_report.yml").exists()
    assert (project_dir / ".github" / "ISSUE_TEMPLATE" / "feature_request.yml").exists()
    assert (project_dir / ".github" / "ISSUE_TEMPLATE" / "config.yml").exists()

    # Verify precommit task removed and format-check added
    poe_text = (project_dir / "poe_tasks.toml").read_text()
    assert "tasks.precommit" not in poe_text
    assert '"precommit"' not in poe_text
    assert "tasks.format-check" in poe_text
    assert "tasks.test-fast" in poe_text
    assert "--dist=worksteal --max-worker-restart=0" in poe_text
    assert "tasks.test-lowest" in poe_text
    assert "tasks.test-sdist" in poe_text
    assert "tasks.verify-wheel" in poe_text
    assert "python scripts/verify_wheel.py" in poe_text
    assert "tasks.test-snapshot-update" in poe_text
    assert "tasks.zizmor" in poe_text
    assert "tasks.audit" in poe_text
    assert "uv audit" in poe_text
    assert "tasks.check-api" in poe_text
    assert "griffe check demo_app --search src" in poe_text
    assert "tach check-external" in poe_text
    assert "tasks.sync-skills" in poe_text
    assert "tasks.docs-logo" in poe_text
    assert "tasks.clean" in poe_text
    assert "tasks._clean-dist" in poe_text

    # Verify markdown-exec and Python 3.15 in pyproject.toml
    pyproject_text = (project_dir / "pyproject.toml").read_text()
    assert 'license = "MIT"' in pyproject_text
    assert 'license-files = [ "LICENSE" ]' in pyproject_text
    assert "griffe-warnings-deprecated>=" in pyproject_text
    assert "markdown-exec" in pyproject_text
    assert "Programming Language :: Python :: 3.15" in pyproject_text
    assert "Typing :: Typed" in pyproject_text
    assert "hypothesis" in pyproject_text
    assert "pytest-randomly" in pyproject_text
    assert "pytest-sugar" in pyproject_text
    assert "pytest-xdist" in pyproject_text
    assert "syrupy" in pyproject_text
    assert "typos" in pyproject_text
    assert "typst" in pyproject_text
    assert "zizmor" in pyproject_text
    assert "rich>=" in pyproject_text
    assert "typer>=" in pyproject_text
    assert 'demo-app = "demo_app.__main__:main"' in pyproject_text
    assert "default-groups = [" in pyproject_text
    assert "test = [" in pyproject_text
    assert "lint = [" in pyproject_text
    assert "docs = [" in pyproject_text
    assert "mkdocstrings[python]" in pyproject_text
    assert "source-include = [" in pyproject_text

    # Verify markdown-exec fences and mkdocstrings plugin in zensical.toml
    zensical_text = (project_dir / "zensical.toml").read_text()
    assert "markdown_exec.validator" in zensical_text
    assert "[project.validation]" in zensical_text
    assert "invalid_links" in zensical_text
    assert "invalid_link_anchors" in zensical_text
    assert "[project.plugins.mkdocstrings]" in zensical_text
    assert "navigation.instant.preview" in zensical_text
    assert "search.suggest" in zensical_text
    assert "toc.follow" in zensical_text
    assert "signature_crossrefs = true" in zensical_text
    assert 'members_order = "source"' in zensical_text
    assert "pymdownx.snippets.check_paths = true" in zensical_text
    assert "pymdownx.snippets.dedent_subsections = true" in zensical_text
    assert 'zensical.extensions.preview.targets.include = ["*"]' in zensical_text
    assert "[project.plugins.gh-admonitions]" in zensical_text
    assert "[project.plugins.markdown-exec]" in zensical_text
    assert "[project.plugins.llmstxt]" in zensical_text
    assert 'full_output = "llms-full.txt"' in zensical_text
    assert 'inventories = ["https://docs.python.org/3/objects.inv"]' in zensical_text
    assert 'options.backlinks = "tree"' in zensical_text
    assert 'options.extensions = ["griffe_warnings_deprecated"]' in zensical_text
    assert "options.line_length = 88" in zensical_text
    assert "options.relative_crossrefs = true" in zensical_text
    assert "options.scoped_crossrefs = true" in zensical_text
    assert "options.show_inheritance_diagram = true" in zensical_text
    assert "options.show_signature_type_parameters = true" in zensical_text
    assert "options.summary = true" in zensical_text
    assert "options.type_parameter_headings = true" in zensical_text
    assert "options.show_symbol_type_heading = true" in zensical_text
    assert "options.show_symbol_type_toc = true" in zensical_text
    assert "options.parameter_headings = true" in zensical_text
    assert "options.docstring_options.ignore_init_summary = true" in zensical_text
    assert 'options.annotations_path = "brief"' in zensical_text
    assert "options.show_bases = true" in zensical_text
    assert "options.unwrap_annotated = true" in zensical_text
    assert "stylesheets/termynal.css" in zensical_text
    assert "javascripts/termynal.js" in zensical_text

    agents_text = (project_dir / "AGENTS.md").read_text()
    assert "## Project Stewardship" in agents_text
    assert "never double backticks" in agents_text
    assert "Reproduce-First Bug Scoping" in agents_text
    assert "Complexity Reset Rule" in agents_text

    coveragerc_text = (project_dir / ".coveragerc").read_text()
    assert "tests" in coveragerc_text
    assert "*/__snapshots__/*" in coveragerc_text
    assert "tests/*" not in coveragerc_text
    assert "core = sysmon" in coveragerc_text
    assert "patch =\n    subprocess\n    _exit" in coveragerc_text
    assert r"return NotImplemented\b" in coveragerc_text
    assert r"(typing\.)?assert_never" in coveragerc_text

    pytest_ini_text = (project_dir / "pytest.ini").read_text()
    assert "-ra" in pytest_ini_text
    assert "--snapshot-warn-unused" in pytest_ini_text
    assert "default::EncodingWarning" in pytest_ini_text
    assert "error::EncodingWarning:demo_app.*" in pytest_ini_text
    assert "minversion             = 9.0" in pytest_ini_text
    assert "strict                 = true" in pytest_ini_text
    assert "log_level              = DEBUG" in pytest_ini_text
    assert "DONT_ACCEPT_TRUE_FOR_1" in pytest_ini_text

    pyrefly_text = (project_dir / "pyrefly.toml").read_text()
    assert 'enabled-ignores      = [ "pyrefly" ]' in pyrefly_text

    ruff_toml_text = (project_dir / "ruff.toml").read_text()
    assert "combine-as-imports = true" in ruff_toml_text

    # Verify docs reference and mermaid diagrams
    ref_text = (project_dir / "docs" / "reference.md").read_text()
    assert "::: demo_app.core" in ref_text
    assert "::: demo_app.cli" in ref_text
    getting_started_text = (project_dir / "docs" / "getting-started.md").read_text()
    assert 'class="termy"' in getting_started_text
    assert 'class="termy"' in (project_dir / "docs" / "index.md").read_text()
    assert "sequenceDiagram" in getting_started_text
    assert "stateDiagram-v2" in getting_started_text

    # Verify zensical commands
    assert 'cmd  = "zensical serve"' in poe_text
    assert "zensical build --strict" in poe_text
    docs_yaml_text = (project_dir / ".github" / "workflows" / "docs.yaml").read_text()
    assert "zensical build --clean --strict" in docs_yaml_text
    assert "uv sync --only-group docs" in docs_yaml_text

    publish_yaml_text = (
        project_dir / ".github" / "workflows" / "publish.yaml"
    ).read_text()
    assert "attestations: write" in publish_yaml_text
    assert "actions/attest-build-provenance@v2" in publish_yaml_text
    assert "attestations: true" in publish_yaml_text

    # Verify python aliases in rumdl.toml
    rumdl_text = (project_dir / "rumdl.toml").read_text()
    assert '"py"' in rumdl_text
    assert '"ruff:check"' in rumdl_text

    # Verify CI workflow has quality and test split
    ci_text = (project_dir / ".github" / "workflows" / "python_tests.yaml").read_text()
    assert "concurrency:" in ci_text
    assert "cancel-in-progress: true" in ci_text
    assert "quality:" in ci_text
    assert "test:" in ci_text
    assert "test-lowest:" in ci_text
    assert "test-dist:" in ci_text
    assert "uv sync --only-group test" in ci_text
    assert "uv sync --only-group test --resolution lowest-direct" in ci_text
    assert "poe format-check" in ci_text
    assert "poe typos" in ci_text
    assert "UV_EXCLUDE_NEWER" in ci_text
    assert (
        "UV_EXCLUDE_NEWER"
        in (
            project_dir / ".github" / "workflows" / "test_redistribute.yaml"
        ).read_text()
    )
    assert "GITHUB_STEP_SUMMARY" in ci_text
    assert "uv run poe fix" in ci_text
    assert "uv run poe test-lowest" in ci_text
    assert (
        "GITHUB_STEP_SUMMARY"
        in (project_dir / ".github" / "workflows" / "docs.yaml").read_text()
    )
    assert "exclude-newer" in (project_dir / "pyproject.toml").read_text()
    assert (
        "uv run poe test-lowest"
        in (project_dir / ".agents" / "skills" / "tool-pytest" / "SKILL.md").read_text()
    )
    assert (
        "exclude-newer"
        in (project_dir / ".agents" / "skills" / "tool-uv" / "SKILL.md").read_text()
    )

    # Verify pre-commit config has typos
    precommit_text = (project_dir / ".pre-commit-config.yaml").read_text()
    assert "crate-ci/typos" in precommit_text

    # Verify Tach setup
    tach_text = (project_dir / "tach.toml").read_text()
    assert 'source_roots = [ "src" ]' in tach_text
    assert 'path       = "demo_app"' in tach_text
    assert 'path       = "demo_app.__main__"' in tach_text
    assert "ignore_type_checking_imports = true" in tach_text

    # Verify hardened pytest.ini, ruff ban-relative-imports, coveragerc overload, and AI policy
    pytest_text = (project_dir / "pytest.ini").read_text()
    assert "--import-mode=importlib" in pytest_text
    assert "--strict-config" in pytest_text
    assert "--strict-markers" in pytest_text
    assert "xfail_strict" in pytest_text
    assert "filterwarnings" in pytest_text

    ruff_text = (project_dir / "ruff.toml").read_text()
    assert 'ban-relative-imports = "all"' in ruff_text
    assert "keep-runtime-typing = true" in ruff_text
    assert "non-empty-init-module" in ruff_text

    coverage_text = (project_dir / ".coveragerc").read_text()
    assert "@overload" in coverage_text

    ai_policy_text = (project_dir / "AI_POLICY.md").read_text()
    assert "Human-in-the-Loop" in ai_policy_text
    assert (TEMPLATE_ROOT / "AI_POLICY.md").exists()

    pr_template_text = (
        project_dir / ".github" / "PULL_REQUEST_TEMPLATE.md"
    ).read_text()
    assert "AI Assistance Disclosure" in pr_template_text

    # Verify Elevator Pitch present in generated README and repo README
    readme_text = (project_dir / "README.md").read_text()
    assert "Elevator Pitch" in readme_text
    assert "Elevator Pitch" in (TEMPLATE_ROOT / "README.md").read_text()
    assert "CLI Layer" in readme_text
    assert "license-MIT" in readme_text
    assert "Verify Wheel" in readme_text

    # Verify AGENTS.md content
    agents_text = (project_dir / "AGENTS.md").read_text()
    assert "uv run poe --help" in agents_text
    assert "Use **Typer** exclusively for any command-line interfaces" in agents_text
    assert "`cli` -> `core` -> external dependencies" in agents_text
    assert ".temp/" in agents_text
    assert ".temp/" in (project_dir / ".gitignore").read_text()
    assert (project_dir / "CLAUDE.md").read_text() == agents_text
    assert (project_dir / ".cursorrules").read_text() == agents_text
    assert (project_dir / ".windsurfrules").read_text() == agents_text
    if hasattr(Path, "is_symlink") and (project_dir / "CLAUDE.md").is_symlink():
        import os

        assert os.readlink(project_dir / "CLAUDE.md") == "AGENTS.md"
        if (project_dir / ".cursorrules").is_symlink():
            assert os.readlink(project_dir / ".cursorrules") == "AGENTS.md"
        if (project_dir / ".windsurfrules").is_symlink():
            assert os.readlink(project_dir / ".windsurfrules") == "AGENTS.md"

    # Verify AI tool configuration files
    assert "uv run poe:*" in (project_dir / ".claude" / "settings.json").read_text()
    assert "workspace-write" in (project_dir / ".codex" / "config.toml").read_text()
    assert "AGENTS.md" in (project_dir / ".aider.conf.yml").read_text()
    assert (
        "AGENTS.md" in (project_dir / ".github" / "copilot-instructions.md").read_text()
    )
    assert "comment: off" in (project_dir / ".github" / "codecov.yml").read_text()


def test_python_315_generation(temp_output_dir: Path) -> None:
    """Test generating a project with Python 3.15."""
    project_dir = Path(
        cookiecutter(
            str(TEMPLATE_ROOT),
            no_input=True,
            output_dir=str(temp_output_dir),
            extra_context={
                "project_name": "Future App",
                "python_version": "3.15",
            },
        )
    )

    assert project_dir.exists()
    pyproject_text = (project_dir / "pyproject.toml").read_text()
    assert 'requires-python = ">=3.15"' in pyproject_text
    assert "Programming Language :: Python :: 3.12" not in pyproject_text
    assert "Programming Language :: Python :: 3.13" not in pyproject_text
    assert "Programming Language :: Python :: 3.14" not in pyproject_text
    assert "Programming Language :: Python :: 3.15" in pyproject_text

    ci_text = (project_dir / ".github" / "workflows" / "python_tests.yaml").read_text()
    assert '["3.15"]' in ci_text

    readme_text = (project_dir / "README.md").read_text()
    assert "python-3.15+-blue.svg" in readme_text


def test_no_cli_generation(temp_output_dir: Path) -> None:
    """Test generating a library project without CLI."""
    project_dir = Path(
        cookiecutter(
            str(TEMPLATE_ROOT),
            no_input=True,
            output_dir=str(temp_output_dir),
            extra_context={
                "project_name": "Pure Library",
                "include_cli": "no",
            },
        )
    )

    assert project_dir.exists()
    assert (project_dir / "src" / "pure_library" / "core.py").exists()
    assert not (project_dir / "src" / "pure_library" / "cli.py").exists()
    assert not (project_dir / "src" / "pure_library" / "_lazy.py").exists()
    assert not (project_dir / "src" / "pure_library" / "__main__.py").exists()
    no_cli_init = (project_dir / "src" / "pure_library" / "__init__.py").read_text()
    assert "_lazy" not in no_cli_init
    assert "_LAZY_MEMBERS" not in no_cli_init
    assert not (project_dir / "tests" / "test_cli.py").exists()
    assert not (project_dir / "docs" / "javascripts" / "termynal.js").exists()
    assert not (project_dir / "docs" / "stylesheets" / "termynal.css").exists()
    assert not (project_dir / "docs" / "stylesheets").exists()
    assert "termynal" not in (project_dir / "zensical.toml").read_text()
    assert "termy" not in (project_dir / "docs" / "getting-started.md").read_text()
    assert "termy" not in (project_dir / "docs" / "index.md").read_text()

    pyproject_text = (project_dir / "pyproject.toml").read_text()
    assert (
        "dependencies = [  ]" in pyproject_text or "dependencies = []" in pyproject_text
    )
    assert "typer" not in pyproject_text
    assert "rich" not in pyproject_text

    tach_text = (project_dir / "tach.toml").read_text()
    assert '"cli"' not in tach_text
    assert 'layers                       = [ "core" ]' in tach_text

    readme_text = (project_dir / "README.md").read_text()
    assert "CLI Layer" not in readme_text

    ref_text = (project_dir / "docs" / "reference.md").read_text()
    assert "::: pure_library.core" in ref_text
    assert "::: pure_library.cli" not in ref_text

    agents_text = (project_dir / "AGENTS.md").read_text()
    assert (project_dir / "CLAUDE.md").exists()
    assert "Use **Typer** exclusively for any command-line interfaces" in agents_text
    assert "The `core` module must never import from `cli`" not in agents_text
    assert "`core` -> external dependencies" in agents_text


def test_no_ci_testing(temp_output_dir: Path) -> None:
    """Test generating a project without CI testing workflows."""
    project_dir = Path(
        cookiecutter(
            str(TEMPLATE_ROOT),
            no_input=True,
            output_dir=str(temp_output_dir),
            extra_context={
                "project_name": "Publish Only",
                "include_ci_testing": "no",
                "include_ci_publishing": "yes",
            },
        )
    )

    assert project_dir.exists()
    assert (project_dir / ".github" / "workflows" / "publish.yaml").exists()
    assert (project_dir / ".github" / "workflows" / "docs.yaml").exists()
    assert not (project_dir / ".github" / "workflows" / "python_tests.yaml").exists()
    assert not (
        project_dir / ".github" / "workflows" / "test_redistribute.yaml"
    ).exists()
    assert not (
        project_dir / ".github" / "workflows" / "guard-dependencies.yaml"
    ).exists()
    assert not (project_dir / ".github" / "codecov.yml").exists()
    assert (project_dir / ".zizmor.yml").exists()
    assert "[tasks.zizmor]" in (project_dir / "poe_tasks.toml").read_text()
    readme_text = (project_dir / "README.md").read_text()
    assert "[![CI]" not in readme_text


def test_no_ci_publishing(temp_output_dir: Path) -> None:
    """Test generating a project without CI publishing workflows."""
    project_dir = Path(
        cookiecutter(
            str(TEMPLATE_ROOT),
            no_input=True,
            output_dir=str(temp_output_dir),
            extra_context={
                "project_name": "Tests Only",
                "include_ci_testing": "yes",
                "include_ci_publishing": "no",
            },
        )
    )

    assert project_dir.exists()
    assert (project_dir / ".github" / "workflows" / "python_tests.yaml").exists()
    assert (project_dir / ".github" / "workflows" / "test_redistribute.yaml").exists()
    assert (project_dir / ".github" / "workflows" / "guard-dependencies.yaml").exists()
    assert (project_dir / ".github" / "codecov.yml").exists()
    assert not (project_dir / ".github" / "workflows" / "publish.yaml").exists()
    assert not (project_dir / ".github" / "workflows" / "docs.yaml").exists()
    assert (project_dir / ".zizmor.yml").exists()
    assert "[tasks.zizmor]" in (project_dir / "poe_tasks.toml").read_text()
    readme_text = (project_dir / "README.md").read_text()
    assert "[![CI]" in readme_text


def test_no_github_actions(temp_output_dir: Path) -> None:
    """Test generating a project without GitHub actions (legacy flag or both disabled)."""
    project_dir = Path(
        cookiecutter(
            str(TEMPLATE_ROOT),
            no_input=True,
            output_dir=str(temp_output_dir),
            extra_context={
                "project_name": "Local Only",
                "include_ci_testing": "no",
                "include_ci_publishing": "no",
            },
        )
    )

    assert project_dir.exists()
    assert not (project_dir / ".github").exists()
    assert not (project_dir / ".zizmor.yml").exists()
    assert not (project_dir / ".agents" / "skills" / "tool-zizmor").exists()
    poe_text = (project_dir / "poe_tasks.toml").read_text()
    assert "[tasks.zizmor]" not in poe_text
    assert '"zizmor"' not in poe_text
    readme_text = (project_dir / "README.md").read_text()
    assert "[![CI]" not in readme_text


def test_no_license(temp_output_dir: Path) -> None:
    """Test generating a project without LICENSE."""
    project_dir = Path(
        cookiecutter(
            str(TEMPLATE_ROOT),
            no_input=True,
            output_dir=str(temp_output_dir),
            extra_context={
                "project_name": "Proprietary",
                "license": "None",
            },
        )
    )

    assert project_dir.exists()
    assert not (project_dir / "LICENSE").exists()
    pyproject_text = (project_dir / "pyproject.toml").read_text()
    assert "license =" not in pyproject_text
    assert "license-files" not in pyproject_text
    readme_text = (project_dir / "README.md").read_text()
    assert "badge/license" not in readme_text
    assert "All rights reserved." in readme_text
    assert "[LICENSE](LICENSE)" not in readme_text


def test_package_name_keyword_validation(temp_output_dir: Path) -> None:
    """Test that python keywords are rejected as package names."""
    with pytest.raises(FailedHookException):
        cookiecutter(
            str(TEMPLATE_ROOT),
            no_input=True,
            output_dir=str(temp_output_dir),
            extra_context={
                "project_name": "def",
            },
        )


def test_native_booleans_and_dynamic_year(temp_output_dir: Path) -> None:
    """Test native boolean variables and dynamic year injection."""
    from datetime import UTC, datetime

    current_year = str(datetime.now(UTC).year)
    project_dir = Path(
        cookiecutter(
            str(TEMPLATE_ROOT),
            no_input=True,
            output_dir=str(temp_output_dir),
            extra_context={
                "project_name": "Modern App",
                "include_cli": True,
                "include_ci_testing": False,
                "include_ci_publishing": False,
                "license": "MIT",
            },
        )
    )

    assert project_dir.exists()
    assert (project_dir / "src" / "modern_app" / "cli.py").exists()
    assert not (project_dir / ".github").exists()

    license_text = (project_dir / "LICENSE").read_text()
    assert f"Copyright (c) {current_year}" in license_text


def test_slugify_special_characters(temp_output_dir: Path) -> None:
    """Test robust slugification of special characters and punctuation in project_name."""
    project_dir = Path(
        cookiecutter(
            str(TEMPLATE_ROOT),
            no_input=True,
            output_dir=str(temp_output_dir),
            extra_context={
                "project_name": "Zenith's Cool Tool (v2)",
            },
        )
    )

    assert project_dir.exists()
    assert project_dir.name == "zenith-s-cool-tool-v2"
    assert (project_dir / "src" / "zenith_s_cool_tool_v2" / "__init__.py").exists()
    assert (project_dir / "src" / "zenith_s_cool_tool_v2" / "core.py").exists()


def test_verify_wheel_execution(temp_output_dir: Path) -> None:
    """Test that scripts/verify_wheel.py builds and verifies the wheel in an isolated venv."""
    import subprocess
    import sys

    project_dir = Path(
        cookiecutter(
            str(TEMPLATE_ROOT),
            no_input=True,
            output_dir=str(temp_output_dir),
            extra_context={
                "project_name": "Wheel Smoke App",
                "include_cli": "yes",
            },
        )
    )

    verify_script = project_dir / "scripts" / "verify_wheel.py"
    assert verify_script.exists()

    # Execute verify_wheel.py directly inside the generated project
    result = subprocess.run(
        [sys.executable, str(verify_script)],
        cwd=str(project_dir),
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, (
        f"verify_wheel.py failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )
    assert "Wheel verification successful" in result.stdout

    # Execute verify_wheel.py with --run-tests to verify test suite against distribution
    result_tests = subprocess.run(
        [sys.executable, str(verify_script), "--run-tests"],
        cwd=str(project_dir),
        capture_output=True,
        text=True,
        check=False,
    )
    assert result_tests.returncode == 0, (
        f"verify_wheel.py --run-tests failed:\nSTDOUT:\n{result_tests.stdout}\nSTDERR:\n{result_tests.stderr}"
    )
    assert "Distribution test suite passed successfully" in result_tests.stdout


def test_lazy_load_behavior(temp_output_dir: Path) -> None:
    """Test that PEP 562 lazy loading prevents eager submodule imports."""
    import subprocess
    import sys

    project_dir = Path(
        cookiecutter(
            str(TEMPLATE_ROOT),
            no_input=True,
            output_dir=str(temp_output_dir),
            extra_context={
                "project_name": "Lazy App",
                "include_cli": "yes",
            },
        )
    )

    verify_code = """
import sys
import os

sys.path.insert(0, os.path.abspath("src"))
import lazy_app

# 1. lazy_app.cli and lazy_app.__main__ must NOT be imported eagerly on package import
assert "lazy_app.cli" not in sys.modules, "lazy_app.cli was imported eagerly!"
assert "lazy_app.__main__" not in sys.modules, "lazy_app.__main__ was imported eagerly!"

# 2. Accessing core function directly via lazy resolution works
greeting = lazy_app.get_greeting("Antigravity")
assert greeting == "Hello, Antigravity!"
assert "lazy_app.core" in sys.modules
assert "lazy_app.cli" not in sys.modules, "lazy_app.cli was imported by get_greeting!"

# 3. dir() returns lazily exported members and globals
members = dir(lazy_app)
assert "app" in members
assert "get_greeting" in members
assert "__version__" in members

# 4. Unknown attribute raises AttributeError
try:
    lazy_app.nonexistent_symbol
except AttributeError:
    pass
else:
    raise AssertionError("AttributeError not raised for missing member")
"""
    result = subprocess.run(
        [sys.executable, "-c", verify_code],
        cwd=str(project_dir),
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, (
        f"Lazy loading test failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )
