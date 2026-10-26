# B2-279 2026-09-26 refold-stability falsifier over the PRODUCTION fold.
# Shape per the brief: refold the production log N times with a dummy append
# between, and any active item change dies. The dummy is a log-only note event
# (op "note", carries no state) with an exact decimal-string seq past 2^53,
# minted like the B2-40 scheme (quoted string so JSON.parse never quantizes
# it into the inexact double band). Notes are state-free markers, so any
# active-item or fold-warning diff between refolds is pure sort behavior.
#
# Usage (.venv python):
#   .venv/Scripts/python.exe B2_279_refold_falsifier.py before 3
#   .venv/Scripts/python.exe B2_279_refold_falsifier.py after 5
# Writes B2_279_refold_<phase>_results.json next to this script.
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
INBOX = ROOT / "watch" / "inbox"
EVENTS = INBOX / "index_events.jsonl"
INDEX = INBOX / "INDEX.json"
HOST = ROOT / "scripts" / "index_fold_host.mjs"


def run_rebuild():
    r = subprocess.run(
        ["node", str(HOST), "rebuild"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=180,
    )
    return r.returncode, r.stdout, r.stderr


def events_sha():
    return hashlib.sha256(EVENTS.read_bytes()).hexdigest().upper()


def snapshot():
    d = json.loads(INDEX.read_text(encoding="utf-8"))
    # derived_at and event_count move on every fold by design; the stability
    # claim is about the active item set and its canonical order.
    return {"items": d["items"], "fold_warnings": d.get("fold_warnings", [])}


def next_exact_seq():
    """Max parseable seq + 1, emitted as a decimal STRING past 2^53-1 so the
    fold sees it exact (the B2-40 emission law)."""
    lim = 2**53 - 1
    mx = 0
    for ln in EVENTS.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            ev = json.loads(ln)
        except ValueError:
            continue
        s = ev.get("seq")
        if isinstance(s, int) and s >= 0:
            mx = max(mx, s)
        elif isinstance(s, str) and s.isdigit():
            mx = max(mx, int(s))
    nxt = mx + 1
    return nxt if nxt <= lim else str(nxt)


def append_dummy(i):
    ev = {
        "seq": next_exact_seq(),
        "ts": __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc
        ).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "op": "note",
        "file": "burn_wave_20260926/QUEUE.md",
        "purpose": f"B2-279 refold-stability falsifier dummy note {i} (log-only marker, carries no state)",
        "writer": "b2-279-refold-falsifier",
    }
    with EVENTS.open("a", encoding="utf-8", newline="") as fh:
        fh.write(json.dumps(ev) + "\n")
    return ev


def main():
    phase = sys.argv[1] if len(sys.argv) > 1 else "after"
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    snaps = []
    steps = []
    for i in range(1, n + 1):
        pre_sha = events_sha()
        rc, out, err = run_rebuild()
        post_sha = events_sha()
        snap = snapshot()
        snaps.append(snap)
        steps.append(
            {
                "iter": i,
                "rebuild_rc": rc,
                "events_sha_before": pre_sha,
                "events_sha_after": post_sha,
                "concurrent_append_detected": pre_sha != post_sha,
                "items": len(snap["items"]),
            }
        )
        print(f"[{phase}] refold {i}: rc={rc} items={len(snap['items'])} "
              f"concurrent={pre_sha != post_sha}")
        if i < n:
            ev = append_dummy(i)
            print(f"[{phase}] dummy note appended seq={ev['seq']}")
    identical = all(snaps[0] == s for s in snaps[1:])
    # item-level diff detail for the first divergence, if any
    diff = None
    if not identical:
        for i, s in enumerate(snaps[1:], start=2):
            if s != snaps[0]:
                a = {it["path"]: json.dumps(it, sort_keys=True) for it in snaps[0]["items"]}
                b = {it["path"]: json.dumps(it, sort_keys=True) for it in s["items"]}
                diff = {
                    "first_divergent_refold": i,
                    "changed_or_added": sorted(
                        p for p in b if a.get(p) != b[p]
                    )[:20],
                    "removed": sorted(p for p in a if p not in b)[:20],
                    "order_changed": [it["path"] for it in snaps[0]["items"]]
                    != [it["path"] for it in s["items"]],
                }
                break
    result = {
        "phase": phase,
        "refolds": n,
        "active_items_stable": identical,
        "steps": steps,
        "diff": diff,
        "first_snapshot_paths": [it["path"] for it in snaps[0]["items"]],
        "first_snapshot_fold_warnings": snaps[0]["fold_warnings"],
    }
    out = Path(__file__).resolve().parent / f"B2_279_refold_{phase}_results.json"
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"[{phase}] ACTIVE ITEMS STABLE ACROSS {n} REFOLDS: {identical}")
    print(f"[{phase}] wrote {out}")
    return 0 if identical else 2


if __name__ == "__main__":
    sys.exit(main())
