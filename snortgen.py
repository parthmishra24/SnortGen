"""Compatibility shim for running SnortGen as a script."""

from snortgen.cli import run

if __name__ == "__main__":  # pragma: no cover
    run()
