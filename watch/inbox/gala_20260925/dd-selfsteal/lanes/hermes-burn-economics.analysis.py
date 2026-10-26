"""hermes-burn-economics lane audit script.

Reads memory/runs/hermes_burn/usage.jsonl (1,099 rows) + the landed
output dir watch/inbox/hermes_burn/ and prints the full economics:
per-day, per-model, per-plan(prefix), receipts vs nothing, goodput,
double-spend decomposition. Read-only over the estate; all outputs
to stdout so the raw run is capturable for the check file.
"""
import json
import collections
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
LEDGER = ROOT / "memory/runs/hermes_burn/usage.jsonl"
OUTDIR = ROOT / "watch/inbox/hermes_burn"

rows = []
for i, line in enumerate(LEDGER.open(encoding="utf-8"), 1):
    line = line.strip()
    if not line:
        continue
    r = json.loads(line)
    r["_line"] = i
    rows.append(r)

print(f"LEDGER {LEDGER.as_posix()}")
print(f"rows={len(rows)}")

def money(x):
    return f"${x:.4f}"

# ---------- totals ----------
tot_cost = sum(r["cost_usd"] for r in rows)
tot_pt = sum(r["prompt_tokens"] for r in rows)
tot_ct = sum(r["completion_tokens"] for r in rows)
tot_rt = sum(r.get("reasoning_tokens", 0) for r in rows)
print(f"\n== TOTALS ==")
print(f"cost={money(tot_cost)} prompt_tokens={tot_pt} completion_tokens={tot_ct} reasoning_tokens={tot_rt} all_tokens={tot_pt+tot_ct+tot_rt}")

# ---------- per day ----------
print(f"\n== PER DAY ==")
by_day = collections.defaultdict(lambda: {"rows": 0, "cost": 0.0, "pt": 0, "ct": 0, "ok": 0, "bad": 0, "dbl": 0, "dbl_cost": 0.0, "refused": 0})
for r in rows:
    d = r["ts"][:10]
    b = by_day[d]
    b["rows"] += 1
    b["cost"] += r["cost_usd"]
    b["pt"] += r["prompt_tokens"]
    b["ct"] += r["completion_tokens"]
    b["ok" if r.get("ok") else "bad"] += 1
    if r.get("doubled_key"):
        b["dbl"] += 1
        b["dbl_cost"] += r["cost_usd"]
    if r.get("refused"):
        b["refused"] += 1
for d in sorted(by_day):
    b = by_day[d]
    print(f"{d} rows={b['rows']:4d} cost={money(b['cost']):>9} pt={b['pt']:9d} ct={b['ct']:8d} ok={b['ok']:4d} bad={b['bad']:3d} doubled={b['dbl']:3d} ({money(b['dbl_cost'])}) refused={b['refused']:3d}")

# ---------- per model ----------
print(f"\n== PER MODEL ==")
by_model = collections.defaultdict(lambda: {"rows": 0, "cost": 0.0, "pt": 0, "ct": 0, "ok": 0, "bad": 0})
for r in rows:
    m = by_model[r["model"]]
    m["rows"] += 1
    m["cost"] += r["cost_usd"]
    m["pt"] += r["prompt_tokens"]
    m["ct"] += r["completion_tokens"]
    m["ok" if r.get("ok") else "bad"] += 1
for m in sorted(by_model, key=lambda k: -by_model[k]["cost"]):
    b = by_model[m]
    print(f"{m:32s} rows={b['rows']:4d} cost={money(b['cost']):>9} pt={b['pt']:9d} ct={b['ct']:8d} ok={b['ok']:4d} bad={b['bad']:3d}")

# ---------- per plan prefix ----------
print(f"\n== PER PLAN (id prefix) ==")
by_prefix = collections.defaultdict(lambda: {"rows": 0, "cost": 0.0, "ok": 0, "bad": 0, "dbl": 0, "dbl_cost": 0.0, "refused": 0, "ids": set()})
def prefix_of(r):
    rid = r["id"]
    # known plan families: longest prefix before a digit/underscore tail
    for p in ("TAVERN", "DND0", "DUEL1", "DUEL2", "A1", "A2", "A3", "B1", "B2", "C1", "D1", "D2", "D3",
              "DG1", "LENS1", "N1", "N1R", "SP1", "SUBSTANCE", "T1W1", "T1W2", "T1W3", "T1R1",
              "T2SP2", "T2SP3", "T3R2", "GALA", "BARFIGHT", "DND", "MOUNTAIN", "WILD", "KABUKI",
              "PARTYCHAT", "SEASON", "THE", "WIRE", "SESSION"):
        if rid == p or rid.startswith(p + "_") or rid.startswith(p + " "):
            return p
    return rid.split("_")[0]
