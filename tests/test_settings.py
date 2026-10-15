import json
from pathlib import Path

from src.settings import Settings

CONFIG_JSON = Path(__file__).resolve().parent.parent / "config.json"


def test_an_empty_config_gives_the_defaults():
    assert Settings.from_config({}) == Settings()


def test_the_shipped_config_gives_the_defaults():
    assert Settings.from_config(json.loads(CONFIG_JSON.read_text())) == Settings()


def test_every_key_is_read():
    settings = Settings.from_config({
        "decks": ["Exam", "Exam::Week 2"],
        "min_pace_seconds": 30,
        "max_pace_seconds": 7200,
        "initial_stability": 10,
        "answers_to_cross": {"again": 2, "hard": 8, "good": 10, "easy": 4},
        "rate_band": 2,
        "volume_brake": 0.1,
        "answers_for_half_volume": 20,
    })
    assert settings == Settings(
        decks=("Exam", "Exam::Week 2"), min_pace=30, max_pace=7200,
        initial_stability=10, answers_to_cross=(2, 8, 10, 4), rate_band=2,
        volume_brake=0.1, half_volume=20,
    )


def test_a_bad_value_falls_back_to_its_default():
    settings = Settings.from_config({
        "min_pace_seconds": "fast",
        "initial_stability": 150,
        "answers_to_cross": {"good": 0, "easy": True, "again": 5},
        "rate_band": 0.5,
        "volume_brake": 2,
        "answers_for_half_volume": -1,
    })
    assert settings == Settings(answers_to_cross=(5, 9, 9, 3))


def test_a_maximum_pace_below_the_minimum_restores_both():
    settings = Settings.from_config({"min_pace_seconds": 600, "max_pace_seconds": 60})
    assert (settings.min_pace, settings.max_pace) == (60, 14_400)


def test_only_non_empty_deck_names_are_kept():
    assert Settings.from_config({"decks": [1, "Exam", "  ", None]}).decks == ("Exam",)
    assert Settings.from_config({"decks": "Exam"}).decks == ()
