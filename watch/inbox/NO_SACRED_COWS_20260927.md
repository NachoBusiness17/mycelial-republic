# NO-SACRED-COWS EXECUTION — 2026-09-27 (operator: "these were all the best ideas we had at the time")

The Socratic tease-out's asks, executed on that grant. Rules are
best-ideas-at-the-time, revisable; nothing gated on ceremony survived the day.

## 1. The daemon recycle — DONE, empirically proven

Killed the two stale chain writers (ghost loop from 09:04, autorun loop from
12:52 — both loaded pre-guard verkle_knot) and relaunched headless on the
repo venv via scripts/run_{ghost,autorun}_loop.py (launcher scripts carry
the root bootstrap; inline -c launches failed on quoting — receipts in the
transcript). Arm C-200 untouched per the handoff. Duplicate ghost (uv-python
twin) killed; one of each loop alive.
**Proof the race is dead: 25 chain rows landed post-restart (7,981 → 8,006
leaves) with ZERO breaks**, under live ghost+autorun cycling. The
order-pollution memlang failures are GONE (green in the batch run that
previously poisoned them).

## 2. The chain-equivalence (ablation-with-rollback) — EXECUTED on GROUNDING_WAVE

The 09-16 staging (operator word + named second seat) executed via the v4
verbs themselves — delete-as-append, cross-signed with the operator's own
word as the witness authority (seat "operator", evidence field carries the
verbatim GO; zcode posted on that authority, provenance transparent):

- `void #122 MALFORMED` — the truncated row frozen since 09-16 + witness.
- `void #123 MALFORMED` — the orphan behind it, per the original staging.
- `void #104 EVIDENCE_DEAD` — **MISFIRE, caught and reversed**: the test's
  failure message prints 0-based indices; the dead pointer lived on 1-based
  #105, not #104 (fish schooling — innocent). Reversed through the DESIGNED
  void-of-void path (`SUPERSEDED`, witnessed) — the reversal mechanism's
  first live fire, and it worked.
- `void #105 EVIDENCE_DEAD` — the real culprit (operator-screenshot receipt
  row naming privlidge_school_receipt_20260913.png, never on disk; siblings
  privlidge_ERROR_receipt_20260913.png exist) + witness.

Tests updated to the v4 reader law (walk only LIVE rows per _admission +
_live_claim; prev linkage honors _reanchor_ok) — the tests predated v4.
**tests/test_falsifier_ledger.py 3/3 green, no xfail marks left.**

## 3. The salvage split — structural half dispatched

Lane running: attic orphan census by shape (tar -tf tables of contents
only, no extraction; the encrypted ESSENTIALS pack recorded
OUT-OF-SCOPE) → watch/inbox/lens_20260927/ATTIC_ORPHAN_CENSUS.md.
Valued-orphan judgment stays with the operator, per the split.

## Suite score at close (vs the morning's honest 40F)

**28 fixed outright, 0 xfails, 12 remain**: desk_baseline_probe 6 (dashboard
spec reconciliation) + 6 singles (all_seat_interaction, healthz breach-503,
mirror_intro markup, no_win reframe, pack_modes build-excerpt,
substrate_identity fixture path). New this pass: falsifier_ledger 2 (the
ablation), memlang order-pollution 4 (the restart), wave_driver 1,
supervision_soak, ghost_spooky, loop_death_guards (the chain health).