for r in rows:
    p = prefix_of(r)
    b = by_prefix[p]
    b["rows"] += 1
    b["cost"] += r["cost_usd"]
    b["ok" if r.get("ok") else "bad"] += 1
    if r.get("doubled_key"):
        b["dbl"] += 1
        b["dbl_cost"] += r["cost_usd"]
    if r.get("refused"):
        b["refused"] += 1
    b["ids"].add(r["id"])
for p in sorted(by_prefix, key=lambda k: -by_prefix[k]["cost"]):
    b = by_prefix[p]
    print(f"{p:12s} rows={b['rows']:4d} cost={money(b['cost']):>9} ok={b['ok']:4d} bad={b['bad']:3d} doubled={b['dbl']:3d}({money(b['dbl_cost'])}) refused={b['refused']:3d} distinct_ids={len(b['ids'])}")

# ---------- receipts: which ask ids landed an output file ----------
print(f"\n== RECEIPTS (landed output files) ==")
landed = {p.stem: p for p in OUTDIR.glob("*.md")}
print(f"files in {OUTDIR.as_posix()}: {len(landed)}")

def base_id(rid):
    # strip a trailing _rN revision suffix used in filenames
    return rid

# ledger ids -> did any output file exist whose stem starts with the id?
all_ids = collections.defaultdict(lambda: {"rows": 0, "cost": 0.0, "ok": 0, "bad": 0, "dbl": 0, "pt": 0, "ct": 0})
for r in rows:
    b = all_ids[r["id"]]
    b["rows"] += 1
    b["cost"] += r["cost_usd"]
    b["pt"] += r["prompt_tokens"]
    b["ct"] += r["completion_tokens"]
    b["ok" if r.get("ok") else "bad"] += 1
    if r.get("doubled_key"):
        b["dbl"] += 1

def output_for(rid):
    if rid in landed:
        return landed[rid]
    # try normalized (spaces to underscores)
    cand = rid.replace(" ", "_")
    if cand in landed:
        return landed[cand]
    return None

with_out = {rid: b for rid, b in all_ids.items() if output_for(rid)}
without_out = {rid: b for rid, b in all_ids.items() if not output_for(rid)}
print(f"distinct ledger ask ids: {len(all_ids)}; ids with a landed output file: {len(with_out)}; without: {len(without_out)}")
cost_with = sum(b["cost"] for b in with_out.values())
cost_without = sum(b["cost"] for b in without_out.values())
print(f"cost on ids WITH landed output:    {money(cost_with)}")
print(f"cost on ids WITHOUT landed output: {money(cost_without)}")

print(f"\n-- ids WITHOUT landed output (the nothing), by cost desc --")
for rid, b in sorted(without_out.items(), key=lambda kv: -kv[1]["cost"]):
    print(f"  {rid[:60]:60s} rows={b['rows']:3d} cost={money(b['cost']):>8} ok={b['ok']:3d} bad={b['bad']:3d} dbl={b['dbl']:3d}")

# ---------- goodput ----------
print(f"\n== GOODPUT ==")
# definition: goodput = spend on rows whose ask id has a landed output file
#              (ok rows on landed ids); waste = everything else
good_cost = sum(r["cost_usd"] for r in rows if output_for(r["id"]) and r.get("ok"))
bad_on_landed = sum(r["cost_usd"] for r in rows if output_for(r["id"]) and not r.get("ok"))
dbl_cost_total = sum(r["cost_usd"] for r in rows if r.get("doubled_key"))
print(f"goodput spend (ok rows, landed ids):      {money(good_cost)}")
print(f"failed-spend on landed ids:               {money(bad_on_landed)}")
print(f"failed-spend on never-landed ids:         {money(cost_without - 0):>9} (approx; includes ok rows of ids whose output never landed)")
landed_files = sorted(p.name for p in OUTDIR.glob("*.md") if output_for(p.stem) or True)
# deliverable receipts = output files that are ask outputs; exclude the DAY1_* meta-receipts and *_ASSEMBLED rollups
deliverables = [p for p in OUTDIR.glob("*.md") if not p.stem.startswith("DAY1_") and not p.stem.endswith("_ASSEMBLED") and not p.stem.endswith("_JUDGE")]
print(f"ask-output deliverable files: {len(deliverables)} (of {len(landed)} total md files; DAY1_* and *_ASSEMBLED and *_JUDGE meta files excluded)")
print(f"cost per landed deliverable (total/deliverables): {money(tot_cost)} / {len(deliverables)} = {money(tot_cost/len(deliverables))}")
print(f"cost per usable finding (goodput-only view): {money(good_cost)} / {len(deliverables)} = {money(good_cost/len(deliverables))}")

