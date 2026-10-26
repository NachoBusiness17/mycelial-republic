# ZCODE RATCHET WAVE 2 — enforcement landed — 2026-09-25

Follow-up to [ZCODE_RATCHET_LANDED_20260924.md](ZCODE_RATCHET_LANDED_20260924.md).
Wave 2 turns the ratchet from a tool into LAW, plus two more recreated patterns.
All receipts below were executed 2026-09-25 with `.venv/Scripts/python.exe` at estate root.

## Landed

1. **`githooks/pre-push` + `core.hooksPath=githooks`** — the ratchet's `check --changed`
   now runs on every push to `local` (Mag-backup.git). Nonzero exit blocks the push.
   Hook test-fired directly: `PASS — no unregistered debt`, exit 0. The hook's own header
   states the law: accept debt by NAME via baseline-update, never loosen the hook.
2. **`tools/freshness_check.py`** — boot-doc stale-trap meter. Pre-stated bar:
   doc stale when last-touched >7 days (untracked docs measured by disk mtime) while the
   repo has a commit within 2 days. Frozen docs must be registered in FROZEN_OK with
   reason+date. Bar stated in code before any measurement (meters-not-prose).
3. **AGENTS.md "Build discipline" section** — ZCode's spec-first, no-timeout-masking,
   no-fallback-creep, fix-comment-carries-receipt laws translated into estate terms,
   plus pointers to both meters.

## Execution receipts

- Freshness gate, three runs (two bugs found by the gate refusing to lie — HEAD pathspec
  bug, then untracked-vs-missing distinction): final run FAIL, exit 1, honestly:
  - `BOOT_4_7.md: 11.1d old STALE`
  - `state/HANDOFF.md: 25.3d old [untracked-mtime] STALE`
  - `state/CURRENT.md: 0.6d ok` · `state/START_BRIEF.md: 2.4d ok`
- Hook wired: `git config core.hooksPath githooks`; executable bit set via
  `git update-index --chmod=+x`; direct invocation PASS, exit 0.
- Post-commit sanity: ratchet `check --changed` PASS with this wave's own files in scope
  (freshness_check.py <400 lines, no bare except, no undated TODO — the tool dogfoods its own gate).

## Open (the FAIL is the deliverable, not a debt to silence)

- **BOOT_4_7.md (11.1d) and state/HANDOFF.md (25.3d) are genuinely stale boot truth.**
  Refreshing them means writing today's boot state — main-session work, not to be invented
  here. The meter will keep failing until they are refreshed or registered frozen.
- state/ boot docs are untracked by design (state/ gitignored); if they should be tracked,
  that is an estate-policy call for the operator.
