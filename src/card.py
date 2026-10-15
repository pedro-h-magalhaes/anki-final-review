"""A card's score, its stability after an answer, and its state."""

from __future__ import annotations

from enum import IntEnum

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


class Grade(IntEnum):
    """An answer's grade, numbered like Anki's `ease`."""

    AGAIN = 1
    HARD = 2
    GOOD = 3
    EASY = 4


def is_correct(grade: Grade) -> bool:
    """Return True for Good and Easy, False for Again and Hard."""
    return grade >= Grade.GOOD


def next_stability(
    stability: float, grade: Grade, rate: float, answers: int, settings: Settings
) -> float:
    """Return the stability after one answer.

    A correct answer cuts the distance to 100, a wrong one the distance to 0,
    by `k ** e`, where `e` grows with the hit rate and the number of answers.

    Args:
        stability: From 0 to 100, before the answer.
        grade: The answer's grade.
        rate: Share of correct answers before this one, from 0 to 1.
        answers: Number of answers before this one.
        settings: Holds the grade, rate and volume constants.

    Returns:
        The new stability, from 0 to 100.
    """
    cut = 0.01 ** (1 / settings.answers_to_cross[grade - 1])
    weight = answers**3 / (answers**3 + settings.half_volume**3)
    brake = settings.volume_brake
    if is_correct(grade):
        e = settings.rate_band ** (2 * rate - 1) * (brake + (1 - brake) * weight)
        return 100 - (100 - stability) * cut**e
    e = settings.rate_band ** (1 - 2 * rate) * (1 - (1 - brake) * weight)
    return stability * cut**e
