"""Connect Anki to the add-on.

The only module that will import from Anki. `register()` does all of it, so
importing the module changes nothing. Empty until the add-on is packaged.
"""

from __future__ import annotations


def register() -> None:
    """Connect Anki's hooks to the add-on. Nothing to connect yet."""
