# prereg-attack / candidate two: the freeze covered the bars' words, never the bars' instrument

Candidate: prereg-attack-two. Target: the interference-search prereg
(watch/inbox/INTERFERENCE_REPLICATION_PREREG_20260925.md + amendment 1 +
watch/inbox/BOOT_LANE_INTERFERENCE_BURN_CLOSE_20260926.md). Every claim below
was checked against bytes in this session; commands and outputs cited inline.

## Approach

Attack the prereg's freeze MECHANISM, not any bar's calibration: the frozen
bars are committed prose, but every script, fixture, result row, and the entire
vendored repo that operationalizes and evidences them lives in gitignored
paths with no hash pin and no version history, the instrument was demonstrably
rewritten mid-experiment after partial results existed, the filed 50-state FAIL
is irreproducible from the current tree, and the gemma:2b serving artifact is
an unpinned mutable tag. A third party can therefore neither verify, reproduce,
nor adjudicate a single frozen number, which breaks the prereg's own frozen
claims ("No bar moves after results exist", the cost-unit token clause,
amendment 1's parse-fail-report clause) without touching a single bar.

## Frozen claims this attack breaks (path:line, all read this session)

1. "Bars below are frozen BEFORE any arm runs. No bar moves after results
   exist." (prereg header, INTERFERENCE_REPLICATION_PREREG_20260925.md:5-7)
2. Cost-unit law: "LLM tokens counted and reported for Arm A/C."
   (INTERFERENCE_REPLICATION_PREREG_20260925.md:46-48)
3. Amendment 1 clause 2: "parse-fail rate is reported in the close receipt."
   (INTERFERENCE_REPLICATION_PREREG_AMENDMENT1_20260925.md:29-31)
4. "ARM C budget-50: 0/30, frozen bar kept" (the filed FAIL under the frozen
   50-state bar; BOOT_LANE_INTERFERENCE_BURN_CLOSE_20260926.md:11-13)
5. Commit a5dd96176's committed assertion "interference-search vendored +
   replication (Arm B 30/30 EXACT, prereg+amendment frozen)": that commit
   contains ZERO files under corpus/library/interference-search (verified:
   `git ls-tree -r a5dd96176 --name-only | grep -c "corpus/library/interference-search"`
   returned 0) and zero replication run files; the assertion is backed only by
   ignored working-tree bytes.

## The break, evidence by evidence (exact commands, real outputs)

### A. The entire adjudication surface is gitignored and unversioned

- `git check-ignore -v memory/runs/interference_replication_20260925/run_armC.py
  corpus/library/interference-search/results/fleet_replication_20260925.json`
  returned `.gitignore:92:memory/runs/**` and `.gitignore:197:corpus/library/`.
- `git ls-files corpus/library/interference-search/` returned nothing
  (tracked-count 0); `git ls-files memory/runs/` returned 1 unrelated file.
- `git log --follow` on run_armC.py and on run_armA.py both returned EMPTY:
  neither script was ever committed. No history exists to adjudicate which
  script version produced which filed row.
- watch/ESTATE_INDEX/ESTATE_INDEX.jsonl rows for run_armC.py record only
  path/mtime/size, no content hash.

Consequence for claim 1: "no bar moves after results exist" is unenforceable as
frozen. The bars' operational meaning (rank prompt, batch rule, parse policy,
budget loop) lives in bytes that any process can rewrite with no trail, and
which were in fact rewritten (next item).

### B. The instrument demonstrably moved after results existed

- run_armC.py:7 docstring: "Runs budgets (200,) only since the reboot"; the
  loop at run_armC.py:81 is `for budget in (200,)`. The 50-leg rows were
  produced Sep 25 (armC_gemma2b_judge.jsonl, mtime Sep 25 19:34, verified
  byte-identical to armC_budget50_complete.jsonl via `cmp` -> IDENTICAL), by a
  script version that ran budget 50; the tree's current script cannot rerun it.
  The filed "ARM C budget-50: 0/30" (claim 4) is IRREPRODUCIBLE from the
  current tree: a third party executing the estate's own instrument gets only
  the 200 leg.
- run_armC.py:54-55 comment: keep_alive "2h" pin added because "attempt-1
  starved 5h on problem 2". watch/inbox/DIRECTIVE_WATCHERS_20260926.md incident
  receipt confirms the edit ordering: "script keep_alive fix ('2h') present
  before relaunch" (07:06 ET, Sep 26), i.e. AFTER attempt-1's and attempt-2's
  partial rows were on disk. The same receipt documents a 06:07:19 double-start
  (two PIDs, 9 ms apart, both opening armC_gemma2b_judge_200.jsonl in "w"
  mode), so the output file's provenance includes a truncated-write incident.
