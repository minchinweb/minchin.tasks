from invoke import task

from ._run import utf8_run


@task(help={"color": "Colourize output (disable with `--no-color`)"})
def build(ctx, publish=False, debug=False, carefully=False, color=True):
    """Build a local version of the blog."""

    config = "pelicanconf.py"
    if publish:
        config = "publishconf.py"

    carefully_cli = " --fatal=warnings" if carefully else ""
    debug_cli = " --debug" if debug else ""

    # pass color through
    env = {"FORCE_COLOR": "1"} if color else {}

    utf8_run(ctx, f"pelican -s {config}{debug_cli}{carefully_cli}", pty=False, env=env)


# TODO: serve, without blocking the prompt to wait for a return, allowing
#       setting port
