from src.history import rebuild
from src.settings import Settings

SETTINGS = Settings()


def test_no_history_is_a_new_card():
    card = rebuild([], entered_at=500, settings=SETTINGS)
    assert (card.stability, card.t0, card.answers) == (20, 500, 0)


def test_six_good_answers():
    card = rebuild([(i * 1000, 3) for i in range(6)], entered_at=0, settings=SETTINGS)
    assert round(card.stability, 1) == 51.7
    assert card.answers == 6
    assert card.t0 == 5


def test_entries_without_a_grade_change_nothing():
    plain = rebuild([(1000, 3), (2000, 1)], entered_at=0, settings=SETTINGS)
    with_manual = rebuild([(500, 0), (1000, 3), (1500, 0), (2000, 1)], entered_at=0, settings=SETTINGS)
    assert with_manual == plain


def test_entries_out_of_order_are_sorted():
    ordered = rebuild([(1000, 1), (2000, 3), (3000, 4)], entered_at=0, settings=SETTINGS)
    shuffled = rebuild([(3000, 4), (1000, 1), (2000, 3)], entered_at=0, settings=SETTINGS)
    assert shuffled == ordered


def test_only_wrong_answers_keep_t0_at_the_first_answer():
    card = rebuild([(500, 0), (4000, 1), (9000, 2)], entered_at=0, settings=SETTINGS)
    assert card.t0 == 4
    assert card.answers == 2


def test_the_same_history_always_gives_the_same_card():
    entries = [(1000, 3), (5000, 1), (9000, 4)]
    assert rebuild(entries, 0, SETTINGS) == rebuild(list(entries), 0, SETTINGS)
