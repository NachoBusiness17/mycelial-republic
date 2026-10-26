"""hermes-burn-economics lane audit v3: FINAL, pinned-moment economics.

Producer rule (ledger-internal, since mtimes only record last overwrite):
- producer of an (id,turn) key = its first ok=true fire
- pre-producer fires: billed -> failure bucket; $0 refused -> time-only bucket
- post-producer fires: re-fire waste bucket (the landed-beats-force law
  declares these pure re-burns)
Playground (TAVERN_/DND0_) repeats are run collisions (tools/tavern.py:157
drops the run id from the ask tag); each fire is a distinct game run with a
receipt dir under watch/inbox/playground/, so they are ledger-integrity
damage, not burn waste. Their in-run billed failures still count.
"""
import json
import collections
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
LEDGER = ROOT / "memory/runs/hermes_burn/usage.jsonl"
HERMES_OUT = ROOT / "watch/inbox/hermes_burn"
PLAYGROUND = ROOT / "watch/inbox/playground"
OURO = ROOT / "watch/inbox/gala_20260925/ouroboros"

rows = []
for line in LEDGER.open(encoding="utf-8"):
    line = line.strip()
    if line:
        rows.append(json.loads(line))
now = datetime.now(timezone.utc)
newest = max(r["ts"] for r in rows)
print(f"MOMENT pinned: run_at={now.strftime('%Y-%m-%dT%H:%M:%SZ')} ledger_rows={len(rows)} newest_row_ts={newest}")

def money(x):
    return f"${x:.4f}"

tot = sum(r["cost_usd"] for r in rows)
tot_pt = sum(r["prompt_tokens"] for r in rows)
tot_ct = sum(r["completion_tokens"] for r in rows)
tot_rt = sum(r.get("reasoning_tokens", 0) for r in rows)
print(f"TOTAL cost={money(tot)} prompt={tot_pt} completion={tot_ct} reasoning={tot_rt} tokens_all={tot_pt+tot_ct+tot_rt}")

print("\n== PER DAY ==")
by_day = collections.defaultdict(lambda: {"n": 0, "c": 0.0, "ok": 0, "bad": 0, "dbl": 0})
for r in rows:
    b = by_day[r["ts"][:10]]
    b["n"] += 1; b["c"] += r["cost_usd"]
    b["ok" if r.get("ok") else "bad"] += 1
    if r.get("doubled_key"): b["dbl"] += 1
for d in sorted(by_day):
    b = by_day[d]
    print(f"{d} rows={b['n']:4d} cost={money(b['c']):>9} ok={b['ok']:4d} bad={b['bad']:3d} doubled_flag={b['dbl']:3d}")

print("\n== PER MODEL ==")
by_m = collections.defaultdict(lambda: {"n": 0, "c": 0.0, "pt": 0, "ct": 0, "ok": 0, "bad": 0})
for r in rows:
    b = by_m[r["model"]]
    b["n"] += 1; b["c"] += r["cost_usd"]; b["pt"] += r["prompt_tokens"]; b["ct"] += r["completion_tokens"]
    b["ok" if r.get("ok") else "bad"] += 1
for m in sorted(by_m, key=lambda k: -by_m[k]["c"]):
    b = by_m[m]
    print(f"{m:30s} rows={b['n']:4d} cost={money(b['c']):>9} pt={b['pt']:9d} ct={b['ct']:8d} ok={b['ok']:4d} bad={b['bad']:3d}")

def is_play(rid):
    return rid.startswith(("TAVEN_", "TAVERN_", "DND0_"))

print("\n== PER PLAN FAMILY ==")
fam = collections.defaultdict(lambda: {"n": 0, "c": 0.0, "ids": set(), "ok": 0, "bad": 0})
def family(rid):
    if is_play(rid): return "PLAYGROUND(tavern+dnd0)"
    for p in ("A1", "A2", "A3", "B1", "B2", "C1", "D1", "D2", "D3", "DUEL1", "DUEL2", "DG1",
              "LENS1", "N1_", "N1R", "SP1", "SUBSTANCE", "T1W1", "T1W2", "T1W3", "T1R1",
              "T2SP2", "T2SP3", "T3R2", "GALA", "BARFIGHT", "DND_", "MOUNTAIN", "WILD",
              "KABUKI", "PARTYCHAT", "SEASON", "THE_", "WIRE", "SESSION"):
        if rid == p or rid.startswith(p):
            return p
    return rid.split("_")[0]
for r in rows:
    f = family(r["id"])
    b = fam[f]
    b["n"] += 1; b["c"] += r["cost_usd"]; b["ids"].add(r["id"])
    b["ok" if r.get("ok") else "bad"] += 1
for f in sorted(fam, key=lambda k: -fam[k]["c"]):
    b = fam[f]
    print(f"{f:24s} rows={b['n']:4d} ids={len(b['ids']):3d} cost={money(b['c']):>9} ok={b['ok']:4d} bad={b['bad']:3d}")

# ---------- producer-based buckets ----------
groups = collections.defaultdict(list)
for r in rows:
    groups[(r["id"], r.get("turn"))].append(r)
for k in groups:
    groups[k].sort(key=lambda r: r["ts"])