- This is not covered by prereg text: the prereg's only determinism devices are
  "One seed" (problem RNG), "greedy, temperature 0" (Arm A decode), and Arm B's
  env-delta band (">=27/30 (allows 1-2 hardware/env deltas)", which protects
  Arm B alone). Nothing anticipates instrument edits after partial results.

### C. Frozen clause already broken in the estate's own bytes (no third party needed)

- Claim 2 (tokens): run_armC.py:35 `stats = {"calls": 0, "states_judged": 0,
  "parse_fails": 0}`; rows carry cost/secs but no token count; the ollama
  response's eval_count is captured in run_armA.py:50 but never in run_armC.
  Arm A complies (verified rows: tokens min 54 / median 81 / max 95); the arm
  that IS the steal test cannot produce the token report the prereg froze.
  The eventual 200-leg summary row will ship calls/states_judged/parse_fails
  and no tokens: the frozen cost-unit law is unmet by construction.
- Claim 3 (parse-fail rate in the close receipt): `grep -n -i "parse"
  watch/inbox/BOOT_LANE_INTERFERENCE_BURN_CLOSE_20260926.md` returned nothing
  (exit 1). The datum exists only in an ignored jsonl: the 50-leg summary row
  reads {"budget": 50, "summary": "0/30", "calls": 72, "states_judged": 1714,
  "parse_fails": 0}. The frozen reporting clause is unmet for the only
  completed Arm C leg.
- No sha256/digest exists anywhere in the prereg, amendment, close receipt, or
  B2_140 fold receipt (`grep -c sha256` returned 0 on each; grep for digest in
  both prereg docs returned exit 1).

### D. The serving artifact is an unpinned mutable tag (adjudication basis absent)

- Live probe this session: `curl http://127.0.0.1:11434/api/tags` reports
  gemma:2b digest b50d6c999e592ae4f79acae23b4feaefbdfceaa7cd366df2610e3072c052a160
  (modified 2026-08-28). That digest appears nowhere in the prereg estate.
- The prereg pins the problem RNG to the byte (see honest negatives) but pins
  nothing about the LLM: no model digest, no ollama version, no quantization,
  no thread/batch config for Arms A/C. When the owed 200-leg lands near the
  frozen >=15/30 secondary bar, a third party rerun landing 1-2 problems on
  either side cannot be adjudicated: the prereg cannot say whether the rerun
  broke the claim or merely pulled a different untagged gemma build or ollama
  version. The frozen verdict "PASS/FAIL at 15" would rest on a single draw
  from an unpinned, serving-nondeterministic stack with "One seed" as its only
  (problem-side) determinism device.

## Why this is not already-covered (kill-condition defense)

- The prereg text nowhere covers instrument versioning, model-artifact pinning,
  or evidence-path ignoring; its determinism devices are enumerated in B above
  and none of them reach this surface. Arm B's env-delta allowance is the one
  place the prereg admits environment variance, and it explicitly protects
  only Arm B.
