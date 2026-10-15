from src.decks import deck_search


def test_no_decks_means_no_search():
    assert deck_search([]) is None


def test_one_deck_leaves_out_suspended_and_buried_cards():
    assert deck_search(["Exam"]) == '("deck:Exam") -is:suspended -is:buried'


def test_several_decks_are_joined_with_or():
    assert deck_search(["A", "B::C"]) == '("deck:A" OR "deck:B::C") -is:suspended -is:buried'


def test_search_characters_in_a_name_are_escaped():
    assert deck_search(['My "best"_deck*']) == (
        '("deck:My \\"best\\"\\_deck\\*") -is:suspended -is:buried'
    )
