"""Command line interface for {{ cookiecutter.project_slug }}."""

import typer
from rich.console import Console

from {{ cookiecutter.package_name }} import __version__
from {{ cookiecutter.package_name }}.core import get_greeting

app = typer.Typer(
    name="{{ cookiecutter.project_slug }}",
    help="{{ cookiecutter.description }}",
    no_args_is_help=True,
)
console = Console()


def version_callback(value: bool) -> None:
    """Print the version and exit.

    Raises
    ------
    typer.Exit
        Always exits when version flag is given.

    """
    if value:
        msg = (
            f"[bold cyan]{{ cookiecutter.project_slug }}[/bold cyan] "
            f"version [green]{__version__}[/green]"
        )
        console.print(msg)
        raise typer.Exit


@app.callback()
def main_callback(
    _version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Show version and exit.",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """Entry point callback for global options."""


@app.command()
def greet(
    name: str = typer.Argument("World", help="The name to greet."),
) -> None:
    """Display a personalized greeting."""
    greeting = get_greeting(name)
    console.print(f"[bold green]✨ {greeting}[/bold green]")


def main() -> None:
    """Execute the CLI application."""
    app()


if __name__ == "__main__":
    main()
