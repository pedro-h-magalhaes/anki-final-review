"""The Card, which holds a card's last answer time and its retrievability score."""

from datetime import datetime


class Card:
    def __init__(self):
        self.r_score = None
        self.last_answer_time: datetime = None

    def get_answer_time(self, answer_time: datetime, now: datetime):
        self.last_answer_time = answer_time
        if answer_time == now:
            self.r_score = 100
        else:
            self.r_score = None
