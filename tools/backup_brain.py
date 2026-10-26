#!/usr/bin/env python3
"""backup_brain.py — the orchestration drill for the April vision (2026-10-18).

Operator source (X @NachoQuixotic, the blackout post): the internet dies, the
pocket device keeps thinking on a local quantized model anchored to the
personal archive, tasks queue offline, and on reconnection the whole system
gets smarter together. The estate owns most organs; what was missing is THE
ORCHESTRATION LEVEL — the thing that knows the pieces fit and proves the loop
runs. This is that level, v0: it audits the mosaic (no sacred cows — every
organ is byte-checked, handwaved paths are named MISSING) and drills the two
states that matter:

  inventory            every loop organ: EXISTS / MISSING, with ages and tips
  drill --severed      the blackout drill: LOCAL ONLY — local-model probe (via
                       the mag.ollama_policy organ, which owns the daemon
                       boundary), chain tip read, WAL queue import, zero WAN
  drill --reconnect    the reconnection drill: git state, corpus FTS freshness,
                       served-field age (best effort)
  report               markdown crosswalk (vision row -> organ -> verdict)

Design law: drills never mutate live estate state (the severed drill writes
its own ledger, opens nothing for write, never enqueues); a drill that could
break the thing it drills is not a drill. Network boundary: this module makes
no HTTP calls of its own — local-inference probing is delegated to
mag.ollama_policy, the existing organ that owns the daemon boundary. Receipt:
watch/inbox/BACKUP_BRAIN_ORCHESTRATION_20261018.md
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

DRILL_LOG = ROOT / "logs" / "backup_brain_drill.jsonl"

# The loop's organs, byte-audited. role: which beat of the blackout loop.
# kind: file | dir; a None path with kind "missing" is a named gap.
INVENTORY = [
    # INFERENCE (local quantized, offline)
    ("inference", "local ollama battery", str(ROOT / "mag" / "ollama_policy.py"), "file",
     "local quantized inference policy; owns the daemon boundary"),
    # MEMORY (the personal archive: knows your way of thinking)
    ("memory", "verkle lattice", str(ROOT / "mag" / "bintree_v2.py"), "file",
     "bintree v2 — the chain the archive hangs from"),
    ("memory", "checkpoints", str(ROOT / "memory" / "biography_v2" / "checkpoints_v2.jsonl"), "file",
     "append-only checkpoint chain (frozen leaves; the north pole)"),
    ("memory", "person models", str(ROOT / "state" / "palace"), "dir",
     "OCEAN person-models: knows your way of thinking"),
    ("memory", "rib vault", str(ROOT / "memory" / "rib"), "dir",
     "law packs: the estate's committed intentions"),
    ("memory", "tesuji corpus", str(ROOT / "corpus" / "steal"), "dir",
     "pattern-breaks harvested under constraint (the April tesuji mine)"),
    ("memory", "tesuji intake cards", str(ROOT / "watch" / "inbox"), "dir",
     "TESUJI_* cards live here (6 as of 2026-10-18)"),
    # QUEUE (offline task queue)
    ("queue", "WAL task queue", str(ROOT / "mag" / "wal_queue.py"), "file",
     "SQLite WAL queue: leases, dead-PID reaper, hypothesis dedup"),
    ("queue", "SEVERED-mode consumer", None, "missing",
     "MISSING: no offline_queue consumer runs the WAL without network (v1 build)"),
    # SYNC (reconnection)
    ("sync", "body router", str(ROOT / "mesh_router.py"), "file",
     "routes tasks to phones/bodies via pocket_mcp; battery/RAM gates"),
    ("sync", "corpus FTS index", str(ROOT / "tools" / "corpus_fts_rebuild.py"), "file",
     "FTS5 freshness via --check (exit 2 = stale, rebuild through one writer)"),
    ("sync", "knot proof CLI", None, "missing",
     "MISSING: verify_knot_v2 consistency-proof CLI named in the manifesto card "
     "does not exist (the proofs live in bintree_v2 internals, no CLI)"),
    # SETTLEMENT (the rail)
    ("settlement", "GSTD drain", str(ROOT / "tools" / "gstd_drain.py"), "file",
     "greed-law drain to the GSTD rail (v8 relay live per memory)"),
    ("settlement", "GSTD beacon", str(ROOT / "tools" / "gstd_beacon.py"), "file",
     "wallet-as-node beacon organ"),
    ("settlement", "tails settlement ledger", None, "missing",
     "MISSING: the manifesto card's tails.jsonl settlement ledger does not exist "
     "(watch/steer_field/TAILS.md is steer tails, a different organ)"),
    ("settlement", "gold anchor", None, "missing",
     "MISSING: no gold-buyback organ exists anywhere in mag/ or tools/ "
     "(the April post's auto-gold anchor is currently prose, not code)"),
    # FACE (the orchestration's surface)
    ("face", "the Room", str(ROOT / "dashboard" / "static" / "room.html"), "file",
     "what was worked on, when, what exists (v0 reads; v1 write path owed)"),
    ("face", "the Globe", str(ROOT / "dashboard" / "static" / "smith_globe.html"), "file",
     "the estate on the 3D smith chart; frozen leaves at the north pole"),
    ("face", "the Vislab", str(ROOT / "dashboard" / "static" / "vislab.html"), "file",
     "the exhibit floor: every organ navigable, honesty chips"),
]


def _age_days(p: Path) -> float:
    try:
        return round((time.time() - p.stat().st_mtime) / 86400.0, 2)
    except OSError:
        return -1.0


def inventory() -> list[dict]:
    rows = []
    for role, name, path, kind, note in INVENTORY:
        if kind == "missing":
            rows.append({"role": role, "name": name, "status": "MISSING", "note": note})
            continue
        p = Path(path)
        ok = p.exists() and (p.is_dir() if kind == "dir" else p.is_file())
        rows.append({
            "role": role, "name": name, "status": "EXISTS" if ok else "MISSING",
            "path": str(p), "age_days": _age_days(p), "note": note,
        })
    return rows


def chain_tip() -> dict:
    """Read the checkpoint chain tip (read-only)."""
    cp = ROOT / "memory" / "biography_v2" / "checkpoints_v2.jsonl"
    try:
        last = cp.read_text(encoding="utf-8", errors="ignore").strip().splitlines()[-1]
        row = json.loads(last)
        return {"tip": row.get("chain_id", "?")[:16], "n_new": row.get("extends_proof", {}).get("n_new")}
    except (OSError, IndexError, json.JSONDecodeError):
        return {"tip": None, "n_new": None}


def local_brain_probe(timeout: float = 3.0) -> dict:
    """Local-only: can the pocket brain think right now?
    Delegates to mag.ollama_policy.list_tags — the organ that owns the daemon
    boundary. This module opens no sockets of its own."""
    out = {"ollama": "DOWN", "models": []}
    try:
        import mag.ollama_policy as op
        tags = op.list_tags(timeout=timeout)
        models = sorted(tags.keys())[:8]
        out.update({"ollama": "UP" if models else "EMPTY", "models": models})
    except Exception as e:  # a probe failure IS a finding; recorded, not silent
        out["error"] = repr(e)[:120]
    return out


def wal_openable() -> bool:
    """Read-only proof the WAL queue imports (never enqueues — drill law)."""
    try:
        import mag.wal_queue as wq  # noqa: F401
        return True
    except Exception as e:  # import failure is a drill finding, recorded
        _log({"drill": "wal_openable", "error": repr(e)[:120]})
        return False


def drill_severed() -> dict:
    """The blackout drill. LOCAL ONLY by design: no WAN touches."""
    tip = chain_tip()
    res = {
        "drill": "severed",
        "ts": dt.datetime.now(dt.timezone.utc).isoformat(),
        "brain": local_brain_probe(),
        "chain_tip": tip["tip"],
        "n_blocks": tip["n_new"],
        "wal_openable": wal_openable(),
        "network": "NONE (by design)",
    }
    res["verdict"] = ("THINKING" if res["brain"]["ollama"] == "UP" and res["wal_openable"]
                      else "IMPAIRED: " + ("no local model" if res["brain"]["ollama"] != "UP" else "WAL unopenable"))
    _log(res)
    return res


def drill_reconnect() -> dict:
    """The reconnection drill: which resync surfaces are fresh?"""
    res = {"drill": "reconnect", "ts": dt.datetime.now(dt.timezone.utc).isoformat()}
    try:
        g = subprocess.run(["git", "log", "-1", "--format=%h %cI"], cwd=ROOT,
                           capture_output=True, text=True, timeout=15)
        res["git_tip"] = g.stdout.strip()[:40]
        st = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT,
                            capture_output=True, text=True, timeout=15)
        res["dirty_files"] = len(st.stdout.strip().splitlines())
    except (OSError, subprocess.TimeoutExpired):
        res["git_tip"] = None
    try:
        fts = subprocess.run([sys.executable, str(ROOT / "tools" / "corpus_fts_rebuild.py"), "--check"],
                             cwd=ROOT, capture_output=True, text=True, timeout=120)
        res["fts_fresh"] = fts.returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        res["fts_fresh"] = None
    field = ROOT / "dashboard" / "static" / "steer_field" / "FIELD.json"
    res["field_age_days"] = _age_days(field)
    res["verdict"] = ("RESYNC-READY" if res.get("fts_fresh") and (res.get("field_age_days") or 99) < 2
                      else "RESYNC-LAGGING (stale surface named above)")
    _log(res)
    return res


def _log(res: dict) -> None:
    try:
        DRILL_LOG.parent.mkdir(parents=True, exist_ok=True)
        with DRILL_LOG.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(res, ensure_ascii=False) + "\n")
    except OSError:
        pass


def report_md() -> str:
    rows = inventory()
    missing = [r for r in rows if r["status"] == "MISSING"]
    lines = ["# BACKUP BRAIN — live crosswalk", "",
             "The April loop, byte-audited at " + dt.datetime.now(dt.timezone.utc).isoformat(), ""]
    for role in sorted({r["role"] for r in rows}):
        lines.append("## " + role)
        for r in rows:
            if r["role"] != role:
                continue
            mark = "EXISTS" if r["status"] == "EXISTS" else "**MISSING**"
            age = (" (age " + str(r["age_days"]) + "d)") if r.get("age_days") is not None and r["age_days"] >= 0 else ""
            lines.append(f"- {mark} — {r['name']}: {r['note']}{age}")
        lines.append("")
    lines.append(f"**{len(missing)} missing organs** — each one is a named build, not a hope.")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="backup brain orchestration drill")
    ap.add_argument("cmd", choices=["inventory", "drill", "report"])
    ap.add_argument("--severed", action="store_true", help="blackout drill (local only)")
    ap.add_argument("--reconnect", action="store_true", help="resync drill")
    ap.add_argument("--json", action="store_true", help="machine output")
    a = ap.parse_args()
    if a.cmd == "inventory":
        rows = inventory()
        if a.json:
            print(json.dumps(rows, indent=1))
        else:
            for r in rows:
                print(f"{r['status']:>7}  [{r['role']:<10}] {r['name']} — {r['note']}")
        return 0
    if a.cmd == "drill":
        outs = []
        if a.severed:
            outs.append(drill_severed())
        if a.reconnect:
            outs.append(drill_reconnect())
        if not outs:
            ap.error("pick --severed and/or --reconnect")
        print(json.dumps(outs, indent=1))
        return 0
    print(report_md())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
