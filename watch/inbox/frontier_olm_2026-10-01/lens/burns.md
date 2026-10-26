# burns lens 2026-10-01: what was already mined this week, so nobody re-banks it

Lens seat: lens-burns, carrier `watch/inbox/frontier_olm_2026-10-01/`. This continues
`watch/inbox/frontier_olm_2026-09-30/lens/burns.md` (2026-09-30). Everything below was read or
run in this ask (2026-10-01, repo root). All times on carrier listings are local unless suffixed Z.

## 0. Commands actually run (the evidence base)

- `wc -l memory/burns/LEDGER.jsonl` = 693; `tail -n 30` of it (max-ts rows).
- Day-count greps on the ledger: 2026-09-25 = 23, 09-26 = 517, 09-27 = 108, 09-28 = 45
  (`grep -o '"ts": "2026-09-NN' | uniq -c`), identical to the 09-30 lens counts; max ts
  2026-09-28T13:45:00Z re-read from the tail.
- `find watch/inbox -maxdepth 1 -type d -newermt 2026-09-28 -printf '%TY-%Tm-%Td %TH:%TM %p\n'`
  (last-3-days carrier census) and per-dir `ls` peeks on the new ones.
- `wc -l memory/runs/hermes_burn/usage.jsonl` = 16 rows; awk sum of `cost_usd` = 5.9155; first ts
  2026-10-01T13:11:41Z, last ts 2026-10-01T13:53:33Z.
- Read: `watch/inbox/hermes_burn/WINDOW1_STATE.md` (2,690 B) and the prior 09-30 burns lens.

## 1. Old burn ledger: STILL nothing new since 09-28. The 09-30 lens remains authoritative.

- `memory/burns/LEDGER.jsonl` holds nothing but 09-25..09-28 (day counts in section 0 sum to 693).
  Zero rows dated 09-29, 09-30, or 10-01 (grep for those prefixes returned nothing).
- The standing burn lanes (free-resource-landscape 35 rows, middle-path-doctrine 30,
  doctrine-owed-chase 26, world-models-multi-agent 19, stego-canon-pipeline 19, third-way-game 17,
  adversarial-self-probes 15, rsi-harness 12, queue-field 11, steering-theory 11, b2-wave-fold 11,
  judge-lane-spec 10, prompt-uplift-lane 8, atlas-fix-queue 4) and their latest landings are
  tabled in `watch/inbox/frontier_olm_2026-09-30/lens/burns.md` sections 1-2. Re-deriving any of
  those lanes is re-banking.

## 2. NEW burn surface since that lens: the hermes descent, window 1 (closed today)

The burn seat moved to the descent protocol; the old LEDGER.jsonl is dormant, the live money
ledger is `memory/runs/hermes_burn/usage.jsonl`:

- 16 rows, $5.9155 summed this ask, all ts 2026-10-01T13:11:41Z..13:53:33Z (matches carrier commit
  1a1efc67f "ledger $5.92 + $0.005 assembly"). Models seen: claude-sonnet-5.5, claude-fable-5.1,
  claude-opus-5.5; per-turn $0.15..$0.58; every row `ok: true`.
- State carrier: `watch/inbox/hermes_burn/WINDOW1_STATE.md` - 9 deliverables landed in
  `watch/inbox/hermes_burn/` (A2 duel provenance, A3 corroboration bootstrap, B1 outbox receipt
  bridge, B2 drift-rows attribution, D1 doctrine roast movement 1, A1 steer-seal and C1 censorship
  designs done in the reasoning channel; A1 + C1 ASSEMBLED cards landed 09:57 today).
- Already banked there, do not re-mine: A1 HMAC steer-envelope + safe-fail design, A3
  unauthenticated-witness catch, the memlance fork (Ollama cannot inject residual vectors; C1
  rides prompt-level instruments), D1 premium-refutes-cheap symphony cycle.
- Named owed (WINDOW1_STATE.md): turn-2 empty-carrier defect, force-refire duplicate gate,
  movement 2 adjudication, duel volume leg toward $70+.

## 3. Frontier mining already banked this week: two prior olm carriers

