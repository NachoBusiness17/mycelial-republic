"""B2-50: diff watch/inbox/INDEX.json vs watch/inbox/index_events.jsonl.

Finds files referenced on one side but not the other. The fold script's own
normalizer (scripts/index_fold_host.mjs normInboxFile) is mirrored here.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
INBOX = os.path.join(ROOT, "watch", "inbox")


def norm(f):
    p = str(f or "").strip().replace("\\", "/")
    p = p.lstrip("/")
    for pre in ("board/inbox/", "app/inbox/"):
        if p.startswith(pre):
            p = p[len(pre):]
    while p.startswith("inbox/"):
        p = p[6:]
    return p


def main():
    with open(os.path.join(INBOX, "INDEX.json"), encoding="utf-8") as f:
        idx = json.load(f)
    idx_paths = {it["path"] for it in idx["items"]}

    evs = []
    malformed = 0
    with open(os.path.join(INBOX, "index_events.jsonl"), encoding="utf-8") as f:
        for l in f:
            l = l.strip()
            if not l:
                continue
            try:
                evs.append(json.loads(l))
            except Exception:
                malformed += 1

    print(f"INDEX items: {len(idx_paths)}  events: {len(evs)}  malformed lines: {malformed}")

    reg = {}
    for e in evs:
        if e.get("op") == "register":
            reg.setdefault(norm(e.get("file")), []).append(e)

    in_idx_not_ev = sorted(idx_paths - set(reg))
    in_ev_not_idx = sorted(set(reg) - idx_paths)

    print(f"\n=== In INDEX fold but NO register event: {len(in_idx_not_ev)}")
    for p in in_idx_not_ev:
        print("  ", p)

    print(f"\n=== Register event but NOT in INDEX fold: {len(in_ev_not_idx)}")
    for p in in_ev_not_idx:
        # show op history summary
        ops = [e.get("op") for e in reg[p]]
        print(f"   {p}  ops={ops}")

    # Also: invalidate coverage — active-vs-invalidated in the fold
    inval = {norm(e.get("file")) for e in evs if e.get("op") == "invalidate"}
    still_listed = sorted(inval & idx_paths)
    print(f"\n=== Invalidated events but path still listed in INDEX: {len(still_listed)}")
    for p in still_listed[:20]:
        print("  ", p)

    # On-disk files (top level of inbox) missing from INDEX
    on_disk = set()
    for name in os.listdir(INBOX):
        full = os.path.join(INBOX, name)
        if os.path.isfile(full) and name not in ("INDEX.json", "index_events.jsonl"):
            on_disk.add(name)
    on_disk_not_idx = sorted(on_disk - idx_paths)
    print(f"\n=== On-disk inbox files missing from INDEX: {len(on_disk_not_idx)}")
    for p in on_disk_not_idx:
        print("  ", p)


if __name__ == "__main__":
    main()
