"""Build the Anki search for the eligible cards of the chosen decks."""

from __future__ import annotations

from collections.abc import Sequence


def deck_search(decks: Sequence[str]) -> str | None:
    """Return a search for the chosen decks' cards that are neither suspended nor buried.

    Each name is quoted and its `\\`, `"`, `_` and `*` escaped, so it matches
    that deck and its subdecks, never a pattern.

    Args:
        decks: Full deck names.

    Returns:
        The search, or None when `decks` is empty.
    """
    if not decks:
        return None
    terms = " OR ".join(f'"deck:{_escape(name)}"' for name in decks)
    return f"({terms}) -is:suspended -is:buried"


def _escape(name: str) -> str:
    for char in '\\"_*':
        name = name.replace(char, "\\" + char)
    return name
