# Six tests, run unattended (night of 2026-10-24)

All six completed, ~5 minutes of wall clock, ~$0.06 of lane spend plus local compute.
Receipts: `memory/runs/six_tests/t1..t6.json` (+ `_index.json`). Nothing here was
hand-tuned after seeing the numbers; each test's falsifier was written in the plan first.

## T4 — JUNG: nothing was disowned into a shadow scheduler

37 `Mag*` scheduled tasks censused; **0 write git directly, 0 touch the chain** by their
own command lines or scripts. The lens predicted that banned capabilities (no second
scheduler, chain read-only) would return as unnamed cron work. **Falsified** for git and
chain. Honest caveat: the check reads task command lines and referenced scripts; a
script that shells into Python which then calls git would hide from it.

*What we learned:* the single-writer law is actually holding at the scheduler layer —
the sweeper really is the only thing committing. That is a stronger result than a hunt
would have produced.

## T2 — ELLUL: 69% of the session was procedure, not choice

Two independent classifiers labelled all 24 steps; they agreed on **100%** of them, and
**69.2%** were labelled PROCEDURE (state file, git status, test suite, re-run audit,
compare counts, check falsifier dates…).

**But the sample is mine.** The step list was authored by the same seat whose session it
describes, so 69% measures the composition of *my list*, not the estate's true work mix.
The agreement (100%) is real; the ratio is not yet a fact about the estate.

*What we learned:* the classification is stable enough to be worth doing properly —
next time the step list must come from the log (receipts/commands), not from memory.

## T3 — McLUHAN: the surface changes the decision — confirmed

Same finding, four surfaces, four lanes each:

| surface | modal next action |
|---|---|
| prose | filter probe (3/4) |
| receipt | filter probe (3/4) |
| **cockpit** | **read/consume (3/4)** |
| **json** | **read/consume (4/4)** |

Two distinct modal actions from identical content. Rendered as a *cockpit line* or
*JSON*, the same numbers read as "data to be consumed"; rendered as prose or a receipt,
they read as "a defect to be fixed".

*What we learned:* form is not cosmetic — it selects the verb. Which means the cockpit
should carry a **verb**, not only a number, when the goal is action. This is the first
finding today that changes a design rather than a metric.

## T5 — FERMAT: free lanes win on speed, paid wins on quality, local wins on nothing but privacy

| route | mean latency | cost | judge score (1–5) |
|---|---|---|---|
| free (groq/ollama) | **2.1 s** | $0 | 2–3 |
| paid (deepseek-flash) | 7.3 s | ~$0.001 | 2–5 (one 5, two 4s) |
| local 7B | 14.5 s | $0 | 2–3 |

Free is **7× faster than local with the same judged quality**, and paid edges both on the
hard tasks (parable, synthesis). Local wins only where privacy or offline matters.

*What we learned:* the "local is cheaper" intuition is true but irrelevant — at these
sizes both free and local cost nothing, so latency and quality decide, and local loses
both. Keep local for offline and for the 6 GB box's own dogfood, not as a cost play.

## T6 — HALL: receipts and cockpit agree; the census does not carry an action

Three artifacts, three cold readers:

| artifact | implied action | agreement |
|---|---|---|
| wave receipt | fix the gate | 3/3 |
| cockpit output | fix the gate | 3/3 |
| queue census | *other* (2), filter probe (1) | none |

*What we learned:* the receipt and the cockpit are already readable in the same way —
that pair is coherent. The census is evidence without a verb, which is exactly what T3
says turns a finding into "data" instead of a decision. **Add an action line to
`queue_census.py`'s output** — the smallest fix with the clearest evidence behind it.

## T1 — BERNAYS: the clock is running

Two artifacts made from the same 60 live rows are in
`watch/inbox/demand_probe_20261024/` (`A_digest.md`, `B_spec.md`, `CLOCK.txt`).
Citations are counted by `tools/demand_probe_count.py`, which compares A, B and a control
set of the bare rows. Its verdict vocabulary is fixed in advance:
`dead` / `neutral` / `demand created`.

A cron job **`queue-demand-probe`** (job `f23dc625cec2`) now runs daily at 08:00 and
reports the census plus the demand verdict with continuity, so the 48-hour window is
measured by the estate and not by a seat remembering to look.

## Cross-test conclusion

Two lenses produced design changes (McLuhan: put a verb in the cockpit line; Hall: put an
action line in the census). One lens was falsified (Jung). One was measured but its sample
was contaminated by the experimenter (Ellul). One killed an intuition (Fermat: local is
not the cheap route, it is the slow one). One started a clock (Bernays).

The pattern under all six: **claims that carry a verb travel; claims that carry only a
number do not.** That is the same finding as the day's main result — statements do not
bind until something acts on them.
