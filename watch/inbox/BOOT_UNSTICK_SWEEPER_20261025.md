# BOOT 2026-10-25 - unstick-sweeper closed + two gate-era findings

Writer: seat (ZCode fresh boot, operator "Fresh boot"). Cockpit RED item
`[unstick-sweeper]` from warm_state diagnosed and closed same boot.

## The jam (two independent blockers, one symptom)

1. **Self-referential symlink** `memory/cas/cas -> memory/cas` (created
   2026-10-24 00:19, untracked, no git history, zero consumers in
   tools/queue/mag/configs/scripts). Git for Windows ENOSYS on any `git add`
   touching it; every memory-area sweeper batch died since 10-24 11:29Z.
   Removed; dry-run `git add -A -n memory/` exits 0.
2. **Large-blob gate freeze** (found only after the symlink cure): the
   2026-10-24 secret-gate chain (`tools/precommit_secret_check.py`) refuses
   staged blobs >32 MB. `memory/biography_v2/chain_v2.jsonl` (append-only
   biography ledger) crossed 32 MB (33,397,317 bytes) AFTER the gate landed,
   so the gate permanently froze every batch carrying it - the ledger that
   landed daily since 10-24 12:50Z can never land again. The 180-char
   failure notes truncated below the actual refusal line (gitleaks PASS
   INF lines are what got captured), which is why the notes looked clean.

## Fixes landed this boot

- Symlink `memory/cas/cas` removed (self-loop, recreatable, no consumer).
- `chain_v2.jsonl` untracked via `git rm --cached` + `.gitignore` entry with
  dated reason; file stays on-disk truth (gate doctrine: data lakes stay on
  disk), git history retains all past versions. Commit `02bb44e8eb`.
- Sweeper breath `B-20261025T191107Z-b45916`: canon, dashboard, queue,
  memory/game, **memory** (4c2fe1d283, the formerly frozen batch) landed;
  percolator/corpus/biography_v2 drained to "nothing staged". Working tree
  749 -> 363 dirty.

## Still refused (policy class, named owners)

- **watch (28 files):** 52 real gitleaks `mag-env-assignment` findings in
  historical records (watch/RBN_SCORED_20260906.md,
  watch/hermes_wings/scratch/traj.txt, et al.) - dead-key-shaped strings in
  append-only receipts. Operator call: redact, move to
  C:/Users/foste/.mag_secrets_intake/, or scope the area. Seat did not edit
  record bytes.
- **tools (7 files):** prior_art_check refuses 5 new `tools/mag_relay/`
  files (built 2026-10-25 ~12:00, sibling lane live). Owner adds the
  `prior_art:` header at next commit. **Gate gap found:** the rules data
  file `tools/mag_relay/router/routing_rules.json` can NEVER pass - JSON
  has no comment syntax and the gate regex requires a `prior_art:` line,
  so any data file under tools/ deadlocks forever. Gate needs a
  data-file exemption or a JSON-key form. NOT fixed this boot (1-day-old
  gate, first refusals are teaching the law; change is an owner decision).
- **corpus (325 files):** gitleaks false positives - `generic-api-key`
  fires on mycology prose ("secretes 3,... acid",
  corpus/drive_fostertron_20261025/text/b7ac1966...txt) and
  `mag-env-assignment` fires on DF game data
  (corpus/df_mine/df_procedural.json `"grants": "[SECRETION:...:POISON..."`).
  Allowlist or allowlist-path decision owed.

## Owed register (new)

- Operator: watch/corpus findings disposition; chain-ledger rotation or
  archival custody design (untrack is the stopgap; the ledger grows forever).
- mag_relay owner: 5 prior_art headers.
- prior_art_check owner: data-file deadlock gap (json/jsonl cannot comply).
- commit_sweeper: consider capturing the FULL hook refusal (note truncation
  at 180 chars hid the real refuser for three sweeps).

## Boot sequence note

Load order executed: newest state (CURRENT.md 10-23, machinery pages
excluded per row 0a), zknot LATEST, rib_boot (11 law ribs + 5 amendments
mounted), warm boot paid the 109k-min chain age debt. Instrument: gitleaks
8.x via .githooks/gitleaks.toml; per-file verify runs are read-only
detect/protect against a throwaway GIT_INDEX_FILE (one footgun noted: a
status count taken with GIT_INDEX_FILE still exported to a deleted file
reads the whole repo as untracked - 98,600 phantom; true count 363).
