"""One final review: when each card entered and which card was just answered."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from .card import CardState
from .history import rebuild
from .review_queue import next_card
from .settings import Settings


class Session:
    """The state of one final review between turning it on and off.

    Attributes:
        settings: The constants in use; replaced when the config changes.
        last_answered: The id of the card answered last, or None.
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.last_answered: int | None = None
        self._first_seen: dict[int, float] = {}

    def states(
        self, histories: Mapping[int, Sequence[tuple[int, int]]], now: float
    ) -> dict[int, CardState]:
        """Rebuild every eligible card from its history.

        A card seen for the first time is remembered as entering at `now`.

        Args:
            histories: Each eligible card's `(revlog_id, ease)` entries, by id.
            now: Seconds since the epoch.

        Returns:
            Each card's state, by id.
        """
        return {
            cid: rebuild(entries, self._first_seen.setdefault(cid, now), self.settings)
            for cid, entries in histories.items()
        }

    def choose(
        self, histories: Mapping[int, Sequence[tuple[int, int]]], now: float
    ) -> int | None:
        """Return the card to show next.

        Args:
            histories: Each eligible card's `(revlog_id, ease)` entries, by id.
            now: Seconds since the epoch.

        Returns:
            A card id, or None when there are no eligible cards.
        """
        return next_card(self.states(histories, now), now, self.settings, self.last_answered)

    def record_answer(self, card_id: int) -> None:
        """Remember `card_id` as the card just answered.

        Args:
            card_id: The answered card's id.
        """
        self.last_answered = card_id
