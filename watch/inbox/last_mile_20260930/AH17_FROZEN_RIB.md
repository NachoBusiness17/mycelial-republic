# AH17 — FROZEN RIB now binds manifest + verkle tip (audit §2.2 gap closed, code side)

**2026-09-30 · owner seat: rib_cache lane · status: LANDED**

## The finding (audit §2.2)

AGENTS.md "Deliberate-ask" (L28) names the frozen RIB as
`system+bootloader+manifest+verkle tip`. `mag/rib_cache.FROZEN_RIB` was a hardcoded
doctrine-only string: no manifest sha, no verkle tip, no timestamp, no formula
reference. The formula was aspirational; the constant carried a quarter of it.

## What landed

`mag/rib_cache.py`:

- **`freeze_rib(manifest_path=None)`** composes the formula-named rib:
  1. doctrine text = the existing FROZEN_RIB body **minus the AH4-conditionalized
     LANGUAGE line** ("this model's native tongue is Chinese" is one model family's
     property, not fleet law; callers that need the language contract pass it in the
     ask/tail);
  2. a **BINDING BLOCK**: manifest sha (explicit path wins; else
     `state/manifest_anchor.json#manifest_hash`; else sha256 of
     `seed/MANIFEST.sha256`'s own bytes — both default locations probed), verkle tip
     root + n_leaves read fresh from `memory/biography/verkle_tip.json`, UTC freeze
     timestamp, and the AGENTS.md formula reference verbatim.
- **Cache**: `memory/runs/frozen_rib_cache.json` keyed by `(manifest_sha, tip_root)`,
  plus an in-process memo — first call composes and writes, every later call in the
  process is free (`cache: miss -> memory -> disk`); a fresh process hits the disk
  layer with the ORIGINAL frozen_at (honest: same binding = same freeze time).
- **Honest invalidation**: tip and manifest are re-read every call; a moved tip is a
  new key, so recomposition is automatic and the old binding survives on disk as
  history, never served as current. A corrupt cache file recomposes rather than
  serving garbage. Nothing to bind (no manifest, no tip) fails closed with a named
  error — the unbound rib is exactly the gap this closes; it does not ship.
- **Compat**: `FROZEN_RIB` is now `_DOCTRINE_CORE + _LANGUAGE_LINE` — byte-identical
  (sha256 `7ca50bdccea3731f748d95166cdd6947c2e48f53e413429dbf3d000adfec01d2`, 3092
  chars, verified before and after). Legacy callers (max_distill, invariant,
  seed_percolator, rib_chat, burst fallback) are untouched; new callers use
  `freeze_rib()`. CLI: `python -m mag.rib_cache freeze`.

## Evidence

- Byte-stability: hash computed from the pre-edit module, re-asserted post-edit and
  pinned as a test (`test_frozen_rib_bytes_are_pinned`) — the constant cannot drift
  silently again.
- Live tip-key proof during the landing session itself: the chain moved from
  root `c180e40c…` / 8645 leaves to `afcf940a…` / 8646 leaves between two reads;
  the second freeze took the miss path on the new key exactly as designed.
- First live composition: 3551 chars / ~887 tokens, manifest
  `111fc776cb9739f3f84421c56180c2f696f1a7c6fff5d79fe536eeba09df5ace`
  (source `state/manifest_anchor.json#manifest_hash`).

## Tests

`tests/test_rib_freeze.py` — 15 passed (composition carries all four parts; AH4 line
dropped; FROZEN_RIB pinned + split law; cache miss/memory/disk; corrupt-cache
recompose; tip-change recompose with history kept; anchor/seed/explicit manifest
sources; fail-closed paths). Consumer test files touching rib_cache/FROZEN_RIB/
max_distill/seed_percolator/rib_store: 22 passed across 3 files; invariant-family
consumer sweep recorded in the session log. Instrument: `pytest -q -p
no:cacheprovider`, venv `.venv/Scripts/python.exe`, moment 2026-09-30 ~12:10Z.

## Refire verification (audit 2.2 second pass, 2026-09-30 ~12:30Z)

Re-verified from the landed bytes, fresh instrument runs:

- `pytest -q -p no:cacheprovider tests/test_rib_freeze.py tests/test_ah4_rib_fixes.py`
  → **23 passed** (15 AH17 + 8 AH4). All required cases present: four parts, cache
  miss/memory/disk, tip-change recompose.
- Live `python -m mag.rib_cache freeze` → ok, 3551 chars / ~887 tok, manifest
  `111fc776…` (anchor source), tip `0f6e8dff…` / 8647 leaves. Second in-process call
  hit the memory layer; FROZEN_RIB sha256 still `7ca50bdc…` (pinned).
- **Live tip-move recompose proved again during verification itself**: the chain
  advanced `0f6e8dff…` → `038fbab3…` (8647 leaves) between the CLI call and a fresh
  process moments later; the fresh process took the miss path on the new key and the
  disk cache now holds 4 entries (one per binding ever frozen — history kept).
- Composes with AH4: freeze_rib() rides `_DOCTRINE_CORE` (language line omitted);
  `FROZEN_RIB = _DOCTRINE_CORE + _LANGUAGE_LINE` stays byte-pinned for compat.
- Rib files match HEAD — AH4+AH17 are committed, not working-tree drift.

**Flagged, NOT AH17's (outside this lane's file ownership):**
`tests/test_invariant.py::test_preamble_separates_stable_and_tail` FAILS pre-existing —
`mag/session_route.learned_block("fix a typo")` returns empty, so `invariant.tail()`
is empty and the delimiter never enters the preamble text. Supported by direct probe
(2026-09-30); the path never touches rib_cache. Owner: invariant/session_route lane.
