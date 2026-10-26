"""B2-280 probe: 2^53 inexact seq band census + steal analysis over index_events.jsonl.

Read-only. Mirrors scripts/index_fold_host.mjs normInboxFile / OUTSIDE_RE /
seqOf / compareBySeqTs. Node's JSON.parse rounds past-2^53 numeric literals to
the nearest double (ulp 256 at this magnitude); python json.loads keeps the
exact int, so the raw literal is re-rounded through float() to emulate the fold.
A numeric seq is INEXACT iff it fails Number.isSafeInteger (|n| outside
(-2^53, 2^53)); the double rounding already happened inside the fold.
"""
import json, re, sys
from collections import defaultdict

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
LOG = ROOT + r"\watch\inbox\index_events.jsonl"
TWO53 = 9007199254740991  # Number.MAX_SAFE_INTEGER
BAND_ROOTS = [
    "C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox",
    "C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox",
]
OUTSIDE_RE = re.compile(
    r"^(mag|memory|queue|scripts|dashboard|docs|site|tests|models|backend|configs?|deploy"
    r"|state|watch|research|corpus|dist_audit|attic|handoff|tools|bridge|harness|router"
    r"|experiments|window|agents)/"
)

def norm(f):
    p = str(f or "").strip().replace("\\", "/")
    while p.startswith("/"):
        p = p[1:]
    p = re.sub(r"^(board|app)/inbox/", "", p)
    while p.startswith("inbox/"):
        p = p[6:]
    for root in BAND_ROOTS:
        r = root.lower() + "/"
        if len(p) > len(r) and p[: len(r)].lower() == r:
            p = p[len(r):]
            break
    while p.startswith("inbox/"):
        p = p[6:]
    return p

def seq_class(ev):
    """('seq', exact_int_or_quantized_double_int) | ('null',) ; emulates seqOf."""
    s = ev.get("seq")
    if isinstance(s, bool) or s is None:
        return ("null", None)
    if isinstance(s, int):
        q = int(float(s))  # node double rounding
        return ("inexact", q) if not (-TWO53 < s < TWO53) else ("exact", s)
    if isinstance(s, str) and re.fullmatch(r"\d+", s or ""):
        return ("exact", int(s))
    return ("null", None)

def sort_key(idx_ev):
    i, ev = idx_ev
    cls, v = seq_class(ev)
    ts = ev.get("ts") or ""
    # B2-279 landed law (scripts/index_fold_host.mjs seqOrderKey): tier 0
    # no-seq events below tier 1 inexact band below tier 2 exact seqs; inside
    # a tier ts then file order. (The first draft of this probe ordered all
    # seq events by value alone, which misreads sub-band exact registers as
    # band losers; the tier order is the production law since B2-279 landed.)
    if cls == "null":
        return (0, 0, "", ts, i)
    tier = 1 if cls == "inexact" else 2
    return (tier, v, ts, i)

def main():
    raw = open(LOG, "rb").read().splitlines()
    events = []
    for i, lb in enumerate(raw, 1):
        try:
            ev = json.loads(lb.decode("utf-8"))
        except Exception:
            continue
        ev["_line"] = i
        if isinstance(ev.get("file"), str):
            ev["_nf"] = norm(ev["file"])
            ev["_outside"] = bool(OUTSIDE_RE.match(ev["_nf"]))
            ev["_unresolved"] = (
                not ev["_outside"]
                and (
                    ev["_nf"] == ""
                    or re.match(r"^[A-Za-z]:/", ev["_nf"])
                    or re.search(r"(^|/)\.\.(/|$)", ev["_nf"])
                )
            )
        events.append(ev)

    band = [e for e in events if seq_class(e)[0] == "inexact"]
    census = {
        "lines": len(raw),
        "events_parsed": len(events),
        "inexact_seq_events": len(band),
        "inexact_distinct_doubles": sorted({seq_class(e)[1] for e in band}),
        "inexact_by_op": {},
        "inexact_by_writer": {},
    }
    for e in band:
        census["inexact_by_op"][e.get("op", "?")] = census["inexact_by_op"].get(e.get("op", "?"), 0) + 1
        w = e.get("writer", "(none)")
        census["inexact_by_writer"][w] = census["inexact_by_writer"].get(w, 0) + 1

    order = sorted(enumerate(events), key=sort_key)
    # fold with last-register-wins + invalidate removal (mirrors fold())
    active = {}       # path -> winning event
    reg_hist = defaultdict(list)  # path -> [(ts, line, ev)] register events in ts order
    for _, ev in order:
        p = ev.get("_nf")
        if ev.get("op") == "register" and p is not None:
            if ev.get("_outside") or ev.get("_unresolved"):
                continue  # dropped before item creation
            active[p] = ev
            reg_hist[p].append(ev)
        elif ev.get("op") == "invalidate" and p is not None:
            active.pop(p, None)

    # steal analysis: band registers whose file's fold winner is not the
    # chronologically-latest register of that file
    steals = []
    for p, hist in reg_hist.items():
        band_regs = [e for e in hist if seq_class(e)[0] == "inexact"]
        if not band_regs:
            continue
        chrono_latest = max(hist, key=lambda e: (e.get("ts") or "", e["_line"]))
        win = active.get(p)
        if win is None:
            continue  # item inactive; nothing to steal
        if win["_line"] != chrono_latest["_line"]:
            steals.append({
                "file": p,
                "winner_line": win["_line"],
                "winner_seq_raw": json.dumps(win.get("seq")),
                "winner_ts": win.get("ts"),
                "winner_op": win.get("op"),
                "winner_writer": win.get("writer"),
                "chrono_latest_line": chrono_latest["_line"],
                "chrono_latest_seq_raw": json.dumps(chrono_latest.get("seq")),
                "chrono_latest_ts": chrono_latest.get("ts"),
                "chrono_latest_writer": chrono_latest.get("writer"),
                "band_regs_of_file": [
                    {"line": e["_line"], "ts": e.get("ts"), "raw": e.get("seq")}
                    for e in band_regs
                ],
            })
    census["files_with_band_regs"] = sum(1 for h in reg_hist.values() if any(seq_class(e)[0] == "inexact" for e in h))
    census["active_steals"] = steals
    # band members whose file is inactive or correctly ordered cannot steal
    census["band_regs_on_active_files"] = sum(
        len([e for e in h if seq_class(e)[0] == "inexact"])
        for h in reg_hist.values() if h[0].get("_nf") in active
    )
    print(json.dumps(census, indent=1)[:12000])

if __name__ == "__main__":
    main()
