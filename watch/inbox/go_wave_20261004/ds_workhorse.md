# ds_workhorse lane receipt - GO wave 2026-10-04 (items 3 + 9, merged)

Lane 3 (ds-workhorse) of the coordinator-partitioned GO wave over
corpus/steal/MASTER_MICKEY17_V2.md section 9. Every number below carries the
command that proved it. All live commands ran via
`.venv/Scripts/python.exe` (repo venv). No em-dashes in any authored byte.

## Sub-item results (fold item 3: delta-study receipt repair)

1. **Register caveats + tally + ds_capped + measured cost**
   `watch/inbox/frontier_delta_register_20261003.json` rewritten from a bare
   14-row array to `{"meta": ..., "rows": ...}` (parse-back verified: 14 rows,
   original fields intact, additions appended). Meta carries: a 6-key caveats
   block (ds cap, flash file-access asymmetry, gaming_corpus missing arm, judge
   methodology, counter rules), judge_tally_published_20261003
   {frontier 8, flash 5, ds 0/26, 39 items, judge deepseek-chat},
   judge_tally_gaming_corpus_recount {frontier 9, flash 5}, judge_tally_v3_refire
   {frontier 12 - ds 2; flash 13 - ds 1; ds 3/28}, measured_cost_usd with the
   per-leg sums. Each row gained: ds_capped=true, ds_cost_usd_v2,
   ds_cost_usd_v3, judge_v3_frontier_ds, judge_v3_flash_ds. Cites:
   a05#0 (cap), a05#1 (tally append, judge model now recorded per row), a05#3
   (caveat-free register), a05#5 (cost), a05#6 (gaming_corpus), a05#9 (vendor
   default), a14#2 (fold into the register instead of a re-fire).
   Proof: `.venv/Scripts/python.exe` round-trip parse-back assert block in the
   rewrite script; `python -c` json.loads succeeds.

2. **STANDING_RAILS.md:49-50 corrected to 39/39** linking
   `memory/runs/ds_batches/delta_judge_results.jsonl` (closed 2026-10-03T13:04Z),
   naming the capped-arm supersession and this receipt. Cite: a14#2, a05#4.
   The old "30/50 lanes, ~20 killed, re-fire cheap on GO" line is gone. Proof:
   Read of the file post-edit.

3. **$0.14 figure restated, not dropped**: the figure lives in
   `watch/inbox/frontier_delta_steal_20261003.md:30-31`, which is NOT in this
   lane's ownership, so the measured restatement is banked in the register
   meta.measured_cost_usd.note: the $0.14 headline matches no ledger (43 pct
   low vs the v2 arm $0.0977, 30 pct high vs the four 2026-10-03 ds legs summed
   $0.2000). Measured sums re-run 2026-10-04 over the cost_usd column of all
   six ds_batches jsonl files: v1_delta 0.0013, v1_gapfold 0.0073, v2 0.0977,
   judge_1003 0.0938, refire_v3 0.1292, judge_v3 0.0724, grand 0.4017.
   Command: `.venv/Scripts/python.exe -c` sum over the six files. Cite: a05#5.

4. **gaming_corpus pairing judged by the prompt's own rule**: flash DNF-ed
   SUBSTANCE_gaming_corpus (flash_chars 0, no replay file, no judge lanes);
   the judge prompt rule "one may be truncated or missing; treat missing as a
   loss for that arm" scores it a frontier win, making the frontier-flash
   headline 9-5 over 14 scenarios, not 8-5. Banked as
   judge_tally_gaming_corpus_recount in the register meta. No judge call spent
   (the rule is the judgment). Cite: a05#6.

5. **max_tokens 2000 override deleted** from tools/ds_workhorse.py ask() body
   (was line 52). Fix comment names cause (a05#0/#9: a harness choice at a
   quarter of the vendor default) and evidence ("default is 8K in non-thinking
   mode", 393216 ceiling, api-docs.deepseek.com/api/create-chat-completion,
   byte-grepped 2026-10-03). The content[:6000] store slice went with it -
   same defect at the storage layer; full completions bank now. Proof: the
   refire produced 0 rows at exactly 6000 chars (13/14 v2 rows were 6000).
   Note: tests/test_inference_budget.py:339 asserts a 2000 floor in
   tools/model_garden.py (its own code), not ds_workhorse; untouched and
   passing.

6. **ds arm re-fired, uncapped, thinking-off, file-backed**:

   ERRATUM 2026-10-04: the 'thinking-off' label on this re-fire is unverified
   and false-by-ordering: the run (04:38:32Z) predates the d4 probe
   (06:00:41Z) and the explicit-key fix (06:11:38Z), so its ask() OMITTED the
   thinking key; omission is measured ON for deepseek-v4-flash
   (d4_thinking_probe.md) though this batch ran model deepseek-chat
   (tools/ds_workhorse.py:64), never probed. The 0/26 vs 3/28 delta is a
   budget-axis result (harness 2000 cap vs vendor default), not a
   thinking-axis result. The explicit disabled key landed post-run at
   tools/ds_workhorse.py:93.
   (Landed verbatim 2026-10-04, law-amendments lane; original text below,
   kept unmodified, NIGHT_CLOSE pattern.)
   `.venv/Scripts/python.exe -m tools.ds_workhorse run --in
   memory/runs/ds_batches/frontier_delta_items.jsonl --prompt-file
   memory/runs/ds_batches/frontier_delta_prompt.md --out
   memory/runs/ds_batches/frontier_delta_results_v3.jsonl`
   -> 14/14 ok_api=True ok_material=True, $0.1292, outputs 5788-31000 chars,
   0 rows at 6000, per-row prompt_tokens banked (6368-30007). No routing table
   needs to cite 0-for-26 from a capped arm again.

   **New judge tally vs the published one:**
   - Published (2026-10-03, capped arm): ds 0/26.
   - Refire batch (2026-10-04, uncapped): 27 judge items
     (delta_judge_items_v3.jsonl, built by build_judge_items_v3.py which
     byte-asserts contract-head equality against the original items),
     judged by the same judge model (deepseek-chat), 27/27 conf=H,
     $0.0724 -> delta_judge_results_v3.jsonl.
   - frontier vs ds: frontier 12, ds 2 (ds wins: SUBSTANCE_gaming_corpus,
     WIRE_PLAN, both conf=H).
   - flash vs ds: flash 13, ds 1 (the ds win is the rule-scored
     gaming_corpus pair; flash deliverable missing).
   - **ds 3/28 total** (26 published pairs + the 2 gaming_corpus pairs the
     original batch dropped). The uncapped arm is still the losing arm against
     the archived opus deliverable and the repo-accessed flash seat; the
     difference is that the losses are now measured on capability, not on a
     2000-token harness cap. Lane spend this sitting: $0.1292 + $0.0724 =
     $0.2016 (under the $2 cap).

