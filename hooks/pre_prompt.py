"""Pre-prompt validation hook executed before any questions are asked.

Validates that system prerequisites (Python version, uv, and git) are installed.
"""

import shutil
import sys

MIN_PYTHON_VERSION = (3, 12)


def main() -> None:
    if sys.version_info < MIN_PYTHON_VERSION:
        version_str = f"{sys.version_info.major}.{sys.version_info.minor}"
        print(
            f"ERROR: Zenith requires Python {MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]}+ "
            f"to generate projects. Current version: {version_str}",
            file=sys.stderr,
        )
        sys.exit(1)

    if shutil.which("uv") is None:
        print(
            "ERROR: Zenith projects require 'uv' for dependency management and builds.\n"
            "Please install uv before continuing: https://docs.astral.sh/uv/getting-started/installation/",
            file=sys.stderr,
        )
        sys.exit(1)

    if shutil.which("git") is None:
        print(
            "ERROR: Zenith projects require 'git' to be installed and available in PATH.",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
