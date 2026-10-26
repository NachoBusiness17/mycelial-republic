# AH4 — rib fixes: language-line conditionality, tip-derived knot, warm_rib script move (audit finding #15)

**2026-09-30 · owner seat: rib_cache/grok_warm_rib lane · status: LANDED (refire complete)**

## The finding (audit #15)

Three rot points in the rib surface:

1. `mag/rib_cache.FROZEN_RIB` carried `LANGUAGE: … This model's native tongue is
   Chinese` into EVERY lane it touched — a claim true for exactly one model family
   (z.ai GLM), false for grok/deepseek/llama lanes. Doctrine rot riding every call.
2. `mag/grok_warm_rib.py` hardcoded the standing knot id (`710745b79a0a149d`) and
   verkle root (`caec3c98c7625bda`) — stale by construction: the chain moves, frozen
   text does not. Proof this session: the tip moved TWICE during the fix itself
   (229144e1 → 7da93da0 → 1e0cd4e4, n_leaves 8646 → 8647).
3. `mag/_warm_rib.py` was a script named like a module: metered `rib_chat` call at
   IMPORT time + hardcoded absolute paths — any accidental `import mag._warm_rib`
   paid a metered call and only worked on one machine.

## What landed

**1. Language line — per-target, default OMIT** (`mag/rib_cache.py`)

- Doctrine bytes split into `_DOCTRINE_CORE` + `_LANGUAGE_LINE`;
  `FROZEN_RIB = _DOCTRINE_CORE + _LANGUAGE_LINE` stays byte-identical
  (sha256 `7ca50bdccea3731f748d95166cdd6947c2e48f53e413429dbf3d000adfec01d2`,
  still pinned in `tests/test_rib_freeze.py`).
- `is_chinese_native(model, lane)` — True for `glm*` models / `z_ai*` lanes.
- `frozen_rib(*, model, lane, chinese_native=None)` — returns full FROZEN_RIB for
  Chinese-native targets, `_DOCTRINE_CORE` (line OMITTED) for everyone else;
  explicit `chinese_native=` overrides detection. Per-target determinism keeps each
  lane's prefix byte-stable → cache-mining survives.
- `rib_chat()` now sends `frozen_rib(model=model, lane=lane)` — the line rides only
  z.ai GLM targets (interacts with AH17: `freeze_rib()` composes from
  `_DOCTRINE_CORE` and never carries the line).

**2. Tip-derived knot id** (`mag/grok_warm_rib.py`)

- `_verkle_tip()` reads `memory/biography/verkle_tip.json` at CALL time (missing/
  unreadable → `{}`); `_stone_line()` derives knot=`last_leaf_hash[:16]`,
  root=`root[:16]`; when the tip is unavailable the rib NAMES the gap rather than
  inventing ids. No hardcoded ids remain in the file.
- Byte-stability between tip moves preserved (that stability IS the cache hit);
  rib_bus content-hash dedup makes a moved tip republish as a new rib.
- **Store retirement (this session):** republished the rib (fold
  `2026-09-30_1225_rib-grok-cli_rib_bus__26ff9e48`, leaf 608ed6c5…, n_leaves 8647)
  and REMOVED the stale 2026-08-26 entry `9874f90696aacbd6` from
  `memory/rib_bus/grok_cli.json` (rib_bus has no retire API; surgical delete via its
  own `_load_store`/`_save_store`). `python -m mag.grok_warm_rib show` now serves
  ONLY the tip-derived stone line — verified no `710745b79a0a149d` in mounted ribs.

**3. Script move** (`mag/_warm_rib.py` → `scripts/warm_rib.py`)

- Old file deleted (was already gone from HEAD; worktree confirms absent).
- New script: everything under `main()` behind `__main__` guard, `--skip-warm` flag
  for zero metered calls, `ROOT = Path(__file__).resolve().parent.parent` (repo-root
  derived, no hardcode), imports inside functions (import is side-effect free).
- Importer sweep: `grep -rn "_warm_rib" --include=*.py` over mag/ harness/ scripts/
  tools/ tests/ main.py → only docstring mentions; no code importers to update.
- Byte-proof: `.venv\Scripts\python.exe scripts\warm_rib.py --skip-warm` →
  `RIB written -> queue\handoff\zcode\RIB.md, chars=3092 tokens_est=773`.

## Tests

`tests/test_ah4_rib_fixes.py` (13 tests): detection matrix, line-rides-native-only +
byte-pin `frozen_rib(glm)==FROZEN_RIB` / `frozen_rib(grok-4)==_DOCTRINE_CORE`,
rib_chat system capture per target (hold/lite_guard/provider monkeypatched), tip
derivation + tip-move tracking + no-stale-ids-when-missing + live-tip match,
script-moved + import-safe (no write, no metered call at import, ROOT == repo root).

```
.venv/Scripts/python.exe -m pytest tests/test_ah4_rib_fixes.py tests/test_rib_freeze.py -q
23 passed in 0.92s   (2026-09-30, this session, pre-retirement run; post-retirement rerun 23 passed)
```

## Load order pointer

`mag/rib_cache.py` · `mag/grok_warm_rib.py` · `scripts/warm_rib.py` ·
`tests/test_ah4_rib_fixes.py` · sibling: `AH17_FROZEN_RIB.md` (freeze_rib binding).
