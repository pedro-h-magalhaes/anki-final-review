"""Which decks the deck window locks and which it saves."""

from __future__ import annotations

from collections.abc import Iterable


def locked_names(names: Iterable[str], checked: Iterable[str]) -> set[str]:
    """Return the decks a checked ancestor already brings in.

    Args:
        names: Every deck's full name, such as `"Biology::Cells"`.
        checked: The full names the student checked.

    Returns:
        The names under a checked deck, which the window shows checked and locked.
    """
    checked = set(checked)
    return {name for name in names if any(a in checked for a in _ancestors(name))}


def chosen_names(names: Iterable[str], checked: Iterable[str]) -> list[str]:
    """Return the decks to save from what the student checked.

    Drops a checked name that no longer exists and one under a checked deck,
    since the deck search already brings in subdecks.

    Args:
        names: Every deck's full name.
        checked: The full names the student checked.

    Returns:
        The names to save, sorted.
    """
    names = list(names)
    checked = set(checked) & set(names)
    return sorted(checked - locked_names(names, checked))


def _ancestors(name: str) -> list[str]:
    """Return the full names of the decks above `name`, top first."""
    parts = name.split("::")
    return ["::".join(parts[:end]) for end in range(1, len(parts))]
