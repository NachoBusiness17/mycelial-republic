---
name: epistemology-engine-v4
description: Grounding_wave v4 admission boundary BUILT (26 tests green) —
  write-time gates make row-122 bypass impossible; void/contest/witness/view
  verbs live; Amendment Obligation wired into tide cron; row 122+123 VOID staged
  awaiting operator signature + second seat
metadata:
  node_type: memory
  type: project
  originSessionId: sess_f8f2909b-0ac5-4763-abba-fbd8ba748f54
---

Grounding_wave v4 admission boundary BUILT 2026-09-16 — the epistemology engine's first executable stone (A2 design → code).

**What v4 adds over v3:**
- Write-time gates (G1 structural hash+chain, G2 source binding src_sha256_12, G3 warrant hashed into row) — row 122's bypass path (missing hash, no prev) is now physically impossible through any v4 writer
- `void` verb (reason_code enum MALFORMED|FORGED|EVIDENCE_DEAD|CONTEST_SUSTAINED; cross-signature required — named second seat)
- `contest` verb (CONTESTED + 7-day stale counter)
- `witness` verb (records g1/g2/g3_exit; SELF_SIGNED refusal)
- `view` verb (effective ledger: RECORDED → CORROBORATED → CONTESTED → VOID ladder)
- Ladder: RECORDED → CORROBORATED (≥2 distinct non-author witnesses, checks pass) → CONTESTED → VOID
- No migration: v1/v2/v3 rows hash byte-identically (test-pinned); live row 122 untouched until operator voids it

**Tests:** 26 new in test_grounding_wave_v4.py (all passing). Full suite: 65 passed, 2 pre-existing failures unrelated.

**Staged operator action:** void row 122 (MALFORMED — no hash, prev≠row 121) and row 123 (empty-prev unseeded SUPPORTED) + matching void for row 123's companion; then second seat appends witness rows; verify returns LINKAGE-PASS.

**Adopted from AdventureNLearn sibling lineage** (Hive Operating Floor pack, independently derived same constitution): Gate-0 default-skip lock with mandatory yes/no logging ("invisible skip is where capture hides"); claims table shape (state/basis/source/fetched_at/veto/lane/label) matching A2's row design; stranger-executable rebuild recipes as the cold-start witness standard.

**Amendment Obligation wired into tide cron** (automation-b0ebbbb9, daily 06:15): every cycle must propose ≥1 amendment to a fleet rule appended to state/fuel/amendments.jsonl with falsifier; a tide with no amendment must name the rule examined and why it stands. First seed row = the obligation itself. CG4 mesh salon source (operator: "steal it").
