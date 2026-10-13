"""arena_feed - the gwap->gps FEED MAP machinery (split from arena_gwap,
D10 landing 2026-10-05: the banking adapter had grown past the 400-line
ratchet fence, and feed-map concerns are a seam of their own).

The quarantine law moves with the code (unchanged bytes): a banked dir
later QUARANTINED under a staging root (scenarios_lane9/
void_stamp_collision_tavern_20261004T083959Z) orphaned its chain scenes
and the feed refused UNMAPPED_SCENE ~23h until the map resolved them.
Quarantined dirs are void as PLAY data but their chain rows exist: the
FEED MAP resolves them via their banked-id tag; the BANK walk stays
top-level-only so a quarantined run is never re-banked.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

PLAY_DIR = ROOT / "watch" / "inbox" / "playground"


def _ag():
    """Lazy import: arena_gwap imports this module for the back-compat
    surface, so a module-level import here would cycle."""
    from tools import arena_gwap

    return arena_gwap


def _quarantined_run_dirs() -> list[Path]:
    """Run dirs nested one level below PLAY_DIR under staging/quarantine roots."""
    out: list[Path] = []
    for root in PLAY_DIR.iterdir():
        if not root.is_dir() or (root / "transcript.jsonl").is_file():
            continue  # a run dir itself, not a staging/quarantine root
        for d in sorted(root.iterdir()):
            if d.is_dir() and (d / "transcript.jsonl").is_file():
                out.append(d)
    return out


def _original_run_name(d: Path) -> str | None:
    """The run name a quarantined dir carried when the chain banked it.

    Byte-backed, no convention parse of the quarantine rename: every paid
    tavern row's banked id embeds the run (BURN-ID law 2026-10-03,
    tools/tavern.py: tag = TAVERN_<kind>_<stamp>_r<round>_<actor>), so the
    prefix before the first _r<round> IS the original dir name. None when
    no tag parses: the feed then refuses rather than guess a routing key."""
    for r in _ag()._rows(d):
        tag = str(r.get("tag") or "")
        if tag.startswith("TAVERN_"):
            orig = tag.split("_r", 1)[0][len("TAVERN_"):]
            if orig:
                return orig
    return None


def _quarantine_scene_map(d: Path) -> dict[str, str]:
    """scene_id -> model for one quarantined dir, keyed by its ORIGINAL run
    name so the ids match the chain rows banked pre-quarantine."""
    orig = _original_run_name(d)
    if orig is None:
        return {}
    return {f"arena-{orig}-{actor}": model
            for actor, model, _payload in _ag().actor_payloads(d)}


def feed_scene_map() -> dict[str, str]:
    """scene_id -> model_id over every resolvable run dir on disk: top-level
    live dirs (banked or not) plus quarantined dirs under staging roots (keyed
    by their pre-quarantine run name, from the banked-id tag). The bridge
    walks the WHOLE ledger and refuses on any scene_id missing from the map
    (fail-closed, no guessed routing keys: UNMAPPED_SCENE)."""
    full_map: dict[str, str] = {}
    walk = [d for d in PLAY_DIR.iterdir()
            if d.is_dir() and (d / "transcript.jsonl").is_file()]
    for d in walk:
        for _actor, model, payload in _ag().actor_payloads(d):
            full_map[payload["scene_id"]] = model
    for d in _quarantined_run_dirs():
        full_map.update(_quarantine_scene_map(d))
    return full_map
