# SALON FOLD: ARC-SEED AS DEFAULT — recovery without breakage (Sep 7, 2026)
**Commissioned:** Operator — "make this default without breaking everything... always
have a recovery... feed them through our existing surfaces. consult all vertexes. fan out."
**Fan-out executed:** free-lane bench via lane_salon (7 witnesses: grok-cli, openrouter,
groq, cerebras, together, deepseek-pro UP; nvidia-flash DOWN missing key — 6/7 up, $0
except together paid:true) + swarm blackboard seq 210 + CONVO mesh row to all seats.
Receipt: watch/ARC_SEED_DEFAULT_LANES_20260907.json · Dossier:
watch/ARC_SEED_DEFAULT_DOSSIER_20260907.md

## THE CONVERGENCE (unanimous where it matters)
All up chairs ruled the same architecture:
- **HOOK: knot-at-close** (`mag/knot_at_close.py`) — the seed compiles when a session
  closes (GRACE_H=2h), as an additive silent-fail step riding the existing knot. No new
  writer class, no per-N-turns (duplicate-order + one-steerer laws), no new cron.
- **BACKFILL: the night shift** (23/02/05, existing cadence) sweeps ended sessions
  missing seeds — catching seats that died without a close.
- **REFUSED by consensus:** biography-chain appends for arc roots (the chain is sacred,
  not ours to spam), new schedulers, live-session instrumentation.
groq/cerebras/openrouter/together/deepseek all named knot-at-close first; deepseek
proposed night-shift-primary for batch coverage — folded as both (close-time primary,
night catch-up).

## WHAT WAS IMPLEMENTED (landed before this fold was written)
1. `mag/arc_seed.py`: **redaction pass** (secrets law — key-shaped strings redacted
   from L1 forks) + **idempotent arc-root-addressed filenames** (re-running a close is
   a no-op; content-addressed CAS, kills the duplicate-seeding race).
2. `mag/knot_at_close.py`: **`_seed_session()` hook** — additive try/except, called
   after each successful backfill knot; **`--seed-sweep` mode** — the night-shift
   backfill pass (read-only, no chain writes).
3. Night-shift automation re-armed (step 3.5): the sweep runs at 23:00/02:00/05:00,
   counts ride the wire row.
4. **LIVE PROOF:** first sweep executed tonight — 505 ended sessions scanned, 0
   crashes, 0 seeded, 505 skipped-no-rollout. Silent-fail demonstrated on real data.

## THE HONEST BOUNDARY (discovered live, not assumed)
Vendor rollouts PRUNE — only live/recent sessions still have one (0/505 old sessions).
So the recovery guarantee is TIME-BOUNDED: a session seeded at close (or by the nightly
sweep while its rollout survives) gets the full 3-layer recovery; sessions whose
rollouts died before seeding degrade to knot-level recovery (title + first-message
excerpt + chain row). Next station (owed, not urgent): db part-table fallback in
_seed_session for post-prouting backfill — thought_bank_app already proved the part
table holds verbatim history to day one.

## RECOVERY PROTOCOL (the answer to "always have a recovery")
1. Seat dies → fresh seat reads the CONVO tail; finds `watch/arc_seeds/arc_seed_<sess>_<root>.md`.
2. States its next move BLIND (the falsifier as honesty gate — written before reading L2).
3. Reads L2 (committed artifacts), diffs stated-vs-committed; discrepancies = the
   recovery gap, named in the resume row.
4. CONVO row: `RECOVERED <session> from arc root <root>, gap: <none|list>`.
5. No seed (crash pre-close)? → knot-level resume + the nightly sweep seeds whatever
   rollout remains, marked PARTIAL.

## SURFACES (feed through what exists)
- **Carry the seed:** watch/arc_seeds/ (files — the durable record; idempotent names).
- **Carry pointers:** CONVO rows (root + path), room.jsonl events.
- **Dashboard:** Fleet Console visual deck gains an arc-seeds tile (owed, trivial).
- **Untouched:** biography verkle chain (no appends), live-session behavior (zero
  in-loop changes), provider spend ($0 default path).

## VERDICT
- "Default arc-seeding via knot-at-close + night backfill is safe to enable" — **SUPPORTED** (implemented + live-proven silent-fail same night).
- "Full-recovery coverage for ALL historical sessions" — **DISPUTED → bounded** (rollout pruning; db-fallback owed).
- **FALSIFIERS:** (F1) the replay test — fresh flash session given a seed states the original arc's next move, 2-of-3, this week, $0. (F2) 7 consecutive night sweeps with zero live-session errors and zero duplicate-seed collisions = no-breakage proven. (F3) one REAL recovery: kill a window mid-lane on purpose, resume from its seed, match the next move.
