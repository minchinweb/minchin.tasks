Minchin.Tasks
=============

Common development tasks for use with `Invoke <https://www.pyinvoke.org/>`_.
Defaults to a ``uv`` and ``ruff`` setup, but should continue to work with
``black``, ``isort``, and ``pip-tools``. Useful for applying my in-house Python
style, see https://github.com/minchinweb/python-style-guide

In your ``tasks.py`` (import each for clarity)::

    from minchin.tasks import check, format_code, lint, test, update, upgrade  # noqa: F401
    from minchin.tasks import pelican_build  # noqa: F401


This gives you:

- ``invoke update`` -- update requirements to the current versions
- ``invoke upgrade`` -- install the locked requirements
- ``invoke lint`` -- report only format check, including ``pyproject.toml``
- ``invoke format`` -- fix formatting issues
- ``invoke test`` -- runs ``pytest`` by default, or the command set in
  ``minchin_tasks.test_command`` in ``invoke.yaml``. A custom command is run as
  written: prefix it with ``uv run`` and add (no) color explicitly if needed.
  If unset, ``releaser.test_command`` is used, unless it starts with ``inv``
  (i.e. *invoke*).
- ``invoke check`` -- ``lint`` and ``test``.
- ``invoke pelican-build`` -- build the local Pelican site


Sample ``invoke.yaml`` configuration::

  # invoke.yaml
  minchin_tasks:
    test_command: uv run battlestation test app --keepdb --noinput --color=always
