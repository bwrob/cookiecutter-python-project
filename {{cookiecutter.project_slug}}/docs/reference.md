# API Reference

This page documents the API of **{{ cookiecutter.project_name }}**.

## Core Functions

Core functionality provided by the package.

### get_greeting

`get_greeting(name: str) -> str`

Generates a formatted greeting message.

- `name`: The name string to greet. Returns `"Hello, World!"` if blank.
- **Returns**: Formatted greeting string.

```python
from {{ cookiecutter.package_name }} import get_greeting

greeting = get_greeting("Alice")
```
{%- if cookiecutter.include_cli == "yes" %}

## CLI Application

Command-line interface commands and options.

### Subcommands

- `greet [NAME]`: Prints a styled greeting to standard output using Rich.
- `--version`: Displays the installed version and exits.
- `--help`: Displays help information.
{%- endif %}
