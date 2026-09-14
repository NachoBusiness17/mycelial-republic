# Builder — surface log
state: ARMED (throttle organ gate BUILT 2026-09-04, receipt-002; race-verified)
(append receipts below; manager browses this file)

---

## receipt-002 — window throttle organ (salon day direction item 3)

- **Task:** One primary per work window — night windows triple-booked (sweeps +
  burns 2/4 + ractor panels, 23:00-09:00, no coordinator); the Launch Law's
  same-turn builders need this before they multiply.
- **Built:** `mag/window_throttle.py` — claim/release/status/sweep. A primary is a
  file `watch/windows/<window>.json` (schema `window_throttle.v1`: holder, purpose,
  pid, ts, ttl_s, expires_at, token) claimed by atomic create (temp-write +
  os.rename; win32 FileExistsError = the CAS). Stale takeover is judge-then-CAS:
  re-read + tomb-move ONLY on token match (bay_organs FINDING-1 discipline); any
  race-away = honest loss, no write. `pid_alive` imported from `mag.bay_organs`
  (one measured win32 probe, not a fork). CLI exit codes 0 win / 3 loss-refused /
  2 usage: `python -m mag.window_throttle claim <window> --holder H --purpose P [--ttl S]`.
- **Evidence:** `watch/test_window_throttle_race_20260904.py` — 4 REAL subprocesses,
  READY/GO gate, all state in tempdir. **Run 1 FAIL (96 checks, 50 failures)**:
  2-3 winners/round. Diagnosis: pid-death-release (inherited from bay_organs) is
  wrong here — CLI claimants exit in milliseconds, so every claim read stale and
  got stolen. Fix = **LEASE LAW** (expiry-only lease; claim outlives the claimant;
  pid is attribution). **Run 2 PASS: 154 checks, 0 failures** — TEST A fresh race
  4x10 rounds exactly 1 winner; B takeover race 4x4 on expired leases single-winner,
  zero unexpired claims tombed; B2 regression: dead-pid unexpired lease unstealable
  by 4 racers; C token-guarded release; D live primary never stolen; E dead-holder
  holds / expired taken; F sweep hygiene (expired + old debris swept, unexpired kept).
  CLI smoke: exit codes + held_by context on loss verified.
- **Tri-state:** Single-winner under 4-way contention = **Supported** (14 contended
  rounds, real OS processes, byte-level file==winner asserts). Lease law (claim
  outlives short-lived claimant) = **Supported** (run-1 counterexample + B2/E
  regression + CLI smoke showing held_active with pid_alive=false). POSIX safety =
  **Unproven** (os.rename overwrites on POSIX; win32-only organ by design — same
  stance as bay_organs).

## receipt-003 — grok riddler map wired at campaign root (SELF_STEAL O1 part 1)

- **Task:** O1 part 1 — grok's daylight build deliverable unwired:
  `load_riddler_map` reads campaign root only; grok's five-room map never playable.
- **Built:** `campaigns/villains_guild/riddler_map.json` — byte-identical copy of
  `campaigns/villains_guild/daylight/riddler_map.json` (bind, not move; daylight
  deliverable set untouched). Pre-copy assert: root map did not exist. sha256
  `075aba0943d05f62db084e94d321886419fc9e4f8288f6c39b8fe369f3ae9999` both sides.
- **Evidence:** `load_riddler_map(Path("campaigns/villains_guild/module.json").parent)`
  — the engine CLI's exact bind path — returns the map: `riddler_campaign_map.v1`,
  `villains_guild`, 5 rooms keyed by id, ids exactly matching `module.json`. Full
  detail in the BIND RECEIPT appended to `watch/SELF_STEAL_GROK_ORPHANS_20260904.md`
  (backup `.bak-20260904` taken before append).
