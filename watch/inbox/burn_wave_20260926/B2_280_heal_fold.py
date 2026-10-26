"""B2-280 heal pass: re-express the band's stranded power on exact seqs.

After the B2-279 total-order law demoted the 2^53 quantization band below
every exact seq, two residues surfaced on the production fold that the first
B2-280 pass (231 band-winner re-pins, seqs ...491-...722) did not cover:

  1. STRANDED SEALS: active items whose chronologically-latest register is a
     band event (the drift-patrol hash refreshes carrying the CURRENT bytes)
     but whose law winner is an older exact-seq register. The band seal holds
     the true latest bytes and can no longer win. Heal: re-register the file
     at a fresh exact seq on current bytes (bytes equal the stranded band
     seal for 34 of 35; THE50_W6_T26_DRIFT_STAMP.receipt.json moved past
     every register and is re-sealed on current bytes with that stated).
  2. RESURRECTED GHOSTS: dead-path registers (09-21 cathedral-era files since
     removed from the inbox) that the patrol's band INVALIDATEs used to mask
     by quantized value; the law demoted those invalidates, the exact
     registers won, and the items surfaced as MISSING. Heal: invalidate at a
     fresh exact seq, completing the patrol's own demoted invalidates.

Both heals are the same instrument as pass one: the brief's "invalidate plus
exact-seq re-register" migration, applied where the band still decides (or
used to decide by an illegal magnitude) an active item. A second note event
records the counts on the log itself.
"""
import json, re, hashlib, os, sys
from datetime import datetime, timezone
from collections import Counter

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
INBOX = os.path.join(ROOT, "watch", "inbox")
LOG = os.path.join(INBOX, "index_events.jsonl")
WRITER = "zcode-b2-280-seq-band"
TWO53 = 9007199254740991
OUTSIDE_RE = re.compile(
    r"^(mag|memory|queue|scripts|dashboard|docs|site|tests|models|backend|configs?|deploy"
    r"|state|watch|research|corpus|dist_audit|attic|handoff|tools|bridge|harness|router"
    r"|experiments|window|agents)/"
)
INBOX_ROOTS = ["c:/users/foste/documents/projects/local_sovereign_agent/watch/inbox"]

def norm(f):
    p = str(f or "").strip().replace("\\", "/")
    while p.startswith("/"):
        p = p[1:]
    p = re.sub(r"^(board|app)/inbox/", "", p)
    while p.startswith("inbox/"):
        p = p[6:]
    for root in INBOX_ROOTS:
        r = root + "/"
        if len(p) > len(r) and p[: len(r)] == r:
            p = p[len(r):]
            break
    while p.startswith("inbox/"):
        p = p[6:]
    return p

def seq_class(ev):
    s = ev.get("seq")
    if isinstance(s, bool) or s is None:
        return ("null", None)
    if isinstance(s, int):
        return ("inexact", int(float(s))) if not (-TWO53 < s < TWO53) else ("exact", s)
    if isinstance(s, str) and re.fullmatch(r"\d+", s or ""):
        return ("exact", int(s))
    return ("null", None)

def sort_key(item):
    i, ev = item
    cls, v = seq_class(ev)
    ts = ev.get("ts") or ""
    if cls == "null":
        return (0, 0, "", ts, i)
    tier = 1 if cls == "inexact" else 2
    return (tier, v, ts, i)

