Minchin.Tasks
=============

Common development tasks for use with `Invoke <https://www.pyinvoke.org/>`_.
Defaults to a ``uv`` and ``ruff`` setup, but should continue to work with
``black``, ``isort``, and ``pip-tools``. Useful for applying my in-house Python
style, see https://github.com/minchinweb/python-style-guide

In your ``tasks.py`` (import each for clarity)::

    from minchin.tasks import check, format_code, lint, test, update, upgrade  # noqa: F401

The tasks are defined in ``minchin.tasks.dev``; ``minchin.tasks`` re-exports them.

This gives you:

- ``invoke update`` -- update requirements to the current versions
- ``invoke upgrade`` -- install the locked requirements
- ``invoke lint`` -- report only format check, including ``pyproject.toml``
- ``invoke format`` -- fix formatting issues
- ``invoke test`` -- run ``pytest``.
- ``invoke check`` -- ``lint`` and ``test``.
