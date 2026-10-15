These settings only change the order of the final review. They never touch Anki's own deck options or FSRS parameters, and every answer still counts for Anki's normal scheduling. A value of the wrong type or out of range is replaced by its default.

**decks** — the decks that take part in the final review, by full name, such as `["Exam", "Biology::Cells"]`. A deck brings its subdecks with it. With `[]`, the final review has no cards.

**min_pace_seconds** — default `60`. How many seconds the score of a card with stability 0 takes to fall from 100 to 1. Raise it and the weakest cards wait longer before coming back; lower it and they come back sooner.

**max_pace_seconds** — default `14400` (4 hours). The same for a card with stability 100. Raise it and well-known cards come back less often; lower it and they come back more often. It must be above `min_pace_seconds`, or both go back to their defaults.

**initial_stability** — default `20`, from 0 to 100. The stability of a card with no answers. Raise it and new cards wait longer before their first answer; lower it and they come sooner.

**answers_to_cross** — default `{"again": 3, "hard": 9, "good": 9, "easy": 3}`. How many answers in a row with each grade take a card from one end of the stability scale to 1 point from the other. Lower a grade's number and that grade moves the card further each time; raise it and each answer moves the card less.

**rate_band** — default `3`, at least 1. How much the card's hit rate speeds up or slows down each answer: a card always answered right moves up up to 3 times faster and down 3 times slower, and the opposite for a card always answered wrong. `1` turns the hit rate off.

**volume_brake** — default `0.05`, above 0 and at most 1. The smallest share of the speed a card's number of answers allows: a card with few answers rises at 5% of the speed, and one with many answers falls at 5%. Raise it toward `1` to make the number of answers matter less.

**answers_for_half_volume** — default `15`. How many answers a card needs before its number of answers counts for half. Raise it and cards need more answers to be protected from sudden drops; lower it and they need fewer.
