import keyword
import re
import sys

PACKAGE_REGEX = r"^[a-zA-Z][_a-zA-Z0-9]*$"
package_name = "{{ cookiecutter.package_name }}"

if not re.match(PACKAGE_REGEX, package_name) or keyword.iskeyword(package_name):
    print(
        f"ERROR: The package name '{package_name}' is not a valid Python package name. "
        "It must start with a letter, contain only alphanumeric characters and underscores, "
        "and must not be a Python reserved keyword."
    )
    sys.exit(1)

PROJECT_SLUG_REGEX = r"^[-a-zA-Z0-9_]+$"
project_slug = "{{ cookiecutter.project_slug }}"

if not re.match(PROJECT_SLUG_REGEX, project_slug):
    print(
        f"ERROR: The project slug '{project_slug}' is invalid. "
        "It can only contain alphanumeric characters, dashes, and underscores."
    )
    sys.exit(1)
