from src.deck_choice import chosen_names, locked_names

NAMES = ["A", "A::B", "A::B::C", "D"]


def test_a_checked_deck_locks_all_its_subdecks():
    assert locked_names(NAMES, ["A"]) == {"A::B", "A::B::C"}


def test_a_deck_with_a_longer_name_is_not_a_subdeck():
    assert locked_names(["Bio", "Biology"], ["Bio"]) == set()


def test_unchecking_the_parent_unlocks_the_subdecks():
    assert locked_names(NAMES, []) == set()


def test_a_subdeck_under_a_checked_parent_is_saved_once_as_the_parent():
    assert chosen_names(NAMES, ["A", "A::B", "D"]) == ["A", "D"]


def test_a_deck_that_no_longer_exists_is_dropped():
    assert chosen_names(["A"], ["A", "Gone"]) == ["A"]


def test_nothing_checked_saves_no_decks():
    assert chosen_names(NAMES, []) == []
