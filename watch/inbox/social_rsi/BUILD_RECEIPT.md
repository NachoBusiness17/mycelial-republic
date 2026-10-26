# SOCIAL RSI v0 BUILD RECEIPT - 2026-10-04

Free-lane ($0) build, seat: zcode GLM-5.3 day window. Ask: automate the
operator's manual "Recursive Social Improvement" recipe (his words: "I
do this manually, but it would actually be awesome to do it
autonomously!") per watch/inbox/X_INTEL_PAPERS_20261004.md section 6.
WIRED-ORGAN constraint held: NO new database, NO new store - the tool
is a query + packet surface over ledgers that already exist (lane
trails, logs/failure_kb.jsonl, watch/inbox receipts).

## What landed

- `tools/social_rsi.py` v0 - deterministic, stdlib-only (the only
  non-stdlib reach is `mag.lane_runner.normalize_detail`, reused so the
  cross-lane roll-up keys classes identically to the per-lane
  CLUSTER_REPORTs; a simple-tokenizer fallback stands in if that import
  is unreachable). CLI: `--check` (roll-up table, stdout only, writes
  nothing), `--packets`, `--top N` (default 5), `--days N` (default 14),
  `--root` (tests point it at tmp trees). Zero em-dashes in any byte it
  emits (quoted trail details are scrubbed; asserted in tests).
- `tests/test_social_rsi.py` - 7 tests, tmp-path fake mag roots (fake
  lanes/trails incl. one green-CYCLE before/after pair + one FIX-family
  pair + one no-pair lane, a windowed/out-of-window failure_kb row, an
  inbox receipt hit and miss). Count assertions are normalizer-arm-
  independent (identical raw details share a bucket in any arm).
- 3 synthesis packets written to `watch/inbox/social_rsi/` (paths
  below), each carrying: the instrument-named pattern, before/after
  evidence pairs, receipt citations, the SYNTHESIS ASK (five card rules
  per watch/inbox/IMAGE_BLASTER_GO_20261003.md, template
  .agents/skills/image-blast/SKILL.md), and the promote-gate footer:
  drafting the card is a separate seated step BY DESIGN, the commit
  stays human (`mag.cmd promote --apply`).

## What fired (live tree, instruments named)

Test instrument: `.venv\Scripts\python.exe -m pytest tests/test_social_rsi.py
-q -p no:cacheprovider` -> **7 passed** in every run (0.72-1.40s across
three runs, moments 2026-10-04T10:44Z-10:47Z).

Roll-up instrument: `.venv\Scripts\python.exe tools/social_rsi.py
--check`, moment 2026-10-04T10:48:03Z, window 14d, keying
mag.lane_runner.normalize_detail, 12 trails / 7,921 rows scanned / 0
malformed / 0 unusable ts, 17,841 windowed failure_kb rows joined:

| rank | count | class | first | last | lanes | fkb |
|---|---|---|---|---|---|---|
| 1 | 825 | exc oserror errno invalid argument | 2026-09-25 | 2026-10-04 | research(454), builder(344), night(26), prose(1) | 0 |
| 2 | 14 | lane-down http error too many requests | 2026-09-20 | 2026-10-03 | elder(14) | 0 |
| 3 | 10 | exc httperror http error too many | 2026-09-21 | 2026-10-02 | harvest(10) | 0 |
| 4 | 1 | 404 | 2026-10-04 | 2026-10-04 | elder(1) | 0 |
| 5 | 1 | lane-down invalid header value b bearer | 2026-10-04 | 2026-10-04 | elder(1) | 0 |

Read of the live numbers: the errno-22 OSError storm is 96.9% of all
windowed lane-cycle failures (825 of 851) across 4 lanes, first seen
2026-09-25, still failing at 10:15Z today (the moving tree grew 7,919
rows at the 10:45:20Z run to 7,921 at the 10:48:03Z run, about three
minutes apart). The failure_kb join is honestly 0 for every pattern:
the KB's 17,841 windowed rows are seat/session failures (tool_fail,
swarm_health, guard_registry classes) - the lane-cage errno-22 storm is
NOT in it, which is itself new evidence (each packet says so).

Packet instrument: `.venv\Scripts\python.exe tools/social_rsi.py
--packets --top 3` (2026-10-04T10:47Z), wrote:

1. `watch/inbox/social_rsi/packet_exc-oserror-errno-invalid-argument_2026-10-04.md`
   - pairs: builder CYCLE_FAIL 2026-10-04T09:45:33Z -> CYCLE (+63s);
   night 2026-10-03T23:08:04Z -> CYCLE (+171s). research (454 fails)
   has NO pair: its storm was still failing at packet time, no green
   row after - honest absence, named in the packet.
   - receipts: watch/inbox/MIGRATION_CLEANUP_20260919.md,
   watch/inbox/audit_20260926/LANE2_DOGFOOD_TOOLS.md,
   watch/inbox/audit_20260926/WAVE2_LANE2_PUSH_BLOCKERS.md
2. `watch/inbox/social_rsi/packet_lane-down-http-error-too-many-requests_2026-10-04.md`
   - pair: elder 2026-10-03T12:00:10Z -> CYCLE (+73,230s); receipts:
   burn_reset_20260927/flash50/deep-legibility.md, fillball/elder-salvage.md,
   frontier_olm_2026-10-03/DIGEST.md
3. `watch/inbox/social_rsi/packet_exc-httperror-http-error-too-many_2026-10-04.md`
   - pair: harvest 2026-10-02T06:30:27Z -> CYCLE (+86,394s); receipts:
   FREE_LANE_INTEL_BONSAI2_20260923.md, GAMING_CORPUS_PASS_20260923.md,
   STIGMERGY_WITNESS_SCAFFOLD_20260913.md

Receipt-scan bounds (deterministic, named because watch/inbox is 6.3G /
4,899 md files): top-level *.md sorted first, then subdirs sorted, per
file cap 1MB, total scan cap 48MB.

## Design notes (why the shape is what it is)

- Step 3 is a PACKET, not a card: the ractor50 verdict ("waves are the
  fuzzer, cards are the commits") and the skill census law keep the
  commit human - `mag.cmd promote --apply`. The packet footer writes
  that contract into every deliverable.
- The receipt grep is needle-based (longest tokens of the class key,
  2+ hits to match) - deterministic and cheap; ranked by hits desc then
  path asc, capped 3 per pattern.
- FIX-family rows are event names containing "FIX" (the live tree's
  only instance is LEASE_LAW_FIX_APPLIED); green evidence is a plain
  CYCLE row strictly after the lane's last fail of the class.
- Same-day reruns overwrite the same packet filename (a refresh, not a
  new artifact); packet slugs are capped 40 chars of the class key.

## Owed next (not this build)

- A seated step drafts the three cards from the packets (free lane or
  next window), then the operator promotes.
- The falsifier per section 6: a session with the drafted card active
  fails less on that class than without, measurable by arena/gwap.
- The errno-22 storm itself wants a root-cause fix (a malformed
  /app/... path in the cage runner), independent of the skill loop.

No commits made (per ask). No paid organs fired. Runtime environment:
.venv\Scripts\python.exe only (Python 3.11.15), stdlib + existing mag
imports, no network.
