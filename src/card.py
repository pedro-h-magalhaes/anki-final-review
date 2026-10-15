"""A card's score, its stability after an answer, and its state."""

from __future__ import annotations

from dataclasses import dataclass, replace
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


@dataclass(frozen=True)
class CardState:
    """What the queue knows about one card.

    Attributes:
        stability: From 0 to 100.
        t0: Seconds since the epoch of the last correct answer; without one,
            of the first answer, or of entering the queue.
        answers: Number of answers.
        correct: Number of those that were Good or Easy.
    """

    stability: float
    t0: float
    answers: int = 0
    correct: int = 0

    @property
    def rate(self) -> float:
        """Return the share of correct answers, or 0.5 with no answers."""
        return self.correct / self.answers if self.answers else 0.5

    def score_at(self, now: float, settings: Settings) -> float:
        """Return the score at `now`, in seconds since the epoch.

        Args:
            now: Seconds since the epoch; a time before `t0`, as from a clock
                set ahead, counts as `t0`.
            settings: Holds the pace constants.

        Returns:
            The score, from 0 to 100.
        """
        return score(max(0.0, now - self.t0), self.stability, settings)

    def answer(self, grade: Grade, at: float, settings: Settings) -> CardState:
        """Return the state after an answer with `grade` at time `at`.

        The stability moves with the rate and answers from before the answer;
        only a correct answer moves `t0` to `at`.

        Args:
            grade: The answer's grade.
            at: Seconds since the epoch.
            settings: Holds the formula constants.

        Returns:
            A new state; this one is left unchanged.
        """
        stability = next_stability(self.stability, grade, self.rate, self.answers, settings)
        if is_correct(grade):
            return replace(self, stability=stability, t0=at,
                           answers=self.answers + 1, correct=self.correct + 1)
        return replace(self, stability=stability, answers=self.answers + 1)


def new_card(entered_at: float, settings: Settings) -> CardState:
    """Return the state of a card with no answers.

    Args:
        entered_at: Seconds since the epoch when it entered the queue.
        settings: Holds the initial stability.

    Returns:
        A state at the initial stability whose score is 100 at `entered_at`.
    """
    return CardState(stability=settings.initial_stability, t0=entered_at)
