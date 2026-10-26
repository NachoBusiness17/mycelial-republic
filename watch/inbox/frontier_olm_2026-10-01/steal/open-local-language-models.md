# Steal card: open-local-language-models (frontier olm 2026-10-01, round 2)

Round-2 draft. The round-1 critique (VERDICT: not approved yet) named one
prior-art hole and two fixable breaks plus six approve-after items; all six
are applied below and round-1's defects are owned in Retractions, not silently
patched. Round-1 text is overwritten by this file. The finds themselves stand;
the critique verified them independently and this round adds no new find
claims.

## Checks run THIS ask (round 2: commands and outputs, not claims)

1. Probe tool read IN FULL (the critique read only its header):
   `tools/abliterate_p1_probe.py`, 349 lines. What the estate already holds:
   a 20-prompt battery of the fleet's own janitor task shapes (:78-146,
   families socratic/guinea/diary/salon/afk/workrow, every row citing its
   estate source), a keyword verdict channel `classify()` :223-240 over
   REFUSAL_STRINGS :173-180 and CAPABILITY_MARKERS :186-198 (verdicts
   error | silent_empty | safety_refusal | capability_task_failure | complied),
   FKB cross-ref :243-251, the same /api/chat wire as mag/afk_loop.py
   (`_ollama_ask` def at `mag/afk_loop.py:103`, read this ask; the probe's
   endpoint is hardcoded `http://localhost:11434/api/chat` at :267),
   --model/--runs/--out args :279-282, fail-loud model-in-tags check :284-288,
   output schema `abliterate_p1_census.v1` :323, default out
   `watch/inbox/ball2/abliterate_p1_runs.json` (:33). DECISIVE nuance the
   header-only read missed: the battery is janitor TASK shapes, not harmful
   probes, so today's battery would not elicit safety refusals. The amendment
   therefore ADDS a refusal-probe battery family; it does not assume the
   existing battery can carry the A/B alone.
2. Baseline: `watch/inbox/ball2/abliterate_p1_runs.json` on disk, 42,936
   bytes, mtime Sep 29 11:07 (ls). INDEX registration measured precisely:
   `grep -n "abliterate" watch/inbox/INDEX.json` (14,217 lines) returns two
   rows, :12261 "ball2/abliterate-p1.md" (the lane receipt) and :12267
   "gala_20260925/ball-20260929/lanes/abliterate-p1.json". The RUNS JSON
   itself has no INDEX row, before or after this round's rebuild; the
   critique's "registered INDEX.json:12261" names the receipt row. The
   baseline bytes are on disk and cited by path.