## Sub-item results (fold item 9: hollow-batch enforcement)

7. **Void-stamps landed in place** (a10#0/#1/#3):
   `memory/runs/ds_batches/gapfold_results.jsonl` 15/15 rows and
   `memory/runs/ds_batches/frontier_delta_results.jsonl` 14/14 rows each gained
   void=true + a named void_reason + ok_api=true + ok_material=false; original
   fields preserved. Classification verified byte-wise before stamping:
   gapfold - all 15 outputs carry generic lane-g<n> ids and none carries its
   item id (the falsifier law voids them); delta v1 - all 14 rows are
   refusals/UNVERIFIED shells (9 head with UNVERIFIED, 5 carry it after a
   heading; the a05 lane's "all 14 UNVERIFIED-headed" was loose, bytes read
   this sitting). Downstream counts can no longer read these rows as material
   success. Proof: post-write recount, void=true count 15/15 and 14/14.

8. **ok_api + ok_material split with per-row prompt_tokens** at the ds_workhorse
   run() row schema (was lines 90-94): ok_api = the wire answered (a 200 with
   empty text is still ok_api true); ok_material = the completion carries
   rendered material (never empty, never an __ERROR__ echo); prompt_tokens
   banked per row so a hollow prompt is visible at write time. Retry cost is
   now summed across attempts (the old code overwrote it - undercount).
   Old single "ok" field removed; per-row "model" field added (the a05#1 gap:
   the 2026-10-03 judge batch did not record its judge model).

9. **Rails law 2 pasted + render guards**: the hollow-batch law
   ("Material must render ... outputs without their material are VOID") is in
   the ds_workhorse docstring with cause (the 2026-10-03 incident, 30/30 rows
   ok:true) and evidence pointers. run() now fails the batch BEFORE any spend
   when the template lacks {text} or an item's text renders empty (SystemExit
   naming the item id). Cite: a10#3.

10. **Render-law test landed**: `tests/test_ds_workhorse_render.py` (4 tests).
    Instrument: `.venv/Scripts/python.exe -m pytest tests/test_ds_workhorse_render.py -q`
    -> **4 passed in 0.73s**. Covers: empty completion text banks ok_api true +
    ok_material false with a retry-on-empty (the sub-item's named case: empty
    text is not success even when the API returns 200); real completion banks
    ok_material true; template without {text} fails before any ask() call; an
    empty-text item fails the render guard naming the id before any call.

11. **AGENTS.md commands card pointer**: one line added after
    `python main.py verkle-audit --dry` naming the STANDING_RAILS hollow-batch
    law and the ok_api/ok_material split (closes the a10#3 "still zero:
    AGENTS.md" gap). Also the ONE permitted pointer line on the STANDING_RAILS
    commands-card section (the ds_workhorse drop-in table row now names law 2
    enforcement). Census bullet untouched.

## Test verdicts

- `pytest tests/test_ds_workhorse_render.py -q` -> 4 passed (0.73s).
- `pytest tests/test_ds_workhorse_render.py tests/test_inference_budget.py -q`
  -> 23 passed (1.32s) - the ds-adjacent file named by
  `git grep -l ds_workhorse tests/`.
- `pytest tests/test_instance_guard.py -q` -> 10 passed (0.79s) - the guard
  ds_workhorse imports.
- Live end-to-end: two real batches (14 asks + 27 judge items) ran clean
  through the new code path with the new schema.

## Files touched

- tools/ds_workhorse.py (edited: cap deleted, slice deleted, schema split,
  guards, docstring law)
- tests/test_ds_workhorse_render.py (new)
- watch/inbox/frontier_delta_register_20261003.json (rewritten: meta + per-row
  additions; 14 rows preserved)
- queue/STANDING_RAILS.md (lines 49-50 replaced; ds_workhorse drop-in row
  gained the law pointer; census bullet untouched)
- AGENTS.md (one pointer line in the Commands block)
- memory/runs/ds_batches/: gapfold_results.jsonl + frontier_delta_results.jsonl
  (void-stamped), frontier_delta_results_v3.jsonl (new, refire),
  delta_judge_items_v3.jsonl + delta_judge_results_v3.jsonl (new, judge),
  build_judge_items_v3.py (new, reproducible builder)
- this receipt

## Blockers

None. Two notes for the coordinator: (1) the $0.14 line itself sits in
watch/inbox/frontier_delta_steal_20261003.md, outside this lane's ownership -
the restatement is banked in the register and should be folded into the steal
doc by whoever owns it; (2) GO item 5 runs tools/md_record_seal.py over the
register - the register bytes changed this sitting, so sealing must run after
this wave, not before.
