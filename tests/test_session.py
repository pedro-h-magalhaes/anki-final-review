from src.session import Session
from src.settings import Settings


def test_a_card_first_seen_mid_session_does_not_jump_ahead():
    session = Session(Settings())
    session.choose({1: [(0, 3)]}, now=0)
    assert session.choose({1: [(0, 3)], 2: []}, now=100) == 1


def test_a_new_card_keeps_the_time_it_was_first_seen():
    session = Session(Settings())
    session.choose({2: []}, now=0)
    assert session.choose({2: [], 3: []}, now=1_000) == 2


def test_the_answered_card_waits_one_turn():
    session = Session(Settings())
    histories = {1: [(0, 1)], 2: [(0, 3)]}
    assert session.choose(histories, now=100) == 1
    session.record_answer(1)
    assert session.choose(histories, now=100) == 2


def test_a_synced_answer_counts_at_the_next_choice():
    session = Session(Settings())
    before = session.states({1: [(0, 3)]}, now=10)[1]
    after = session.states({1: [(0, 3), (5_000, 3)]}, now=10)[1]
    assert after.answers == before.answers + 1
    assert after.stability > before.stability
