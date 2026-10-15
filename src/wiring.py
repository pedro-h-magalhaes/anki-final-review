"""Connect Anki to the add-on: the deck-list row, the deck window, the reviewer and the answers.

The only module besides `dialog.py` that imports from Anki. `register()` does
all of it, so importing the module changes nothing.
"""

from __future__ import annotations

import time

from anki.cards import Card
from anki.scheduler.v3 import QueuedCards, SchedulingContext
from aqt import gui_hooks, mw
from aqt.reviewer import Reviewer, V3CardInfo

from .counts import queue_counts
from .deck_row import OPEN, insert_row, message_action, row_html
from .decks import deck_search
from .dialog import DeckWindow
from .session import Session
from .settings import Settings

_session: Session | None = None
_original_get_next = Reviewer._get_next_v3_card

# SQLite limits how long one statement can be, so card ids go in chunks.
_CHUNK = 5000


def _settings() -> Settings:
    """Read the current add-on config into settings."""
    return Settings.from_config(mw.addonManager.getConfig(__name__) or {})


def _histories(col, search: str) -> dict[int, list[tuple[int, int]]]:
    """Return each eligible card's `(revlog_id, ease)` entries, by card id.

    Args:
        col: The open collection.
        search: The search from `deck_search`.

    Returns:
        Every card the search finds, with an empty list when it has no history.
    """
    card_ids = list(col.find_cards(search))
    histories: dict[int, list[tuple[int, int]]] = {cid: [] for cid in card_ids}
    for start in range(0, len(card_ids), _CHUNK):
        chunk = ",".join(str(cid) for cid in card_ids[start:start + _CHUNK])
        for cid, rid, ease in col.db.all(f"select cid, id, ease from revlog where cid in ({chunk})"):
            histories[cid].append((rid, ease))
    return histories


def _queues(col, card_ids: list[int]) -> list[int]:
    """Return the Anki queue number of each of `card_ids`."""
    queues: list[int] = []
    for start in range(0, len(card_ids), _CHUNK):
        chunk = ",".join(str(cid) for cid in card_ids[start:start + _CHUNK])
        queues.extend(col.db.list(f"select queue from cards where id in ({chunk})"))
    return queues


def _counts(col, settings: Settings) -> tuple[int, int, int]:
    """Return the new, learning and review counts of the chosen decks' eligible cards."""
    search = deck_search(settings.decks)
    if search is None:
        return (0, 0, 0)
    return queue_counts(_queues(col, list(col.find_cards(search))))


def _queue_kind(queue: int):
    """Map a card's Anki queue number to the kind the reviewer counts it under."""
    if queue == 0:
        return QueuedCards.NEW
    if queue in (1, 3):
        return QueuedCards.LEARNING
    return QueuedCards.REVIEW


def _get_next_v3_card(self: Reviewer) -> None:
    """Show the session's choice while the final review is open, else Anki's own card."""
    if _session is None:
        _original_get_next(self)
        return
    col = self.mw.col
    search = deck_search(_session.settings.decks)
    if search is None:
        return
    histories = _histories(col, search)
    card_id = _session.choose(histories, time.time())
    if card_id is None:
        return
    backend_card = col._backend.get_card(card_id)
    new_count, learning_count, review_count = queue_counts(_queues(col, list(histories)))
    queued = QueuedCards(
        cards=[QueuedCards.QueuedCard(
            card=backend_card,
            states=col._backend.get_scheduling_states(card_id),
            context=SchedulingContext(),
            queue=_queue_kind(backend_card.queue),
        )],
        new_count=new_count,
        learning_count=learning_count,
        review_count=review_count,
    )
    self._v3 = V3CardInfo.from_queue(queued)
    self.card = Card(col, backend_card=backend_card)
    self.card.start_timer()


def _clear_anki_queues(proceed_ease: tuple[bool, int], reviewer, card) -> tuple[bool, int]:
    """Empty Anki's cached study queues before a final-review answer.

    Anki refuses to answer a card that is not at the top of its own cached
    queue; saving the card again without an undo entry drops that cache.

    Args:
        proceed_ease: Whether the answer goes ahead, and its ease.
        reviewer: The reviewer about to answer.
        card: The card about to be answered.

    Returns:
        `proceed_ease` unchanged.
    """
    if _session is not None and proceed_ease[0]:
        col = reviewer.mw.col
        col.update_card(col.get_card(card.id), skip_undo_entry=True)
    return proceed_ease


def _on_answer(reviewer, card, ease) -> None:
    """Remember the answered card, so it does not come right back."""
    if _session is not None:
        _session.record_answer(card.id)


def _on_config_saved(config: dict) -> None:
    """Use the new settings at the next choice and redraw the deck list's counts."""
    if _session is not None:
        _session.settings = Settings.from_config(config)
    if mw.state == "deckBrowser":
        mw.deckBrowser.refresh()


def _on_render(deck_browser, content) -> None:
    """Put the Final Review row, with its counts, first in the deck list."""
    content.tree = insert_row(content.tree, row_html(_counts(mw.col, _settings())))


def _on_js_message(handled: tuple[bool, object], message: str, context) -> tuple[bool, object]:
    """Answer the Final Review row's clicks and leave every other message to Anki.

    Args:
        handled: Whether an earlier handler took the message, and its result.
        message: The string the page passed to `pycmd`.
        context: The page's owner, unused.

    Returns:
        `(True, None)` for the row's clicks, else `handled` unchanged.
    """
    action = message_action(message)
    if action is None:
        return handled
    if action == OPEN:
        _start()
    else:
        _open_deck_window()
    return (True, None)


def _start() -> None:
    """Start a final review on the chosen decks and open the study screen.

    With no chosen deck that exists, the deck window opens instead.
    """
    global _session
    settings = _settings()
    deck_ids = [mw.col.decks.id_for_name(name) for name in settings.decks]
    deck_ids = [did for did in deck_ids if did]
    if not deck_ids:
        _open_deck_window()
        return
    _session = Session(settings)
    mw.col.decks.select(deck_ids[0])
    mw.col.startTimebox()
    mw.moveToState("review")


def _open_deck_window() -> None:
    """Let the student check the decks, then save them and redraw the deck list."""
    decks = mw.col.decks.all_names_and_ids(skip_empty_default=True, include_filtered=False)
    window = DeckWindow(mw, [deck.name for deck in decks], list(_settings().decks))
    if not window.exec():
        return
    config = mw.addonManager.getConfig(__name__) or {}
    config["decks"] = window.chosen
    mw.addonManager.writeConfig(__name__, config)
    mw.deckBrowser.refresh()


def _on_state_change(new_state: str, old_state: str) -> None:
    """End the final review when the study screen closes, by any path."""
    global _session
    if new_state != "review":
        _session = None


def register() -> None:
    """Hook the deck list, the row's clicks, the reviewer, the answers and the state changes."""
    Reviewer._get_next_v3_card = _get_next_v3_card
    gui_hooks.reviewer_will_answer_card.append(_clear_anki_queues)
    gui_hooks.reviewer_did_answer_card.append(_on_answer)
    gui_hooks.deck_browser_will_render_content.append(_on_render)
    gui_hooks.webview_did_receive_js_message.append(_on_js_message)
    gui_hooks.state_did_change.append(_on_state_change)
    mw.addonManager.setConfigUpdatedAction(__name__, _on_config_saved)