def main():
    apply = "--apply" in sys.argv
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
                and (ev["_nf"] == "" or bool(re.match(r"^[A-Za-z]:/", ev["_nf"])) or bool(re.search(r"(^|/)\.\.(/|$)", ev["_nf"])))
            )
        events.append(ev)
    order = [e for _, e in sorted(enumerate(events), key=sort_key)]
    active = {}
    reg_hist = {}
    for ev in order:
        p = ev.get("_nf")
        if not p or ev.get("_outside") or ev.get("_unresolved"):
            continue
        if ev.get("op") == "register":
            active[p] = ev
            reg_hist.setdefault(p, []).append(ev)
        elif ev.get("op") == "invalidate":
            active.pop(p, None)

    stranded = []
    for p, w in active.items():
        hist = reg_hist.get(p, [])
        chrono = max(hist, key=lambda e: (e.get("ts") or "", e["_line"]))
        if seq_class(chrono)[0] == "inexact" and chrono["_line"] != w["_line"]:
            stranded.append((p, w, chrono))
    ghosts = []
    for p, w in active.items():
        if not os.path.exists(os.path.join(INBOX, p.replace("/", os.sep))):
            ghosts.append((p, w))
    print(f"stranded band seals: {len(stranded)}  resurrected ghosts: {len(ghosts)}")
    if not apply:
        for p, w, chrono in stranded[:8]:
            print(f"  would re-register {p} (winner line{w['_line']} {w.get('ts')}, band seal line{chrono['_line']} {chrono.get('ts')})")
        for p, w in ghosts[:8]:
            print(f"  would invalidate {p} (winner line{w['_line']} {w.get('ts')})")
        print("run with --apply to write")
        return

    max_seq = max((seq_class(e)[1] for e in events if seq_class(e)[1] is not None), default=0)
    last_nonce = 0
    for e in events:
        if e.get("writer") == WRITER and isinstance(e.get("nonce"), int):
            last_nonce = max(last_nonce, e["nonce"])
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.") + f"{datetime.now(timezone.utc).microsecond // 1000:03d}Z"
    out = []
    seq = max_seq
    nonce = last_nonce
    for p, w, chrono in sorted(stranded, key=lambda kv: ((kv[2].get("ts") or ""), kv[2]["_line"])):
        fpath = os.path.join(INBOX, p.replace("/", os.sep))
        if not os.path.exists(fpath):
            continue
        digest = hashlib.sha256(open(fpath, "rb").read()).hexdigest().upper()
        seq += 1
        nonce += 1
        out.append(json.dumps({
            "seq": str(seq), "ts": now, "op": "register", "file": p,
            "sha256": digest,
            "class": chrono.get("class") or w.get("class") or "UNPROVEN",
            "purpose": (f"B2-280 heal pass: stranded band seal re-expressed on an exact seq; "
                        f"chrono-latest register was band event line {chrono['_line']} "
                        f"(seq {json.dumps(chrono.get('seq'))}) demoted below exact winner line "
                        f"{w['_line']} by the B2-279 law; sha re-sealed on current bytes"),
            "writer": WRITER, "nonce": nonce,
        }, ensure_ascii=False))
    for p, w in sorted(ghosts):
        seq += 1
        nonce += 1
        out.append(json.dumps({
            "seq": str(seq), "ts": now, "op": "invalidate", "file": p,
            "reason": (f"B2-280 heal pass: dead-path register resurrected when the B2-279 law "
                       f"demoted the band invalidates that masked it (file absent from the "
                       f"inbox; completing the patrol's own demoted invalidate of this path)"),
            "writer": WRITER, "nonce": nonce,
        }, ensure_ascii=False))
    seq += 1
    nonce += 1
    out.append(json.dumps({
        "seq": str(seq), "ts": now, "op": "note", "writer": WRITER, "nonce": nonce,
        "note": (f"B2-280 heal pass census: {len(stranded)} stranded band seals re-registered "
                 f"on exact seqs (the 2^53 band had carried the true latest bytes for these "
                 f"files; the B2-279 demotion stranded those seals behind older exact "
                 f"registers) and {len(ghosts)} dead-path registers invalidated (the patrol's "
                 f"band invalidates used to mask them by quantized value; the demotion "
                 f"resurrected them as MISSING). Receipt: "
                 f"burn_wave_20260926/B2_280_seq_band_20260926.md"),
    }, ensure_ascii=False))
    with open(LOG, "ab") as fh:
        for line in out:
            fh.write(line.encode("utf-8") + b"\n")
    print(f"APPLIED: appended {len(out)} events (seq {max_seq + 1}..{seq}), writer {WRITER}")

if __name__ == "__main__":
    main()
