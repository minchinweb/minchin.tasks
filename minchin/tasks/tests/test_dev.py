"""Tests for the shared development tasks."""

from __future__ import annotations

from invoke import Collection, Context

from minchin.tasks import dev as tasks


class RecordingContext(Context):
    """Stands in for an Invoke context and records the commands it is given."""

    def __init__(self):
        super().__init__()
        self.commands = []

    def run(self, command, **kwargs):
        self.commands.append((command, kwargs))


def run_task(task):
    ctx = RecordingContext()
    task(ctx)
    return ctx.commands


def test_update_and_upgrade_mirror_apt():
    assert run_task(tasks.update)[0][0] == "uv lock --upgrade"
    assert run_task(tasks.upgrade)[0][0] == "uv sync"


def test_lint_changes_nothing_and_checks_pyproject():
    commands = [c for c, _ in run_task(tasks.lint)]
    assert commands == [
        "uv run ruff check",
        "uv run ruff format --check",
        "uv run validate-pyproject pyproject.toml",
        "uv run taplo format --colors always --check pyproject.toml",
    ]


def test_format_still_formats_when_lint_fixes_fail():
    commands = run_task(tasks.format_code)
    assert commands[0][0].rstrip() == "uv run ruff check --fix"
    assert commands[0][1]["warn"] is True
    assert [c for c, _ in commands[1:]] == [
        "uv run ruff format",
        "uv run taplo format --colors always pyproject.toml",
    ]


def test_task_names_match_the_documented_commands():
    names = set(Collection.from_module(tasks).task_names)
    assert names == {"check", "format", "lint", "test", "update", "upgrade"}


def test_check_runs_lint_then_test():
    assert [t.__name__ for t in tasks.check.pre] == ["lint", "test"]
