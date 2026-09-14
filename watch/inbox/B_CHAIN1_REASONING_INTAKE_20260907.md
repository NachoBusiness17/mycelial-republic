# B-CHAIN-1 — REASONING INTAKE (2026-09-07)

> **[AUDIT-TYPED 2026-09-08]** status: LIVE · claims: mag/reasoning_intake.py parses window exports into schema-v2 sealed TrajectorySteps where `why` is chain-load-bearing, with v1 byte-stability and gate teeth — SUPPORTED (5 falsifier drills all PASS in card: specimen parse, corruption, backward compat, tamper, gate teeth) · falsifier: stated in card — a failing drill (tampered why not detected, v1 hash change, or crash on corrupt input) would break the claim

Card: watch/MYCELIAL_REPUBLIC_DISSECTION_20260907.md (build B-CHAIN-1). The
REASONING chain (stated why / claims / method) existed only as UNSEALED window
exports; this organ parses the traj.txt paste format into discrete turns and
seals each one as a schema-v2 TrajectoryStep through the W0 writer — gates,
caps, and hash chain inherited, nothing bypassed. $0-local: files only, no
docker, no config, no secrets, Desktop exports touched READ-ONLY.

## 1. Schema v2 migration note (mag/bash_local.py, backup
mag/bash_local.py.bak-intake-20260907)

- A row that CARRIES `why` is schema_version **2**; rows without stay v1.
  v2 = v1 + optional `why` string, head-capped at WHY_CAP = 1024 chars.
- **Hash rule, exact:** the canonical row content pre-hash gains ONE extra key
  `why` — `step_hash = sha256(json.dumps({v1 hash fields + "why"},
  sort_keys=True, ensure_ascii=False))[:16]`. v1 canonical content is
  unchanged, so existing row hashes are byte-stable.
- Verifier accepts BOTH versions. Two new teeth: a **v1 row carrying `why` is
  REJECTED** (its hash would not cover the why — tampering would go unseen),
  and a **v2 why over cap is REJECTED** (len > 1024).
- Writer: `build_row(..., why=...)` auto-upgrades to v2; CLI gains
  `--why=` flag (peeled from the command string, wins over `WORLDLINE_WHY`
  env); sealed rows print `(session X, v2) [why sealed]` on stderr.

## 2. Parser spec (mag/reasoning_intake.py)

`python -m mag.reasoning_intake parse <export.txt> [--session-id X]
[--dry-run]` · `verify-export <export.txt>` = report only · default session
`intake-<filestem>-<date>`.

- Turn delimiters: a bare-integer line followed by a line containing "session"
  (the specimen's `95` / `Main session`). Section headers (case-insensitive):
  Reasoning / Assistant / Tool call / Input / Output / Tool result / User /
  System. Meta lines (durations `30.7s`, middots, timestamps, `Collapse`,
  `IN n` / `· OUT n`) are consumed as structure, never content; the full
  section timestamp and token/duration cluster are captured into the row.
- Command extraction: the tool body's leading tool-name + hex call-id are
  peeled, then the JSON is read with `raw_decode` (first JSON object wins —
  trailing export notes like "Too many records, showing the most recent calls"
  are tolerated); falls back to raw head. In this export the JSON lives under
  the nested `Input` header, not `Tool call` — both are scanned.
- Row mapping (all head-capped, W2 truncation lesson): input = tool command
  else User prompt, 4KB; output = Assistant text 4KB; tool_result =
  {output_head 2KB, tool, call_id, exit_code: null, source:
  "reasoning_intake"}; **why = Reasoning block 1KB → schema v2**; reasoning
  (v1 field) = ""; timing = {source_ts, duration_s, tokens_in, tokens_out,
  turn}. ts = seal time; the export's own time rides in timing.source_ts —
  honest provenance (sealed-when != said-when).
- Tolerance: unmatched garbage lines are skipped AND COUNTED; the report
  prints turns found / sealable / empty, lines skipped, and parse coverage %
  (non-empty lines consumed by recognized structure / non-empty lines).

## 3. Specimen parse stats (the operator's hand-saved
C:\Users\foste\Desktop\music-ai\traj.txt — read-only)

