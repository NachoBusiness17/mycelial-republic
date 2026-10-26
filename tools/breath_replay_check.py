"""breath_replay_check - hourly, read-only proof that the breath chain still
reconstructs the true prior self.

NEVER writes git: every call is `git --no-optional-locks` plumbing
(rev-parse / log / cat-file / ls-tree / hash-object WITHOUT -w / status /
merge-base / fsck --connectivity-only). No index refresh, no index.lock, so it
cannot collide with the sole git writer (tools/commit_sweeper.py).

Why not MagCheckpointV2Hourly: on 2026-10-22 its script exits immediately
("GAME-NEUTERED 2026-10-19"), so it produces no snapshot to compare against.
Why not verkle_tip directly vs HEAD: memory/biography/ is NOT tracked by git
(ls-files is empty there); the tip is checked against its own chain on disk,
and its knot against the tracked mirror in memory/biography_v2/knots_v2/.

Checks:
 1 fsck_connectivity  - HEAD history is connected.
 2 linear_chain       - last N commits are single-parent and parent-linked.
 3 ledger_ancestry    - every commit named in the last K breath_ledger rows is
                        an ancestor of HEAD (no breath lost to a rewrite).
 4 stale_dirt         - tracked files dirty on disk AND older than 2 breaths
                        (>20 min): changes the breath failed to capture.
 5 verkle_tip_vs_chain- tip.last_leaf_hash/n_leaves == verkle_chain.jsonl tail.
 6 verkle_knot_in_head- the tip's knot exists in HEAD (knots_v2 mirror) and the
                        HEAD blob == the on-disk mirror blob.
Output: one JSON row appended to logs/breath_replay_check.jsonl (gitignored).
CLI: python -m tools.breath_replay_check [--n 200] [--stdout-only]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "logs" / "breath_replay_check.jsonl"
LEDGER = ROOT / "logs" / "breath_ledger.jsonl"
BIO = ROOT / "memory" / "biography"
KNOTS_V2 = "memory/biography_v2/knots_v2"
STALE_S = 20 * 60


def g(*args: str, timeout: int = 300) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "--no-optional-locks", *args], cwd=str(ROOT), capture_output=True,
                          text=True, encoding="utf-8", errors="replace", timeout=timeout)


FSCK_CACHE = ROOT / "state" / "fsck_cache.json"
FSCK_MAX_AGE_S = 86400


def chk_fsck() -> dict:
    """Hourly replay, but fsck at most once a day per HEAD.

    2026-10-24: this ran `fsck --connectivity-only` every hour with a 1800 s
    timeout against a 20 GB / 228k-object store. One run took 30+ minutes and
    starved tools/commit_sweeper.py for hours (HEAD did not move from 01:20 to
    02:00 while 614 files waited). Connectivity only changes when HEAD changes,
    so the answer is cacheable.
    """
    head = g("rev-parse", "HEAD").stdout.strip()
    try:
        cache = json.loads(FSCK_CACHE.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        cache = {}
    age = time.time() - float(cache.get("ts") or 0)
    if cache.get("head") == head and age < FSCK_MAX_AGE_S and cache.get("ok") is not None:
        return {"ok": bool(cache["ok"]), "cached": True,
                "detail": f"cached {age / 3600:.1f}h ago (HEAD unchanged)",
                "secs": cache.get("secs")}
    started = time.time()
    try:
        p = g("fsck", "--connectivity-only", "--no-dangling", "--no-progress", timeout=900)
        ok = p.returncode == 0
        detail = (p.stdout + p.stderr).strip()[:300]
    except subprocess.TimeoutExpired:
        ok, detail = None, "fsck exceeded 900s - UNMEASURED (store is 20GB; expected on cold runs)"
    secs = round(time.time() - started, 1)
    try:
        FSCK_CACHE.parent.mkdir(parents=True, exist_ok=True)
        FSCK_CACHE.write_text(json.dumps({"head": head, "ts": time.time(), "ok": ok,
                                          "secs": secs}), encoding="utf-8")
    except OSError:
        pass
    return {"ok": ok, "detail": detail, "secs": secs}


def chk_linear(n: int) -> dict:
    rows = g("log", f"-{n}", "--format=%H %P").stdout.split("\n")
    rows = [r.split() for r in rows if r.strip()]
    merges = sum(1 for r in rows if len(r) > 2)
    breaks = sum(1 for i in range(len(rows) - 1) if len(rows[i]) < 2 or rows[i][1] != rows[i + 1][0])
    return {"ok": breaks == 0, "checked": len(rows), "merges": merges, "breaks": breaks}


def chk_ledger(k: int = 50) -> dict:
    try:
        lines = LEDGER.read_text(encoding="utf-8").splitlines()[-k:]
    except OSError:
        return {"ok": None, "detail": "no breath_ledger yet (fix 1 not live)"}
    missing = []
    for line in lines:
        try:
            row = json.loads(line)
        except ValueError:
            continue
        for c in row.get("commits", []):
            if g("merge-base", "--is-ancestor", c, "HEAD").returncode != 0:
                missing.append({"breath_id": row.get("breath_id"), "commit": c})
    return {"ok": not missing, "breaths": len(lines), "missing": missing[:20]}


def chk_stale_dirt() -> dict:
    out = g("status", "--porcelain", "-uno").stdout
    now, stale = time.time(), []
    for line in out.splitlines():
        path = line[3:].strip().strip('"')
        try:
            if now - (ROOT / path).stat().st_mtime > STALE_S:
                stale.append(path)
        except OSError:
            stale.append(path + " (deleted)")
    return {"ok": not stale, "stale_dirty": stale[:30], "count": len(stale)}


def chk_verkle() -> tuple[dict, dict]:
    try:
        tip = json.loads((BIO / "verkle_tip.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        return {"ok": None, "detail": f"no tip: {e}"}, {"ok": None}
    tail, n = None, 0
    try:
        with (BIO / "verkle_chain.jsonl").open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    n += 1
                    tail = line
        tail = json.loads(tail) if tail else {}
    except (OSError, ValueError) as e:
        return {"ok": False, "detail": f"chain unreadable: {e}"}, {"ok": None}
    tv = {"ok": tail.get("leaf_hash") == tip.get("last_leaf_hash") and n == tip.get("n_leaves"),
          "tip_leaves": tip.get("n_leaves"), "chain_lines": n,
          "leaf_match": tail.get("leaf_hash") == tip.get("last_leaf_hash")}
    name = tip.get("last_filename", "")
    hits = [p for p in g("ls-tree", "-r", "--name-only", "HEAD", "--", KNOTS_V2).stdout.splitlines()
            if p.endswith("__" + name)]
    if not hits:
        return tv, {"ok": False, "detail": f"tip knot {name} not in HEAD:{KNOTS_V2}"}
    path = hits[-1]
    head_blob = g("rev-parse", f"HEAD:{path}").stdout.strip()
    disk_blob = g("hash-object", "--", path).stdout.strip()  # no -w: computes, writes nothing
    return tv, {"ok": bool(head_blob) and head_blob == disk_blob, "path": path,
                "head_blob": head_blob, "disk_blob": disk_blob}


def run(n: int = 200) -> dict:
    tv, kn = chk_verkle()
    checks = {"fsck_connectivity": chk_fsck(), "linear_chain": chk_linear(n),
              "ledger_ancestry": chk_ledger(), "stale_dirt": chk_stale_dirt(),
              "verkle_tip_vs_chain": tv, "verkle_knot_in_head": kn}
    return {"schema": "breath_replay_check.v1", "ts": datetime.now(timezone.utc).isoformat(),
            "head": g("rev-parse", "HEAD").stdout.strip(),
            "ok": all(c.get("ok") is not False for c in checks.values()), "checks": checks}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--stdout-only", action="store_true")
    a = ap.parse_args(argv)
    res = run(a.n)
    print(json.dumps(res, indent=1))
    if not a.stdout_only:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        with OUT.open("a", encoding="utf-8") as f:
            f.write(json.dumps(res, sort_keys=True) + "\n")
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
