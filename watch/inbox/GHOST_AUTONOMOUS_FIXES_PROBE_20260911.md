# GHOST AUTONOMOUS FIXES PROBE — did the silent machines actually fix things? 2026-09-11

**Commission:** wave rotation, night run. Next-lane flag from
`watch/inbox/HOLLOW_MASS_BODIES_20260911.md`: check whether the orc asks actually
executed. Target: `memory/runs/ghost/autonomous_fixes/`. Read-only except this file.

**Method:** directory censused (ls + mtimes); companion trail parsed
(`memory/runs/ghost/autonomous_trail.jsonl`, 1,493 rows); chain grepped
(`verkle_chain.jsonl`: 0 hits for `autonomous_fix`); writer code located
(`mag/ghost.py` ~1418-1460 mints the janitor asks); ask-side cross-check against
the biography dossiers and `trail.jsonl`; 5 artifacts read (2 of them are the
direct receipts for the hollow-mass orc asks). Plain English, tri-state.

---

## 1. Inventory

The directory **EXISTS**: `memory/runs/ghost/autonomous_fixes/`.

- **Count:** 19 files, all `.md`.
- **Span:** Aug 8 2026 → Sep 6 2026 by mtime (content internally dated 08-09 → 09-07).
- **Format:** one FKB-signal diagnosis card per file, named `{tool}_{hash12}.md`
  (e.g. `run_python_2e689948ccfa.md`, `__86902901b952.md`), plus a few named quests
  (`spider_blind.md`, `operator_escalate_loop.md`, `operator_steer_override*.md`,
  `refine_loop_grok_402_drainer_idle.md`, `guard_registry_8ebc2e7c6cb1.md`).
  Each card: signal + count + window header, root cause traced against live code,
  recommended fix, and (on re-triggers) appended re-verification sections.
- **The writer:** `mag/ghost.py` mints the asks — "$0 ... Write to
  memory/runs/ghost/autonomous_fixes/<sig>.md. **Read-only except for the output
  file.**" The read-only charter is baked into the ask itself.
- **Companion trail:** `memory/runs/ghost/autonomous_trail.jsonl` — 1,493 rows,
  2026-08-08 → 2026-09-09. Outcomes are ONLY `spawned` (1,329) and `spawn_failed`
  (164); 402 rows fall in the Aug 19-31 hollow-mass window; families: fkb 1,489,
  verkle_stale 3, spider_blind 1. The trail records spawns, never completions.
- **The chain:** `verkle_chain.jsonl` contains **zero** `autonomous_fix` mentions.
  Knot-silence confirmed at the source.
- **Delivery is not 100%:** asks exist for `swarm_sense_7fc55a50e2e8.md` (in the
  biography dossiers) and `verkle_audit.md` (in ghost.py) — neither file exists.

## 2. The 5 samples

