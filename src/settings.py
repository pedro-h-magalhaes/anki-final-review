"""The add-on's settings: every constant of the formulas and the chosen decks."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """The constants the formulas use, with the defaults from `Cálculos da fila`.

    Attributes:
        decks: Names of the decks that take part in the final review.
        min_pace: Seconds the score takes to fall from 100 to 1 at stability 0.
        max_pace: The same at stability 100.
        initial_stability: Stability of a card with no answers.
        answers_to_cross: Answers in a row, for Again, Hard, Good and Easy,
            that take a card from one end of the scale to 1 point from the other.
        rate_band: How many times faster a card with every answer correct moves.
        volume_brake: The smallest share of the speed the volume allows.
        half_volume: Answers at which the volume weight reaches one half.
    """

    decks: tuple[str, ...] = ()
    min_pace: float = 60.0
    max_pace: float = 14_400.0
    initial_stability: float = 20.0
    answers_to_cross: tuple[float, float, float, float] = (3.0, 9.0, 9.0, 3.0)
    rate_band: float = 3.0
    volume_brake: float = 0.05
    half_volume: float = 15.0
