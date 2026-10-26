"""B2-50: fold-exact diff. Replicates scripts/index_fold_host.mjs fold semantics
in Python and diffs the computed active set against INDEX.json and the disk."""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
INBOX = os.path.join(ROOT, "watch", "inbox")

OUTSIDE_RE = re.compile(
    r"^(mag|memory|queue|scripts|dashboard|docs|site|tests|models|backend|configs?|deploy|state|watch|research|corpus|dist_audit|attic|handoff|tools|bridge|harness|router|experiments|window|agents)/"
)


def norm(f):
    p = str(f or "").strip().replace("\\", "/").lstrip("/")
    p = re.sub(r"^(board|app)/inbox/", "", p)
    while p.startswith("inbox/"):
        p = p[6:]
    return p


def seqkey(e):
    s = e.get("seq")
    return (s, "") if isinstance(s, (int, float)) else (0, str(e.get("ts") or ""))


def main():
    raw = open(os.path.join(INBOX, "index_events.jsonl"), encoding="utf-8").read().splitlines()
    events, skipped = [], []
    for i, line in enumerate(raw):
        if not line.strip():
            continue
        try:
            ev = json.loads(line)
            if isinstance(ev.get("file"), str):
                ev["file"] = norm(ev["file"])
            ev["_outside"] = isinstance(ev.get("file"), str) and bool(OUTSIDE_RE.match(ev["file"]))
            events.append(ev)
        except Exception:
            skipped.append(i + 1)
    events.sort(key=seqkey)
    print(f"events={len(events)} malformed_lines={skipped}")

    active, seen, invalidated, outside = {}, set(), set(), []
    for ev in events:
        op = ev.get("op")
        f = ev.get("file")
        if op == "register":
            if not f:
                continue
            if ev.get("_outside"):
                outside.append(f)
                continue
            seen.add(f)
            active[f] = {
                "class": ev.get("class") or "UNPROVEN",
                "sha256": ev.get("sha256") or "",
                "seq": ev.get("seq"),
                "ts": ev.get("ts") or "",
            }
        elif op == "invalidate":
            invalidated.add(f)
            active.pop(f, None)

    with open(os.path.join(INBOX, "INDEX.json"), encoding="utf-8") as fh:
        idx = json.load(fh)
    idx_paths = {it["path"] for it in idx["items"]}

    computed = set(active)
    print(f"computed active={len(computed)}  INDEX items={len(idx_paths)}")
    print()
    print("=== A: in INDEX, NOT in computed fold (phantom items, next rebuild drops them) ===")
    for p in sorted(idx_paths - computed):
        print("  ", repr(p))
    print()
    print("=== B: in computed fold, NOT in INDEX (fold newer than INDEX) ===")
    for p in sorted(computed - idx_paths):
        print("  ", repr(p), active[p]["ts"])
    print()
    print("=== C: invalidate events whose target still active or in INDEX ===")
    for p in sorted(invalidated & (computed | idx_paths)):
        print("  ", repr(p))
    print()
    print("=== D: malformed events' files (untriaged log rows) ===")
    for ln in skipped:
        print("  line", ln, "->", raw[ln - 1][:160])
    print()
    on_disk = {
        n for n in os.listdir(INBOX)
        if os.path.isfile(os.path.join(INBOX, n))
        and n not in ("INDEX.json", "index_events.jsonl")
    }
    unreg = sorted(on_disk - computed)
    print(f"=== E: on-disk inbox files with NO active registration: {len(unreg)} ===")
    for p in unreg:
        mt = os.path.getmtime(os.path.join(INBOX, p))
        import datetime
        print(f"   {p}  mtime={datetime.datetime.fromtimestamp(mt).isoformat(timespec='minutes')}")


if __name__ == "__main__":
    main()