1. **`__86902901b952.md`** (Aug 23) — the DIRECT receipt for orc ask
   orc-t0e05c0cf60 ("[janitor] FKB signal '_:86902901b952' has 7 occurrences...
   write diagnosis... $0"). **EXECUTED.** The file is a real diagnosis: every
   occurrence is an identical deepseek `queue_error` at spawn ("quota exhausted or
   not configured"), session_id null on all — a provider-level failure, not a code
   bug. The ask said 7 occurrences; the agent independently counted 30-in-window /
   190-total and said so. It did its own forensics, not parroting the trigger.

2. **`run_python_2e689948ccfa.md`** (Aug 9, re-verified 08-31 and 3x on 09-07,
   10.9 KB) — the DIRECT receipt for orc ask orc-tc829720ddb. **EXECUTED, five
   times over — and the best artifact in the directory.** Four-layer error-masking
   chain traced live: `tools/code_execution.py::run_python` drops the traceback →
   `backend/server.py::run_task` doesn't lift `result.error` →
   `mag/agent_cli.py::_run_tool_http` substitutes the literal "backend reported
   failure" → `mag/failure_kb.py` hashes the constant, collapsing every distinct
   snippet bug into one mega-signature (reproduced the hash byte-for-byte). Count
   tracked 862 → 8,641 across trips. The machine's own words: "**Fix still NOT
   APPLIED** ... this is the 5th janitor trip on the same signature ... a code
   change a read-only janitor cannot make and needs a coding-agent/human."

3. **`loop_breaker_a3bb873230e0.md`** (Aug 31) — the ghost diagnosing ITSELF: 9
   concurrent byte-identical `while True: cycle()` processes (9 pids listed),
   duplicate-brains storm on the `ghost_cycle` singleton slot, 227 detector fires
   across two bursts ~75 min apart, same 9 pids alive through both. "**Read-only
   diagnosis; no code changed.**"

4. **`source_trace_e23bf7d75ffa.md`** (Aug 31) — the same storm seen by a second
   detector: 185 more `runaway_python` events, identical pid set 02:58→05:04,
   cross-references sample 3. Two detectors watched the machines' own runaway for
   two hours and filed forensics on it while it kept running.

5. **`search_files_d151f494f5d0.md`** (Aug 31) — backend-down infrastructure
   failure (10 identical `tool_fail`s, provider deepseek-v4-flash); diagnosis
   verified with a LIVE health probe against `127.0.0.1:8000` (backend had since
   recovered on its own), plus dedup/supervisor recommendations and a re-verification
   section.

## 3. The verdict (tri-state)

- **SUPPORTED — the silent machines executed real work the knots never recorded.**
  19 substantive diagnosis artifacts, Aug 8 → Sep 6; chain mentions: zero. Both
  hollow-mass janitor FKB asks (orc-t0e05c0cf60, orc-tc829720ddb) EXECUTED — their
  output files exist and are accurate; sample 2 re-verified its own diagnosis
  against live code five separate times. The hollow mass hid genuine deed.

- **DISPUTED — they fixed nothing. "autonomous_fixes" is a misnomer: it is an
  autonomous DIAGNOSES directory.** 19/19 files are diagnosis cards; 0 applied
  patches; several say so explicitly ("no code changed", "fix still NOT APPLIED").
  This is by charter (read-only except output file), not laziness — but the
  pipeline structurally ends one step before the deed, and no seat or human ever
  picked up the recommendations. Even the machines' own 9-copy respawn storm,
  diagnosed twice by two detectors in one night, was never killed: they filed
  400+ detection events on their own runaway and left it running.

- **UNPROVEN — the other two orc asks.** The republic_os round (orc-t2b1ecf8a72):
  the ask sits in the ghost's attention queue ("[mag] run republic_os round to
  reinforce/prune graph", visible in trail.jsonl state rows) and dispatched as a
  stub session, but no artifact exists anywhere in the ghost tree. The overmind
  orphan fold (orc-t08ea29162c): trail.jsonl carries orphan-count snapshots
  (51 novel orphans, Aug 11) but no fold receipt. Also unproven: the full
  ask→delivery rate (two asked files confirmed absent; full denominator unknown
  without reading every dossier).

## 4. Bottom line for the hollow-mass lane

The record pipeline under-committed twice: the knots recorded neither dialogue nor
deed (0 chain mentions), and the fixes trail records spawns, not completions. The
only completion receipts that exist are the .md files themselves — any future audit
must go to the filesystem; the chain alone will always show nothing. And the
diagnoses are still-live work orders: the `2e689948ccfa` masking chain is a real,
precisely-specified one-line-fix candidate (lift `result.error`/`result.output` in
`mag/agent_cli.py::_run_tool_http`, plus the two sibling paths) that would collapse
an 8,641-count fake mega-signature polluting the FKB. Recommended next lane: hand
that fix to a coding seat, then re-baseline the signature.

**CYCLE GENETICS:** flag(from hollow-mass)→exists(19 files, Aug8→Sep6)→trail(1,493
rows, spawned-only)→chain(0 mentions)→samples(2 direct orc receipts EXECUTED as
diagnoses; ghost diagnosed its own storm twice, fixed nothing)→verdict(SUPPORTED
deed / DISPUTED fix / UNPROVEN republic+fold)→next(hand 2e689948ccfa fix to a
coding seat; filesystem is the only receipt surface).
