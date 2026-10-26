---
name: reset-day-execution-20260927
description: Operator "start the day now, go wide" executed 9/27 morning — all
  gates fixed not registered; reset-day builds verified landed; two autopsy root
  causes (.env OLLAMA_HOST locality, rescan Set-Location); queue close verb
  used; board drained
metadata:
  node_type: memory
  type: project
  originSessionId: sess_bb9913b3-7c0e-45ff-9e15-d94e98cdb6aa
---

2026-09-27 morning window (operator: "stop waiting for arbitrary time of day and
execute the order to start the day and go through all processes now take as
long and go as wide as you need").

**What was executed (all receipts in watch/inbox/GATE_DEBT_BATCH_20260927.md,
PURGE_LIST_MERGED_20260927.md, SESSION_CLOSE receipt):**

1. All daily gates fired by hand pre-08:30 (census --collect PASS 2,303/352
   exact; FTS deep match; improve; freshness; catch-up quiet).
2. Ratchet: 8 NEW debts FIXED (zero registered): queue_dupes_check repo-anchor,
   transport_precheck + visor + ledger_lock + openrouter_free_gate except-passes
   → named handlers, secret_gate 749-line split into rules/scan/CLI (3 files,
   each <400; falsifier state/fuel/sg_split_ref/ pre/post counts MATCH on a
   live scope, prefilter parity MATCH), probe20_run 421→400 (TASKS table →
   tools/probe20_tasks.py, --demo reproduces 3 scenarios).
   **Lesson: ratchet --changed scope GREW 114→115 files between two same-morning
   scans and surfaced 4 debts the first hid — always re-run gates after edits.**
3. md_record: 55 unsealed today-files sealed via the seal hook; audit
   "purpose" field joined _has_ref (59 historical op=None beacon rows were
   schema-gap, not writer debt; append-only log never rewritten) → RECORD CLEAN.
4. Shared surface: ok:false(51 errors) → ok:True(0). Fold rebuild + 55
   registers + 3 living ledgers registered living-open + 5 misfiled LINKS rows
   relocated to EVENTS under LedgerLock (LOCK FILE IS `<ledger>.lock`, never
   the ledger itself — the constructor will lock the real file and refuse) +
   58 stale/dead register heals (14 edit-shaped as living-open, 5 invalidates).
   Fold host exits nonzero on its inexact-seq WARN while the add SUCCEEDS —
   judge by validator, not exit codes.
5. Queue: Q-046 + Q-030 closed via tools/queue_close.py (bindings table Edit
   + verb run; 5 closed total). Q-001 verkle99 stays OPEN (execute is
   operator-gated per its card). **Supersede-verb still absent** — stale-dupe
   rows cannot be marked; only open→closed exists.
6. Reset-day BURN_PLAN items 1-4 (SEED-RIB, seed-mcp, ractor panel, free-lane
   tandem) ALL LANDED 09-26 already — the plan was stale; B2 board fully
   drained 498/498 checked; no open briefs to fold ("200+ for next burn" in
   the session recap = what the NEXT fullsend self-feeds, not a standing board).
7. History purge scan harvested: 7,079 unique / 21 blocking in 4 families
   (lan.key; live xai key ×9 copies incl biography_backup_20260825 +
   portable_bags; dead telegram token steps.jsonl:1994; stripe-shaped
   boe*.html + module_audit.ipynb). Merged list = PURGE_LIST_MERGED_20260927.md.
   Purge itself operator-gated (ROTATE-FIRST-WIPE-SECOND).
8. **Autopsy A:** MagCorpusRescanDaily exit 1 every fire =
   scripts/corpus_rescan_daily.ps1 missing `Set-Location $Root` (both sibling
   dailies have it; python -m needs CWD=repo root). Fixed + incremental
   validated live (67,566 rows added, exit 0).
9. **Autopsy B:** improve "work lands but exit 1" = .env line
   `OLLAMA_HOST=http://ollama:11434` (docker network name, unresolvable on
   host) while host ollama answers 127.0.0.1:11434 — the EXACT trap
   mag/doctor.py LOCALITY LAW (B2-107) names. Fixed .env → loopback; all 3
   compose services override OLLAMA_HOST themselves so docker unaffected;
   improve --once now rc=0 all phases PASS ("dual-local multi-model is real").

**Why:** the operator's order was to stop gating on clock times; the day's
real demand turned out to be debt-clearing + the handoff queue, not new burns
(the burn waves had already drained everything demanded).

**How to apply:** on "start the day" orders, fire every daily process
immediately by hand, fix every FAIL in-window (never register), trust the
newest handoff receipt (HANDOFF_20260927_SESSION_CLOSE.md pattern) over older
standing plans, and check whether named builds already landed before
re-dispatching them. Related: [[late-swarm-findings-20260927]],
[[lean-fires-queue-drain-20260927]].