- Staged, not built: config-integrity seal over configs/*.json (migration-ledger steal) —
  deliberately deferred: keys.json rotates legitimately and a seal would cry wolf unless
  rotations go through a named update act. Revisit when key rotation is frequent enough to need it.

## RATCHET V2 — three new rules from this week's real diseases — 2026-09-25 later

Each rule is backed by a disease we actually hit or measured this week, not by taste:

- `except-pass` — silent `except ...: pass`. Day-one count: **650 files**. The estate's
  single biggest disease class, now counted; new ones fail.
- `env-key-read` — direct `os.environ`/`os.getenv` of a key-shaped name
  (`API|TOKEN|SECRET|_KEY|KEY_`) outside `mag/key_law.py` + `models/env_load.py`.
  This is the Key Law ("no reader guesses env names") gaining a ratchet tooth.
  Day-one count: **22 files** — matches the grep census exactly.
- `cwd-relative-path` — module-level `X = Path("relative/...")`, the audit_log disease
  (cwd-dependent constants). Day-one count: **3 files** (audit_log.py, constants.py,
  steer_receipt_wire.py). Absolute `Path("C:/...")` constants do NOT fire.

Receipts: self-check NONE (the gate does not flag itself); probe with all three diseases
→ `check --changed` FAIL with exactly three NEW fingerprints
(`f93e065f…` except-pass, `b60f7b75…` env-key-read, `1c9d5818…` cwd-relative-path);
probe removed → PASS. Register: 192 → **867 claims** (650 except-pass + 187 file-too-long
+ 22 env-key-read + 3 cwd-relative-path + 5 other). Day-to-day pushes test only
`--changed`; the full 1,116-file check is the sweep meter.

## METERS ON A SCHEDULE — Estate Ratchet daily 09:45 — 2026-09-25 latest

- `scripts/ratchet_daily.ps1` (runner: freshness check + full ratchet check →
  `logs/ratchet_daily.log`, exit 1 if either fails — the honest nag) +
  `scripts/register_ratchet_task.ps1` (clones the register_improve_task.ps1 pattern).
- Task **"Estate Ratchet"** registered on the estate's morning stack (09:45, after
  Spine 09:00 / Librarian 09:15 / Gopher 09:25 / requeue 09:35).
- Fired by hand: both meters ran, log holds the receipt — freshness **FAIL (BOOT_4_7.md
  11.4d, state/HANDOFF.md 25.6d — still open, main-session truth)**, ratchet
  867/867 NEW=0. Runner verified by direct run: `END freshness=1 ratchet=0`.
- Sandbox caveat receipt: an instance launched from inside an agent shell gets swept at
  call end (LastTaskResult 0xC000013A) — the 09:45 self-launch by Task Scheduler is the
  production path; check `logs/ratchet_daily.log` for the END line to confirm it.

### Fix queue — worst except-pass offenders (hits per file)

```
 70  mag/ghost.py            43  mag/orchestrator.py     32  mag/agent_cli.py
 31  mag/voice_turn.py       23  mag/power.py            15  mag/game_campaign.py
 14  mag/governor_autorun.py 14  mag/diary_node.py       11  mag/lane_runner.py
 10  mag/voice_dig_board.py
```
650 files total. These ten hold 263 of the hits — fixing them is a third of the disease.
Not auto-fixable: a silent pass is sometimes a decision; each needs eyes
(`prune` recovers the claim on fix).

## FIX QUEUE FIRST DENT — ghost.py loop-death guards — 2026-09-25 latest

Taxonomy from reading ghost.py's 70 except-pass sites (4,244 lines, 140 except-Exception
total, zero bare excepts):

1. **Aggregator guards (majority)** — capability-sensing blocks reading dozens of optional
   memory sources; a missing/corrupt source just omits its key. Silence is BY DESIGN;
   these stay as counted register debt (file-grained claim leaves only when the file is
   fully clean — prune correctly no-ops after partial fixes).
2. **Loop-death guards (the black-hole species) — FIXED**: `_cost_enforcer_loop_wrapper`
   and `_bard_loop_wrapper` swallowed their own death — a crash at import/first-tick made
   cost enforcement / the Chronicle weave vanish with no trace, indistinguishable from
   never-started. Fixed with LOOP-DEATH GUARD prints following the file's own
   FOLD-SWALLOW GUARD pattern (line 1520). Diff +20/−4; compile OK.
3. **Daemon cycle guards** — `except Exception: pass  # never crash the daemon` with
   stated intent: acceptable as a class, flagged for a future logging pass.

Test receipt: test_ghost.py + test_ghost_spooky.py + test_ghost_memlance_notebook.py =
**38 passed, 1 failed** — the failure (`test_probe_carries_real_verkle_proof`) is
**pre-existing verkle tip drift**: stored tip root `2fcda535…` (tip written 09-22) vs
recomputed `a3daab3e…`. Not touched by this diff (handlers only); the estate's own
`verkle-audit --dry` corroborates `verkle_gaps: 1`. Chain repair deliberately NOT done
here — sacred artifact, own lap, `repair_tip_if_consistent` exists when the operator GOs it.

Live-drift receipt: the changed-gate caught another lane's brand-new
`tools/audio_channel.py:31` silent-pass mid-lap — left unregistered (someone's WIP;
their push will meet the gate).

## VERKLE TIP REPAIRED + TORN-WRITE HARDENING — 2026-09-25 latest (operator GO'd)

Diagnosis (read-only, done with 5 windows live):
- Chain SOUND: last row's committed root == recomputed merkle root over all 9,823 leaves.
- Tip STALE: root `2fcda535…` (mtime 09-22 13:32:42) vs chain `a3daab3e…` (mtime :44) —
  two seconds apart, same leaf count, different last_leaf. The chain was rewritten right
  after the tip was committed and the tip never caught up.
- DAMAGE: `_verify_chain_consistent` gates every append ("never build on a lie") — the
  stale tip made **every chain append estate-wide bounce** (bard weave, ghost folds,
  usage digests) since 09-22. The chain silently accepted no writes for days.

Repair (operator GO): `repair_tip_if_consistent()` — proves the chain gate, then
rewrites ONLY the tip pointer under `verkle_lock`. Result: `ok=true, repaired=true`,
verify "chain consistent (9823 leaves)", spooky tests 4/5→**5/5**, `prove_latest`
returns a verified O(log n) reconstruction (index 9822).

Hardening landed: two of the three tip writers used plain `TIP.write_text` (torn-write
window = a killed write mid-tip produces exactly this disease). Consolidation
(verkle_knot.py) and usage_digest.py now use `_write_tip_atomic` (tmp + os.replace).
Compile OK; verkle tests 11 passed / 2 failed — the 2 are pre-existing dashboard-HTML
pin drift in test_desk_baseline_probe.py (`">Verkle artifacts<"` + `btnDaysCopyKnot`
expected in a generated page; unrelated to the tip path).

Forensics note, filed honestly: the repair overwrote the stale tip before its `note`
field was read — the exact writer identity (append vs consolidation vs usage_digest)
is unrecoverable from the artifact; the torn-write window is the likely mechanism.
Lesson: photograph the evidence before repairing it.

## MIMOSA DEEP SCAN — SEALED VERDICT — 2026-09-25

- Job scan-job-muh9asiw-8b9936bfbdbdc454 → COMPLETED 18:15:59Z (25 min, deep, static-only).
- Seal: `sha256:92540e87a43098a483438cb603072386928e619336c6386aeb3ede2c89d10894`
- Report dir: `~/.mimosa/security-scans/project-8af8c49a6c1b0282e16b1e73/scan-2026-09-25T18-15-58.463Z-fd400a18ce93`
- Plain English: **zero confirmed vulnerabilities.** 5,294 raw findings tallied; ~103
  business-logic hypotheses raised (sensitive ops without observed role checks; resource
  ids from requests without ownership binding; missing sibling-route authorization) —
  every one verdict **inconclusive / candidate / verdictEffect none**, i.e. patterns for
  human eyes, not confirmed holes. For a single-operator local harness with no
  multi-tenant surface, the ownership/tenant-binding family is expected noise.
- The one actionable number: **dependency advisories — 121 advisories matching 41 of
  3,334 scanned packages** (offline advisory DB). Next lap if wanted: triage the 41
  packages against actual usage (many will be unused transitive deps).

## WINDOW CLOSE-OUT — 2026-09-25 — do-it-all lap

### Advisory + finding triage (the scan, disaggregated)

The 5,294 headline findings are 97.7% FOREIGN-SHELF: **5,176 findings sit under
mine/, corpus/, watch/** — the read-only stolen-repo shelves (Picasso law: foreign
code lives on the shelf, never runs as estate code). They are not estate attack
surface. The estate-owned subset is **75 findings (60 high / 2 medium / 13 low)**:

- ~50 path-traversal flags on operator-run `scripts/` (wave_driver, the50_*, tg_harvest,
  m12_pairing, hunger_ledger, ack_reaper, …) — CLI args into paths; "attacker" is the
  operator. Low practical risk while they stay local scripts; the queue matters when any
  graduates into a service.
- 2 code-injection flags: `main.py:1342`, `tools/tier_probe.py:84` (eval/exec family).
- 1 command-injection: `tools/pupeteer_gauntlet.py:558` — already in the ratchet register.

Filed as a classified queue, deliberately NOT mass-fixed: each needs eyes, and the
ratchet/pre-push gate stops new instances.

### Boot docs — frozen, not refreshed

Both flagged docs are self-declared fossils: BOOT_4_7.md's own header says "SUPERSEDED
2026-09-23 … Kept only as lineage. Do not paste this"; state/HANDOFF.md is the
2026-08-31 session-maze snapshot (live state = state/CURRENT.md, fresh). Registered in
the freshness meter's FROZEN_OK with reasons+dates — the meter's own remedy. Live docs
(CURRENT.md, START_BRIEF.md) stay monitored. **FRESHNESS: PASS.**

### Config seal — the migration-ledger steal, landed

`tools/config_seal.py`: sha256 register over configs/* (47 files, json+yaml) →
`configs/.config_seal.json`. `verify` fails on modified/missing/unsealed bytes;
`update --by --note` is the named act (key rotations re-seal by hand, never silently).
Wired into the daily sweep (three meters now: seal, freshness, ratchet).
Receipts: first seal 47 files → PASS; self-inclusion bug caught by its own verify
(seal sealed itself → fixed by excluding the seal file); planted unsealed config →
FAIL naming it → removed → PASS. **CONFIG-SEAL: PASS.**

### Meter state at window close

`CONFIG-SEAL: PASS · FRESHNESS: PASS · RATCHET: FAIL` — the ratchet's FAIL is exactly
one item: `tools/audio_channel.py:31` (silent except-pass), another lane's live WIP,
left unregistered by design so their push meets the gate. Register: 867 claims.

### The day, in one paragraph

ZCode (our own harness) open-sourced → surveyed 10+3 lanes, 75 path-verified steals →
recreated the fingerprint ratchet (v1+v2, 867-claim register, pre-push gate, daily
09:45 task) → resurrected a dead spore and audit_log (first audit write ever) →
13-law operating playbook wired into AGENTS.md → fixed the verkle tip freeze that had
been bouncing every estate chain append since 09-22 (spooky tests 5/5, chain accepting
writes again) → deep-scanned the estate, sealed: zero confirmed vulns, 97.7% of
findings on the foreign shelf, 75-file classified queue filed.

## SPORE RESURRECTION COMPLETED — 2026-09-25 later

The ratchet's day-one haul (`mag/spore_seed.py`) is now fully alive. Execution revealed
TWO more wounds the parser could never see (the execution-receipt law earning its keep):

- **Wound 5**: `SPORE_SEED_FILE` is a `Path` in constants.py — `.format()` on it crashes
  (`AttributeError: 'WindowsPath' object has no attribute 'format'`). Fixed via
  `_seed_file()` helper; constants.py stays the single canonical name.
- **Wound 6 (in `mag/audit_log.py`, not the spore)**: `os.environ` used with no
  `import os` — audit_log has NEVER successfully logged anything until today. Fixed.
- Design repair (spec-first): the phantom `verkle_knot(data=, prev=)` call named an API
  that does not exist (the real chain API is session-knot-shaped); the spore's own
  append-only jsonl is the seed record, per its own docstring. `validate_spore_seed` now
  hashes the SAME material generate does (timestamp included) — before, every seed it
  generated would have failed its own validation.

Receipts (all 09-25, .venv python):
- `generate --seat zcode` → exit 0, seed `a91d36ba…` anchored to live tip root
  `2fcda535…` (9,823 leaves); record appended to `memory/spore_seeds/zcode.jsonl`.
- `verify --seat zcode --min 1` → "2 seeds, 1 consecutive valid", exit 0.
- Falsifiability: `validate(real)=True`, `validate(tampered)=False`.
- `memory/audit.log` received its first `spore_seed_generated` entry ever.
- Design note: verify fails "Chain root repeated" when two seeds share one tip root —
  by design; seed continuity expects the chain root to ADVANCE between seeds.
- Register: another lane's new `tools/seed_v2.py` (462 lines) accepted by name into the
  register (192 claims); gate PASS.
- Also landed: `corpus/steal/ZCODE_OPERATING_PLAYBOOK_20260925.md` (13 verified
  operating laws from the deep dig) wired into AGENTS.md build-discipline.