waste = 0.0; waste_n = 0
fail_billed = 0.0; fail_n = 0
refused_n = 0
waste_by_key = collections.defaultdict(float)
TWIN_KEYS = {("DUEL2_train_02_r2", 1), ("DUEL2_train_03_r2", 1), ("DUEL2_train_04_r2", 1),
             ("DUEL2_train_05_r2", 1), ("DUEL2_train_06_r2", 1), ("DUEL2_train_08_r2", 1),
             ("DUEL2_train_09_r2", 1), ("DUEL2_train_10_r2", 1), ("DUEL2_train_11_r2", 1),
             ("DUEL2_train_12_r2", 1), ("DUEL2_train_13_r2", 1), ("DUEL2_train_14_r2", 1),
             ("N1R_parables_songmap", 1)}
twin_waste = 0.0; twin_both = 0.0; twin_real = 0.0
for (rid, t), g in groups.items():
    producer_seen = False
    for r in g:
        if r.get("refused"):
            refused_n += 1
            continue
        if not r.get("ok"):
            fail_billed += r["cost_usd"]; fail_n += 1
            continue
        if not producer_seen:
            producer_seen = True
            if (rid, t) in TWIN_KEYS:
                twin_real += r["cost_usd"]; twin_both += r["cost_usd"]
            continue
        # post-producer fire = re-fire waste
        waste += r["cost_usd"]; waste_n += 1
        waste_by_key[rid] += r["cost_usd"]
        if (rid, t) in TWIN_KEYS:
            twin_waste += r["cost_usd"]; twin_both += r["cost_usd"]

print("\n== WASTE BUCKETS (producer rule) ==")
print(f"post-producer re-fire waste: {waste_n} fires {money(waste)}")
for rid in sorted(waste_by_key, key=lambda k: -waste_by_key[k]):
    print(f"  {rid[:52]:52s} {money(waste_by_key[rid])}")
print(f"pre-producer billed failures: {fail_n} fires {money(fail_billed)}")
print(f"refused ($0, time-only): {refused_n} fires")
print(f"TOTAL QUANTIFIED WASTE: {money(waste + fail_billed)} of {money(tot)} = {100*(waste+fail_billed)/tot:.1f} percent")

print("\n== DESCENT-TWIN WINDOW, byte-verified ==")
print(f"13 keys = DUEL2_train_02..14_r2 (12, no 07) + N1R_parables_songmap; fired in pairs 2026-10-01T21:40-21:54Z")
print(f"both-fires sum: {money(twin_both)}  (e3c7d341c documented: $2.25)")
print(f"single-pass real: {money(twin_real)}  (e3c7d341c documented: $1.09)")
print(f"twin excess (the actual double-spend): {money(twin_waste)}")

print("\n== PLAYGROUND COLLISION CLASS ==")
play = [r for r in rows if is_play(r["id"])]
play_dbl = [r for r in play if r.get("doubled_key")]
att = ROOT / "memory/attention.md"
n_alarm = sum(1 for l in att.open(encoding="utf-8", errors="replace") if "doubled-key alarm" in l)
print(f"play rows={len(play)} cost={money(sum(r['cost_usd'] for r in play))} distinct_ids={len(set(r['id'] for r in play))} doubled_flag={len(play_dbl)}")
print(f"doubled-key alarm lines in memory/attention.md: {n_alarm}")

print("\n== LANDING / RECEIPTS ==")
landed_hermes = {p.stem for p in HERMES_OUT.glob("*.md")}
run_dirs = sorted([d for d in PLAYGROUND.iterdir() if d.is_dir()]) if PLAYGROUND.exists() else []
ids = set(r["id"] for r in rows)
herm_ids = [i for i in ids if not is_play(i) and (i in landed_hermes or i.replace(" ", "_") in landed_hermes)]
play_ids = [i for i in ids if is_play(i)]
galaid_ok = [i for i in ids if i.startswith("GALA_")]
no_land = [i for i in ids if not (is_play(i) or i in landed_hermes or i.replace(" ", "_") in landed_hermes or i.startswith("GALA_"))]
print(f"distinct ask ids paid: {len(ids)}")
print(f"  landed in watch/inbox/hermes_burn/: {len(herm_ids)}")
print(f"  playground run receipts (per-run dirs): {len(run_dirs)} dirs for {len(play_ids)} collision ids")
print(f"  GALA ouroboros lane (sibling lane dir): {len(galaid_ok)} ids, dir exists={OURO.exists()}")
print(f"  NEVER landed anywhere: {no_land}")
deliverables = [p for p in HERMES_OUT.glob("*.md") if not p.stem.startswith("DAY1_") and not p.stem.endswith("_ASSEMBLED")]
units = len(deliverables) + len(run_dirs) + (1 if OURO.exists() else 0)
print(f"usable-finding units: {len(deliverables)} hermes deliverables + {len(run_dirs)} play runs + {1 if OURO.exists() else 0} ouroboros lane = {units}")
prod = tot - (waste + fail_billed)
print(f"goodput: productive spend {money(prod)} / total {money(tot)} = {100*prod/tot:.1f} percent")
print(f"cost per usable finding (total/units): {money(tot)}/{units} = {money(tot/units)}")
print(f"cost per usable finding (productive/units): {money(prod)}/{units} = {money(prod/units)}")
print("\nDONE_V3")