```
PARSE REPORT traj.txt
  turns found:    5          (export turns 95-99, the Nous provider hunt)
  turns sealable: 5 (empty: 0)
  lines: 856 non-empty / 980 total; skipped (unparseable): 0
  parse coverage: 100.0%
  section hits: assistant=3, input_hdr=5, output=2, reasoning=5, system=1, user=1
```

**SEALED: 5 rows** (this session's real thought-trajectory became tape) —
session `intake-traj-20260907`, chain
4c0112c00445e37a → 7dc1cf281ad91c92 → 5e1ae37adfeb31a1 → 52e79e24da1902fc →
3995a9a932da0b75. Every row v2 with why (1024B/619B/921B/1024B/24B — turn 98's
reasoning was the big one, head-capped at the 1KB gate).

## 4. Falsifiers — all PASS

| # | drill | result |
|---|-------|--------|
| a | real specimen parse + seal | 5/5 turns, 100.0% coverage, 5 v2 rows sealed, chain intact (above) |
| b | corrupted input (`memory/runs/trajectory/traj-corrupted-drill.txt`: file truncated at 62% mid-tool-result, binary garbage, fake headers, broken JSON, dangling `99`/`Main session` at EOF) | **never crashed**, exit 0, honest report: 5 turns found, 2 empty (truncated ends), 2 lines skipped, coverage 99.6% — degradation stated, not hidden |
| c | backward compat | `verify` PASS byte-identical BEFORE and AFTER the schema extension (`PASS 53 rows, 19 session(s), tip=5e07f5758cc34332` both times, diff empty); final mixed tape PASS (65 v1 + 6 v2) |
| d | why tamper (`memory/runs/trajectory/tamper-drill-{control,tampered}.jsonl`) | control copy PASS; one flipped char in row 66's why → `FAIL … row 66: hash mismatch` **plus the whole downstream session chain breaks** (rows 67-70 prev_step_hash mismatch) — the why is chain-load-bearing |
| d+ | gate teeth (`gate-drill.jsonl`, hashes honestly re-handed so only the gates could fire) | `row 1: REJECTED — v1 row carries why (upgrade to schema v2; v1 hash would not cover it)`; `row 2: REJECTED — v2 why 2000 chars > cap 1024` |

## 5. Dogfood

Final seal through `python -m mag.bash_local "python -m mag.bash_local verify"
--why="…"` — session `bchain1-intake-20260907`, step **741830c404aa5543**
(genesis), v2, why sealed (172B): *the reasoning intake organ is live; this
verify ran through the wrapper carrying the first declared-intent why — seal
the thought, not just the behavior.* The first habitual v2 row.

Tape after: **PASS — 71 rows, 24 session(s), tip=741830c404aa5543, chains
intact.** Honest census note: 53 rows at baseline → 71 at close; 12 rows landed
from concurrent live fleet lanes during the build (the mesh writes while you
work — every intermediate verify stayed PASS). Drill artifacts kept:
traj-corrupted-drill.txt, tamper-drill-control/tampered.jsonl, gate-drill.jsonl.

## 6. Honest boundaries

- The parser is tuned to TODAY's export shape (numbered turns + section
  headers, ZCode window paste). Other windows' export formats (different UI,
  manual copy variants) may need header-set extensions — the tolerance +
  coverage report will say so honestly instead of lying.
- One row per TURN: turn 97 carried 32 tool results (a batch) — they merged
  into one row's 2KB tool_result head. Turn-level fidelity, not per-tool-call
  fidelity; per-call splitting is a v2 of the intake if dissection needs it.
- Why blocks are head-capped at 1KB: turn 98's 5.4KB reasoning sealed its head
  1024B only. The full text stays in the original export; the tape row proves
  intent, not volume.
- B-CHAIN-2 (dissector) not started here — this lane is the prerequisite
  intake only.
