"""Common development tasks to use from `invoke`.

In a project's ``tasks.py``::

    from minchin.tasks import (  # noqa: F401
        check,
        format_code,
        lint,
        test,
        update,
        upgrade,
    )

Uses ``uv run`` under the hood by default, or ``pip-tools`` on "legacy" setups.
The tasks themselves live in `minchin.tasks.dev`.
"""

from __future__ import annotations

from minchin.tasks.dev import check, format_code, lint, test, update, upgrade
from minchin.tasks.pelican import build as pelican_build

__version__ = "1.1.2"

__all__ = ["check", "format_code", "lint", "pelican_build", "test", "update", "upgrade"]
