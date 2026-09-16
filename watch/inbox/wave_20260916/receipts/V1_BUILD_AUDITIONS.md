# V1_BUILD_AUDITIONS — independent re-run of tonight's lanes

- Date: 2026-09-16
- Auditor: fresh vantage, no shared state with building lanes
- Law: trust bytes, not reports. No git. No paid APIs. `.venv\Scripts\python.exe` + node only.
- Node: v22.23.1 (present)
- Python: repo venv `.venv\Scripts\python.exe`

## Status: AUDITIONS IN PROGRESS

Per-artifact results appended below as each audition lands. Final audition table at bottom.

## Audition 1 — tests/test_wow_bones_session.py

```
...........                                                              [100%]
11 passed in 0.23s
```
- Wall time: 3.24s (`real 0m3.236s`)
- Warnings: none.
- Verdict: GREEN.

## Audition 2 — tests/test_bones_adapter.py

```
.................                                                        [100%]
17 passed, 1 warning in 0.96s
```
- Wall time: 4.64s (`real 0m4.644s`)
- Warning decoded: `discord/player.py:30: DeprecationWarning: 'audioop' is deprecated and slated for removal in Python 3.13` — third-party (discord.py imports the stdlib `audioop` module at import time); not the artifact's code, no test impact.
- Verdict: GREEN.

## Audition 3 — tests/test_hydro_xor_sim.py

```
...............                                                          [100%]
15 passed in 0.37s
```
- Wall time: 3.26s (`real 0m3.263s`)
- Warnings: none.
- Verdict: GREEN.

## Audition 4 — tests/test_wow_player.py

```
.................                                                        [100%]
17 passed in 4.48s
```
- Wall time: 7.59s (`real 0m7.593s`)
- Warnings: none.
- Verdict: GREEN.

## Audition 5 — tests/test_link_library.py

```
........................                                                 [100%]
24 passed in 0.24s
```
- Wall time: 2.72s (`real 0m2.722s`)
- Warnings: none.
- Verdict: GREEN.

## Audition 6 — regression: test_wow_bones.py + test_wow_family.py + test_wow_manifest.py (one pytest invocation)

```
........................                                                 [100%]
24 passed in 5.48s
```
- Wall time: 8.62s (`real 0m8.618s`)
- Warnings: none.
- Verdict: GREEN.

## Audition 7 — scripts/test_toy.js (node v22.23.1)

```
PASS  1 A: toy compiles + window.TOY live + sha256 matches node:crypto
PASS  2 A: same seed + same tape twice -> identical event log (byte-identical JSON)
PASS  3 A: same seed + same tape twice -> identical receipt sha256
PASS  4 A: receipt sha256 is the hash of its own canonical body
PASS  5 A: batching-invariant — pump(3600) x1 == pump(60) x60 -> same sha
PASS  6 A: the verb actually fired (telegraph -> roll -> hit_dodged -> kill) and first telegraph < 3s
PASS  7 B: flipped input -> receipts diverge (sha differs, tape is load-bearing)
PASS  8 B: fork is named at the exact frame — first differing event is the flipped input
PASS  9 B: the verb fork — at the telegraph end, TAPE_A dodged the bite and TAPE_B ate it
PASS 10 C: P-LEGAL sweep on TAPE_A — harness recomputes: no hit without a rollable telegraph
PASS 11 C: P-LEGAL sweep on TAPE_C (facetank tape, same seed) — still no hit without a telegraph
PASS 12 C: divergence is legal play — same seed, different tape, different log, both P-LEGAL

12/12 lanes green
toy: 232 lines, seed 20260916, tape A sha 678ddd9d2e189555…, verdict win, duration 1.717s
```
- Exit code: 0. Wall time: 0.086s (`real 0m0.086s`).
- Warnings: none.
- Verdict: GREEN.

## Audition 8 — full wow family: `pytest tests -k wow -q`

**Run 1 (first independent re-run):**

```
FAILED tests/test_wow_world.py::test_wow_world_cli_start_turn_receipt - KeyEr...
1 failed, 63 passed, 1405 deselected, 2 warnings in 9.28s
```
- Wall time: 12.9s.
- Failure decoded: `mag/wow_world.py:310 in main` → `ap.parse_args(argv)` received a DICT
  (`{'draw_index': 0, 'encounter_state': 'TO_BE_DECIDED', 'ok': True, 'room': 'atrium', …}` —
  exactly the `start` receipt body shape) instead of an argv list → `argparse` `KeyError: 0`.
  `main(argv)` takes a list; only `tests/test_wow_world.py` calls it and always with a list.
  The traceback source line rendered as `???` = pytest could not re-read the source file →
  **the file changed under the running suite.**
- Root cause evidence: `mag/wow_world.py` and `tests/test_wow_world.py` were re-stamped
  **16:52** — DURING this audition window, and test_wow_world.py grew 7431 → 7445 bytes.
  A concurrent lane was live-editing the tree while I audited it. The isolated test passes
  alone (`1 passed in 0.23s`); no pytest-randomly installed; no tests/conftest.py.

**Runs 2-4 (after the 16:52 edits settled):**

