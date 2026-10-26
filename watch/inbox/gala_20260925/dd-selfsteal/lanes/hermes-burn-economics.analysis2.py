"""hermes-burn-economics lane audit v2: waste decomposition.

Corrections over v1:
- TAVERN_/DND0_ repeated ids are RUN COLLISIONS (tools/tavern.py:157 drops
  the run id; each fire is a distinct game run with its own receipt dir in
  watch/inbox/playground/), so they are ledger-integrity damage, not burn
  waste.
- Output landing is checked across watch/inbox/hermes_burn/ AND
  watch/inbox/playground/ AND the GALA ouroboros lane dir.
- Twin window: (id,turn) groups with a near-simultaneous second fire
  (delta < 600s), the descent-twins signature, verified from bytes.
"""
import json
import collections
from datetime import datetime
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

def ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))

def money(x):
    return f"${x:.4f}"

tot = sum(r["cost_usd"] for r in rows)
print(f"rows={len(rows)} total_cost={money(tot)}")

# ---------- landing classification ----------
landed_hermes = {p.stem for p in HERMES_OUT.glob("*.md")}
run_dirs = sorted([d for d in PLAYGROUND.iterdir() if d.is_dir()]) if PLAYGROUND.exists() else []
tavern_runs = [d for d in run_dirs if d.name.startswith("tavern_")]
dnd_runs = [d for d in run_dirs if d.name.startswith("dnd0_")]
print(f"hermes_burn md files={len(landed_hermes)} playground run dirs={len(run_dirs)} (tavern={len(tavern_runs)} dnd0={len(dnd_runs)})")
print(f"ouroboros lane dir exists={OURO.exists()}")

PLAY_IDS = ("TAVERN_", "DND0_")
def is_play(rid):
    return rid.startswith(PLAY_IDS)

def landed(rid):
    if is_play(rid):
        return True  # receipts live per-run in playground dirs (verified: DONE+GWAP_BANKED+transcript)
    if rid in landed_hermes or rid.replace(" ", "_") in landed_hermes:
        return True
    if rid.startswith("GALA_") and OURO.exists():
        return True
    return False

# ---------- (id,turn) groups ----------
groups = collections.defaultdict(list)
for r in rows:
    groups[(r["id"], r.get("turn"))].append(r)
for k in groups:
    groups[k].sort(key=lambda r: r["ts"])

print("\n== REFIRE EXCESS, NON-PLAYGROUND IDS ==")
excess_rows = []  # (row, kind) kind in twin/late
for (rid, t), g in groups.items():
    if is_play(rid) or len(g) == 1:
        continue
    for prev, cur in zip(g, g[1:]):
        delta = (ts(cur["ts"]) - ts(prev["ts"])).total_seconds()
        excess_rows.append((cur, delta, rid, t))
twin = [e for e in excess_rows if e[1] < 600]
late = [e for e in excess_rows if e[1] >= 600]
print(f"non-play excess fires: {len(excess_rows)} = {money(sum(e[0]['cost_usd'] for e in excess_rows))}")
print(f"  twin (delta<600s): {len(twin)} fires {money(sum(e[0]['cost_usd'] for e in twin))}")
print(f"  late refire:       {len(late)} fires {money(sum(e[0]['cost_usd'] for e in late))}")
print("twin fires detail:")
for cur, delta, rid, t in sorted(twin, key=lambda e: e[0]["ts"]):
    print(f"  {cur['ts'][:19]}Z +{delta:7.0f}s {rid} turn={t} ok={cur.get('ok')} cost={money(cur['cost_usd'])}")

print("\n-- A1_steer_antiforgery fire span --")
a1 = [r for r in rows if r["id"] == "A1_steer_antiforgery"]
a1.sort(key=lambda r: r["ts"])
print(f"fires={len(a1)} cost={money(sum(r['cost_usd'] for r in a1))} first={a1[0]['ts'][:19]}Z last={a1[-1]['ts'][:19]}Z")
print(f"first-fire cost={money(a1[0]['cost_usd'])} -> excess={money(sum(r['cost_usd'] for r in a1) - a1[0]['cost_usd'])}")

