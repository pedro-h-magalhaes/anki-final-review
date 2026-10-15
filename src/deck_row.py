"""The "Final Review" row of Anki's deck list: its HTML, its place and its clicks."""

from __future__ import annotations

OPEN = "open"
OPTIONS = "options"

_PREFIX = "final_review:"
_DRAG_ROW = "<tr class='top-level-drag-row'>"
_CELL = "style='padding: 4px 12px'"


def row_html(counts: tuple[int, int, int]) -> str:
    """Return the table row that opens the final review.

    Copies Anki's deck row with the name in the filtered-deck blue; the `tr`
    has no `deck` class, so Anki's drag and drop leaves it alone.

    Args:
        counts: The new, learning and review counts.

    Returns:
        One `<tr>` element.
    """
    new, learning, review = counts
    cells = "".join(
        f"<td align=end {_CELL}>{_count(number, klass)}</td>"
        for number, klass in ((new, "new-count"), (learning, "learn-count"), (review, "review-count"))
    )
    return (
        "<tr class='final-review'>"
        f"<td class=decktd colspan=5 {_CELL}><span class=collapse></span>"
        f"<a class='deck filtered' href=# onclick='return pycmd(\"{_PREFIX}{OPEN}\")'>"
        "Final Review</a></td>"
        f"{cells}"
        f"<td align=center class=opts {_CELL}>"
        f"<a onclick='return pycmd(\"{_PREFIX}{OPTIONS}\")'>"
        "<img src='/_anki/imgs/gears.svg' class=gears></a></td></tr>"
    )


def insert_row(tree: str, row: str) -> str:
    """Put `row` first among the decks of Anki's deck tree HTML.

    It goes after the top-level drag row; without one, after the first row,
    which is the header; without any row, at the start.

    Args:
        tree: The `tree` section Anki is about to render.
        row: The row from `row_html`.

    Returns:
        The tree with the row in it.
    """
    start = max(tree.find(_DRAG_ROW), 0)
    end = tree.find("</tr>", start)
    if end == -1:
        return row + tree
    end += len("</tr>")
    return tree[:end] + row + tree[end:]


def message_action(message: str) -> str | None:
    """Return which of the row's clicks `message` is.

    Args:
        message: The string a page passed to `pycmd`.

    Returns:
        `OPEN` or `OPTIONS`, or None for any other message.
    """
    if not message.startswith(_PREFIX):
        return None
    action = message[len(_PREFIX):]
    return action if action in (OPEN, OPTIONS) else None


def _count(number: int, klass: str) -> str:
    """Wrap a count the way Anki does, greyed out when it is zero."""
    return f'<span class="{klass if number else "zero-count"}">{number}</span>'
