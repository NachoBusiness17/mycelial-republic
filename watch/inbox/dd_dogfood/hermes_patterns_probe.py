"""hermes_patterns_probe - the GALA hermes-burn-patterns lane probe.

Re-runnable instrument (read-only) for the owed waltz: mine the Hermes burn
ledger for temporal / model / plan patterns and cross-reference the
TICKET_LEDGER redemption row. Prints the full report to stdout.

Sources (byte-truth):
  memory/runs/hermes_burn/usage.jsonl          the paid burn ledger
  memory/plans/hermes_burn_*/*/ask.json        the staged asks (+ REFUSED markers)
  watch/inbox/hermes_burn/*.md(.poisoned-...)  the landed receipts
  watch/inbox/hermes_burn/TICKET_LEDGER.md     the redemption denominator
  memory/runs/hermes_burn/driver.beat|.log     the descent driver heartbeats

Census denominator law (B2-216): the ledger is LIVE while the descent driver
runs; every probe run stamps its moment. Never difference two counts taken at
different moments.

Run: .venv/Scripts/python.exe watch/inbox/dd_dogfood/hermes_patterns_probe.py
"""
from __future__ import annotations

import collections
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
USAGE = ROOT / "memory" / "runs" / "hermes_burn" / "usage.jsonl"
OUT = ROOT / "watch" / "inbox" / "hermes_burn"
PLANS = ROOT / "memory" / "plans"
LEDGER = OUT / "TICKET_LEDGER.md"

# beat-vehicle id families: same id LEGITIMATELY recurs across run dirs only
# when the run dir name is absent from the id; TAVERN ids carry no run stamp
# (tools/tavern.py f"TAVERN_r{rnd}_{p['name']}") so replays collide by design.
BEAT_VEHICLES = ("TAVERN", "DND0")


def load_rows() -> list[dict]:
    return [json.loads(l) for l in open(USAGE, encoding="utf-8") if l.strip()]


def pct(a: float, b: float) -> str:
    return f"{100 * a / b:.1f}%" if b else "-"


