"""Choose the next card: the lowest score, then the lowest stability."""

from __future__ import annotations

from collections.abc import Mapping

from .card import CardState
from .settings import Settings


def next_card(
    states: Mapping[int, CardState],
    now: float,
    settings: Settings,
    exclude: int | None = None,
) -> int | None:
    """Return the id of the card to show next.

    Compares (score, stability, id); `exclude` is skipped unless it is the
    only card left.

    Args:
        states: Every eligible card's state, by card id.
        now: Seconds since the epoch.
        settings: Holds the pace constants.
        exclude: The card just answered, or None.

    Returns:
        A card id, or None when `states` is empty.
    """
    candidates = [cid for cid in states if cid != exclude] or list(states)
    if not candidates:
        return None
    return min(
        candidates,
        key=lambda cid: (states[cid].score_at(now, settings), states[cid].stability, cid),
    )
