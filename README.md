# Final Review

An Anki add-on for the final stretch before an exam. It will not schedule cards for other days: after every answer, it shows the card with the lowest retrievability score, a number from 100 down that falls faster on the cards mastered least.

Click Final Review at the top of the deck list to start; leaving the study screen ends it. The gear on that row chooses the decks. The other settings are explained in `config.md`.

## Development

The tests run without the Anki app, from the add-on folder:

```sh
python3.12 -m venv .venv
.venv/bin/pip install pytest
.venv/bin/pytest
```

The queue the add-on is meant to run is tried out first in the [queue simulation](../queue-simulation/README.md), a separate repository beside this one.
