# Final Review

## Problem

In the last stretch before an exam, there is no time left for a card to come back days later, and Anki's scheduling stops helping. The student needs each session to spend most of its answers on the cards they master least, without splitting them by hand by tag or deck.

## Goal and success

The add-on replaces day-based scheduling with a queue that only orders the cards. After every answer, it shows the card with the lowest retrievability score. The full design is in [Cálculos da fila](../../../../Docs/Final%20review%20queue/C%C3%A1lculos%20da%20fila.md).

The system is done when:

1. The tests give the same values as the example in `Cálculos da fila`, to two decimal places.
2. In Anki, after every answer, the eligible card with the lowest score shows up.
3. Each card's values come out the same every time they are rebuilt from its review history, on any computer.
4. Over a long session of the [queue simulation](https://github.com/coduruja/anki-final-review-simulation), about 80% of the answers land on the 20% of cards with the lowest stability.

## Out of scope

1. Scheduling cards for other days.
2. Splitting the cards that enter the queue by tag, group or deck.
3. Running the final review on Anki's phone apps.

## Glossary

| Term | What it is |
|---|---|
| Score `R` | The relative retrievability score, from 0 to 100; the lower it is, the sooner the card shows up. |
| Stability `S` | How well the card is mastered, from 0 to 100. |
| Pace `T(S)` | The seconds the score takes to go from 100 to 1. |
| `t0` | The time of the last correct answer; without one, the time of the first answer, or of entering the queue for a card with no answer. |
| `t` | The seconds since `t0`. |
| `n` | The card's total number of answers. |
| `p` | The card's correct-answer rate before the current answer. |
| Correct answer | Good or Easy. |
| Wrong answer | Again or Hard. |
| Review history | Anki's record of every answer a card got, on any device, which sync carries between devices. |
| Chosen deck | A deck the student picked in the settings to take part in the final review. |
| Eligible card | A card in a chosen deck that is neither suspended nor buried, and was not just answered. |

## Functional requirements

**FR1: the score.** The score is `R = 100^(1 − t/T(S))`, with `T(S) = 60 · 240^(S/100)` seconds on the default settings.

Acceptance criteria:

- Given `S = 0` and `t = 0`, when the score is computed, then it is 100.
- Given `S = 0` and `t = 60`, when the score is computed, then it is 1.
- Given `S = 100` and `t = 14,400`, when the score is computed, then it is 1.
- Given `S = 50` and `t = 300`, when the score is computed, then it is 22.6.
- Given the same card, when `t` grows, then the score only falls and never goes negative.

**FR2: the new stability.** Every answer recomputes `S` with the update formula in `Cálculos da fila`, using the `p` and `n` from before the answer.

Acceptance criteria:

- Given `S = 50`, `n = 15` and `p = 0.5`, when the card gets Good, Easy, Hard or Again, then `S` becomes 61.8, 77.7, 38.2 or 22.3.
- Given a new card, when it gets 6 Good in a row, then `S` goes through 22, 27.8, 33.4, 39, 45 and 51.7.
- Given a card with 20 correct answers and `S = 99`, when it gets Again, Good and Good, then `S` goes through 83.5, 94.1 and 98.
- Given any card, when it gets any grade, then `S` stays between 0 and 100.

**FR3: recording the answer.** After recomputing `S`, the answer adds 1 to `n` and, on a correct answer, adds 1 to the correct answers.

Acceptance criteria:

- Given a card, when it gets Good or Easy, then `t0` becomes the time of the answer and the score goes back to 100.
- Given a card, when it gets Again or Hard, then `t0` does not change and the score drops at once.

**FR4: the new card.** A card with no answers starts with the initial stability (20 by default), `p = 0.5`, `n = 0` and `t0` equal to the time it entered.

Acceptance criteria:

- Given a card that just entered, when the score is computed, then it is 100.
- Given a new card and an answered card with a lower score, when the queue chooses, then the new card does not jump ahead.

**FR5: choosing the next card.** The queue chooses the eligible card with the lowest score and, on a tie, the one with the lowest stability.

Acceptance criteria:

- Given two eligible cards with different scores, when the queue chooses, then the one with the lower score comes.
- Given two cards with the same score, when the queue chooses, then the one with the lower stability comes.
- Given a suspended or buried card with the lowest score, when the queue chooses, then it does not come.
- Given the card that was just answered with the lowest score, when the queue chooses, then it does not come.
- Given a card outside the chosen decks with the lowest score, when the queue chooses, then it does not come.

**FR6: rebuilding from the review history.** Each card's `S`, `t0`, `n` and correct answers are rebuilt by running every graded answer in its review history through FR2 and FR3, in order, starting from FR4.

The rebuild runs again after every answer and after every sync, so answers given on the phone count as soon as they are synced. Learning and relearning answers count; history entries without a grade, such as a manual reschedule, are skipped.

Acceptance criteria:

- Given a card whose history holds 6 Good, when it is rebuilt, then `S` is 51.7 and `n` is 6.
- Given a card answered on the phone, when the sync ends, then its values include that answer.
- Given a card with a manual reschedule in its history, when it is rebuilt, then that entry changes nothing.
- Given a card whose history holds only wrong answers, when it is rebuilt, then `t0` is the time of its first answer.
- Given any card, when Anki closes and opens again, then its rebuilt values are the same.

**FR7: the queue in Anki.** An item in Anki's Tools menu starts the final review on the chosen decks, and after every answer Anki shows the card chosen by FR5.

Acceptance criteria:

- Given an open final review, when the student answers a card, then the next card shown is the one with the lowest score among the eligible cards.
- Given the final review is not started, when the student reviews a deck, then Anki behaves as it does without the add-on.

**FR8: answers count for Anki too.** An answer given in the final review goes to Anki's own scheduler like any other answer.

Acceptance criteria:

- Given an answer in the final review, when it is saved, then it appears in the card's review history and Anki reschedules the card as usual.

**FR9: choosing the decks.** The settings hold the list of decks that take part in the final review.

Acceptance criteria:

- Given a deck left out of the settings, when the final review runs, then none of its cards show up.

**FR10: the settings.** Every constant of the formulas can be changed in Anki's add-on config screen, and a Markdown page beside it explains how to change each one.

The constants are the minimum and maximum pace, the initial stability, the `n` of each grade, the hit-rate band (3), the volume brake `m` (0.05) and the number of answers for half the volume (15). Each one defaults to the value in `Cálculos da fila`.

Acceptance criteria:

- Given a changed constant, when the queue chooses, then the scores and stabilities use the new value.
- Given any change to these settings, when Anki schedules a card, then Anki's own settings and parameters are left alone.
- Given the config screen, when the student opens it, then the Markdown page explains what each constant does, its default and what raising or lowering it changes.

**FR11: edited and merged cards.** Editing a card leaves its values alone, and a merged card is treated like any other card.

A merge keeps the card with the most answers, edited to hold both, so the kept card goes on with its own review history.

Acceptance criteria:

- Given an edited card, when it is rebuilt, then its values are the same as before the edit.
- Given two merged cards, when the kept card is rebuilt, then its values come only from its own review history.

## Non-functional requirements and constraints

1. The add-on is written in Python 3.12 and tested with pytest.
2. The tests run without Anki open.
3. Only `src/wiring.py` imports from Anki.
4. The add-on runs only in Anki on the computer; phone answers reach it through sync.
5. Time is counted in seconds, both for the timestamps and for the difference between them.
6. Python turns a score below about 10⁻³²⁴ into 0, and the stability tie-break settles those cases.
7. Every Python file passes `ruff check`.
8. The algorithm is written test-first (TDD).

## Technical decisions

| Decision | Reason | Rejected alternative |
|---|---|---|
| Hard counts as a milder wrong answer. | In the last stretch, a Hard shows the card is not mastered yet. | Hard as a weak correct answer, as in FSRS. |
| Card values are rebuilt from the review history and never stored. | Sync already brings the phone answers into the history, so nothing else has to be kept in step. | Storing `S`, `t0`, `n` and the correct answers on each card. |
| The score is never stored. | The score changes every second, and a stored value would go stale. | Storing the score and refreshing it from time to time. |
| The pace scale is geometric. | The precision sits on the short paces, where telling one weak card from another matters. | A linear scale between 60 s and 14,400 s. |
| On a score tie, the card with the lowest stability comes. | It keeps the queue on the least mastered cards once the score has turned 0. | Putting the new card at score 0, which would end the alternation between new and seen cards. |
| The gain does not depend on the score at the time of the answer. | The queue answers cards with very close scores in a row, and the rule would not change the order. | The FSRS adjustment that raises the gain when the score was low. |
| Only one module imports from Anki. | The algorithm stays testable without Anki. | Calls to Anki spread across the code. |

## Slice plan

| Slice | What it delivers | Test |
|---|---|---|
| 1. The score | `R` from `S` and `t` | FR1 |
| 2. The new stability | `S'` from the grade, `S`, `p` and `n` | FR2 |
| 3. The answer | The update of `S`, `t0`, `n` and correct answers | FR3 and FR4 |
| 4. The choice | The next card among the eligible ones | FR5 |
| 5. The rebuild | Card values from the review history | FR6 |
| 6. The settings | Every constant editable, with its Markdown page | FR10 |
| 7. The decks | Only cards from the chosen decks | FR9 |
| 8. The queue in Anki | The Tools menu item, and Anki shows the chosen card after every answer | FR7 and FR8 |
| 9. Editing and merging | Values kept on an edit and on a merge | FR11 |