- `watch/inbox/frontier_olm_20260928/` (complete): DIGEST.md 41,801 B, register.jsonl 21 finds,
  percolator_candidates.jsonl 5 rows, 13 steal cards. Window 2026-08-29..09-28 over 8 areas x 4
  doors. Headline fold: percolator promote gate is a bare counter (mag/percolator.py:264-272) vs
  the unwired paired-blind gate (mag/seed_percolator.py:6-16). A same-window sweep is a re-bank.
- `watch/inbox/frontier_olm_2026-09-30/` (completed AFTER that day's burns lens was written):
  sweep/ = 45 files (8 areas x 4 doors: open-and-local-language-models, quantization-compression,
  agent-memory-continuity, kv-cache-context-engineering, inference-efficiency,
  evals-self-improvement, finetuning-adaptation, swarm-orchestration), lens/ = 6 files, steal/ =
  6 cards landed 09-30 16:48..21:34 (agent-memory-continuity, kv-cache-context-engineering,
  open-and-local-language-models x3 door variants, quantization-compression).
  NO register.jsonl / DIGEST.md / RECEIPT.md exists in that carrier (find returned nothing this
  ask) - its finds are banked as sweep returns + steal cards only; dedupe against those filenames.

## 4. watch/inbox carrier directories, last three days (dirs with mtime >= 2026-09-28)

Full dated census ran this ask (`find ... -newermt 2026-09-28`). New or newly-touched since the
09-30 lens snapshot (which covered through ~09-30 12:35):

- 09-30 afternoon: `48h_synth/` (18:11; STORY, lattice, laws, measure, next, steals),
  `ds_batches/` (18:29; codex one-turn batch prompt+items+results jsonl), `frontier_asks/` (18:30;
  ASK1-8 + _shared_context + run_asks.py + results/ + volley2), `mountain_selfplay_20260929/`
  (19:41; SELFPLAY_RECEIPT.md), `mountain_climb/` (20:27; FIFTY_QUESTIONS + answers, ROUTE_*,
  OPUS_BRIEF, SHERPA_DOSSIER, LENSING set), `last_mile_20260930/` (22:39).
- 10-01: `localfirst/` (05:20; adjacent/aida/atlas/lbrain/ownmem/pam/ragos memory-landscape cards
  + probe_ragos_fingerprint.py; root files LOCALFIRST_MEMORY_LANDSCAPE_20261001.md +
  signals jsonl), `ractor50/` (06:06; MCP_PARITY_R20, accuracy/communication/logic/mcp/operations/
  selfsteal/skills + lanes/), `secret_gate_results/` (08:13), `music/` (08:41; STYLE_SPEC,
  audio-dna, cutter cuts, lyric-archaeology, remix-mechanics, taxonomy), `gala_20260925/` (09:38
  touch), `hermes_burn/` (09:57; section 2), `frontier_olm_2026-10-01/` (10:03; this carrier).
- 10-01 root-level mined artifacts before filing anything similar: DRIFT_PATROL_20261001.md
  (08:12; oauth-shaped-token excision per carrier commit 7072e988d), fix_everything_20261001.md
  (06:25), x_intel_drop_20261001.md (06:40), model_mating_paper_dig_20261001.md (06:51),
  ghidra_followon_20261001.md (07:01), ESTATE_CENSUS_20261001.md (09-30 19:09), plus the daily
  free-resource scout landing (carrier commit b42f7df7d). Contents of these were NOT read;
  filename/size peeks only.
- Standing do-not-re-mine surfaces from the prior lens still apply: `burn_wave_20260926/`
  (771 entries), `last_mile_20260930/` (127 entries), `burn_reset_20260927/`, `gala_20260925/`.

## 5. OWED / not done by this seat (stated, not guessed)

- The 09-30 olm carrier never landed its register/DIGEST/RECEIPT; whether one is owed or the
  run was closed card-less is not recorded anywhere I read. I did not create one (not asked).
- Carrier contents listed in section 4 were filename-peeks only; only WINDOW1_STATE.md, the prior
  09-30 burns lens, and ledger/usage rows were read as text.
- INDEX.json registration of this lens file: not performed (the workflow publishes).
- Pre-09-25 burn history: still not located; ledger claims remain scoped to the 693 rows.
