"""Collect the add-on folder as a plain folder, not as a package.

The folder has an __init__.py, so pytest would treat it as a package and
import that file before running any test under it. That file needs Anki.
"""
from pathlib import Path

import pytest

ADDON = Path(__file__).resolve().parent.parent


def pytest_collect_directory(path, parent):
    if path == ADDON:
        return pytest.Dir.from_parent(parent, path=path)
    return None
