"""The add-on's settings: every constant of the formulas and the chosen decks."""

from __future__ import annotations

import math
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any


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

    @classmethod
    def from_config(cls, config: Mapping[str, Any]) -> Settings:
        """Read the add-on config into settings.

        A missing value, a value of the wrong type or one out of range takes
        that key's default; a maximum pace not above the minimum restores both.

        Args:
            config: The dict Anki loads from `config.json` and the config screen.

        Returns:
            The settings, every value checked.
        """
        default = cls()
        min_pace = _number(config.get("min_pace_seconds"), default.min_pace, lambda v: v > 0)
        max_pace = _number(config.get("max_pace_seconds"), default.max_pace, lambda v: v > 0)
        if max_pace <= min_pace:
            min_pace, max_pace = default.min_pace, default.max_pace
        crossing = config.get("answers_to_cross")
        crossing = crossing if isinstance(crossing, Mapping) else {}
        decks = config.get("decks")
        decks = decks if isinstance(decks, list) else []
        return cls(
            decks=tuple(d for d in decks if isinstance(d, str) and d.strip()),
            min_pace=min_pace,
            max_pace=max_pace,
            initial_stability=_number(
                config.get("initial_stability"), default.initial_stability, lambda v: 0 <= v <= 100
            ),
            answers_to_cross=tuple(
                _number(crossing.get(name), fallback, lambda v: v > 0)
                for name, fallback in zip(GRADE_KEYS, default.answers_to_cross)
            ),
            rate_band=_number(config.get("rate_band"), default.rate_band, lambda v: v >= 1),
            volume_brake=_number(config.get("volume_brake"), default.volume_brake, lambda v: 0 < v <= 1),
            half_volume=_number(config.get("answers_for_half_volume"), default.half_volume, lambda v: v > 0),
        )


GRADE_KEYS = ("again", "hard", "good", "easy")


def _number(value: Any, default: float, valid: Callable[[float], bool]) -> float:
    """Return `value` when it is a finite number that passes `valid`, else `default`."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return default
    if not math.isfinite(value) or not valid(value):
        return default
    return value
