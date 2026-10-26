# s2-23: the full receipt lifecycle census (2026-09-28)

Question: how does a receipt go from gopher output to committed file to INDEX.json item to quantizer pack to context pack? What are the gates at each stage? What gets lost?

Method: every code claim cites the file and line read this session; every number comes from a command run this session (commands listed at the end). Census is read-only over every surface it measures: no quantizer recompile, no baseline-update, no gate fix, no manual rebuild. The one live FAIL found (ratchet NEW debt) belongs to sibling lanes and is left for its owner. One write outside measurement was made on purpose: the two banked twins below were registered into INDEX through the sanctioned add writer at their final bytes (postscript documents why).

## Stage 1: gopher output -> banked file

The ask itself is the first gate: it carries the no-fabrication law, the em-dash law, and the exact bank path (this ask's own text: "never fabricate (OWED if unverifiable)", "Bank to watch/inbox/burn_reset_20260927/flash50/").

The workflow that spawned the gopher passed `tools/workflow_gate.py check --script` before CreateWorkflow. The gate enforces seven checks on the script text (tools/workflow_gate.py:13-21, definitions :45-80):

- G1 multiplicity: Mickey17 gopher fan-out, per-item named actors.
- G2 passoff: an earlier actor's output feeds a later ask.
- G3 steering: reviewer verdict carried back into a revision ask (plus the B2-206 judge-model soft warn, :96-114).
- G4 salvage: incremental report() inside the fan-out so work survives a dead run.
- G5 deliverable: published artifact plus report-shape return.
- G6 receipts: "durable receipt landing in watch/inbox with a dated stamp" (tools/workflow_gate.py:71-74); a mention without a `source-fetched:`-style YYYY-MM-DD stamp is a SOFT warn, never a block (:117-135).
- G7 laws: "no em-dashes" AND no-fabrication wording carried inside the asks (:75-79).

Every submission registers a ledger row in memory/workflows/REGISTRY.jsonl (docstring :10-11); scenario cards in configs/workflow_gate_scenarios re-prove each gate against real FAIL rows (docstring :22-31).

Writer-side hook: the gopher's Write/Edit under the estate's durable roots fires `tools/md_record_seal.py`: a PreToolUse gate blocking Write of content over 8 MB into watch/, and a PostToolUse seal appending ONE autoseal line to watch/inbox/index_events.jsonl; since the 2026-09-26 writer-contract fix a REGISTER event joins the autoseal so the INDEX fold lifts the file into active items (tools/md_record_seal.py:8-21). The hook is fail-open by law: any internal error exits 0 with a stderr note (:18-21).

Gets lost here: a session that dies before its first report() loses everything before it (G4 narrows, never closes); files created by shell redirection or python writes never pass through the Write hook, so no autoseal fires for them; the G6 dated stamp is soft, so an undated receipt lands with no gate noise.

## Stage 2: file -> git commit

The gopher commits by pathspec (sibling lanes share one tree; the commit-race convention is documented in the f-24 landing commit message on this branch). The push carries the gates: githooks/pre-push, in order:

| Gate | Line | Enforcing? |
|---|---|---|
| violation_ratchet check --changed over mag/+tools/ | :9-10 | exit 1 blocks |
| config_seal verify | :11-12 | exit 1 blocks |
| description_pin | :19-23 | WARN-ONLY (TODO-FLIP-TO-ENFORCE) |
| freshness_gate (today's watch/inbox/*.md, 5-receipt cap, date-stamp prefilter) | :41-56 | WARN-ONLY |
| census_drift_patrol (stale = exit 1 WARN; blind cannot-verify = exit 2 BLOCKS, :85-100) | :76-101 | blind blocks |
| checkbox_receipt_gate | :104-116 | WARN-ONLY |
| caption_ledger_verify (conditional on generator/verifier diff) | :140-166 | WARN-ONLY |
| refold_gate (conditional on fold-host/pins diff) | :203-231 | WARN-ONLY |

Plus the scenario-suite gate from AGENTS.md build discipline: a working-tree or pushed-range change to tools/workflow_gate.py runs the LAW-12 card suite read-only and a red suite blocks the push.

Live check this session: `.venv/Scripts/python.exe tools/violation_ratchet.py check --changed` exited 1: "scope=14 changed files; hits=14; registered=11; NEW=3": NEW debt mag/corpus_gap_research.py:663 file-too-long, mag/corpus_selfsteal.py:460 file-too-long, tools/fossil_check.py:73 shell-true. Those files are sibling lanes' uncommitted edits, not mine: the ratchet is TREE-WIDE, so one sibling's in-flight debt blocks every lane's push until it is fixed or accepted by name. Shared-tree contention is a structural property of this gate, not a bug in it.

Gets lost here: untracked receipts. Measured: flash50 holds 309 files on disk, 196 tracked by git, 113 NOT tracked (`git ls-files watch/inbox/burn_reset_20260927/flash50` vs disk walk). Untracked receipts can never be pushed, so their lineage exists only on this disk. The WARN-ONLY gates cannot stop a stale or unreceipted push; and pushes are operator-paced, so local commits sit unpushed indefinitely (branch mag/run-beta1-factory-build-audi-20260806T231709Z has no upstream shown in `git status -sb`, so ahead/behind is unknowable from status alone).

## Stage 3: file -> INDEX.json item

Design (scripts/index_fold_host.mjs:1-135 header): writers never read-modify-write INDEX.json. Every change is APPENDED as one JSON line to watch/inbox/index_events.jsonl and INDEX.json is a DERIVED fold. The log is the source of truth; events are never erased; invalidate marks an item inactive instead of deleting its register.

Two writer paths:

1. Manual: `node scripts/index_fold_host.mjs add <file> [class] [purpose] [--living|--living-open]` (:703-748). It hashes the exact bytes once (:722-730), mints a BigInt-safe seq (B2-40 scheme, :331-346), a per-writer nonce, then appends and refolds INDEX.json atomically via tmp+rename (:529-554).
2. Automatic: md_record_seal autoseal+register on every Write/Edit under watch/inbox (stage 1).

Gates on this stage:

- B2-147 writer-side poison guard: add/invalidate DIE before append when the normalized path matches OUTSIDE_RE (repo roots like mag/, memory/, watch/...) or has no inbox-relative form (:679-688, regex :226).
- B2-40 fold warning channel: outside-dropped and unresolvable registers are counted per top segment and surfaced WARN + exit 2 instead of vanishing silently (:359-366, :496-509).
- B2-342 closed key vocabulary configs/events_key_schema.json: the fold WARNS on unknown event keys (:396-426); `mag.shared_surface validate` ERRORS on the same keys (mag/shared_surface.py:237-258).
- B2-42 malformed-line hygiene: the fold's reader tolerates bad JSON forever, so validate errors on any NEW malformed line not grandfathered by content sha in configs/events_malformed_baseline.json (mag/shared_surface.py:194-229).
- B2-156 living-file law: `--living` seals (sha256, size) over the first N bytes so append-only growth passes while prefix mutation fails; `--living-open` is an unsealed edit board (mag/shared_surface.py:303-337).
- B2-297 living-downgrade watchlist: a plain re-register legally drops the living flag (last-register-wins), so validate warns when one of the three known living paths folds flag-free (mag/shared_surface.py:121-133, :347-370).
- Whole-file hash verification on every validate run (mag/shared_surface.py:299-337) and on `node scripts/index_fold_host.mjs verify` (:569-651).

Live checks this session (both run to completion):

- `node scripts/index_fold_host.mjs verify`:
  - "skipped malformed lines: 94,95,96"
  - "verify: INDEX.json item count (1415) != folded count (1639)"
  - "verify: 1594 hash-clean, 5 living-ok, 18 living-open, 18 mismatched, 4 missing, 0 living-unverified (of 1639 active items)"
  - failures include 4 MISSING files (registered sha256, file gone: burn_reset_20260927/queue/Q_032_body_patch.py, Q_038_debug.js, fifty_wide_20260917/FW09_mag_moves.md.placeholder, flash50/_fix_emdash_deep_operator_model.py) and 18 HASH MISMATCH files edited after their register.
- `.venv/Scripts/python.exe -m mag.shared_surface validate` -> exit 1, ok=false: 6 errors (1 LINKS event-kind row SCOUT-QUIET-3 line 377 + 5 whole-file hash mismatches: SELF_STEAL_REBUILD_RETEST_SALON_20260831.md, GAP1_SPAWN_MANIFEST_20260906.md, REVEAL_FIVE_REHEARSALS_20260906.md, SEAT_SPORes_AUDIT_CELL_20260912.md, STEALTH_SWEEP_LATEST.md), 1 warning (91 unindexed top-level inbox files), 1415 indexed items checked, events key scan clean (5482 lines, 0 unknown keys), malformed 3/3 grandfathered/0 new, living 5 ok + 18 open + 0 unverified + 0 downgraded.

Gets lost here (the stage with the most structural loss):

1. Materialization lag. INDEX.json's own derivations block says derived_at 2026-09-28T18:27:28.578Z from event_count 4696 -> active_items 1415. The log now holds 5488 parseable events. A fresh fold yields 1639 active items (verify's own count), so 224 receipts are invisible to every INDEX.json reader until somebody reruns rebuild/add. My flash50 sibling receipts: 184 distinct paths active in a fresh fold (my python reimplementation of the fold semantics over index_events.jsonl: register/invalidate last-op-wins over normalized paths) vs 14 present in the stale materialized INDEX.json -> 170 flash50 receipts currently invisible to INDEX readers. Nothing schedules the refold.
2. Subfolder blind spot. validate's unindexed-file warning scans only TOP-LEVEL inbox files (mag/shared_surface.py:268, `INBOX.iterdir()` non-recursive), so an unregistered file inside a dated subfolder (flash50 included) can never trigger it. All 91 warned files are top-level; subfolder coverage is verify-only and verify is hand-run.
3. Tolerant reader residue. 3 malformed lines (94,95,96) fold over forever, gated only by the content-sha baseline; the no-erase law keeps them in the log.
4. Ops the fold ignores. Op counts over the log this session: register 4091, autoseal 1147, invalidate 135, amend 17, note 14, repair 1, windowseal 1, filed 1, and 81 events with NO op key at all. The fold loop handles only register and invalidate (index_fold_host.mjs:440-485). Concretely: 17 `amend` events carry fresh sha256s the fold NEVER applies, so the INDEX keeps the stale hash until a full re-register (this is the mechanism behind the 18 hash mismatches verify found); the 81 no-op-key events parse clean and pass the key-schema gate (their keys are registered) yet register nothing: e.g. writer "sancho" line: `{"t": ..., "path": ..., "seq": 1788238807095, ...}` uses path/t where the fold reads file/ts.
5. Free-text class. The class field has no enum: measured distribution over the 1415 materialized items: BACKFILL 569, receipt 482 (lowercase), RECEIPT 161 (uppercase), data 26, artifact 21, FACT 15, STEAL 15, AMENDMENT 14, UNPROVEN 12 (the default when add gets no class), PROPOSAL 6, DECODE 5, PLAN 5. Consumers cannot rely on the casing.
6. Authority stays unclassified. The INDEX header authority is "untrusted_data_until_classified" (mag/shared_surface.py contract checks; visible in INDEX.json itself): an INDEX item is a pointer, never a verdict.

## Stage 4: receipt text -> quantizer pack

The hop the ask names ("INDEX.json item to quantizer pack") DOES NOT EXIST AS CODE. tools/thought_quantizer.py reads exactly one input: memory/percolator/invariants.json (tools/thought_quantizer.py:36, DEFAULT_IN). Invariants are written by mag/percolator.py `percolate(text)` (module docstring :1-25; INVARIANT_REGISTRY :41), and its callers this session's grep found are mag/chord_pipeline.py:98, mag/evolving_wave.py:223, mag/compiler_lang.py:110, mag/research_class.py:112, mag/social_hone.py:103, mag/poc_stage2.py:93, mag/frontier_help.py:152: lane pipelines, NOT the inbox or INDEX. A receipt that no lane feeds through percolate() never becomes an invariant, no matter how well it is banked, committed, and registered. This is the widest silent gap in the lifecycle: every later stage can be green while the receipt's content never entered the thought pipeline at all.

Percolator gates (deterministic, $0, stdlib-only per docstring): sentences classified SIGNAL vs THEATER vs NOISE by lexicon; repeat (seen canonical fingerprint) -> compiled invariant deduped by content hash; novel -> memory/percolator/explore.jsonl; noise -> memory/ghost/noise/. Evidence the gate mangles: invariant 1182ee5e2bc05248 reads "backend not reachable at http://127. Start it with: python -m backend.": the URL was split mid-address by sentence segmentation. Counts are echo-inflated (top row count=232214), which is why the quantizer demotes raw counts to "provenance only".

Quantizer gates (tools/thought_quantizer.py):

- refuse fragments under 25 chars (:52, :62-64)
- two-pass v0.3: pure telemetry refused, but error-quoting LAWS kept when imperative-shaped (:44-79, counted as error_quoting_laws_kept)
- dedupe by 60-char normalized signature (:103-107)
- weight = recency (buckets :82-96) x shape (:99-100); raw percolator count is provenance, never weight (:18-19)
- pack caps: frontier 24, flash 12, local 12 rows (:228-230)
- flash tier = first sentence truncated at 220 chars (:53, :110-113); local = 10 words (:54, :116-118)
- fossil arm `--check`: packs stale at 24h -> exit 1 (:200-217)

Live checks this session:

- `.venv/Scripts/python.exe tools/thought_quantizer.py --check` -> "THOUGHT-QUANTIZER: fresh, 7.6h old (v0.3)", exit 0.
- compile_report.json stats: in 331 -> refused_telemetry 2, refused_fragments 9, dedupes 13, kept 307 (error_quoting_laws_kept 37); packs frontier 24, flash 12, local 12.
- 307 kept minus 24 in the largest pack = 283 kept laws (92.2 percent) are in NO pack. Rank cutoff is silent: kept-but-unranked rows vanish with no counter anywhere.
- Dumped all 12 flash rows: 3 of 12 are shell error fragments now compiled as fleet law: "No such file or directory: 'Get-ChildItem'" (raw_count 9), "...'type'" (9), "...'powershell'" (4027). They passed because "file" is an IMPERATIVE_RE keyword (tools/thought_quantizer.py:39-43) and "No such file or directory" is imperative-shaped by the classifier. Row 0 is cut mid-clause at the 220-char cap ("...output contract (<=N words, shape"). Rows 10-11 are probe-table rows ("pro-21b9e9bea9 -> ok (Verify with git diff...") that kept their telemetry shape because an imperative verb is present.

## Stage 5: quantizer pack -> context pack

Delivery seam: mag/context_pack.py `_quantized_laws` (:343-391) reads instructions_flash.jsonl + compile_report.json; older than 7 days it renders a one-line STALE debt pointer INSTEAD of law (:376-378); otherwise it renders the header line plus flash entries up to a 1800-char cap, breaking at the cap without notice (:379-390). The pack dict carries it at :917 ("quantized_laws"); the renderer places it immediately after the standing objective (:1070-1080), with the receipt comment naming landing 3eb6dc251 (2026-09-27) and the v0.2 fossil's lesson: wired-but-never-rendered is still unconsumed.

Clip ladder (format_context_pack_text :1235-1279), five stages: full render -> drop L4 heat (:1238-1244) -> compact L3 task (:1245-1260) -> drop L0d/L0f context blocks while keeping directives (:1261-1275) -> hard clip at max_chars-20 (:1276-1278). Every shed and clip appends a row to watch/inbox/PACK_OFFLOAD.jsonl.

Live checks this session (`build_context_pack(fast=True)` then format):

- quantized_laws renders 902 chars (all 12 flash rows fit the 1800 cap).
- full mode renders 4496 chars and DOES include "### L0b Compiled laws".
- janitor mode (the default for ask/steward, MODE_CONFIG mag/context_pack.py:52-66, budget 1200) renders 1196 chars and does NOT include the laws: the standing objective alone exceeds the budget, so the stage-4 hard clip cuts MID-OBJECTIVE and the compiled laws never reach janitor seats. Same finding the s2-08 census banked; re-confirmed live today.
- The quantizer's own staleness bar (24h, exit 1) and the delivery vehicle's bar (7d, hide law) disagree by 6 days: days 1-7 after a missed recompile, every seat renders stale law as obey-law while the fossil arm already says recompile owed.
- watch/inbox/PACK_OFFLOAD.jsonl: 870 rows. full mode has hit ALL FOUR shed stages 184 times each (184/184 recorded full renders end in the hard clip); build mode 18/18/18/18; janitor rows present too. The loss-ledger works, and the ledger file itself is in validate's unindexed-files warning list: the audit surface of the loss is itself unregistered.

## What gets lost (roll-up, one line each)

1. Never banked: a dead session loses un-report()ed work (G4 narrows this, never closes it).
2. Banked but uncommitted: 113 of 309 flash50 files untracked by git (measured).
3. Committed but unregistered: subfolder files are invisible to validate's unindexed warning (:268 non-recursive); 91 top-level files unindexed at check time.
4. Registered but unfolded: 224 items in the log beyond the stale materialized INDEX (1639 fresh vs 1415); flash50 alone 170 (184 vs 14).
5. Folded but unverifiable: 18 hash mismatches + 4 missing files of 1639 (edits after register; the 17 amend ops never apply their new sha).
6. Percolated never: no code path feeds INDEX items/receipt text to percolate(); only specific lane pipelines do. Everything downstream can be green on a receipt whose content never entered the thought pipeline.
7. Percolated but refused/deduped: 2 telemetry + 9 fragments + 13 dedupes of 331 in.
8. Kept but unraced: 283 of 307 kept laws (92.2 percent) in no pack, silently (rank cutoff).
9. Packed but degraded: 220-char flash truncation mid-clause; 1800-char L0b cap; janitor 1200-char budget hard-clips the laws out entirely (1196-char render, laws absent, live).
10. Rendered but stale-accepted: 24h fossil arm vs 7d render bar -> up to 6 days of stale law shown as obey-law.
11. Garbage promoted: 3 of 12 flash laws are shell error fragments; sentence segmentation mangles URLs in invariants ("http://127.").
12. The gates' own residue: 3 malformed event lines folded forever; 81 no-op events parse clean and pass the key gate yet register nothing; the ratchet is tree-wide so sibling debt blocks every push (live exit 1, NEW=3).

## Commands run this session (evidence)

- `node scripts/index_fold_host.mjs verify` (counts + failures above)
- `.venv/Scripts/python.exe -m mag.shared_surface validate` (exit 1; errors/warnings above; output saved to flash50/_s223_validate.json)
- `.venv/Scripts/python.exe tools/thought_quantizer.py --check` (fresh, 7.6h, exit 0)
- `.venv/Scripts/python.exe tools/violation_ratchet.py check --changed` (exit 1, NEW=3; output saved to flash50/_s223_ratchet.txt)
- `.venv/Scripts/python.exe -c "...build_context_pack(fast=True)... format_context_pack_text"` (902 / 4496 / 1196 chars; laws present full, absent janitor)
- python one-liners over watch/inbox/INDEX.json (derivations, items, class distribution), watch/inbox/index_events.jsonl (op counts, flash50 fresh-fold reimplementation, amend/no-op samples), memory/percolator/invariants.json (359 rows, mangled-URL row), memory/corpus/quantized_thought/*.jsonl + compile_report.json (pack rows, kept-vs-packed gap), watch/inbox/PACK_OFFLOAD.jsonl (870 rows, per-mode-per-stage counts)
- `git ls-files` + disk walk over flash50 (309/196/113); `git status -sb`; `git log -1 --format=... -- watch/inbox/burn_reset_20260927/flash50` (last commit touching flash50: e1fe0411b, 2026-09-28T20:12:39-04:00)

Files read: scripts/index_fold_host.mjs (whole), mag/shared_surface.py (whole), tools/thought_quantizer.py (whole), tools/md_record_seal.py (:1-60), tools/workflow_gate.py (:1-140), mag/percolator.py (:1-60 + greps), mag/context_pack.py (:330-448, :860-1360, MODE_CONFIG :52-110), scripts/gopher_packs.py (whole; namesake only: it is the S1 wave launcher writing queue/lanes/jev/trail.jsonl, not the receipt path), githooks/pre-push (whole).

Twin: s2-23.md is byte-identical to this file (checked byte-for-byte after the final write, this session); em/en dash scan over the final bytes of both files: 0 hits (venv python, this session). The final bytes sha256 is recorded in the run result note (a file cannot contain its own final sha).

## Postscript: this receipt demonstrated the lifecycle on itself (live, 2026-09-29T00:24Z)

While this census was being banked, the exact gaps it documents fired on its own files:

- The Write of receipt-lifecycle.md fired md_record_seal live: index_events.jsonl gained one register (seq 1790629545742399542, class receipt, inbox-relative path) plus one autoseal at 2026-09-29T00:24:53Z, sha256 cb842bf826fcbea3... That sha is the FIRST draft: the em-dash rescan found 8 dashes, two edit passes followed, so the registered hash went stale the moment the file was touched again (the 17 amend events the fold ignores are precisely the op meant for this, and nothing applies them). The file was born into the hash-mismatch class within one minute.
- s2-23.md was created by a python copyfile (not the Write tool), so the PostToolUse seal never fired: grep of index_events.jsonl for s2-23 returns ZERO events. A byte-identical twin of a registered receipt is itself invisible until a manual add.

Remediation, run after this line was written: both twins were registered through the sanctioned manual writer (`node scripts/index_fold_host.mjs add <file> receipt <purpose>`) at their FINAL bytes, which also refolds INDEX.json; the add output and the post-add verify are quoted in the run result note. Until that refold, INDEX.json readers saw 1415 items and neither final byte-hash.