# ---------- double-spend decomposition ----------
print(f"\n== DOUBLE-SPEND DECOMPOSITION ==")
# For each doubled row: was the FIRST banked row for (id,turn) ok or not?
first_seen = {}
for r in rows:
    k = (r["id"], r.get("turn"))
    if k not in first_seen:
        first_seen[k] = r
dbl_pure = 0.0; dbl_retry = 0.0; n_pure = 0; n_retry = 0
for r in rows:
    if not r.get("doubled_key"):
        continue
    k = (r["id"], r.get("turn"))
    first = first_seen.get(k)
    if first is not None and first.get("ok"):
        dbl_pure += r["cost_usd"]; n_pure += 1
    else:
        dbl_retry += r["cost_usd"]; n_retry += 1
print(f"doubled_key rows: {n_pure + n_retry} total {money(dbl_pure + dbl_retry)}")
print(f"  pure waste (first (id,turn) was ok=True): {n_pure} rows {money(dbl_pure)}")
print(f"  retry-after-fail (first ok=False):        {n_retry} rows {money(dbl_retry)}")

# twin window per the tool comment: 13 doubled keys / $2.25
dbl_rows = [r for r in rows if r.get("doubled_key")]
print(f"\nall doubled rows by day:")
by_d = collections.defaultdict(lambda: [0, 0.0])
for r in dbl_rows:
    d = r["ts"][:10]
    by_d[d][0] += 1
    by_d[d][1] += r["cost_usd"]
for d in sorted(by_d):
    print(f"  {d}: {by_d[d][0]} rows {money(by_d[d][1])}")

# first 13 doubled rows chronologically (the documented twin window)
first13 = sorted(dbl_rows, key=lambda r: r["ts"])[:13]
print(f"first 13 doubled rows sum: {money(sum(r['cost_usd'] for r in first13))} (window {first13[0]['ts']} .. {first13[-1]['ts']})")

# ---------- top burners ----------
print(f"\n== TOP 15 (id,turn) BURNERS ==")
agg = collections.defaultdict(lambda: {"n": 0, "cost": 0.0, "ok": 0, "dbl": 0})
for r in rows:
    k = (r["id"], r.get("turn"))
    a = agg[k]
    a["n"] += 1
    a["cost"] += r["cost_usd"]
    a["ok" if r.get("ok") else "bad"] += 0
    if r.get("ok"):
        a["ok"] += 1
    if r.get("doubled_key"):
        a["dbl"] += 1
for (rid, t), a in sorted(agg.items(), key=lambda kv: -kv[1]["cost"])[:15]:
    print(f"  {rid[:52]:52s} turn={t} fires={a['n']:3d} cost={money(a['cost']):>8} ok={a['ok']:3d} dbl={a['dbl']:3d}")

# ---------- refusal economics ----------
print(f"\n== REFUSAL ECONOMICS ==")
ref_rows = [r for r in rows if r.get("refused")]
print(f"refused rows: {len(ref_rows)} cost={money(sum(r['cost_usd'] for r in ref_rows))} (refused rows bill $0 per DAY1 receipt claim; verifying)")
nonzero_ref = [r for r in ref_rows if r["cost_usd"] > 0]
print(f"refused rows with nonzero cost: {len(nonzero_ref)}")
if nonzero_ref:
    for r in nonzero_ref[:10]:
        print(f"  {r['ts']} {r['id']} cost={money(r['cost_usd'])}")

# ---------- failed rows (ok=False, not refused, not doubled) ----------
print(f"\n== FAILURE ECONOMICS ==")
fail_rows = [r for r in rows if not r.get("ok")]
fail_nonref = [r for r in fail_rows if not r.get("refused")]
print(f"ok=False rows: {len(fail_rows)} cost={money(sum(r['cost_usd'] for r in fail_rows))}")
print(f"  of which refused: {len(ref_rows)} cost={money(sum(r['cost_usd'] for r in ref_rows))}")
print(f"  non-refused failures: {len(fail_nonref)} cost={money(sum(r['cost_usd'] for r in fail_nonref))}")
by_day_f = collections.defaultdict(lambda: [0, 0.0])
for r in fail_nonref:
    d = r["ts"][:10]
    by_day_f[d][0] += 1
    by_day_f[d][1] += r["cost_usd"]
for d in sorted(by_day_f):
    print(f"  {d}: {by_day_f[d][0]} rows {money(by_day_f[d][1])}")

print("\nDONE")
