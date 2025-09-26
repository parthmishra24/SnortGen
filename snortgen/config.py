"""Utility helpers for locating SnortGen data files."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
from typing import Final

try:  # Python 3.9+
    from importlib import resources
except ImportError:  # pragma: no cover
    import importlib_resources as resources  # type: ignore

PACKAGE_DATA_DIR: Final[str] = "snortgen.data"
USER_DATA_ENV: Final[str] = "SNORTGEN_HOME"
DEFAULT_USER_DIR: Final[Path] = Path.home() / ".snortgen"


def get_user_data_dir() -> Path:
    """Return the directory used to persist user-specific SnortGen data."""
    base = os.getenv(USER_DATA_ENV)
    if base:
        directory = Path(base).expanduser().resolve()
    else:
        directory = DEFAULT_USER_DIR
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def ensure_user_data_file(filename: str) -> Path:
    """Ensure a data file exists in the user directory and return its path."""
    user_dir = get_user_data_dir()
    user_file = user_dir / filename
    if user_file.exists():
        return user_file

    try:
        with resources.files(PACKAGE_DATA_DIR).joinpath(filename).open("rb") as src, user_file.open("wb") as dst:
            shutil.copyfileobj(src, dst)
    except FileNotFoundError:
        # If the packaged file is missing just create an empty placeholder
        user_file.touch(exist_ok=True)
    return user_file


def get_packaged_file(filename: str) -> Path:
    """Return the path to a packaged data file."""
    with resources.as_file(resources.files(PACKAGE_DATA_DIR).joinpath(filename)) as path:
        return path