print("\n== THE DESCENT-TWIN WINDOW (13 doubled keys / $2.25 per e3c7d341c) ==")
tw = [e for e in twin if e[0]["ts"] < "2026-10-02"]
tw_keys = sorted(set((e[2], e[3]) for e in tw))
tw_cost_all = 0.0
for (rid, t) in tw_keys:
    g = groups[(rid, t)]
    tw_cost_all += sum(r["cost_usd"] for r in g)
print(f"twin-window keys (delta<600s, pre-10-02): {len(tw_keys)} keys")
print(f"sum of BOTH fires for those keys: {money(tw_cost_all)}")
tw_excess = sum(e[0]["cost_usd"] for e in tw)
print(f"excess (second-fire) sum: {money(tw_excess)}")
for (rid, t) in tw_keys:
    g = groups[(rid, t)]
    print(f"  {rid} turn={t} fires={len(g)} both={money(sum(r['cost_usd'] for r in g))} first={money(g[0]['cost_usd'])}")

print("\n== STUB / FAILURE SPEND (ok=False rows that billed) ==")
fail_billed = [r for r in rows if not r.get("ok") and r["cost_usd"] > 0]
print(f"ok=False rows: {sum(1 for r in rows if not r.get('ok'))}; billed: {len(fail_billed)} sum={money(sum(r['cost_usd'] for r in fail_billed))}")
for r in fail_billed:
    print(f"  {r['ts'][:19]}Z {r['id'][:50]:50s} {r['model']} cost={money(r['cost_usd'])} note={r.get('note','')[:60]}")
ref = [r for r in rows if r.get("refused")]
print(f"refused rows: {len(ref)} sum={money(sum(r['cost_usd'] for r in ref))} (verify $0)")

print("\n== PLAYGROUND RUN-COLLISION CLASS ==")
play_rows = [r for r in rows if is_play(r["id"])]
play_dbl = [r for r in play_rows if r.get("doubled_key")]
print(f"play rows={len(play_rows)} cost={money(sum(r['cost_usd'] for r in play_rows))} doubled_flag={len(play_dbl)} ({money(sum(r['cost_usd'] for r in play_dbl))})")
print(f"distinct play ids={len(set(r['id'] for r in play_rows))}; runs landed={len(run_dirs)}")

print("\n== ATTENTION ALARM COUNT ==")
att = ROOT / "memory/attention.md"
n_alarm = sum(1 for l in att.open(encoding="utf-8", errors="replace") if "doubled-key alarm" in l)
print(f"doubled-key alarm lines in memory/attention.md: {n_alarm}")

print("\n== WASTE LEDGER (final) ==")
a1_excess = sum(r["cost_usd"] for r in a1) - a1[0]["cost_usd"]
twin_excess_w = sum(e[0]["cost_usd"] for e in tw)
twin_excess_post = sum(e[0]["cost_usd"] for e in twin if e[0]["ts"] >= "2026-10-02")
stub = sum(r["cost_usd"] for r in fail_billed)
late_excess = sum(e[0]["cost_usd"] for e in late)
# overlap guard: A1 excess fires are late-refires; subtract from late
late_only = late_excess - a1_excess
print(f"1. day-1 re-fire theater on landed asks (incl A1 excess {money(a1_excess)}): {money(late_excess)}")
print(f"2. descent-twin double-spend (pre-10-02 twin excess):  {money(twin_excess_w)}  (ask's $2.25 framing = both fires; excess = total - real)")
print(f"3. post-10-02 twin excess:                              {money(twin_excess_post)}")
print(f"4. stub/failed billed spend:                            {money(stub)}")
print(f"total quantified waste: {money(late_excess + twin_excess_w + twin_excess_post + stub)}")
print(f"  (overlap note: A1 excess is inside item 1; twin items exclude playground collisions)")
print("\nDONE_V2")
