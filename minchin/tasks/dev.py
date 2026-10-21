"""Common development tasks (lint, format, test, ...) to use from `invoke`.

Uses ``uv run`` under the hood by default, or ``pip-tools`` on "legacy" setups.
"""

from __future__ import annotations

import sys
from pathlib import Path

from invoke import task

from minchin.text import title

__all__ = ["check", "format_code", "lint", "test", "update", "upgrade"]


def _uses_uv() -> bool:
    # A `uv.lock` implies the project is managed by uv
    return Path("uv.lock").is_file()


def _pip_tools_inputs() -> list[Path]:
    # look for `.in` files in both `.requirements/*.in` or the repo root `*.in`
    found = [*Path(".requirements").glob("*.in"), *Path().glob("*.in")]
    # blacklist `MANIFEST.in` as a setuptools file
    return sorted(p for p in found if p.name.lower() != "manifest.in")


def _compiled_requirements() -> dict[str, Path]:
    """Get a list of the requirement files.

    `requirements-base.in` is assumed to the "main" one.
    """
    found = {}
    for path in _pip_tools_inputs():
        compiled = path.with_suffix(".txt")
        if not compiled.is_file():
            continue
        name = compiled.stem.removeprefix("requirements").lstrip("-_")
        if name in ("", "base"):
            name = "main"
        found[name] = compiled
    return found


def _uses_black() -> bool:
    # Black/isort config in `pyproject.toml` without a ruff config
    pyproject = Path("pyproject.toml")
    if not pyproject.is_file():
        return False
    text = pyproject.read_text(encoding="utf-8")
    legacy = "[tool.black]" in text or "[tool.isort]" in text
    return legacy and "[tool.ruff" not in text


def _run_prefix() -> str:
    # run uv projects using `uv`
    return "uv run " if _uses_uv() else ""


@task
def update(ctx):
    """Refresh the requirements with the current versions.

    Rewrites `uv.lock`, or recompiles pip-tools' `.txt`.
    """
    title("Update python requirements to latest versions")

    if _uses_uv():
        ctx.run("uv lock --upgrade", pty=False)
        return
    inputs = _pip_tools_inputs()
    if not inputs:
        raise SystemExit("No `uv.lock` or pip-tools `.in` files found.")
    for source in inputs:
        ctx.run(f"pip-compile --upgrade {source.as_posix()}", pty=False)


@task(
    iterable=["extra"],
    help={
        "extra": "Also install this requirements set, e.g. `dev` ("
        "pip-tools projects only)",
        "all_": "Install every compiled requirements file (pip-tools only)",
        "dry_run": "Show what would change without installing anything",
    },
)
def upgrade(ctx, extra=None, all_=False, dry_run=False):
    """Install based on the current requiremnts.

    Runs `uv sync`, or `pip-sync` on the main compiled pip-tools file plus any
    sets named with `--extra` (or all of them with `--all`).

    Use `--dry-run` to check first.
    """
    title(
        "Upgrade python requirements to version specified in requirements files/uv.lock"
    )

    flag = " --dry-run" if dry_run else ""
    if _uses_uv():
        ctx.run(f"uv sync{flag}", pty=False)
        return
    available = _compiled_requirements()
    if not available:
        raise SystemExit("No `uv.lock` or compiled pip-tools `.txt` files found.")
    names = list(available) if all_ else ["main", *(extra or [])]
    unknown = [n for n in names if n not in available]
    if unknown:
        raise SystemExit(
            f"No compiled requirements for: {', '.join(unknown)}. "
            f"Available: {', '.join(available)}."
        )
    # pip-sync wants each file once; keep the order given
    files = dict.fromkeys(available[n].as_posix() for n in names)
    ctx.run(f"python -m piptools sync{flag} {' '.join(files)}", pty=False)


@task
def lint(ctx):
    """Check code, formatting and `pyproject.toml`."""
    title("Check code formatting")

    run = _run_prefix()
    if _uses_black():
        ctx.run(f"{run}black --check .", pty=False)
        ctx.run(f"{run}isort --check-only .", pty=False)
        print(
            "WARNING: pyproject.toml was not checked (validate-pyproject and "
            "taplo only run for ruff projects); review it by hand.",
            file=sys.stderr,
        )
        return

    ctx.run("uv run ruff check", pty=False)
    ctx.run("uv run ruff format --check", pty=False)
    ctx.run("uv run validate-pyproject pyproject.toml", pty=False)
    ctx.run("uv run taplo format --check pyproject.toml", pty=False)


# named `format_code` so it doesn't shadow the builtin (ruff rule `A`)
@task(name="format")
def format_code(ctx):
    """Apply safe lint fixes, import sorting and formatting (code and TOML)."""
    title("Fix code formatting")

    if _uses_black():
        run = _run_prefix()
        ctx.run(f"{run}isort .", pty=False)
        ctx.run(f"{run}black .", pty=False)
        return

    # unfixable problems exit non-zero; still format, `lint` reports them
    ctx.run("uv run ruff check --fix", pty=False, warn=True)
    ctx.run("uv run ruff format", pty=False)
    ctx.run("uv run taplo format pyproject.toml", pty=False)


@task
def test(ctx):
    """Run the test suite.

    Assumes `pytest`.
    """
    ctx.run(f"{_run_prefix()}pytest", pty=False)
    title("Run test suite")


@task(pre=[lint, test])
def check(ctx):
    """lint, formatting and tests.

    Useful for single-run CI runs.
    """
