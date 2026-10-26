#!/usr/bin/env python3
"""B2-359 probe 2: dynamic byte-still probes over the four production trees.

The B2-86 pattern: snapshot production bytes, run the suspect tests under the
repo venv, snapshot again, attribute every moved byte. Two tiers:

  bracket  : one full walk of memory/ logs/ queue/ watch/ (size+mtime) before
             the whole batch and after it, so no byte movement escapes the
             census even where the per-run subset is blind (memory/runs is
             47k files; walking it 46 times is not).
  per-run  : a high-signal subset walked before and after EACH pytest file
             run: memory/{training,improve,pile,burns,ledger,registry_state,
             seals,factory,skills,working}, top-level memory/*.json+md files,
             logs/, queue/, watch/inbox/burn_wave_20260926 (the lane's own
             board, cheap and shared). Diff -> sha256 + tail attribution for
             every changed/new file.

Ambient control: two subset walks 30s apart with NO test run measure the
concurrent-writer noise floor (B2-86 named autorun_cycle / fkb_failure as
standing background writers), so probe-time movement is attributable.

Append-marker attribution: every appended row is scanned for test markers
(test, pytest, tmp, fake, synthetic, PROBE, POISON, unit, stub).
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).parent
PY = ROOT / ".venv" / "Scripts" / "python.exe"

SUBSET_DIRS = [
    "memory/training", "memory/improve", "memory/pile", "memory/burns",
    "memory/ledger", "memory/registry_state", "memory/seals", "memory/factory",
    "memory/skills", "memory/working", "memory/steal", "logs", "queue",
    "watch/inbox/burn_wave_20260926", "state",
    "memory/runs/seat_registry_trail.jsonl", "memory/runs/seat_guard",
]
SUBSET_TOPFILES_PREFIXES = tuple(
    f"memory/{n}" for n in (
        "decisions_log.jsonl", "attention.md", "bonds_active.json",
        "bonds_active.md", "warm_state.json", "MEMORY.md", "handoff_state.json",
        "thread.json", "nervous_system.json", "nervous_system.md",
        "living_map.json", "policy.json", "steer_policy.json",
        "operator_inbox.json", "context_pack_latest.json",
        "context_pack_latest.md", "agent_preamble_latest.md",
        "MEMORY.md.bak-refix-20260907",
    )
)

MARKERS = ("test", "pytest", "tmp", "fake", "synthetic", "probe", "poison",
           "unit", "stub", "b2_359")


def snapshot(dirs):
    out = {}
    for rel in dirs:
        base = ROOT / rel
        if base.is_file():
            try:
                st = base.stat()
                out[rel.replace("\\", "/")] = (st.st_size, st.st_mtime_ns)
            except OSError:
                pass
            continue
        for dp, dn, fn in os.walk(base):
            dn[:] = [x for x in dn if x not in ("__pycache__",)]
            for f in fn:
                p = os.path.join(dp, f)
                try:
                    r = os.path.relpath(p, ROOT).replace("\\", "/")
                except ValueError:
                    continue  # NUL-mount / cross-drive entry cannot be a repo file
                try:
                    st = os.stat(p)
                    out[r] = (st.st_size, st.st_mtime_ns)
                except OSError:
                    pass
    return out


def full_snapshot():
    return snapshot(["memory", "logs", "queue", "watch"])


def diff(pre, post):
    changed, added, removed, touched = [], [], [], []
    for k, v in post.items():
        if k not in pre:
            added.append(k)
        elif v[0] != pre[k][0]:
            changed.append(k)
        elif v[1] != pre[k][1]:
            touched.append(k)
    for k in pre:
        if k not in post:
            removed.append(k)
    return {"changed": sorted(changed), "added": sorted(added),
            "removed": sorted(removed), "touched": sorted(touched)}


def sha_of(rel):
    h = hashlib.sha256()
    try:
        with open(ROOT / rel, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
        return h.hexdigest()[:16]
    except OSError:
        return None


def tail_marker_scan(rel, max_tail=20):
    """Read the file tail, count lines carrying a test marker."""
    p = ROOT / rel
    try:
        with open(p, "rb") as fh:
            fh.seek(0, os.SEEK_END)
            size = fh.tell()
            fh.seek(max(0, size - 262144))
            data = fh.read().decode("utf-8", errors="replace")
    except OSError:
        return {"marker_lines": 0, "sample": ""}
    lines = [l for l in data.splitlines() if l.strip()][-max_tail:]
    hits = [l for l in lines if any(m in l.lower() for m in MARKERS)]
    return {"marker_lines": len(hits), "sample": (hits[-1] if hits else lines[-1] if lines else "")[:220]}


def probe_file(test_rel, subset_dirs):
    pre = snapshot(subset_dirs)
    t0 = time.time()
    try:
        r = subprocess.run(
            [str(PY), "-m", "pytest", test_rel, "-q", "--no-header", "-x",
             "-p", "no:cacheprovider", "--rootdir", str(ROOT)],
            cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=300,
        )
        summary = (r.stdout or "").strip().splitlines()[-1] if (r.stdout or "").strip() else ""
        code = r.returncode
    except subprocess.TimeoutExpired:
        summary = "TIMEOUT 300s"
        code = -1
    dt = round(time.time() - t0, 1)
    post = snapshot(subset_dirs)
    d = diff(pre, post)
    detail = {}
    for k in d["changed"] + d["added"]:
        detail[k] = {"sha": sha_of(k), "kind": "new" if k in d["added"] else "size-changed",
                     **tail_marker_scan(k)}
    return {"file": test_rel, "exit": code, "secs": dt, "summary": summary,
            "diff": {k: v for k, v in d.items() if v}, "detail": detail}


def main():
    subset = SUBSET_DIRS + [p for p in SUBSET_TOPFILES_PREFIXES if (ROOT / p).exists()]
    report = {"started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "subset_dirs": subset, "ambient": {}, "runs": [], "bracket": {}}

    # ambient noise floor: 30s with no test run
    a0 = snapshot(subset)
    time.sleep(30)
    a1 = snapshot(subset)
    amb = diff(a0, a1)
    report["ambient"] = {k: v for k, v in amb.items() if v}
    for k in report["ambient"].get("changed", []) + report["ambient"].get("added", []):
        report["ambient"].setdefault("_detail", {})[k] = tail_marker_scan(k)
    print("ambient drift:", json.dumps({k: (len(v) if isinstance(v, list) else "detail")
                                        for k, v in report["ambient"].items()}))

    g_pre = full_snapshot()
    report["bracket"]["pre_files"] = len(g_pre)

    files = [l.strip() for l in (HERE / "B2_359_probe_filelist.txt").read_text().splitlines()
             if l.strip() and not l.startswith("#")]
    for f in files:
        res = probe_file(f, subset)
        report["runs"].append(res)
        dirty = bool(res["diff"].get("changed") or res["diff"].get("added")
                     or res["diff"].get("removed"))
        print(("DIRTY " if dirty else "still "), f, "|", res["summary"][:60], "|",
              json.dumps(res["diff"])[:220] if dirty else "")
        sys.stdout.flush()

    g_post = full_snapshot()
    report["bracket"]["post_files"] = len(g_post)
    gb = diff(g_pre, g_post)
    report["bracket"]["diff_counts"] = {k: len(v) for k, v in gb.items() if v}
    detail = {}
    for k in (gb["changed"] + gb["added"])[:80]:
        detail[k] = {"sha": sha_of(k), **tail_marker_scan(k, max_tail=5)}
    report["bracket"]["detail"] = detail
    print("bracket diff:", json.dumps(report["bracket"]["diff_counts"]))

    report["finished"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    out = HERE / "B2_359_byte_still_results.json"
    out.write_text(json.dumps(report, indent=1), encoding="utf-8")
    print("wrote", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
