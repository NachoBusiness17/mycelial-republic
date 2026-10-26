# ENVELOPE DATUM: FIRST RATE LIMIT AT THE 50-WIDE GAME-DIG SHAPE — 2026-09-26

**Shape when it hit:** 5 running workflows (game-mechanics veins) at max_concurrency 10 each = 50 concurrent workflow children, plus the hourly burn cron (3 agents/fire) plus offpeak idle tasks. First 429/1302-family rate limit observed by the operator.

**Meaning per the dispatch laws:** workflow children retry model-side errors internally without limit and the runtime adapts the fan-out, so a rate limit is a throttle, not a loss. Rolling-window law: after a burst, holds decay; width holds while the window drains.

**Datum:** the B2-25 envelope measurement (Task agents clean at 10-12) now has a workflow-children companion point: ~50 children + support load = first limit contact. Next width experiment should step 5 runs x 8 before 5 x 10+.

**Decision:** width HELD at 50 (operator ordered the burn); absorption is the retry loop's job. If errors start surfacing as run failures rather than holds, pull to 5 runs x 5.
