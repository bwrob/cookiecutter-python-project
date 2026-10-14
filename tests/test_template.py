"""Tests for the cookiecutter-python-zenith template."""

import tempfile
from pathlib import Path

import pytest
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
    assert (project_dir / ".coveragerc").exists()
    assert (project_dir / ".gitattributes").exists()
    assert (project_dir / ".prettierrc.yaml").exists()
    assert (project_dir / ".pre-commit-config.yaml").exists()
    assert (
        project_dir / ".agents" / "skills" / "python-style-guide" / "SKILL.md"
    ).exists()
    assert (project_dir / "src" / "demo_app" / "__init__.py").exists()
    assert (project_dir / "src" / "demo_app" / "cli.py").exists()
    assert (project_dir / "tests" / "test_core.py").exists()
    assert (project_dir / "tests" / "test_cli.py").exists()
    assert (project_dir / "docs" / "index.md").exists()
    assert (project_dir / "docs" / "javascripts" / "mathjax.js").exists()
    assert (project_dir / "docs" / "assets" / "python-logo.svg").exists()
    assert (project_dir / ".github" / "workflows" / "python_tests.yaml").exists()
    assert (project_dir / ".github" / "workflows" / "docs.yaml").exists()

    # Verify precommit task removed
    poe_text = (project_dir / "poe_tasks.toml").read_text()
    assert "tasks.precommit" not in poe_text
    assert '"precommit"' not in poe_text

    # Verify markdown-exec and Python 3.15 in pyproject.toml
    pyproject_text = (project_dir / "pyproject.toml").read_text()
    assert "markdown-exec" in pyproject_text
    assert "Programming Language :: Python :: 3.15" in pyproject_text

    # Verify markdown-exec fences in zensical.toml
    zensical_text = (project_dir / "zensical.toml").read_text()
    assert "markdown_exec.validator" in zensical_text

    # Verify python aliases in rumdl.toml
    rumdl_text = (project_dir / "rumdl.toml").read_text()
    assert '"py"' in rumdl_text
    assert '"ruff:check"' in rumdl_text

    # Verify Elevator Pitch present in generated README and repo README
    assert "Elevator Pitch" in (project_dir / "README.md").read_text()
    assert "Elevator Pitch" in (TEMPLATE_ROOT / "README.md").read_text()


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
    assert not (project_dir / "tests" / "test_cli.py").exists()


def test_no_github_actions(temp_output_dir: Path) -> None:
    """Test generating a project without GitHub actions."""
    project_dir = Path(
        cookiecutter(
            str(TEMPLATE_ROOT),
            no_input=True,
            output_dir=str(temp_output_dir),
            extra_context={
                "project_name": "Local Only",
                "include_github_actions": "no",
            },
        )
    )

    assert project_dir.exists()
    assert not (project_dir / ".github").exists()


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
