"""B2-280 migration: retire the 2^53 inexact seq band from every active item.

Owning brief: watch/inbox/burn_wave_20260926/QUEUE.md row B2-280. Spec order:
watch/inbox/LIVING_HASH_LAW_20260926.md section 5 (last-register-wins),
scripts/index_fold_host.mjs B2-279 sort-totality header block (tier 1 band
demoted below every exact seq, census warning on the fold-warning channel),
watch/inbox/burn_wave_20260926/B2_254_living_regression_20260926.md (re-pin
pattern: no-content-change stated in the register purpose).

What this does, once, idempotent by winner-class check:
  1. Re-census tier-1 events (numeric seqs failing Number.isSafeInteger after
     JSON.parse quantization) over the live log.
  2. Every band REGISTER that is the fold's winning event of an active item
     can still steal that item from a later no-seq register (md_record_seal
     autoseals fold in tier 0, strictly below tier 1 by the B2-279 law), and
     its printed seq is a quantized lie. Those winners are re-registered at
     fresh exact decimal-string seqs (tier 2), sha re-sealed on current
     bytes, class and living-shape carried over (none are living today),
     purposes naming the re-pin cause and the original purpose.
  3. One note event records the census and the true chronological order law:
     inside the band order is ts order; exact seqs outrank the band; band
     members that cannot steal (superseded or invalidated history) stay in
     the log untouched, no erase.
  4. The re-pin block is emitted in the original winners' ts order, so the
     block itself records the true chronological order of the band winners.

Concurrency: appends are one sequential bulk write done in under a second;
afterwards the caller must rescan for duplicate seqs (a concurrent fold-host
add could race the chain head) and re-pin any collision.
"""
import json, re, hashlib, os, sys
from datetime import datetime, timezone

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
        events.append(ev)
    order = [e for _, e in sorted(enumerate(events), key=sort_key)]
    active = {}
    for ev in order:
        p = ev.get("_nf")
        if not p or ev.get("_outside"):
            continue
        if ev.get("op") == "register":
            active[p] = ev
        elif ev.get("op") == "invalidate":
            active.pop(p, None)

    band = [e for e in events if seq_class(e)[0] == "inexact"]
    band_regs = [e for e in band if e.get("op") == "register"]
    winners = {p: e for p, e in active.items() if seq_class(e)[0] == "inexact" and e.get("op") == "register"}
    max_seq = max((seq_class(e)[1] for e in events if seq_class(e)[1] is not None), default=0)
    print(f"events={len(events)} tier1={len(band)} tier1_registers={len(band_regs)} "
          f"band_winners={len(winners)} log_max_seq={max_seq}")

    if not winners:
        print("NOTHING TO MIGRATE: no active item is ruled by a band register")
        return
    if not apply:
        for p in sorted(winners)[:10]:
            w = winners[p]
            print(f"  would re-pin {p} (raw seq {w.get('seq')} ts {w.get('ts')})")
        print(f"... {len(winners)} total; run with --apply to write")
        return

    # order re-pins by the original winners' true chronological order
    todo = sorted(winners.items(), key=lambda kv: ((kv[1].get("ts") or ""), kv[1]["_line"]))
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.") + f"{datetime.now(timezone.utc).microsecond // 1000:03d}Z"
    out_lines = []
    seq = max_seq
    nonce = 0
    for p, w in todo:
        fpath = os.path.join(INBOX, p.replace("/", os.sep))
        if not os.path.exists(fpath):
            print(f"SKIP missing on disk: {p}")
            continue
        digest = hashlib.sha256(open(fpath, "rb").read()).hexdigest().upper()
        seq += 1
        nonce += 1
        out_lines.append(json.dumps({
            "seq": str(seq),
            "ts": now,
            "op": "register",
            "file": p,
            "sha256": digest,
            "class": w.get("class") or "UNPROVEN",
            "purpose": (f"{w.get('purpose') or ''} | B2-280 seq-band re-pin: exact string seq "
                        f"replaces past-2^53 quantized literal {w.get('seq')}; sha re-sealed on "
                        f"current bytes; no living flag (whole-file static seal); "
                        f"no content change intended by this event").strip(),
            "writer": WRITER,
            "nonce": nonce,
        }, ensure_ascii=False))
    # one note event: the census and the true chronological order law
    seq += 1
    nonce += 1
    from collections import Counter
    by_op = Counter(e.get("op", "?") for e in band)
    out_lines.append(json.dumps({
        "seq": str(seq),
        "ts": now,
        "op": "note",
        "writer": WRITER,
        "nonce": nonce,
        "note": (
            "B2-280 2^53 inexact seq band census and retirement: "
            f"{len(band)} events carry numeric seq literals that fail Number.isSafeInteger "
            f"after JSON.parse quantization (ulp 256 at this magnitude); all known members "
            f"parse to the single double 1789823567015749376 "
            f"(by op: {dict(by_op)}). True chronological order inside the band is the event "
            f"ts, because the raw magnitudes are destroyed by parsing; exact seqs (safe "
            f"integers and digit-only decimal strings) outrank the whole band per the "
            f"B2-279 total order. {len(todo)} band registers that were the winning event of "
            f"an active item (steal-capable over later no-seq registers) were re-registered "
            f"above in the original winners' ts order; the remaining band members are "
            f"superseded or invalidated history and stay untouched (no erase). Census "
            f"warning channel: scripts/index_fold_host.mjs fold_warnings. Receipt: "
            f"burn_wave_20260926/B2_280_seq_band_20260926.md"
        ),
    }, ensure_ascii=False))

    with open(LOG, "ab") as fh:
        for line in out_lines:
            fh.write(line.encode("utf-8") + b"\n")
    print(f"APPLIED: appended {len(out_lines)} events (seq {max_seq + 1}..{seq}), writer {WRITER}")

if __name__ == "__main__":
    main()
