"""The Card, which holds a card's last answer time and its retrievability score."""

from datetime import datetime


class Card:
    def __init__(self):
        self.r_score = None
        self.last_answer_time: datetime = None

    def get_answer_time(self, answer_time: datetime, now: datetime):
        self.last_answer_time = answer_time
        elapsed_days = (now - answer_time).total_seconds() / 86400
        self.r_score = 100 - elapsed_days
