# Ractor salon: the cast on one day's evidence (2026-10-24, 36 calls, $0.054)

**Method:** kabuki cast from `configs/kabuki_cast.json` (6 actors, personas and word
caps as configured), each seated on 6 live lanes — deepseek-flash, deepseek-v4-pro,
groq-nacho, groq-sd, ollama-nacho, ollama-sd. The brief carried the five findings as
evidence and three open questions, **no conclusion**. 32/36 answers were substantive.

## The fold

**Four of six actors named the same change**, in their own registers:

| actor | the one thing that must change |
|---|---|
| ARAGOTO | "Stop assuming the estate has only 1,521 open items" — the baseline is under-reported |
| ONNAGATA | "The estate must cease generating probe_* model chatter" |
| HANA-GUMO | "Stop treating probe_* model chatter as real open items… an instrumented artifact rather than a genuine task" |
| ONSEI | same, framed as forbidden pattern: labelling false premises "unverifiable" masks errors |

Each attached a falsifier that can actually fire:

- ARAGOTO: *if a later census still reads 1,521, or chatter far below 62.5%, I am wrong.*
- ONNAGATA: *if open count stays above 2,000 with chatter disabled, the claim fails.*
- HANA-GUMO: *if filtering probe_* leaves the open count unchanged, I am wrong.*

## The dissent that carries the weight

**TACHIYAKU** ran the elenchus and refused every premise in turn:

> Intent: partly — the estate's intent is inferred from artifacts, not declared.
> Success: no — 51 distinct strings collapse to one action; 47 calls empty; planted lies
> called false only 5%. Authority: no — **model consensus cannot authorize truth; only
> external verification and adopted repo fixes can.** Continuity: no — the erasure fix
> exists and lifts z.ai 0/7 to 5/5, yet 47/100 still returned nothing; sixteen readers
> refute "no consumer."

That is the correct guard on the other four. A cast agreeing is not evidence; it is a
hypothesis with four witnesses. The thing that makes the probe-chatter claim true is
`tools/queue_census.py` reading 1,492 probe rows out of 2,388 — not the vote.

**WAKA** did what WAKA does: restated the evidence faithfully and did not commit to a
change, which is itself a signal that the brief's open questions were genuinely open.

## What the cast produced that the numbers did not

1. **The defect is at the writer, not the reader.** Four actors independently located the
   problem upstream of the queue: the estate is *manufacturing* probe chatter, and the
   sixteen existing readers are consuming noise. Building a consumer would have scaled
   the noise.
2. **"Unverifiable" is doing double duty.** ONSEI named it as a forbidden pattern: 90% of
   audits say "cannot verify", which is epistemically right but operationally useless if
   nothing ever converts an unverifiable premise into a verified one. That is the gap
   between the tri-state discipline and an actual gate.
3. **Consensus is cheap; falsifiers are not.** Every actor that committed to a change also
   committed to a kill condition. That is the only reason the fold is usable.

## Next

The four-way convergence is a hypothesis with a mechanical test already on disk:
disable `probe_*` at the writer, re-run `queue_census.py`, and check the falsifiers the
cast wrote. If the open count stays above 2,000, they were all wrong together — which is
exactly the outcome TACHIYAKU predicted a panel could produce.

## Landed (operator: "word")

`mag/percolator.py` — a novel row whose domain starts with `probe_` now lands as
`status="probe"`, never `"open"`. The row is still appended (append-only law holds);
it simply stops counting as work. `tools/queue_census.py` recognises both shapes —
legacy rows with a `probe_*` domain and new rows with `status="probe"`.

Tests: `tests/test_percolator_probe_status.py`, 3 passed.

### Did the cast survive its own falsifiers?

| actor | falsifier | result |
|---|---|---|
| ONNAGATA | "if the open count stays above 2,000 with chatter disabled, my claim fails" | chatter-excluded count is **896** → survives |
| HANA-GUMO | "if filtering probe_* leaves the open count unchanged, I am wrong" | 2,390 → 896, a **62.5% drop** → survives |
| ARAGOTO | "if a later census still reads 1,521, or chatter is far below 62.5%" | census reads **2,390** at **62.5%** → survives |

The fix is at the writer, so the number stops growing; the legacy 1,494 rows stay where
they are, counted but not counted *as work*.
