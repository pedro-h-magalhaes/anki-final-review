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


from src.card import Grade, next_stability


def test_one_answer_matches_the_example():
    after = [round(next_stability(50, g, 0.5, 15, SETTINGS), 1)
             for g in (Grade.GOOD, Grade.EASY, Grade.HARD, Grade.AGAIN)]
    assert after == [61.8, 77.7, 38.2, 22.3]


def test_stability_stays_between_0_and_100():
    stability = 50.0
    for answers in range(60):
        stability = next_stability(stability, Grade.EASY, 1.0, answers, SETTINGS)
        assert 0 <= stability <= 100
    for answers in range(60):
        stability = next_stability(stability, Grade.AGAIN, 0.0, answers, SETTINGS)
        assert 0 <= stability <= 100
