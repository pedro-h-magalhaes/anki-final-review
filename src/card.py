"""A card's score, its stability after an answer, and its state."""

from __future__ import annotations

from .settings import Settings


def pace(stability: float, settings: Settings) -> float:
    """Return the seconds the score takes to fall from 100 to 1.

    Args:
        stability: From 0 to 100.
        settings: Holds the minimum and maximum pace.

    Returns:
        The pace in seconds, growing geometrically with stability.
    """
    ratio = settings.max_pace / settings.min_pace
    return settings.min_pace * ratio ** (stability / 100)


def score(elapsed: float, stability: float, settings: Settings) -> float:
    """Return the retrievability score after `elapsed` seconds.

    Args:
        elapsed: Seconds since `t0`; 0 or more.
        stability: From 0 to 100.
        settings: Holds the pace constants.

    Returns:
        100 at `elapsed = 0`, 1 after one pace, and 0.0 once the value is too
        small for a float.
    """
    return 100.0 ** (1 - elapsed / pace(stability, settings))
