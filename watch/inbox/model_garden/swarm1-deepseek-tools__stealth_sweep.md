# swarm1-deepseek-tools__stealth_sweep (deepseek-chat @ deepseek, turn 1, channel: content)

DEFECT 1: `catalog` sorts by `id`, so the cursor's `pool[:MODELS_PER_RUN]` always fires the same alphabetically-first 40 and never advances to unscored models once the front of the list is `done` | EVIDENCE: tools/stealth_sweep.py:88, tools/stealth_sweep.py:104 | FIX: sort the pool by a stable hash of `model` (or preserve catalog order and rotate a persisted offset) so daily runs walk the whole wall instead of re-firing the same head
DEFECT 2: every `call` writes its row to `LEDGER` under `open("a")` inside `as_completed`, so a crash mid-run leaves `done` populated with entries whose `correct` was never observed, silently skipping models on the next run | EVIDENCE: tools/stealth_sweep.py:104, tools/stealth_sweep.py:105 | FIX: append the row only after the `call` result is inspected in `main`, keyed on a per-run batch id, so a torn run is discardable
DEFECT 3: `keys()` reads only two env vars and `call` picks `ks[idx % len(ks)]`, so with one key present all 40 models share it while `k = ks[idx % len(ks)]` gives no rotation across models | EVIDENCE: tools/stealth_sweep.py:44, tools/stealth_sweep.py:63 | FIX: pick the key by `idx % len(ks)` and pass a per-call index, or rotate by task position in the batch, not by enumerate order
DEAD-CODE: `hollow` is written into every row but never read by any consumer in this file, including the report | EVIDENCE: tools/stealth_sweep.py:74, tools/stealth_sweep.py:127
ONE-SITTING FIX: replace the `done` skip with a persisted cursor offset into the catalog so `pool[:MODELS_PER_RUN]` advances each run | EVIDENCE: tools/stealth_sweep.py:88, tools/stealth_sweep.py:100

Falsifier for DEFECT 1: if `catalog` returned a shuffled or time-rotated order, sorted-by-id determinism would not pin the batch; inspect `sorted(out, key=lambda x: x["id"])` at tools/stealth_sweep.py:52 to confirm it does not.

Note: em-dash characters were avoided in this reply; the file contains several, e.g. tools/stealth_sweep.py:1 and tools/stealth_sweep.py:131, which is a house-style violation of the estate but not a DEFECT line as written.
