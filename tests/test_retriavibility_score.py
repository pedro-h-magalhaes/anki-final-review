from datetime import datetime, timedelta, timezone

from src.card import Card


def test_score_100_after_answer():
    card = Card()
    now = datetime(2026, 10, 14, 15, 0, tzinfo=timezone.utc)
    card.get_answer_time(answer_time=now, now=now)
    assert isinstance(card.last_answer_time, datetime)
    assert card.r_score == 100

def test_score_not_100_if_time_is_not_now():
    card = Card()
    now = datetime(2026, 10, 14, 15, 0, tzinfo=timezone.utc)
    answer_time = now - timedelta(seconds=1)
    card.get_answer_time(answer_time=answer_time, now=now)
    assert card.r_score != 100
