from src.card import CardState, new_card
from src.review_queue import next_card
from src.settings import Settings

SETTINGS = Settings()


def test_the_lowest_score_comes():
    states = {1: CardState(50, t0=200), 2: CardState(50, t0=0)}
    assert next_card(states, 300, SETTINGS) == 2


def test_a_score_tie_goes_to_the_lowest_stability():
    states = {1: CardState(10, t0=0), 2: CardState(0, t0=0)}
    assert next_card(states, 100_000, SETTINGS) == 2


def test_a_full_tie_goes_to_the_lowest_card_id():
    states = {7: CardState(0, t0=0), 3: CardState(0, t0=0)}
    assert next_card(states, 100_000, SETTINGS) == 3


def test_the_card_just_answered_does_not_come():
    states = {1: CardState(0, t0=0), 2: CardState(50, t0=0)}
    assert next_card(states, 300, SETTINGS, exclude=1) == 2


def test_the_only_card_comes_back_after_its_answer():
    states = {1: CardState(50, t0=0)}
    assert next_card(states, 300, SETTINGS, exclude=1) == 1


def test_no_cards_means_no_next_card():
    assert next_card({}, 300, SETTINGS) is None


def test_a_new_card_does_not_jump_ahead():
    states = {1: new_card(300, SETTINGS), 2: CardState(50, t0=0)}
    assert next_card(states, 300, SETTINGS) == 2
