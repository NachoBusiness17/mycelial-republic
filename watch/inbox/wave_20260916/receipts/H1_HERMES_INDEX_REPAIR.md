# H1 — HERMES_INDEX_REPAIR (wave_20260916)

**Seat:** Hermes (dormant but dispatch-capable)
**Lane:** H1
**Status:** OPEN
**Law:** receipt first, append as you go. No git commands. No paid inference.

## Plan

1. Run `mag.shared_surface validate`, capture exact failure output, quantify unindexed pile.
2. Find dispatch path (queue/handoff/*.json schema, bones-referee precedent, hermes queue dir).
3. Write directive file (INDEX fold-back) + seed into Hermes inbox.
4. Note (not run) local hermes flush command if one exists.

## Log

- [t0] Receipt opened before any work performed.

## Results

### Step 1 — validate output (captured 2026-09-16)

`./.venv/Scripts/python.exe -m mag.shared_surface validate` → exit code 1, `ok: false`, schema `shared_surface.status.v1`.

**Pile quantification:**

| Metric | Count |
|---|---|
| Files scanned in `watch/inbox` top level | 443 |
| INDEX entries | 140 |
| Unindexed files (all present on disk) | **388** (~4.01 MB) |
| Errors total | 98 |
| — INDEX root wrong (`C:/…/watch/inbox` vs expected `/board/inbox`) | 1 |
| — indexed item missing from disk | 84 (of which 54 point outside inbox, at `/board/` root — historical index drift) |
| — hash mismatch (indexed but bytes changed) | 13 |
| Unindexed with `20260916` in name (tonight's wave) | 22 |

**Biggest unindexed offenders:**
- `dogfood-trajectory save.txt` — 313,735 B
- `kirk_2096316053630415211.jpg` — 239,026 B
- `ractor-salon-001.txt` — 189,753 B
- `exm_2096343368121164050.jpg` — 171,276 B
- `tecmath_2096509074800345136.jpg` — 130,972 B
- `ractor-salon.txt` — 121,424 B
- `SPORE_LEDGER_CHAIN{,_DUP}_20260901.txt` — 99,662 B each (exact dup pair)
- `index_events.jsonl` — 68,838 B

Extension histogram of the 388: `.md` 354 · `.json` 14 · `.txt` 12 · `.jpg` 3 · `.jsonl` 2 · `.mjs` 2 · `.docx` 1.

Full validator JSON captured at repo-root `validate_out_tmp.json` during this lane (transient; to be deleted after wave).

### Step 2 — dispatch path found

- Precedent read: `queue/handoff/HANDOFF-2026-09-16-bones-referee.json` — schema `handoff.v1` (`id/owner/assignee/tier/goal/inputs{paths,facts}/output_contract{artifact,receipt_schema,falsifiers,anti_goals}/budget/sequence`); bones pattern = full directive in `watch/inbox/` + handoff JSON in `queue/handoff/`.
- Hermes queue dir exists: `queue/handoff/hermes/INBOX/` with one prior seed (`20260912T0230Z-zcode-divergence-sync.md`, FROM/TO/RE/PRIORITY memo form). The 09-12 memo establishes the read-your-inbox law: Hermes reads this dir at wake via preamble; there is no separate flush daemon.
- `mag/shared_surface.py` is deliberately read-only — CLI is `path|status|validate` only, **no index subcommand**. The fold must be a manual JSON revision; validator matches items by basename against inbox top level only, sha256 uppercase.
- `watch/inbox/index_events.jsonl` already carries a register/amend event convention (`seq/ts/op/file/sha256/prev_sha256/reason/writer/nonce`) — the fold's append-only mechanism exists; note the log itself is one of the 388 unindexed.
- Hermes CLI surface: `harness/hermes_cli.py` → `main.py hermes-status` (free `--version` probe) and `escalate_via_hermes` (paid; not touched).

### Step 3 — directive written and seeded (2026-09-16T2054Z)

- Directive: `watch/inbox/HERMES_DIRECTIVE_INDEX_FOLDBACK_20260916.md` — ONE artifact (INDEX fold-back): fix `root` to `/board/inbox` (only permitted non-append correction), tombstone the 84 missing items verbatim, amend the 13 hash mismatches via events log, register the 388 unindexed files, register `index_events.jsonl` last. Output contract: validate exits clean or every residual exception itemized with reason. Falsifiers: no file deleted, hashes preserved verbatim, fold append-only (events rows byte-identical), double-validate idempotence, no edits to validator/contract.
- Handoff: `queue/handoff/HANDOFF-2026-09-16-index-foldback.json` (handoff.v1, bones shape; JSON parses clean). Budget lane local, $0.
- Seeded: `queue/handoff/hermes/INBOX/20260916T2054Z-zcode-index-foldback.md` (divergence-sync memo form; loop-closes test = HERMES_INDEX_FOLDBACK_RECEIPT_20260916.md).
- Baseline parked durably: `watch/inbox/wave_20260916/receipts/H1_validate_baseline_20260916.json` (full validator output: 443 files / 388 unindexed / 98 errors).

### Step 4 — local nudge capability

`main.py hermes-status` run (free probe, no inference): **Hermes IS present locally** — `C:\Users\foste\AppData\Local\hermes\bin\hermes.EXE`, Hermes Agent v0.21.1 (2026.9.7), install method git. A local one-shot nudge exists (`hermes -z "read your inbox…"`) but was **NOT run** per the no-paid-inference law. No-cost queue flush command noted for operator: `.\.venv\Scripts\python.exe main.py hermes-status` (probe) — actual dispatch would be `hermes -z "…"`, which starts the agent and was left to its own wake.

## Close-out summary

- **validate before-output:** exit 1, `ok:false` — 443 top-level inbox files · 140 INDEX items · **388 unindexed (~4.01 MB)** · 98 errors (1 wrong root, 84 indexed-missing incl. 54 unreachable `/board/`-root, 13 hash mismatch) · 22 files from tonight's wave. Biggest offenders: `dogfood-trajectory save.txt` 314 KB, `kirk_*.jpg` 239 KB, `ractor-salon-001.txt` 190 KB.
- **directive path:** `watch/inbox/HERMES_DIRECTIVE_INDEX_FOLDBACK_20260916.md`
- **seeded inbox path:** `queue/handoff/hermes/INBOX/20260916T2054Z-zcode-index-foldback.md` (handoff JSON: `queue/handoff/HANDOFF-2026-09-16-index-foldback.json`)
- **nudge:** Hermes can be nudged locally — binary verified on-host (v0.21.1) via free `hermes-status` probe; nudge command noted (`hermes -z`), not run (paid-inference law). Otherwise it picks this up at its next natural wake via the read-your-inbox law.

**Status:** DISPATCHED — awaiting Hermes receipt (`HERMES_INDEX_FOLDBACK_RECEIPT_20260916.md`) as loop-closes test.
