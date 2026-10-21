"""Invoke tasks; run with ``uv run invoke --list``."""

from __future__ import annotations

from minchin.tasks import (check, format_code, lint, test,  # noqa: F401
                           update, upgrade)

try:
    from minchin.releaser import make_release  # noqa: F401
except ImportError:
    print("[WARN] minchin.releaser not installed.")
