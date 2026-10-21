"""Run subprocesses with UTF-8 output passed through intact."""

from __future__ import annotations

# Without these, Python tools (e.g. `black`) piped through Invoke on Windows
# write with the legacy code page and escape non-ASCII output (emoji, etc.)
_UTF8_ENV = {"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}


def utf8_run(ctx, command, env=None, **kwargs):
    """`ctx.run()`, but decode and ask the subprocess to emit UTF-8."""
    return ctx.run(
        command,
        env={**_UTF8_ENV, **(env or {})},
        encoding="utf-8",
        **kwargs,
    )
