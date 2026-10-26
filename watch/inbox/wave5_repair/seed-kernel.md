# seed-kernel: the SEED-RIB kernel repair (wave5, 2026-09-29)

Lane: seed-kernel, division B, gala_20260925 wave5-repair.
Owned files touched: tools/seed_rib.py, tools/seed_mcp.py, plus the seed
artifacts (watch/inbox/seed_rib_20260929/, watch/inbox/SEED_RIB_CURRENT).
Every number below comes from a command run in this session or a file read
in this session; starting points were watch/inbox/burn_reset_20260927/flash50/s2-20.md
and watch/inbox/burn_reset_20260927/flash50/w4-08.md (material the ask gave me).

## The owed work, as found

Reproduced first, before any edit (check file section A):

    .venv/Scripts/python.exe tools/seed_rib.py verify --seed watch/inbox/seed_rib_20260928/seed-rib/seed.json --into <tmp> --source .
    SEAL MISMATCH (pointer vs source): AGENTS.md
    SEAL MISMATCH (pointer vs source): tools/stealth_driver.py
    SEAL MISMATCH (pointer vs source): tools/stealth_fanout.py
    EXIT=1

All four s2-20 symptoms confirmed live: 3/5 pointer seals drifted, the 09-28
seed carried 0 law-role entries while attesting law_refs 12 (verifier printed
the count and checked nothing, old tools/seed_rib.py:159-161), decoded inline
payload 297,744 B vs the 100,000 B budget, and tools/seed_mcp.py:44
DEFAULT_SEED pointed at the frozen 09-26 seed while watch/inbox/SEED_RIB_CURRENT
pointed at the 09-28 seed (split-brain).

## What changed

1. tools/seed_rib.py (7,348 -> 12,169 B measured; the generator grew because
   it now carries the laws it enforces):
   - Budget law bound to DECODED payload (w4-08 correction 3): BUDGET_BYTES =
     100000; build() refuses and verify() fails with "SEAL MISMATCH (budget)"
     naming the levers when sum(inline entry bytes) exceeds it. Proven against
     the old seed: the 09-29 repro run now prints "SEAL MISMATCH (budget):
     decoded inline payload 297744 > 100000 B" on the exact artifact s2-20
     caught violating it (check file section A, line 8).
   - Quine law as a build invariant (w4-08 correction 1): build refuses unless
     the generator itself rides inline in its own seed. The 09-28 seed carried
     zero seed_rib entries (w4-08 section 2, closure drift); the new seed
     carries tools/seed_rib.py inline.
   - Pointer freshness SLO (w4-08 correction 2): verify() prints seed age vs
     FRESHNESS_DAYS=3 (the measured pointer half-life) and warns past it; the
     enforcement half ("any verify exit 1 voids SEED_RIB_CURRENT, re-render")
     is stated in the module docstring and here as law, not wired to exit
     codes, because a time-dependent exit makes the finish line flaky.
   - law_refs cross-check (spec SEED_RIB_FORMAT_v0_20260926.md falsifier (e),
     s2-20 item 2): verify() decodes a carried memory/law/registry.json and
     fails on any law_ref id the carried registry does not hold. Phantom-id
     seeds can no longer pass.
   - --pointer-list: a file of paths force-carried as pointer entries; this is
     the mechanism that moved the receipt mass to pointers.
   - verify --seed/--into now default: seed resolves through
     watch/inbox/SEED_RIB_CURRENT via resolve_current(), --into gets a fresh
     temp dir, so the finish-line command works exactly as written.
   - Dedupe fix: kernel inputs and pointer-list paths are deduped by resolved
     path (a first build emitted AGENTS.md twice; caught by its own verify,
     fixed, rebuilt).
2. tools/seed_mcp.py: DEFAULT_SEED (hardcoded 09-26 path) removed; the default
   seed is resolve_current(source root), so the MCP surface and the named
   current seed cannot split-brain. --list now reports the resolved seed path
   (it printed "None" before the fix). --seed still overrides.
