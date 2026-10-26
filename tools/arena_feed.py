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

The arena CADENCE CENSUS lives here too (GAP_REGISTER 2026-10-10 R2 fill,
2026-10-10: the R2 fold grew arena_gwap past the 400-line fence again, and
the census is a read-only instrument over the harness's own sqlite, the
same status-feed seam): automation_runs fire rows so dawn cadence
receipts carry FAILED fires as rows, never a bare cycle count.
"""
from __future__ import annotations

import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mag.gwap_payload import utc_now_iso  # noqa: E402

PLAY_DIR = ROOT / "watch" / "inbox" / "playground"

# The arena cron's automation id (hourly dungeon + tavern + gwap bank, $25
# daily cap). The automations row itself is DELETED from the index (byte-read
# 2026-10-10: zero rows for this id; GAP_REGISTER 2026-10-10 R7 names deletion,
# not the cap gate, as what ended the overspend), so the id lives here as the
# census key - automation_runs keeps the full fire history it fired.
ARENA_AUTOMATION_ID = "automation-b1ce1342-e449-4b33-b041-f8fbf4f69b0c"
TASKS_INDEX = Path.home() / ".zcode" / "v2" / "tasks-index.sqlite"


def cadence_census() -> list[str]:
    """The arena cron's fire census from automation_runs - failure rows,
    not just counts (GAP_REGISTER 2026-10-10 R2, filled 2026-10-10).

    Cause: the parable's "8 cycles" verse (parable_day_one_20261003.md line 9)
    was byte-true as a fire count at filing but hid that the FIRST fire
    (2026-10-03T13:00Z) failed and that the 20:00Z fire ran three dungeon
    sessions post-cap-crossing; a count cannot carry a failure, a row can.
    Every non-succeeded fire prints as its own FAIL row; the census line
    carries counts + span + the AS-OF moment. Fail-open HONEST-GAP when the
    index is absent or unreadable (never guessed, never skipped silently).
    """
    if not TASKS_INDEX.is_file():
        return [f"ARENA CADENCE: HONEST-GAP - {TASKS_INDEX} absent at this read"]
    try:
        con = sqlite3.connect(f"file:{TASKS_INDEX}?mode=ro", uri=True)
        try:
            fires = [dict(zip(("run_id", "scheduled_at", "outcome", "error"), row))
                     for row in con.execute(
                         "select run_id, scheduled_at, outcome, error "
                         "from automation_runs where automation_id = ? "
                         "order by scheduled_at", (ARENA_AUTOMATION_ID,))]
            live = con.execute(
                "select 1 from automations where automation_id = ?",
                (ARENA_AUTOMATION_ID,)).fetchall()
        finally:
            con.close()
    except sqlite3.Error as exc:
        return [f"ARENA CADENCE: HONEST-GAP - sqlite unreadable: {exc}"]

    def _ts(v) -> str:
        if not v:
            return "?"
        return datetime.fromtimestamp(v / 1000, timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ")

    out = [f"ARENA CADENCE AS-OF {utc_now_iso()} "
           f"({ARENA_AUTOMATION_ID[:26]}, automation_runs census)"]
    if not fires:
        return out + ["fires=0 (no rows for this automation at this read)"]
    failed = [f for f in fires if f["outcome"] != "succeeded"]
    out.append(
        f"fires={len(fires)} span={_ts(fires[0]['scheduled_at'])}"
        f"..{_ts(fires[-1]['scheduled_at'])} "
        f"succeeded={len(fires) - len(failed)} failed={len(failed)} "
        f"automation_row={'LIVE' if live else 'DELETED'}")
    for f in failed:
        out.append(f"FAIL sched={_ts(f['scheduled_at'])} outcome={f['outcome']} "
                   f"run={f['run_id']} err={f['error']}")
    if not failed:
        out.append("FAIL (none): zero failed fires at this read")
    return out


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
