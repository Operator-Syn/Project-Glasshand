"""Report the interpreter, host and library versions a notebook is running against.

Why this module exists: a notebook that prints its environment in a cell cannot be
tested or reused, and a stale output can show versions from a kernel that no longer
exists. Keeping the collection here makes the check callable from a notebook, a test
or a shell one-liner with the same result.
"""

from __future__ import annotations

import platform
import sys
from dataclasses import dataclass
from importlib import metadata

# Distributions this workspace depends on, by their installed package name.
TRACKED_PACKAGES = ("numpy", "pandas", "matplotlib")


@dataclass(frozen=True)
class EnvironmentReport:
    """A snapshot of the runtime a notebook is executing in."""

    interpreter: str
    python_version: str
    host: str
    packages: dict[str, str]

    def format_lines(self) -> list[str]:
        """Render the report as aligned ``label: value`` lines for printing."""
        rows = [
            ("interpreter", self.interpreter),
            ("python", self.python_version),
            ("host", self.host),
        ]
        rows.extend((name, version) for name, version in self.packages.items())
        width = max(len(label) for label, _ in rows)
        return [f"{label:<{width}} : {value}" for label, value in rows]


def installed_version(package: str) -> str:
    """Return the installed version of ``package``, or ``"missing"`` if it is absent."""
    try:
        return metadata.version(package)
    except metadata.PackageNotFoundError:
        return "missing"


def collect(packages: tuple[str, ...] = TRACKED_PACKAGES) -> EnvironmentReport:
    """Build a report for the running interpreter.

    Args:
        packages: distribution names to look up; defaults to this workspace's stack.

    Returns:
        An :class:`EnvironmentReport` describing interpreter, Python version, host and
        the version of each requested package.

    ``sys.executable`` is the field that matters: it distinguishes the project's
    ``.venv`` from whichever other interpreter a kernelspec might point at.
    """
    return EnvironmentReport(
        interpreter=sys.executable,
        python_version=platform.python_version(),
        host=platform.node(),
        packages={name: installed_version(name) for name in packages},
    )