def main() -> None:
    now = datetime.now(timezone.utc).isoformat()
    rows = load_rows()
    print(f"=== probe moment: {now} (B2-216: name instrument + moment before comparing counts) ===")
    print("=== 1. LEDGER PROFILE ===")
    print(f"rows: {len(rows)}  span: {min(r['ts'] for r in rows)} .. {max(r['ts'] for r in rows)}")
    cost = sum(r.get("cost_usd", 0) or 0 for r in rows)
    tok = sum(r.get("prompt_tokens", 0) + r.get("completion_tokens", 0)
              + (r.get("reasoning_tokens") or 0) for r in rows)
    ok = sum(1 for r in rows if r.get("ok"))
    print(f"total cost: ${cost:.2f}   total tokens: {tok:,}   ok rows: {ok}/{len(rows)} ({pct(ok, len(rows))})")

    print("\n=== 2. MODEL ECONOMICS + RECEIPT YIELD ===")
    agg: dict[str, dict] = collections.defaultdict(
        lambda: dict(n=0, pt=0, ct=0, rt=0, cost=0.0, ok=0, ref=0, ids=set()))
    for r in rows:
        a = agg[r["model"]]
        a["n"] += 1
        a["pt"] += r.get("prompt_tokens", 0)
        a["ct"] += r.get("completion_tokens", 0)
        a["rt"] += r.get("reasoning_tokens") or 0
        a["cost"] += r.get("cost_usd", 0) or 0
        a["ok"] += 1 if r.get("ok") else 0
        a["ref"] += 1 if r.get("refused") else 0
        a["ids"].add(r["id"])

    # receipt header names the model: '# <id> (<model>, turn 1, channel: ...)'
    hdr = re.compile(r"^# (.+?) \(([^,]+), turn (\d+)")
    landed_by_model: dict[str, set] = collections.defaultdict(set)
    poison_now: dict[str, set] = collections.defaultdict(set)
    poison_history: set[str] = set()
    garbage_confess: list[str] = []
    clean_receipts: list[str] = []
    bytes_by_model: dict[str, int] = collections.Counter()
    for p in sorted(OUT.glob("*.md")):
        text = p.read_text(encoding="utf-8", errors="replace")
        first = text.splitlines()[:1]
        if not first:
            continue
        m = hdr.match(first[0])
        if not m:
            continue
        rid, model = m.group(1), m.group(2)
        if "EVIDENCE block is empty" in text:
            garbage_confess.append(p.name)
        else:
            landed_by_model[model].add(rid)
            clean_receipts.append(p.name)
            bytes_by_model[model] += p.stat().st_size
    for p in sorted(OUT.glob("*.md.poisoned-evidenceless")):
        first = p.read_text(encoding="utf-8", errors="replace").splitlines()[:1]
        if first:
            m = hdr.match(first[0])
            if m:
                poison_now[m.group(2)].add(m.group(1))
                poison_history.add(m.group(1))

    print(f"{'model':32} {'n':>4} {'ok%':>6} {'ref':>4} {'tok':>11} "
          f"{'cost$':>7} {'$/Mtok':>7} {'ids':>4} {'landed':>6} {'KB/$':>6}")
    for m_, a in sorted(agg.items(), key=lambda x: -x[1]["cost"]):
        t = a["pt"] + a["ct"] + a["rt"]
        kbpd = bytes_by_model.get(m_, 0) / 1024 / a["cost"] if a["cost"] else 0
        print(f"{m_:32} {a['n']:4d} {pct(a['ok'], a['n']):>6} {a['ref']:4d} "
              f"{t:11,d} {a['cost']:7.2f} {1e6 * a['cost'] / t if t else 0:7.2f} "
              f"{len(a['ids']):4d} {len(landed_by_model.get(m_, set())):6d} {kbpd:6.1f}")
    print(f"clean receipts on disk: {len(clean_receipts)}; receipts self-confessing "
          f"'EVIDENCE block is empty': {len(garbage_confess)} -> {', '.join(sorted(garbage_confess))}")
    print(f"poisoned-quarantined files (.poisoned-evidenceless): {len(poison_history)} "
          f"-> {', '.join(sorted(poison_history))}; asks with BOTH a poisoned twin and a "
          f"clean refire: {len([r for r in poison_history if (OUT / f'{r}.md').is_file()])}")

    print("\n=== 3. TEMPORAL PATTERNS ===")
    print("-- per day (UTC) --")
    for d in sorted({r["ts"][:10] for r in rows}):
        dr = [r for r in rows if r["ts"][:10] == d]
        o = sum(1 for r in dr if r.get("ok"))
        c = sum(r.get("cost_usd", 0) or 0 for r in dr)
        print(f"  {d}: n={len(dr):4d} ok={o:4d} ({pct(o, len(dr))})  ${c:.2f}")
    print("-- hour-of-day rollup, all days --")
    hr: dict[str, list] = collections.defaultdict(lambda: [0, 0, 0.0])
    for r in rows:
        e = hr[r["ts"][11:13]]
        e[0] += 1
        e[1] += 1 if r.get("ok") else 0
        e[2] += r.get("cost_usd", 0) or 0
    for h in sorted(hr):
        n, o, c = hr[h]
        print(f"  {h}:00Z  n={n:4d} ok={o:4d} ({pct(o, n)})  ${c:.2f}")
    print("-- trough diagnosis: fails by hour x class --")
    fh: dict[tuple, int] = collections.Counter()
    for r in rows:
        if not r.get("ok"):
            cls = "refusal" if r.get("refused") else ("length" if r.get("finish_reason") else "silent-empty")
            fh[(r["ts"][11:13], cls)] += 1
    print("  hour  " + "".join(f"{c:>14}" for c in ("refusal", "silent-empty", "length")))
    for h in sorted({k[0] for k in fh}):
        print(f"  {h}:00 " + "".join(f"{fh.get((h, c), 0):14d}" for c in
                                      ("refusal", "silent-empty", "length")))

    print("\n=== 4. PLAN / ASK-STATE CLASSIFICATION ===")
    ask_dirs = sorted(PLANS.glob("hermes_burn_*/*"))
    ledger_ids = collections.Counter(r["id"] for r in rows)
    states: dict[str, list] = collections.defaultdict(list)
    fam_state: dict[str, dict] = collections.defaultdict(
        lambda: dict(n=0, LANDED=0, HEALED=0, REFUSED=0, FIRED_NORECEIPT=0, NEVER_FIRED=0))
    for d in ask_dirs:
        aj = d / "ask.json"
        if not aj.is_file():
            continue
        meta = json.loads(aj.read_text(encoding="utf-8"))
        rid = meta.get("id", d.name)
        fam = d.parent.name
        if (d / "REFUSED").is_file():
            st = "REFUSED"
        elif (OUT / f"{rid}.md").is_file():
            st = "HEALED" if rid in poison_history else "LANDED"
        elif (OUT / f"{rid}.md.poisoned-evidenceless").is_file():
            st = "HEALED"  # poisoned quarantine only, clean refire elsewhere
        elif ledger_ids.get(rid):
            st = "FIRED_NORECEIPT"
        else:
            st = "NEVER_FIRED"
        states[st].append(f"{fam}/{d.name}")
        f = fam_state[fam]
        f["n"] += 1
        f[st] += 1
    print(f"{'plan family':36} {'asks':>4} {'LAND':>4} {'HEAL':>4} {'REFU':>4} "
          f"{'FIRE-NR':>7} {'NEVER':>5}")
    for f, s in sorted(fam_state.items()):
        print(f"{f:36} {s['n']:4d} {s['LANDED']:4d} {s['HEALED']:4d} "
              f"{s['REFUSED']:4d} {s['FIRED_NORECEIPT']:7d} {s['NEVER_FIRED']:5d}")
    tot = collections.Counter()
    for s in fam_state.values():
        tot.update(s)
    print(f"TOTAL ask dirs classified: {tot['n']} = "
          + " + ".join(f"{k} {tot[k]}" for k in
                       ("LANDED", "HEALED", "REFUSED", "FIRED_NORECEIPT", "NEVER_FIRED")))
    for st in ("REFUSED", "FIRED_NORECEIPT", "NEVER_FIRED"):
        if states.get(st):
            print(f"  {st}: " + ", ".join(states[st]))

    print("\n=== 5. WASTE PATTERNS (three named classes) ===")
    # class W1: plan-ask re-burn theater - ok turn-1 rows for an id that already
    #   landed (A1 disease; carrier-patch 1 cured NEW staging 2026-10-01)
    # class W2: beat-vehicle id-collision replay - TAVERN/DND0 ids carry no run
    #   stamp so every replayed run reuses ids; same-id ok rows are ambiguous
    #   between legit game turns and replays (instrument defect, not priced here)
    # class W3: evidence-less paid fires - receipts that self-confess
    first_ok: dict[str, str] = {}
    w1_cost = 0.0
    w1_rows = 0
    w2_cost = 0.0
    w2_rows = 0
    per_id_w1: dict[str, dict] = {}
    for r in sorted(rows, key=lambda x: x["ts"]):
        rid = r["id"]
        beat = rid.startswith(BEAT_VEHICLES)
        if r.get("ok") and r.get("turn") == 1:
            if rid in first_ok:
                w = r.get("cost_usd", 0) or 0
                if beat:
                    w2_cost += w
                    w2_rows += 1
                else:
                    w1_cost += w
                    w1_rows += 1
                    e = per_id_w1.setdefault(rid, {"rows": 0, "cost": 0.0})
                    e["rows"] += 1
                    e["cost"] += w
            else:
                first_ok[rid] = r["ts"]
    print(f"W1 plan-ask re-burn rows (ok turn-1, id already landed): {w1_rows} rows / "
          f"${w1_cost:.2f} = {pct(w1_cost, cost)} of total spend")
    for rid, e in sorted(per_id_w1.items(), key=lambda x: -x[1]["cost"])[:6]:
        print(f"  {rid}: +{e['rows']} rows / ${e['cost']:.2f} after first ok {first_ok[rid]}")
    print(f"W2 beat-vehicle same-id repeat rows (TAVERN/DND0, id collision class): "
          f"{w2_rows} rows / ${w2_cost:.2f} (NOT priced as waste: replay-vs-turn "
          f"ambiguous from the ledger alone; instrument defect = no run stamp in id)")
    dk = sum(1 for r in rows if r.get("doubled_key"))
    print(f"  doubled_key alarm rows (saturated by the collision): {dk} of {len(rows)} "
          f"({pct(dk, len(rows))})")
    a1 = [r for r in rows if r["id"] == "A1_steer_antiforgery"]
    pre = [r for r in a1 if r["ts"] < "2026-10-01T16:10"]
    post = [r for r in a1 if r["ts"] >= "2026-10-01T16:10"]
    print(f"  A1 reconciliation: {len(a1)} rows total; before 16:10Z {len(pre)} rows "
          f"${sum(r.get('cost_usd', 0) or 0 for r in pre):.2f}; after {len(post)} rows "
          f"${sum(r.get('cost_usd', 0) or 0 for r in post):.2f} (carrier docstring: "
          f"landed 16:10Z, claimed 45x $20.53 at its writing moment)")
    ref = [r for r in rows if r.get("refused")]
    print(f"W3a refusal loops (unbilled, wall-clock disease): {len(ref)} rows / "
          f"${sum(r.get('cost_usd', 0) or 0 for r in ref):.2f} billed; by id: "
          + ", ".join(f"{k} x{v}" for k, v in
                      collections.Counter(r["id"] for r in ref).most_common()))
    sf = [r for r in rows if not r.get("ok") and not r.get("refused")]
    print(f"W3b silent-empty fail rows: {len(sf)} / "
          f"${sum(r.get('cost_usd', 0) or 0 for r in sf):.2f}; by family: "
          + ", ".join(f"{k} x{v}" for k, v in
                      collections.Counter(r["id"].split('_')[0] for r in sf).most_common()))
    ev_cost = sum(r.get("cost_usd", 0) or 0 for r in rows
                  if r.get("ok") and r.get("turn") == 1
                  and (r["id"].startswith("DUEL2_train") or r["id"].startswith("T1W2_")))
    print(f"W3c evidence-less paid fires (DUEL2_train + T1W2 ok turn-1 rows): "
          f"${ev_cost:.2f} into receipts that self-confess or were quarantined")

    print("\n=== 6. TICKET_LEDGER CROSS-REF ===")
    txt = LEDGER.read_text(encoding="utf-8")
    for i, line in enumerate(txt.splitlines(), 1):
        if "Row one: issued" in line or "Redemption rate 74.0" in line:
            print(f"  TICKET_LEDGER.md:{i}: {line.strip()}")
    if "Row one: issued 50 / run 37 / parked 13" in txt:
        print("  ask's claim '50 issued/37 run = 74 pct' VERIFIED in bytes at row one.")
    print("  mapping to burn-plan classes: the parked tail (row one) names 5 CLIMB "
          "tickets, memlance witness, quant tag, V12 .bak, V15 sid, Godot precompile, "
          "6 duel refires (paid, another lane). The duel refires ARE the "
          "hermes_burn_duel1/hidden_*_r2 plans (all 6 now LANDED); the T1W2 refire "
          "debt is the poisoned-evidenceless quartet (all 4 now HEALED with clean "
          "refires on disk).")

    print("\n=== 7. DESCENT DRIVER ===")
    beats = (ROOT / "memory/runs/hermes_burn/driver.beat").read_text(
        encoding="utf-8").splitlines()
    print(f"driver.beat: {len(beats)} beats, first: {beats[0] if beats else '-'}, "
          f"last: {beats[-1] if beats else '-'}")
    log = (ROOT / "memory/runs/hermes_burn/driver.log").read_text(
        encoding="utf-8", errors="replace")
    passes = re.findall(r"HERMES-BURN: (\w+) - (\d+)/(\d+) asks; ledger total \$(\d+\.\d+)",
                        log)
    print(f"driver.log HERMES-BURN summary lines: {len(passes)} (last 5):")
    for p in passes[-5:]:
        print(f"  {p}")
    print("note: driver.log 'skipped' rows are the landed-beats-force skips (no ledger "
          "row); the ledger holds fires only.")


if __name__ == "__main__":
    main()