```
64 passed, 1405 deselected, 2 warnings in 12.35s
64 passed, 1405 deselected, 2 warnings in 6.80s
64 passed, 1405 deselected, 2 warnings in 3.28s
```
- Warnings (both, all runs), decoded:
  1. `discord/player.py:30 DeprecationWarning: 'audioop' … Python 3.13` — third-party discord.py importing a stdlib module slated for removal; not artifact code.
  2. `fastapi/testclient.py:1 StarletteDeprecationWarning: Using httpx with starlette.testclient is deprecated; install httpx2` — third-party starlette/httpx advisory surfaced at import; not artifact code.
- Verdict: **first audition RED (1F/63P), then 3x GREEN post-edit.** Not a stable suite
  failure — an audit performed on a live-edited tree. Gen-2: never audit a moving tree;
  re-audit after freeze. Receipt W1 (filed 16:37) describes bytes that no longer exist
  (wow_world.py rewritten 16:52 after the receipt).

## Receipt-vs-bytes checks (3 receipts claiming file paths)

1. **toy.html** — claim (U1_UNION_TOY.md): `dashboard/static/games/toy.html`, 12,919 bytes,
   232 lines, sha256 head `ca4c18beebffdb56…`.
   Bytes: exists, **12,919 bytes exact**, sha256
   `ca4c18beebffdb56aa010dc7334a511656a42afd1d029595396020edc21d8bb4` — head MATCHES.
   Lines: 231 real lines (ends with newline); the "232" claim is a `split('\n')` counting
   artifact (231 newlines → 232 elements). Cosmetic; the sha is the load-bearing commitment.
   → **MATCH.**
2. **player ledger** — claim (W2_PLAYER_FILES.md): `mag/wow_player.py` +
   `tests/test_wow_player.py`, "17 falsifier tests, all green".
   Bytes: `mag/wow_player.py` 15,308 B @16:38, `tests/test_wow_player.py` 11,364 B @16:40
   — both mtimes PRECEDE the receipt (16:41), bytes frozen since. Audition 4: 17 passed.
   → **MATCH.**
3. **hydro sim** — claim: **NONE FOUND.** `mag/hydro_xor_sim.py` (13,119 B @16:11) and
   `tests/test_hydro_xor_sim.py` (5,056 B @16:12) exist and pass (15 passed, audition 3),
   but no receipt in wave_20260916 claims either file. Checked: all receipts, U6, G3.
   → **ORPHAN ARTIFACT — suite green but evidence trail missing.** Gen-2: file the claim.

Bonus (W1_WORLD_SKELETON.md): `mag/wow_world.py` exists (16,902 B) but was rewritten
16:52 — 15 min AFTER its receipt (16:37). The receipt's bytes are gone from disk.
→ **STALE-ON-ARRIVAL (superseded by the 16:52 edit).**

---

# AUDITION TABLE — claim vs bytes

| # | Artifact | Claimed | Auditioned (verbatim) | Wall | Claim=bytes? | Color |
|---|----------|---------|----------------------|------|--------------|-------|
| 1 | tests/test_wow_bones_session.py | green | `11 passed in 0.23s` | 3.24s | yes | GREEN |
| 2 | tests/test_bones_adapter.py | green | `17 passed, 1 warning in 0.96s` (discord audioop deprecation) | 4.64s | yes | GREEN |
| 3 | tests/test_hydro_xor_sim.py | green (implicit — no receipt claims it) | `15 passed in 0.37s` | 3.26s | suite yes; RECEIPT MISSING (orphan) | GREEN / evidence GAP |
| 4 | tests/test_wow_player.py | 17 green (W2) | `17 passed in 4.48s` | 7.59s | yes | GREEN |
| 5 | tests/test_link_library.py | green | `24 passed in 0.24s` | 2.72s | yes | GREEN |
| 6 | wow regression trio (bones/family/manifest) | green | `24 passed in 5.48s` | 8.62s | yes | GREEN |
| 7 | scripts/test_toy.js (node v22.23.1) | 12/12 green | `12/12 lanes green`, exit 0, tape A sha `678ddd9d…` | 0.09s | yes (toy.html sha head also matches) | GREEN |
| 8 | pytest tests -k wow -q | green | run1: `1 failed, 63 passed` (tree edited mid-run, wow_world CLI test); runs 2-4: `64 passed, 1405 deselected` x3 | 12.9s / 12.35 / 6.80 / 3.28s | unstable-at-audit; green post-edit | RED→GREEN (re-audit after freeze) |

## Gen-2 fix list (artifacts failing their own advertised audit)

1. **Audition 8 / wow family**: `test_wow_world_cli_start_turn_receipt` went red on the first
   independent run because `mag/wow_world.py` + `tests/test_wow_world.py` were being edited
   (16:52) while suites ran. Fix: freeze the tree before claiming/auditing; re-run
   `pytest tests -k wow -q` after freeze and file a fresh receipt for the NEW bytes
   (W1's receipt describes superseded bytes).
2. **Hydro sim evidence gap**: `mag/hydro_xor_sim.py` + `tests/test_hydro_xor_sim.py` are
   unclaimed — no receipt in wave_20260916 names them. File a receipt (artifact, path,
   sizes, 15-pass evidence) or the work is unfalsifiable.
3. Cosmetic: toy.html "232 lines" claim is a split-'\n' artifact; real count 231. Recount or
   state the method; sha256 commitment itself is exact and MATCHES.

Bottom line: 7 of 8 auditions byte-verified green against their receipts. The one red is
audit-time tree mutation, not a code regression — but it invalidates W1's receipt until the
frozen bytes are re-audited. No git commands used; no paid APIs; `.venv\Scripts\python.exe`
and node v22.23.1 only.