- **Tri-state:** Map findable + bind integrity = **Supported** (sha identical,
  loader verified live). grok's "engine will load the map in play" = flips
  Unproven → **Supported** for the root copy. O1 part 3 (eight codec gaps in
  `mag/riddler.py`) = **still open**, banked as riddler-codec-debt, not touched.

*— builder lane (zcode seat), shift 2, 2026-09-04. Trail:
`queue/lanes/builder/trail.jsonl` (10 rows this shift). Backups:
surface.md / SELF_STEAL doc → `.bak-20260904`.*

## receipt-004 — company library corpus wave 1 (5/5 landed, 1 license trap, 1 Windows surgery)

- **Task:** Background build — start the company library's local corpus: 5 shallow
  clones into `corpus/library/`, per-repo meta, curriculum + license ledger, trails.
- **Built:** `corpus/library/` + `corpus/dumps/`; 5 clones, each with
  `.corpus-meta.json`; `corpus/LICENSES.md` (the fine-tune legal spine);
  `corpus/CURRICULUM.md` appended (scout's catalog preserved, not overwritten).
- **Cloned:** anthropic-courses 202MB **CC-BY-NC-4.0 → RAG-ONLY** · ms-agents-beginners
  941MB MIT W · ms-genai-beginners 1536MB MIT W · hf-agents-course 6MB Apache W ·
  openai-cookbook 1755MB MIT W (worktree extracted manually, 3133/3133 files
  size-verified against the git tree).
- **The trap:** anthropic-courses is NonCommercial — the one license in the set that
  bars fine-tuning. Caught by reading the LICENSE, recorded in LICENSES.md.
- **The surgery:** openai/cookbook cannot be checked out on Windows at all (one
  subtree has an NTFS-invalid trailing-space directory name; kills checkout,
  read-tree, AND git archive at tree-walk). Extracted blob-by-blob via ls-tree +
  cat-file, 4 parallel workers, promisor lazy-fetch pulling the blobs; excluded only
  that subtree (31 sample-data JSONs, filesystem-excluded not license-excluded).
- **Size honesty:** total 4.4GB against a ~500MB budget — breach noted, next-wave
  clone queue NOT started. Trim candidates (translation dirs) identified, not
  deleted — operator GO required.
- **Tri-state:** 5/5 repos usable on disk = **Supported** (file counts + size
  verification; licenses read from files, not API metadata). "Corpus within budget"
  = **Disputed by measurement** (4440MB). Cookbook extraction integrity = Supported
  (3133/3133 sizes match tree; registry.yaml + 34374.jpg repaired and re-verified).

*— builder lane (zcode seat), background build, 2026-09-04. Trail: 7 rows appended to
`queue/lanes/builder/trail.jsonl`, mirrored to `dashboard/static/trails/builder.jsonl`.*

## 2026-09-04T18:30:40Z - RECEIPT-005 (fire-9)
LAW-055 written; lattice at 55 laws; mirrors refreshed.

### GATED DROP ADOPT-1 (salon verdict, watch/STEAL_ORG_VS_FIELD_20260904.md): tool-de
- gate: FAIL ttl:unparseable
- where: mag/ + your own lane tools
- ttl: 2026-09-06
- state: REFUSED

### GATED DROP ADOPT-2: handoff gate (charter clause 9)
- gate: FAIL ttl:unparseable
- where: queue/lanes/*/inbox.jsonl convention
- ttl: 2026-09-06
- state: REFUSED

### GATED DROP 
- gate: FAIL missing:task,missing:where,missing:why,ttl:missing
- where: None
- ttl: None
- state: REFUSED

### GATED DROP 
- gate: FAIL missing:task,missing:where,missing:why,ttl:missing
- where: None
- ttl: None
- state: REFUSED

### GATED DROP 
- gate: FAIL missing:task,missing:where,missing:why,ttl:missing
- where: None
- ttl: None
- state: REFUSED

### GATED DROP 
- gate: FAIL missing:task,missing:where,missing:why,ttl:missing
- where: None
- ttl: None
- state: REFUSED
