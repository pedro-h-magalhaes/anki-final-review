from src.deck_row import OPEN, OPTIONS, insert_row, message_action, row_html

HEADER = "<tr><th colspan=5 align=start>Deck</th></tr>"
DRAG = "<tr class='top-level-drag-row'><td colspan='6'>&nbsp;</td></tr>"
DECK = "<tr class='deck' id='1'><td>Coding</td></tr>"


def test_the_row_shows_new_learning_and_review_in_order():
    row = row_html((11, 2, 576))
    new = row.index('<span class="new-count">11</span>')
    learning = row.index('<span class="learn-count">2</span>')
    review = row.index('<span class="review-count">576</span>')
    assert new < learning < review


def test_a_zero_count_is_greyed_out_like_anki_does():
    row = row_html((0, 1, 1))
    assert '<span class="zero-count">0</span>' in row
    assert "new-count" not in row


def test_the_name_is_blue_like_a_filtered_deck():
    assert "<a class='deck filtered'" in row_html((0, 0, 0))
    assert ">Final Review</a>" in row_html((0, 0, 0))


def test_the_row_is_left_out_of_anki_drag_and_drop():
    row = row_html((0, 0, 0))
    assert row.startswith("<tr class='final-review'>")
    assert "<tr class='deck" not in row


def test_the_name_opens_and_the_gear_opens_the_options():
    row = row_html((0, 0, 0))
    assert 'pycmd("final_review:open")' in row
    assert 'pycmd("final_review:options")' in row
    assert "gears.svg" in row


def test_the_row_goes_right_after_the_drag_row():
    assert insert_row(HEADER + DRAG + DECK, "<R>") == HEADER + DRAG + "<R>" + DECK


def test_without_a_drag_row_the_row_goes_after_the_header():
    assert insert_row(HEADER + DECK, "<R>") == HEADER + "<R>" + DECK


def test_an_empty_tree_gets_just_the_row():
    assert insert_row("", "<R>") == "<R>"


def test_the_row_clicks_are_read():
    assert message_action("final_review:open") == OPEN
    assert message_action("final_review:options") == OPTIONS


def test_other_messages_are_left_alone():
    assert message_action("open:123") is None
    assert message_action("final_review:other") is None