3. Critique step 0 resolved by MY OWN fetch: `curl -sL https://docs.ollama.com/faq`
   = rc 0, 499,530 bytes (matches the critique's figure). Verbatim from the
   page (JSX-compiled MDX, quotes are the readable fragments):
   "OLLAMA_KV_CACHE_TYPE ... - The quantization type for the K/V cache.
   Default is `f16`"; "Currently this is a global option - meaning all models
   will run with the" (sentence continues past my quote window); values q8_0
   and q4_0 both present (2 occurrences each); and the GQA note verbatim:
   "GQA count (e.g. Qwen2) may see a larger impact on precision from
   quantization than models with a low GQA count." Consequence adopted into
   the probe: OLLAMA_KV_CACHE_TYPE is a serve-process env var, so each arm is
   its own server config: sequential restarts between arms (safe on one GPU)
   or a second instance on another port. There is no per-request toggle; the
   round-1 A/B shape was wrong and is retracted.
4. Installed models, MY OWN `ollama list` (the critique ran it first; this
   ask re-ran it): gemma:2b b50d6c999e59 1.7 GB, gemma4:latest c6eb396dbd59
   9.6 GB, qwen2.5:3b-instruct 357c53fb659c 1.9 GB all installed, plus
   qwen2.5:7b and qwen2.5:32b. The paper's exact family arm is available:
   qwen2.5:3b-instruct is the FIRST arm (GQA note above predicts it shows the
   larger KV-quant impact).
5. Duel seed corrected by full read: `watch/inbox/hermes_burn/DUEL1_hidden_1.md`
   read in full this ask (75 lines by the Read instrument; the critique
   counted 74). It is a duel adjudication transcript: contender answer
   "ab1-coremem-safeguard", a spec-review guardrail deliverable (write-admission
   guard clause G1-G7 with hypothesis and falsifier), NOT a refusal-probe
   bank. Round-1's "seeded from the estate's duel items" is retracted; the 20
   refusal probes are written-to-spec.
6. Estate KV-flag usage grep, run this ask: `grep -rn "OLLAMA_KV_CACHE_TYPE|kv_cache"
   tools/ mag/ scripts/ tests/` returns one binary substring hit in
   `tools/llamacpp/llama.dll` and ZERO source hits. No estate code or check
   asserts the KV regime today; find 3's ticket (c) absence claim is
   corroborated within those dirs.
7. Check-surface precedent verified on disk: `scripts/census_patrol_daily.ps1`
   and `scripts/register_census_patrol_task.ps1` both exist (ls). Find 3's
   ticket (a) now names this pattern as its surface (MISSING item 3 fixed).
8. Registration EXECUTED via the sanctioned writer (section below): the
   writer is `mag.shared_surface rebuild` ("the standing INDEX fold repair:
   it heals the surface", `mag/shared_surface.py:7`; INDEX.json is folded
   from append-only `watch/inbox/index_events.jsonl`, :27). MISSING item 1
   fixed.
9. Carried from round 1, independently reproduced by the critique, not re-run
   here: the live arXiv single-ID re-fetches (all three finds' numbers and
   titles byte-verified), register/catalog/sweep/C1/doors line checks, ollama
   0.34.3 + loopback bind (netstat 127.0.0.1:11434 LISTENING), HEAD ebf1b4813.
   Nothing in this round relies on a claim neither round verified.

## Registration (approve-after item 5, executed, outputs verbatim)

Before: `grep -c "frontier_olm_2026-10-01" watch/inbox/INDEX.json` = 0
(re-run this ask; matches the critique). `mag.shared_surface validate`
pre-rebuild: ok false, errors "hash mismatch: PACK_OFFLOAD.jsonl",
"hash mismatch: STEALTH_MINED_FINDINGS.jsonl", "hash mismatch:
DRIFT_PATROL_20261001.md"; warnings "unindexed inbox files: COST_TRUTH_20260930.md,
CYCLE_BRIEF_20260930.md, CYCLE_BRIEF_NEXT.md, DAY_SYNTHESIS_20260930.md,
GATE_DIGEST.md, QUOTA_LEDGER.md, STEALTH_TRIAGE_20260930.md,
STRATA_DROP_20261001.md, model_mating_paper_dig_20261001.md".

Then `./.venv/Scripts/python.exe -m mag.shared_surface rebuild` (heal mode),
then validate again: the three stale-hash errors and all nine unindexed
warnings are GONE (warnings list empty). `grep -c "frontier_olm_2026-10-01"
watch/inbox/INDEX.json` = 37 (was 0): the window's sweep, lens, and both steal
cards are now indexed. Residual validate errors after rebuild, reported as
they are: "hash mismatch: hermes_burn/WINDOW1_STATE.md" (a receipt other
descent lanes are actively writing; hash raced between census and fold) and
"indexed item missing" for two scratch files deleted after their registering
moment ("gala_20260925/vonnegut-final/lanes/vonnegut.checks.json",
"frontier_olm_2026-10-01/lens/_kg_check5.py"). These are other lanes'
in-flight tree, not damage from this rebuild; a later quiet-tree rebuild
folds them out. `abliterate_p1_runs.json` is still not indexed after rebuild
(the writer's scan rules do not pick it up); the baseline stays cited by path.

## Retractions (round-1 defects owned)

1. Prior-art hole on the probe instrument. Round 1 swept the three papers but
   never the probe mechanism: `tools/abliterate_p1_probe.py` and the Sep-29
   baseline census were already estate-held. That is the exact
   never-relearn-expensively failure the descent prior-art clause (which the
   round-1 card itself invoked) exists to stop. Fixed: the probe is an
   AMENDMENT of the banked tool, and results land comparable to the Sep-29
   baseline (same wire, same `classify()` channel, same verdict vocabulary;
   schema bump is additive).
2. Probe shape wrong. Round 1 implied a per-run KV toggle. OLLAMA_KV_CACHE_TYPE
   is a global serve-process option (FAQ verified this ask, check 3). Fixed:
   sequential-restart runbook (or second port), arm config recorded in each
   run file.
3. Duel-seed mislabel. The duel hidden files are adjudication transcripts, not
   a refusal bank (check 5). Fixed: the refusal probes are written-to-spec.
4. Round-1's "no prior estate measurement of gemma:2b refusal rates surfaced
   in this ask's searches" was true of searches that never looked. Superseded
   by re-bank item 1: a Sep-29 baseline census exists with
   safety_refusal/capability_task_failure/complied counts on gemma:2b.

## Re-bank ledger (estate-held, labeled, not re-derived)

- Probe instrument: `tools/abliterate_p1_probe.py` (full inventory in check 1)
  plus baseline `watch/inbox/ball2/abliterate_p1_runs.json` (42,936 bytes,
  Sep 29 11:07; INDEX rows: receipt :12261, lane json :12267; runs file itself
  unregistered). The critique caveat stands: its overlap read was header-only;
  MY full read (check 1) confirms the mechanism and finds the one thing the
  header hides (janitor-shape battery, not harmful probes).
- Find 1's port substance (judge ensembles never keyword rates, serving-regime
  scoring, E4 compression arm): current-window sweep :93-95 and :215-227,
  round-1 read. This card's real deltas: the C1:53 single-channel defect
  identification (verified round 1) and the concrete amended-tool probe below.
- Find 2's port (model-DATE covariate, LLM-coder labeling against a small
  owned reference): sweep :218-219 and :104-106, round-1 read.
