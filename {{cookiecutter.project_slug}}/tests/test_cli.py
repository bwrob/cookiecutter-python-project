"""Unit tests for the command-line interface."""

import pytest
from typer.testing import CliRunner

from {{ cookiecutter.package_name }}.cli import app, main

runner = CliRunner()


def test_cli_help() -> None:
    """Test CLI help flag outputs command information."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.stdout or "Options:" in result.stdout


def test_cli_version() -> None:
    """Test CLI version option outputs version."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "{{ cookiecutter.project_slug }}" in result.stdout


def test_cli_greet() -> None:
    """Test CLI greet subcommand."""
    result = runner.invoke(app, ["greet", "Developer"])
    assert result.exit_code == 0
    assert "Hello, Developer!" in result.stdout


def test_cli_main(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test main entry point invocation."""
    monkeypatch.setattr("sys.argv", ["{{ cookiecutter.project_slug }}", "--help"])
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0
