"""Rebuild a card's state from its entries in Anki's review history."""

from __future__ import annotations

from collections.abc import Iterable

from .card import CardState, Grade, new_card
from .settings import Settings


def rebuild(
    entries: Iterable[tuple[int, int]], entered_at: float, settings: Settings
) -> CardState:
    """Return the card's state after every graded answer in its history.

    Sorts the entries by time, skips those without a grade, and replays the
    rest from a new card whose `t0` is the first graded answer.

    Args:
        entries: `(revlog_id, ease)` pairs; the id is in milliseconds since
            the epoch, and an ease outside 1 to 4 marks an entry without a grade.
        entered_at: Seconds since the epoch when the card entered the queue,
            used only when no entry is graded.
        settings: Holds the formula constants.

    Returns:
        The rebuilt state.
    """
    graded = sorted((rid, ease) for rid, ease in entries if 1 <= ease <= 4)
    if not graded:
        return new_card(entered_at, settings)
    card = new_card(graded[0][0] / 1000, settings)
    for rid, ease in graded:
        card = card.answer(Grade(ease), rid / 1000, settings)
    return card
