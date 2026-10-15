from src.card import pace, score
from src.settings import Settings

SETTINGS = Settings()


def test_pace_runs_from_one_minute_to_four_hours():
    assert pace(0, SETTINGS) == 60
    assert round(pace(100, SETTINGS)) == 14_400


def test_score_is_100_at_the_answer():
    assert score(0, 0, SETTINGS) == 100


def test_score_is_1_after_one_pace():
    assert round(score(60, 0, SETTINGS), 2) == 1
    assert round(score(14_400, 100, SETTINGS), 2) == 1


def test_score_matches_the_example():
    assert round(score(300, 50, SETTINGS), 1) == 22.6


def test_score_only_falls_and_never_goes_negative():
    values = [score(t, 30, SETTINGS) for t in range(0, 100_000, 500)]
    assert values == sorted(values, reverse=True)
    assert min(values) >= 0