- Find 3's port (three-line hardening ticket, live bind measurement,
  slot-restore OWED): round-1 original, genuinely new; the sibling card
  kv-cache-context-engineering.md has zero overlap per the critique's grep
  (18526/slot/tenant/hardening/bind/11434: no hits), not re-run this ask,
  cited from the critique.

## Find-by-find estate map (updated)

### 1. 2609.31678, When Keywords Drop but Classifiers Hold (2026-09-16)

Quote carried (live re-verified round 1, reproduced by the critique): "On
Qwen2.5-3B, keyword refusal falls from 98.0% to 80.5% (McNemar p~1e-8) while
classifier refusal stays near ceiling (99.0%-99.5%) and MMLU accuracy is
unchanged (50.0%)". Sweep anchors :88-98.

Organ: the quantizer and the C1 censorship program's E3. Port: amend
`tools/abliterate_p1_probe.py` (the banked census) with four additive changes:
(a) a NEW refusal-probe battery family, 20 written-to-spec harmful-shape
prompts with long filler context per the paper's protocol shape; the existing
20-prompt janitor battery stays so every row remains comparable to the Sep-29
baseline; (b) a judge channel beside the existing keyword channel
(`classify()` untouched); (c) per-run arm metadata (kv_cache_type, model tag
and digest) in the summary, schema `abliterate_p1_census.v2`, additive fields
only; (d) results to NEW dated --out files, the Sep-29 baseline file untouched.

C1:34 reconciliation (approve-after item 3), one sentence: the Ollama arm of
this probe is a deployment-regime audit under the paper's own "judges matched
to the serving context" clause, not a mechanism measurement; direction
extraction and family-cosine work stays in transformers per
`watch/inbox/hermes_burn/C1_censorship_ASSEMBLED.md:30-34`, and this probe
claims only deployment-regime deltas.

### 2. 2609.25447, Conduct Under Pressure (2026-09-21)

Quotes carried (byte-verified `state/arxiv/2026-09-23/2609.25447v1.txt:6`,
round 1): Spearman -0.64 fold/capability with little vendor effect; six of 17
manner codes sort by vendor (p <= 0.001); LLM coders alpha 0.66 vs human 0.46.
Sweep anchors :99-106.

Organ: C1 experiment design and the gopher fleet's duel labeling. Port
(unchanged substance, now folded into the same probe run): pin model date and
a capability-index proxy as recorded covariates in every E1-E3 run (sweep
:218-219; adopted, not re-derived), adopt the frozen-codebook +
small-owned-reference + LLM-coder labeling scheme for fold/manner, and log
model tag + digest beside every probe row (check 4's digests are the first
entries).

### 3. 2609.18526, The Illusion of Local Privacy (2026-09-16)

Quotes carried (live re-verified round 1): allocator residue surviving
sanitisation; llama.cpp cross-tenant state restore, 200/200 trials. Sweep
anchor :107-115. The 0928 kv sweep's "cache timing side channels" label
remains corrected (round-1 check 5).

