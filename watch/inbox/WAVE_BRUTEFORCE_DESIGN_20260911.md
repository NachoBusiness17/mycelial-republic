# WAVE BRUTE-FORCE — dozens of agents, one shared ledger (design, 2026-09-11)

*Operator: "drive a window with dozens of subagents acting as our wave… allowing
the agents to communicate and dogfood systems live while the last task of an agent
is to take the current state of in-progress work and add it to their shared
hugging face — a long list, like how math problems are being brute-forced, but at
our own scale."*

## WHAT WE ALREADY HAVE (tested tonight)

1. **The driver pattern** — spawn → read the filed cards → extend → write one card.
   Ran at 8-wide all night; rotation on fold proven.
2. **Communication, three ways** — the shared inbox (any worker reads any card),
   the hub relay (seat forwards between workers), and direct pair channels
   (builder↔builder proven with the Astra pair).
3. **Dogfooding live** — every worker already exercises fleet organs and cites
   them; it just needs to be a REQUIRED field, not a habit.
4. **The hash-chained ledger pattern** — grounding wave and failure receipts both
   use it; the brute-force list is the third instance of the same organ.

## WHAT'S MISSING (two organs)

1. **The automated driver.** Tonight a seat drove the rotation by hand. To hold
   dozens, the driver must be the automation window: a cron that every 30 minutes
   counts live workers and spawns two per fold, riding the width line (8→dozens as
   quota allows), never stacking past the refill rate (the 1302 lesson).
2. **The terminal state-dump clause.** One line added to every worker prompt:
   "Your LAST task: append your final state to the wave ledger — what you did,
   what you found, what remains, one JSON row." Constant-name file:
   `watch/WAVE_LEDGER.jsonl`, hash-chained like the grounding wave.

## THE LONG LIST (the brute-force shape)

Each ledger row = one attempt, failures included (they stay in the denominator):
attempt_id, worker, task, result_summary, artifacts_path, token_spend, outcome,
failure_class if any, hash. Math-brute-force datasets publish the misses — the
misses are the value. Ours publishes agent attempts the same way.

## THE HF DOOR (stage 3, behind deploy GO)

Mirror the ledger to one Hugging Face dataset repo — the whisper room the other
window already staged. Token reads from env (`HF_TOKEN`), never written into any
source file. Push on a cadence (per-fold or hourly). The other window's refusal
receipts and our attempt rows merge into one dataset: the percolator mines our
attempts for invariants the way it mined their refusal receipts tonight.

## STAGING

- Stage 1 (now, $0): the ledger organ + the last-task clause in every new prompt.
- Stage 2 (arm on GO): the wave-driver cron, width line at 8, spawn-2-per-fold.
- Stage 3 (arm on deploy GO + HF_TOKEN in env): the HF mirror, cadence per-fold.

## THE BOUNDS (unchanged)

No chain writes (retro-knotter stays gated), no beacon read (his), no credential
values in any file, width never past the refill rate.
