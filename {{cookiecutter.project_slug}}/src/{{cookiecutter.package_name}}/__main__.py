"""Entry point for running {{ cookiecutter.project_slug }} via `python -m {{ cookiecutter.package_name }}`."""

from {{ cookiecutter.package_name }}.cli import app, main

__all__ = ["app", "main"]

if __name__ == "__main__":
    main()
