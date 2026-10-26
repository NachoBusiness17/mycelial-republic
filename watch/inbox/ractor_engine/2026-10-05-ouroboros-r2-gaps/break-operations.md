# OUROBOROS R2 break-operations pass (hostile second pass on the gap-surface lens)

Moment: 2026-10-05T12:34:14Z (all exec-run claims stamped this moment; B2-216 applies).
Mandate held: read-only. No gate, no test suite, no workflow fired. Executed checks this
sitting: full read of tools/mickey17_v2_fold.py (234 lines); ls + mtime census of
memory/runs/mickey17_v2/runs/2026-10-05-exec/; grep -c deep_tier2 over all 16 exec lane/check
files; json parse of a08-rails-laws.checks.json; wc -l + mtime of memory/attention_feedback.jsonl;
find *S2_constrained* over watch/inbox + memory; grep -rln cache_receipt over mag/ + tools/;
ROW_FIELDS read at mag/flight_recorder.py:83-84; tolerant parse of watch/inbox/index_events.jsonl
(10,528 sha rows, 3 malformed) plus sha256 recompute of 2 sealed files; percolator store reads
(29 rows); precise greps over .zcode/workflows/*.dwf.ts.

## VERDICTS (4 lens findings)

### 1. Fold instrument blind to tier-2 verdicts; third blind fold window open -> CONFIRMED (CONVERGENT)

- tools/mickey17_v2_fold.py:181 is byte-exact `for x in (c.get("unconfirmed") or []):`; a full
  read of the file finds ZERO deep_tier2 tokens; the PRISMA walk (:179-201) reads only that
  top-level key. VERIFIED.
- run-0 FOLD_SECTIONS.md:27 prints "deep_tier2 16" while :40 prints "excluded: 0". VERIFIED.
- SHARPENED: a08-rails-laws.checks.json DOES contain the string "unconfirmed" but ONLY as a
  nested verdict value (`"verdict":"unconfirmed"`, my grep -o); a top-level `d.get("unconfirmed")`
  returns None. So even a lane that writes tier-2 verdicts cannot reach the exclusion join: the
  instrument reads a shape that exists nowhere at top level, and the shape that exists (nested
  verdict values, run-0's top-level deep_tier2 lists) is only length-counted (:157-162), never
  walked. The blindness is one degree worse than the lens stated.
- WINDOW: at 2026-10-05T12:34:14Z the exec run dir still holds ONLY lanes/ (last lane write
  02:38:45 EDT, e06-fidelity-audit.json). No FOLD_SECTIONS.md. The window is open ~10h after the
  lanes finished. VERIFIED, moment-stamped.
- CONVERGENT: R1 SYNTHESIS amendment row 1 (same file, same line ranges :179-201/:156-162/:127-129)
  and R1's closing line "The 2026-10-05-exec fold, when it fires, will print excluded: 0 over
  whatever tier-2 verdicts land unless row 1 lands first" independently hold this gap. Three
  derivations (R1, the lens, this pass) rank it 1.
- Executor-fence: NONE. Lanes e01-e08 all finished (mtimes 01:19-02:38). R1's ownership fence is
  lifted. The exec checks carry zero deep_tier2 keys (grep -c = 0 on all 16 files; tier2 tokens
  in e04/e05/e06/e07 are prose values, not keys), so the exec fold will print excluded: 0 REGARDLESS
  until the amendment lands; the amendment is what makes any future fold countable.

### 2. next.md halt rule triggered, unfiled; unbound-aggregate gate unminted (register row 10) -> CONFIRMED + STRENGTHENED

- memory/attention_feedback.jsonl = 2 rows, 432 bytes, mtime 2026-09-29 10:48:56 (my wc -l + ls).
  next.md:248-251 requires >2 rows by 2026-10-03T00:00Z. F3 byte-falsified. VERIFIED.
- STRENGTHENED beyond the lens's scoped greps: the F2 probe receipt is absent by NAMED INSTRUMENT,
  not just pattern-grep: `find watch/inbox memory -name "*S2_constrained*"` returns empty, and
  watch/inbox/frontier_olm_20260928/ exists (DIGEST.md, lens/, steal/, sweep/, register.jsonl,
  percolator_candidates.jsonl, RECEIPT.md) with NO probe/ subdir (my ls). Scope stated: those two
  roots, filename match only; .jsonl contents elsewhere not censused for it.
- MRE section 9 row 10 (corpus/steal/MASTER_READ_ESTATE.md, section 9 register) carries the same
  finding register-side, so the closure is doubly register-backed.
- No executor lane covers row 10: lanes e01-e08 map to register rows 1-7 (e01 note "Unit 1
  executed in full", e03 note "All five register row 2 units landed"; names align e04->row 3,
  e05->row 4, e06->row 5, e07->row 6, e08->row 7). VERIFIED.

### 3. cache_receipt gate nothing feeds -> CONFIRMED; THE MOVE AS WRITTEN LANDS NOTHING

- grep -rln cache_receipt over mag/ + tools/ = tools/cache_kpi.py only (plus its __pycache__).
  b2_cache_receipt.md "Owed (not faked)" section carries verbatim "Producers (dispatch/
  flight-recorder call sites) do not yet stamp `cache_receipt` on usage rows; recv_tok reads 0
  until the first wired lane lands". VERIFIED.
- mag/flight_recorder.py:160-166 cache-field parse, :193-194 append, :199 record_call. VERIFIED.
- THE MISS THE LENS CARRIED: ROW_FIELDS at mag/flight_recorder.py:83-84 is
  ("ts","lane","model","subsystem","latency_ms","status","error_code","in_tok","out_tok",
  "cached_tok","cache_miss_tok","credits_est") and _emit at :191 writes
  `{k: row.get(k) for k in ROW_FIELDS}`. A cache_receipt stamp added at any call site is
  SILENTLY STRIPPED before the JSONL append. The lens's 45-min move ("stamp cache_receipt on the
  usage row fed by context_checkpoint") would bank a fake-done: the reader (tools/cache_kpi.py:102
  `row.get("cache_receipt")`) would still read nothing. The close is TWO edits: add "cache_receipt"
  to ROW_FIELDS at :83-84 AND stamp at the producer (mag/context_checkpoint.py:161
  verify_strict_prefix / :205 gate_skip_recompute are real, my grep). Falsifier: rerun
  tools/cache_kpi.py after both edits; recv_tok still 0 = the stamp never reached the row.

### 4. Seal patrol case-only false drifts -> CONFIRMED, FALSIFIER EXECUTED AND HELD

- tools/prepush_seal_patrol.py:97-105 file_sha256 returns digest.hexdigest() (lowercase);
  :124-125 `actual = file_sha256(path)` / `if actual == sha:` raw compare (lens said :124 for the
  compare; the compare is :125, the assignment :124; immaterial). b7_sweep.md:36-38 carries
  verbatim "17 real drifts + 21 CASE-ONLY false drifts (uppercase-hex seal rows vs lowercase
  actuals... findings like DIGEST.md 5CAA5303B1C3 vs 5caa5303b1c3)". VERIFIED.
- FALSIFIER RUN (the lens named it, I executed it): tolerant parse of
  watch/inbox/index_events.jsonl = 10,528 sha rows, 3 malformed; 3,664 rows carry uppercase hex
  seals (34.8 percent of the ledger, far beyond b7's 21-at-1000-rows sample implied); 14 DIGEST
  uppercase rows; sampled 4 (2 distinct files):
  watch/inbox/G6_HISTORY_DIGEST_20260926.md sealed 23077B0FE3... vs actual 23077b0fe3...;
  watch/inbox/TREE_DOCTRINE_V2_DIGEST_20260925.md sealed 889165413B... vs actual 889165413b...
  BOTH: sealed.lower() == actual bytes sha256. CASE-ONLY false drift, byte-proven. The one-line
  casefold fix at :125 is correct for the sampled class. Finding stands with its falsifier
  executed and failed.

## What the lens missed (all byte-checked this sitting)

### M1. B1 already_inside: 29 dangling edges, filed-not-faked, no lane owns it
- Evidence: watch/inbox/build_wave_20261005/b1_knowledge_graph.md:69-70 "Filed, not faked":
  "29 remaining dangling edges are the pre-existing already_inside defect (prose we_have entries
  never matching real module ids; lens/graph.md item 2) - not one of the four." No exec lane, no
  register row, no R1 row covers it.
- Falsifier: mag/knowledge_graph rebuild prints dangling already_inside > 0 after the builder
  lands.
- Move: 45 min: id-mapping edge builder in mag/knowledge_graph.py (we_have prose ids -> real
  module ids), regenerate memory/knowledge_graph.json, bank dangling=0 in a b1 addendum receipt.

### M2. Held percolator rows: the fence is GONE and the row still is not minted
- Evidence: b9_doors_tier.md "OWED (held, not this lane's to write)": "Percolator candidate row
  carrying the two-clause rule: HELD. Another live workflow owns memory/percolator/candidates.jsonl
  writes this window... Owed to that owner or the next window." The owning window HAS passed:
  rows 20-29 landed 2026-10-05T05:22:33Z (the transfer-debt mint, LINKS-sourced) and NONE of the
  29 rows carries AQLM or the two-clause/backend_tier rule (my grep: AQLM in master store = 0;
  backend_tier/two-clause = 0). The source row exists: watch/inbox/frontier_olm_2026-10-04/
  percolator_candidates.jsonl names the method-tier paper (GPTQ, AWQ, QuIP#, AQLM, BitsAndBytes,
  GGUF ranking; AQLM the sanctioned pick) and the mine card at frontier_olm_2026-10-04/steal/
  quantization-and-compression via arxiv.md.
- Falsifier: a row 30+ in memory/percolator/candidates.jsonl naming the two-clause rule or AQLM
  (my grep was over all 29 current rows; recheck after any mint).
- Move: 20 min: mint the candidate row through the percolator writer (mag/percolator.py:23-27
  owns the path), citing b9's two-clause rule and the AQLM ruling.

### M3. Register rows 8 and 9 have NO executor lane (the lens covered only row 10 of the residuals)
- Evidence: MRE section 9 rows 8 (catalog rescan cure, r08#2) and 9 (research lane consumption
  verdict, r05#3); lane census above maps e01-e08 to rows 1-7 only. Row 9's close is fully
  specified in MRE D9's ruling: "run the owed consumption query over the corpus FTS index, write
  the rate onto queue/lanes/research/surface.md, feed or kill the lane on the answer."
- Falsifier: queue/lanes/research/surface.md carrying a consumption rate row (its absence = open).
- Move: 40 min each: row 9's FTS consumption query + rate write + feed-or-kill verdict (verbs
  minted: the feed-or-kill decision on an 84 percent spooler lane); row 8's catalog rescan cure
  (the D1 disease recurring live per the register row text).

### M4. R1 residual rows 6+7 still fenced, still open
- Evidence: R1 SYNTHESIS rows 6 (workflow_gate stop-cert clause; zombie certs: registry row 75
  minted 2026-10-04T02:34:06Z for retired tree-doctrine-dig) and 7 (FIRE_LEDGER append at check
  time); commit 23d76bb71 holds them "post-executor (ownership fence)".
- Falsifier: a stop-cert clause in tools/workflow_gate.py (grep for retired-status re-cert) or a
  memory/workflows/FIRE_LEDGER.jsonl on disk.
- Move: held (fence: the workflow_gate owner seat); the finding is the fence itself. Not this
  pass's to land.

### M5. GAP_REGISTER row 12 (the lens's OWED item) resolved: still open
- Evidence: watch/inbox/gap_analysis_20261001/GAP_REGISTER.md:85 row 12 ("Spiking synthesis MOVE 1
  ($0 R0 Vulkan gate probe) scheduled nowhere...") carries NO close annotation; :139 still
  instructs "FIRE MOVE 1". todo.md:234 Stone 7 banked the GPU unlock (llama-server Vulkan proof)
  but the probe itself remains unscheduled.
- Falsifier: a close annotation on the register row, or a scheduled task/log naming the gate probe.
- Move: 30 min $0 local: fire the Vulkan gate probe on the RX 5600 XT box, annotate row 12.

### M6. R1 landings the lens admitted it had not verified: verified now, all three byte-true
- Merge clause in all 3 skeletons: mickey17-burn.dwf.ts and mickey17-v2.dwf.ts carry "keep every
  existing key" / "Read the file first if it exists"; gap-analysis.dwf.ts:299 carries the same
  clause in its own phrasing ("Read the file first. Rewrite it whole with the SAME existing keys
  untouched (tier-1 lane/supports/counts and any..."). All 3 confirmed.
- olm-mine strike: olm-mine.dwf.ts:9-10 names the 191.8M headline STRUCK per ERRATA 001 with the
  ERRATA cite. Confirmed.
- max_concurrency: 19 of the dwf.ts files declare it (grep count = 19). Confirmed.

## RANKED CLOSURE TABLE (amended Schmidhuber metric, candidates.jsonl row 19: carried-history
retired + verbs minted primary, defects secondary; CONVERGENT outranks novel)

| # | Gap | One-sitting close | Landing file | Evidence row | Blocked-by |
|---|-----|-------------------|--------------|--------------|------------|
| 1 | Fold blind to tier-2 verdicts; exec fold unfired (window open at 12:34:14Z) | Land R1 row 1: walk deep_tier2, count unconfirmed/crashed into PRISMA excluded code 9, stamp folded_at + sha256(script)[:12], print verdict-value splits | tools/mickey17_v2_fold.py:179-201, :156-162, :127-129 | fold.py:181 c.get("unconfirmed") + zero deep_tier2 tokens; run-0 FOLD_SECTIONS :27 vs :40; exec dir lanes-only at 12:34Z; CONVERGENT R1 row 1 | none (fence lifted, lanes done 02:38) |
| 2 | cache_receipt gate unfed (recv_tok 0 vs 96.6 nominal) | Stamp at the context_checkpoint producer AND add "cache_receipt" to ROW_FIELDS (without the second edit the stamp is stripped at emit) | mag/flight_recorder.py:83-84 (ROW_FIELDS) + producer at mag/context_checkpoint.py:161/:205; verify via tools/cache_kpi.py | grep cache_receipt = reader only; b2_cache_receipt Owed section; ROW_FIELDS :83-84 lacks the field, _emit :191 filters | none |
| 3 | Research lane feed-or-kill undecided (register row 9) | Run the FTS consumption query, write the rate, land the feed-or-kill verdict | queue/lanes/research/surface.md | MRE section 9 row 9 + D9 ruling; no lane covers it | none |
| 4 | Falsification receipt unfiled + unbound-aggregate gate unminted (register row 10) | Two-line receipt beside next.md naming F2/F3 verdicts + halt-rule trigger; add the unbound-aggregate check to the fold tool | watch/inbox/48h_synth/ (receipt) + tools/mickey17_v2_fold.py (check) | attention_feedback.jsonl 2 rows mtime 09-29; *S2_constrained* find empty; no probe/ dir | none |
| 5 | Held percolator rows (two-clause GGUF/AQLM method-tier) unminted after the fence closed | Mint row 30 via the percolator writer citing b9 + the frontier store row | memory/percolator/candidates.jsonl (through mag/percolator.py:23-27) | b9 OWED block; master store 29 rows, AQLM = 0; rows 20-29 landed 05:22:33Z without it | none (window passed) |
| 6 | B1 already_inside 29 dangling edges | Id-mapping edge builder + rebuild + dangling=0 receipt | mag/knowledge_graph.py + memory/knowledge_graph.json | b1_knowledge_graph.md:69-70 | none |
| 7 | Seal patrol case-only false drifts (3,664 uppercase rows ride the ledger) | Casefold the compare (or normalize at parse) | tools/prepush_seal_patrol.py:124-125 | Falsifier executed: G6/TREE_DOCTRINE seals lower() == actual bytes sha256; b7_sweep:36-38 | none |
| 8 | Catalog rescan cure (register row 8, D1 disease live) | The register row's own rescan cure | per row 8 text (catalog writer) | MRE section 9 row 8; no lane covers it | none |
| 9 | R1 rows 6+7 (stop-cert + FIRE_LEDGER) | Stop-cert clause + FIRE_LEDGER append | tools/workflow_gate.py | SYNTHESIS rows 6-7; registry row 75 zombie cert | EXECUTOR-FENCE (workflow_gate owner) |
| 10 | Vulkan gate probe scheduled nowhere | Fire the $0 probe, annotate row 12 | watch/inbox/gap_analysis_20261001/GAP_REGISTER.md:85 | row 12 unannotated; :139 still says FIRE MOVE 1 | none ($0, local box) |

## Amendments to tools/free_lane_fleet.py work generators (the loop adapting its own sensing
instrument; current generators at :14-22: queue drain, percolator probe battery, corridor watch)

1. NEW generator: drain "Owed / probe not fired" clauses from the newest wave receipts into the
   queue. Byte-checked instances the fleet is blind to today: b9_doors_tier.md's unfired Q4_K_M
   vs q8_0 arm battery (20 code prompts) and b2_cache_receipt.md's poisoned-block replay probe.
   Both are named, unfired, free-lane-sized asks sitting in prose the fleet never parses.
2. EXTEND generator 2 beyond memory/percolator/candidates.jsonl to the frontier percolator stores
   (watch/inbox/frontier_olm_*/percolator_candidates.jsonl). The AQLM/method-tier row and its
   falsifiers live there (byte-checked); the fleet's probe battery reads only the master store
   (:54 CANDIDATES constant) and never sees them.
3. NEW $0-local gate-probe generator: auto-drop GAP_REGISTER rows marked "one-sitting ($0)" into
   watch/inbox/free_lane_queue/*.json asks. Row 12's own text says "scheduled nowhere"; the 24/7
   fleet is the scheduler the register lacks.
4. NEW moment-law sensor: each cycle, check whether memory/runs/mickey17_v2/runs/2026-10-05-exec/
   gained FOLD_SECTIONS.md while tools/mickey17_v2_fold.py still lacks a deep_tier2 walk; if so,
   alert memory/attention.md (a blind fold fired). Turns this fold's time-sensitive fact into a
   standing tripwire instead of a per-round race.

## Honest residue (not run / not censused)

- The fold script itself was NOT fired (mutates archives; same refusal as R1).
- No gate/test/workflow fired (read-only mandate; single-script gate runs mint registry rows).
- Exec checks files were grepped and shape-sampled, not all read in full (a08 read in full).
- The S2-receipt absence census is filename-scope over watch/inbox + memory only.
- The exec fold can fire after 12:34:14Z; every window claim above carries that stamp.
