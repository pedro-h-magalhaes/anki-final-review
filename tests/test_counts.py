from src.counts import queue_counts


def test_cards_are_counted_as_new_learning_and_review():
    assert queue_counts([0, 0, 1, 3, 2, 2, 2]) == (2, 2, 3)


def test_no_cards_count_as_zero():
    assert queue_counts([]) == (0, 0, 0)
