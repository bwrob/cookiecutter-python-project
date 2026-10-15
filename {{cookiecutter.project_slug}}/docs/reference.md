# API Reference

This page documents the API of **{{ cookiecutter.project_name }}**, automatically
generated from source code docstrings via **mkdocstrings**.

## Core Module

::: {{ cookiecutter.package_name }}.core
{% if cookiecutter.include_cli in [True, "yes", "true", "True", "1"] %}

## CLI Module

::: {{ cookiecutter.package_name }}.cli
{% endif %}
