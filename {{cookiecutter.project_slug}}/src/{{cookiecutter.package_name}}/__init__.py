"""{{ cookiecutter.description }}"""

from {{ cookiecutter.package_name }}.core import get_greeting

__version__ = "{{ cookiecutter.version }}"
__all__ = ["__version__", "get_greeting"]
