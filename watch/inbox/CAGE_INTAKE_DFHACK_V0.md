# CAGE INTAKE — DFHACK LAYER v0 (2026-09-07, zcode seat)

> **[AUDIT-TYPED 2026-09-08]** status: LIVE · claims: cage_intake seals hermes job receipts into the hash-chained W0 tape idempotently (11/11 sealed, 3/3 falsifiers PASS, census honest about 8 chainless residents) — SUPPORTED (tape verify PASS, chain tips cited, garbage specimen skipped) · falsifier: re-run duplicates rows, tape verify FAILs, or a corrupted card seals anyway

Card: watch/MYCELIAL_REPUBLIC_DISSECTION_20260907.md §7 THE DFHACK LAYER.
Organ: `mag/cage_intake.py`. The DFHack law held: read the memory, don't
interview the dwarf — this whole build touched only files the cage already
wrote. Read-layer only: never posted, never drove hermes.exe, $0.

## What landed

`python -m mag.cage_intake seal [--source DIR] [--dry-run]` — scans
`memory/runs/hermes_jobs/*.md`, parses each job card (tolerant: missing
fields = None, counted), appends ONE TrajectoryStep per receipt to the W0
tape (`memory/runs/trajectory/steps.jsonl`) via mag/bash_local.py's row
builder, so schema gate + hash chain apply unchanged. Session ids:
`ractor-<persona>-<YYYYMMDD>` (date from the receipt filename). Jobs without
a persona seal under persona **helm** — the steering itself. STEER cards
fall back to their `nudge` line as the goal. Re-running is idempotent
(already-sealed receipts matched by filename, skipped, never duplicated).

Row mapping: input = goal head (1024 cap) · output = output body head (4KB
cap) · tool_result = exit_code / duration_s / model / account / receipt
filename / stderr head (256) · reasoning = the why-string · timing = receipt
ts + receipt duration.

`python -m mag.cage_intake census` — per-persona chain state (rows, first/
last ts, chain tip) plus the CHAINLESS roster: cage residents known to exist
with ZERO sealed receipts. Runs a tape verify every time and reports PASS/FAIL.

## First seal — numbers

- jobs found 11 · parsed 11 · skipped 0 · sealed 11 (2nd+ runs: 0, idempotent)
- personas discovered: **gopher** (2), **helm** (9 — 8 `persona: -` dispatch
  smoke tests + 1 STEER card)
- per-persona chains: `ractor-gopher-20260907` 2 rows, tip 6185c960e4a05451;
  `ractor-helm-20260907` 9 rows, tip 3b26448bb5938d84
- missing-field tally on parse: model=1, persona=1 (the steer card) — kept as
  None, counted, not guessed
- tape verify after seal: **PASS 64 rows / 21 sessions** → after dogfood
  **PASS 65 rows / 22 sessions**, tip 62f662151897195f, chains intact
- CHAINLESS residents (zero receipts): aragoto, waka, onsei, tachiyaku,
  onnagata, hana-gumo (kabuki cast, configs/kabuki_cast.json), fermat,
  shitposter (dissection card) — the first census of who has a chain

## Falsifiers

- (a) real receipts seal well-formed: 11/11 sealed, `mag.bash_local verify`
  PASS, per-session prev_step_hash chains genesis→tip intact. **PASS**
- (b) corrupted job card: specimen
  `memory/runs/cage_intake/specimens/GARBAGE_20260907T000000Z.md` (mojibake
  + junk field lines) → `skipped: not a job card (no HERMES header, <2 known
  fields)`, counted, exit 0, no crash, zero tape writes. A garbled-fields
  card (header present, all fields junk) parses with every field = None and
  counted — tested in-memory, no tape pollution. `--dry-run` previews any
  source dir with zero writes. **PASS**
- (c) census honest about zero-receipt personas: 8 chainless residents named
  above, roster source cited, never silent. **PASS**

Dogfood: final census run through `python -m mag.bash_local` — envelope row
session bl-acef860b, step 62f662151897195f, exit 0, census output preserved
in the row.

## Honest limits

- READ-LAYER ONLY. This organ reads receipts and writes our own tape. It
  never posts, never steers, never invokes hermes.exe. POSTING stays
  fostertron-gated per the rotation charter — the cage door and the read
  layer are separate organs (dissection §7, kept true).
- bash_local.py is schema v1 today: no `why` field exists, so the
  why-string ("DFHack read-layer seal of hermes job receipt") rides in the
  hash-covered `reasoning` field. When W0 grows `why`, this module adopts it
  without format change. bash_local.py was NOT modified.
- The 11 landed rows carry seal-wall-clock in timing.start/end because the
  header timestamp format wasn't parsed at seal time (receipt_ts + the
  receipt's own duration_s were preserved). Format fix landed in
  cage_intake.py after the seal; landed rows stay untouched (append-only —
  editing them would break the chain).
- Single-turn personas' receipts are THIN chains: gopher has 2 rows, helm 9
  — chains long enough to prove shape, not behavior-over-time. Dissection =
  the gap between the reasoning chain (what the dwarf says) and this
  behavior chain (what the receipt shows); with one-turn dwarves there is no
  over-time behavior to dissect yet.
- Kabuki grounding stays seat-side per its salon finding: kabuki's 6 cast
  personas run over Hermes/Nous but their per-persona outputs do not land in
  memory/runs/hermes_jobs (the only kabuki echoes in memory/runs are
  brain_reads lane answers, not kabuki receipts). Until kabuki job receipts
  land as files, its personas stay on the CHAINLESS roster — the census will
  flip them the day receipts exist.
- The helm persona is the steering itself, not a dwarf: sealing it under
  `ractor-helm-*` keeps the helm's smoke-test trail (incl. 6 exit-1 ling
  lane 404s and one honest exit-2 gopher dispatch failure) on the record —
  failures sealed, never deleted.
