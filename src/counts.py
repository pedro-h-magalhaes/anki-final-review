"""Count the eligible cards the way the reviewer's footer shows them."""

from __future__ import annotations

from collections.abc import Iterable


def queue_counts(queues: Iterable[int]) -> tuple[int, int, int]:
    """Return how many cards are new, in learning and in review.

    Queue 0 is new, queues 1 and 3 are learning, and any other queue counts
    as review.

    Args:
        queues: Each eligible card's Anki queue number.

    Returns:
        The new, learning and review counts.
    """
    new = learning = review = 0
    for queue in queues:
        if queue == 0:
            new += 1
        elif queue in (1, 3):
            learning += 1
        else:
            review += 1
    return new, learning, review