- The prior adversarial pass (INTERFERENCE_PREREG_ADVERSARIAL_GROK47_20260925.md)
  is already-known territory: its five attacks are (1) 200 sits in a saturated
  regime, (2) 50-bar reinterpretation and non-integer aggregates, (3) two
  budgets as a second life, (4) unfrozen decode/rank prompt, (5) skip-later
  retrofit. None of them names provenance: #4 demanded the rank prompt be
  frozen "in the receipt", and the estate answered by freezing it in CODE
  (run_armC.py llm_score), which is precisely the hole this attack opens: a
  freeze in an unversioned, gitignored, twice-edited-after-partials file is not
  a freeze. This attack also lands on already-filed results (claims 2, 3, 4 are
  broken TODAY by the estate's own bytes), not on a hypothetical future PASS,
  which is what all five Grok attacks targeted.
- Adjacent known item I explicitly do NOT claim: the amendment's "8.1/30" and
  "6.9/30" reference numbers are rounding artifacts of the rates 0.26667 (8/30)
  and 0.23333 (7/30) in results/fleet_replication_20260925.json (0.27*30=8.1,
  0.23*30=6.9); Grok #2 already flagged the non-integer aggregates, so I file
  only the resolution (they are percentage round-trips, actual counts 8 and 7),
  not the attack.

## Honest negatives: attacks I ran that the prereg survived (first-class)

- Problem-set freeze HELD. Ran regeneration with the repo venv:
  `.venv/Scripts/python.exe -c` importing gen_hard_problem from the vendored
  package, `rng = random.Random(11); [gen_hard_problem(rng) for _ in range(30)]`
  compared against memory/runs/interference_replication_20260925/problems.json:
  byte-equal as parsed structures, numbers+target equal in order, 30/30. The
  one thing the prereg pinned to the byte (seed 11) is exactly the one thing
  that survives third-party attack. The contrast is the attack's spine: what
  was left unpinned is the breakable surface.
- Arm B width paraphrase HELD: prereg "width=b//12" matches benchmark.py:48-49
  `width=max(1, b // (3 * len(p["numbers"])))` for 4-number problems.
- Cost-unit judged-state accounting HELD in code: Countdown.judge returns
  `len(states)` as cost (countdown_domain.py:23), so gemma's batched judging
  spends the same unit as the trained judge. A batched-states-are-free attack
  dies on this line.
- Arm A implements its frozen decode: prompt_text imported from their repo,
  temperature 0, num_predict 1500 (run_armA.py:36); 0/30 with 54-95 tokens per
  row (early EOS, not cap truncation); 2 rows contained answer tags, 0 correct.
- Arm B "matches published exactly" HELD at the aggregate level the publishers
  made available: results/fleet_replication_20260925.json rates equal
  results/countdown/countdown_benchmark.json rates at BOTH budgets for all
  three arms (0.26667/0.13333/0.23333 at 50; 0.7/1.0/1.0 at 200). Per-problem
  identity is unpublishable from their artifacts (benchmark.py stores only
  rates), so "EXACT" means aggregate-exact; a wording nit, not filed as a break.

## Moves with estate paths

1. Pin the instrument bytes: track (or force-add past .gitignore:92) run_armA.py,
   run_armC.py, problems.json and every result jsonl under
   memory/runs/interference_replication_20260925/, and record their sha256 in
   an amendment-2 section of watch/inbox/INTERFERENCE_REPLICATION_PREREG_20260925.md.
   Touches: .gitignore:92, the run directory, the prereg doc.
2. Restore 50-leg reproducibility: change run_armC.py:81 `for budget in (200,)`
   back to (50, 200) or add a --budget flag, so the filed 0/30-at-50 is
   generable from the tree again. Touches:
   memory/runs/interference_replication_20260925/run_armC.py:81.
3. Close the cost-unit token gap: capture eval_count per ollama call in
   llm_score and write a tokens field into every row and the summary row.
   Touches: run_armC.py:35,47-63,89-101.
4. Report the parse-fail rate in the close receipt as amendment 1:29-31
   demands; the 50-leg datum already exists (parse_fails 0 of 1714 states,
   72 calls). Touches:
   watch/inbox/BOOT_LANE_INTERFERENCE_BURN_CLOSE_20260926.md.
5. Pin the serving artifact before the owed 200-leg rerun: write the gemma:2b
   digest b50d6c999e592ae4f79acae23b4feaefbdfceaa7cd366df2610e3072c052a160 plus
   the ollama version into the amendment, so a >=15/30 verdict has an
   adjudication basis. Touches:
   watch/inbox/INTERFERENCE_REPLICATION_PREREG_AMENDMENT1_20260925.md and the
   OWED rerun clause at BOOT_LANE_INTERFERENCE_BURN_CLOSE_20260926.md:74-82.

## Falsifier (the attack's own kill test)

If someone shows (a) a committed or hash-pinned copy of the exact script
version that produced the Sep 25 50-leg rows, or (b) a tracked path holding the
result bytes the close receipt and commit a5dd96176 cite, or (c) that the
prereg or amendment already pins the model digest or an equivalent
reproducibility contract for Arms A/C, then this attack's claims 1, 4, and D
collapse to wording preferences and only the outright-unmet clauses (claims 2,
3) survive as debt. Conversely the attack is CONFIRMED the moment a third
party, given commit a5dd96176 plus the working tree, cannot regenerate the
filed 0/30-at-50 (they cannot: the loop runs only budget 200) or find any byte
hash connecting the filed numbers to the scripts that produced them (they
cannot: zero hashes exist, verified by grep).

## Owed

- The Arm C 200-leg itself remains owed (per B2_140 and the close receipt
  addendum); this attack claims no solve count and does not touch the frozen
  bars' values.
- I did not rerun the 50-leg to sample serving nondeterminism: multi-hour leg
  on a shared box, and unnecessary for the break, which rests on script bytes
  and absent hashes, not on a measured variance. A 50-leg rerun after move 2
  would quantify it and is the natural follow-up.
- I did not verify whether the ollama chat template wraps the bare /api/generate
  prompt (a further reproducibility variable); noted, not checked.
- Per-problem Arm B identity: unpublishable from their artifacts (rates only);
  if their repo ever ships per-problem results, the "EXACT" wording should be
  re-audited then.