Organ: the sovereign mirror, concretely the shared janitor host (Ollama
0.34.3, loopback-only bind measured round 1 and reproduced by the critique).
Port: the three-line hardening ticket, surfaces now named (MISSING item 3
fixed): (a) bind assertion as a daily check in the census-patrol pattern
(`scripts/census_patrol_daily.ps1` + its register script, both verified on
disk this ask): netstat -an, FAIL on any 11434 LISTEN line not bound to
127.0.0.1; (b) API-surface enumeration for state save/restore routes
(probe below); (c) prompt-lifetime guarantee ticket, absence corroborated by
check 6's zero source hits within tools/mag/scripts/tests (absence beyond
those dirs not proven).

## The one probe this week (amended: approve-after items 1, 2, 4, 6)

Amend `tools/abliterate_p1_probe.py`; do not roll a new bank.

1. Add the refusal-probe family (20 written-to-spec prompts, long filler
   context) plus the judge channel plus arm metadata (schema v2, additive).
2. Arms in order: qwen2.5:3b-instruct FIRST (the paper's exact family, and
   the FAQ GQA note predicts Qwen2-family shows the LARGER KV-quant impact),
   then gemma:2b (the incumbent janitor). qwen2.5:7b/:32b are installed but
   out of scope this week.
3. Runbook per arm: OLLAMA_KV_CACHE_TYPE is a serve-process env var (FAQ,
   check 3). Arm A: unset (default f16). Arm B: q8_0, applied by a server
   RESTART (sequential, one GPU) or a second instance on another port. OWED
   at run time: confirm the effective KV type from the server's own startup
   log or API before trusting the arm label; the FAQ states the option but
   this ask did not verify the confirmation surface, and `echo` of the env
   var is recorded per arm as the weaker guarantee.
4. Scoring per completion: keyword channel (`classify()`, unchanged) AND
   judge channel: primary judge gemma4 (c6eb396dbd59, installed);
   DISAGREEMENT judge is the cross-family janitor NOT serving as the arm
   (qwen2.5:3b-instruct when gemma:2b is the arm; gemma:2b when
   qwen2.5:3b-instruct is the arm), so the arm never judges itself; residual
   disagreements log to a rows file for operator arbitration, and both judge
   counts are reported either way.
5. Per-arm expected volume: 40 prompts x 3 runs = 120 inferences, plus judge
   passes; all local, zero spend.

Prediction, stated before running: under KV q8_0 the keyword channel's
safety_refusal rate drops materially while the judge channel's refusal rate
stays near ceiling and the janitor battery's complied rate does not move, on
at least the qwen2.5:3b-instruct arm. Falsifier: keyword and judge channels
move together (or neither moves) on both arms, including the Qwen2-family arm
the GQA note says should be most sensitive: then the find does not transfer
to this stack, E3 stays weight-quantization-only, and this card's amendment
dies on local bytes. Either outcome is a banked E3 delta against the Sep-29
baseline.

Per-find alternates banked (judge now named; approve-after item 6): (find 2)
gemma4 plus the same cross-family second judge label fold/manner on 20 banked
duel transcripts against one hand-labeled reference; falsifier: agreement
below the paper's human baseline 0.46 keeps human labels on the duel
instrument. (find 3) two-tenant canary against 127.0.0.1:11434 plus the
API-surface enumeration; falsified if any tenant-B-visible call returns
tenant A's canary or the bind opens beyond loopback.

## OWED / not run (round 2)

- No probe executed this ask; the tool amendment is specced, not coded. The
  only state change this ask is the INDEX rebuild (Registration section) with
  its before/after outputs recorded above.
- Effective-KV-type confirmation surface (server startup log line or API
  readout): not verified; probe step 3 owns it at run time.
- Ollama 0.34.3's embedded llama.cpp version, and whether the flawed
  slot-restore path exists in it: OWED, unchanged since round 1.
- `abliterate_p1_runs.json` remains unindexed after the sanctioned rebuild
  (writer's scan rules; check 2 and Registration); the baseline is cited by
  path and byte count.
- The steer-JSON defect (`.zcode/workflows/olm-mine.dwf.ts:392-393`,
  card JSON not retrievable by the reviewer seat): script-owner note carried
  from round 1; the critique hit it again this round. Fix belongs to the
  script owner: interpolate `JSON.stringify(card)` into the steer ask.
- Sibling-card non-overlap grep and the critique's abliterate overlap read
  are cited from the critique, not re-run this ask (round-2 checks 1, 2, 6
  cover the load-bearing parts first-hand).