3. watch/inbox/seed_rib_20260929/seed-rib/seed.json, built 2026-09-29T10:50:05Z:
   127 entries (29 inline / 98 pointer), 158,398 B on disk, decoded payload
   97,364/100,000 B, law_refs 12, sha256 4bbab60ad7cdb9f41dc12e231a16554b3377738a614987600821be57a580feda.
   Kernel inline: 10 law-role entries with real bytes (9 memory/law/*.md +
   registry.json 9,849 B; every law_ref id machine-checkable against carried
   bytes), docs/DNA.md, CONSTITUTION.md, docs/ref/OPERATOR_CARD.md,
   state/CURRENT.md + state/START_BRIEF.md + state/HANDOFF.md + BOOT_4_7.md
   (the exact four files tools/freshness_check.py:36-41 gates on),
   memory/warm_state.json, memory/live_from_grok.md, configs/lanes.yaml,
   the format spec itself, watch/inbox/SHARED_SURFACE_CONTRACT.json,
   watch/inbox/ESSENTIALS_RESTORE.md, watch/inbox/TWO_MACHINE_SYNC_20260919.md,
   the three operator-named ribs (FREE_USAGE_POLICY, DRIVING_LADDER,
   BEHAVIOR_CARDS), memory/attention.md, and the generator.
   Sealed pointers: AGENTS.md (16,712 B live, over the inline cap, same as
   both prior seeds), queue/todo.md, HANDOFF_MAG_AGENT_TODOS.md, the five
   AGENTS.md load-order docs (FRAMEWORK_LOAD, COMPASS, MYCELIAL_SCIENCE_MAP,
   DIRECTION_ARTIFACT_v2, PROJECT_PROPOSAL), tools/seed_mcp.py, and all 90
   carryable paths of the 09-28 seed (78 receipts + delta code/tests) moved
   to pointer carriers via the pointer list
   (watch/inbox/seed_rib_20260929/seed-rib/paths_seed_20260928.txt).
4. watch/inbox/SEED_RIB_CURRENT re-pointed at the new seed (path, bytes,
   sha256, built 2026-09-29T10:50:05Z stamp, delta note). Addendum appended
   to watch/inbox/SEED_RIB_REFRESH_20260928.md naming the supersession; its
   history section was not rewritten.

## Finish line (all run this session; raw output in
watch/inbox/gala_20260925/wave5-repair/lanes/seed-kernel.check.txt)

1. `python tools/seed_rib.py verify --source .` (exact command, bare python,
   default seed resolved through SEED_RIB_CURRENT): exit 0, inline 29
   hash-matched, pointers 98 source-checked / 0 UNRESOLVED, zero SEAL
   MISMATCH rows. Same under the venv interpreter. Passed in the 10:43Z
   quiet window and again at 10:50:05Z (section E) after a sibling write to
   tools/stealth_driver.py staled the 10:43 seals; the SLO fired exactly as
   designed: verify exit 1 voided CURRENT, one command re-rendered.
2. Law-role real bytes: 10 entries (need >= 8), each decoded, length-checked
   and sha256-checked OK (both passes).
3. `python tools/seed_mcp.py --seed-sha` (default resolution) prints
   4bbab60ad7cdb9f4... == SEED_RIB_CURRENT sha256; --list names the resolved
   path watch/inbox/seed_rib_20260929/seed-rib/seed.json. match=True.
4. Ratchet: `.venv/Scripts/python.exe tools/violation_ratchet.py check
   --changed` exit 1, but every NEW/GROWTH row names sibling lanes' in-flight
   files (mag/corpus_gap_research.py, mag/corpus_selfsteal.py,
   mag/link_library.py, tools/fossil_check.py, mag/shared_surface.py,
   tools/stealth_driver.py); none name tools/seed_rib.py or tools/seed_mcp.py.
   This lane did not accept or baseline anyone's debt. The tool ignores a
   --paths flag (reran --changed), so a per-file scoped pass was not
   available; the absence of my files from the printed census is the evidence.

## The churn measured live (why the SLO is not academic)

While repairing, sibling lanes edited the sealed trio in real time:
AGENTS.md 16,513 -> 16,671 -> 17,170 B; tools/stealth_driver.py 27,500 ->
37,814 -> 39,032 -> larger; tools/stealth_fanout.py 8,394 -> 8,559 -> 9,323
-> 9,317 B, across ~15 minutes. Three verify outcomes were observed: fail
(stale seals), transient pass (verify ran between sibling writes), fail again
(a write landed in the 2-minute window). The final pass was taken in a
measured quiet window (all three mtimes stable >= 90 s), build -> pointer
refresh -> verify done as one atomic block. This is w4-08's decoherence
section happening to the repair itself; pointer half-life is in hours on a
burn day, not days.

## Budget posture

Decoded payload is 97,364/100,000 B: 2,636 B of headroom. The kernel files
are live docs and moved at every rebuild (92,324 -> 93,226 -> 95,774 ->
96,410 -> 97,364 across five builds this session). The next re-render that
crosses 100,000 will be REFUSED by the build with the lever line, by design.
For this JSON kernel the operative levers are pointer-izing the largest
inline entries (attention.md, lanes.yaml, TWO_MACHINE_SYNC, the spec); the
L1-L5 line the refusal names is the directory pack's lever set
(watch/inbox/seed_rib_20260926/seed-rib/SEED_RIB.md, "Budget and growth laws").

## Deliberate decisions and non-goals

- inline_max 12,288 for this seed (recorded in its inline_max_bytes field),
  not the 8,192 default: the repaired generator is 12,169 B and the quine law
  requires it inline; the same raise carries registry.json bytes inline
  (9,849 B), which both prior seeds omitted, closing spec section 4's
  "carry or reference" in bytes. AGENTS.md (16,712 B) and the five load-order
  docs (12,875-16,712 B) stay sealed pointers, so the "boot order is a
  promise" property w4-08 described is preserved. Named here because w4-08's
  premise "seed_rib.py at 7,348B fits the 8,192 cap" is now false: the
  checker grew to carry the laws it enforces.
- memory/briefs/latest.md NOT re-carried: FROZEN per AGENTS.md ("must not be
  consumed as live"); dropping it is deliberate, as s2-20 section 0 already
  ruled defensible.
- queue/handoff/* (116 files) and the full docs/ref/MAG_*.md glob (35 files,
  mostly backlog/plan debris) NOT carried: not in the ask's kernel list,
  heavy churn risk against --source verify. The six AGENTS.md load-order
  rows are carried instead.
- tools/seed_mcp_cold_client.py NOT edited (outside this lane's ownership):
  its docstring line 17 and argparse default still name the 09-26 seed, which
  still exists, and the client passes --seed explicitly, so it still runs.
  Flagged for its owner.
- Nothing committed: the shared tree holds sibling lanes' uncommitted work
  (AGENTS.md and the stealth files are modified by them); s2-20 item 5
  (track or gitignore the seed artifacts) stays an operator call. The seed,
  pointer, and receipt are on the shared surface, which is the durable root.

## Falsifier

The repair is void if any of these fails on a later run: verify --source .
exit 0 with the current SEED_RIB_CURRENT; 10 law-role entries with decoded
sha256-matching bytes; seed_mcp --seed-sha == SEED_RIB_CURRENT sha256; build
refusal on a >100,000 B decoded payload; build refusal when the generator is
missing or pointer-carried; verify failure on a law_ref id absent from the
carried registry.
