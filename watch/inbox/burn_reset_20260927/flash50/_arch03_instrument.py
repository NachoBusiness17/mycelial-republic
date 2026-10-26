"""arch-03 instrument: parse stealth_driver runtime state for the v2 design.

Reads (never writes) the live state surfaces:
  state/fuel/stealth_driver.jsonl       heartbeat rows (cycle wall time, topic values)
  state/fuel/stealth_work_queue.jsonl   work queue growth + drain
  state/fuel/stealth_selfimp_queue.jsonl self-build queue
  state/fuel/stealth_work_state.json    lane spacing + errors + cache stats
  watch/inbox/STEALTH_MINED_FINDINGS.jsonl mined findings register
"""
from __future__ import annotations

import json
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = []


def say(line: str = "") -> None:
    OUT.append(line)


def parse_ts(s: str):
    return datetime.fromisoformat(s)


# ---- heartbeat -------------------------------------------------------------
hb = ROOT / "state" / "fuel" / "stealth_driver.jsonl"
rows = []
for line in hb.read_text(encoding="utf-8").splitlines():
    if line.strip():
        rows.append(json.loads(line))
say(f"heartbeat rows: {len(rows)}")
if rows:
    say(f"first row ts: {rows[0]['ts']}")
    say(f"last  row ts: {rows[-1]['ts']}")
    # cycle wall time: consecutive deltas (only within same-run cycle numbers
    # is unreliable across restarts; report all deltas + within-run deltas)
    deltas = []
    for a, b in zip(rows, rows[1:]):
        dt = (parse_ts(b["ts"]) - parse_ts(a["ts"])).total_seconds()
        deltas.append(dt)
    within = []
    for a, b in zip(rows, rows[1:]):
        if b["cycle"] == a["cycle"] + 1:
            within.append((parse_ts(b["ts"]) - parse_ts(a["ts"])).total_seconds())
    say(f"all consecutive deltas (s): n={len(deltas)} min={min(deltas):.0f} "
        f"med={sorted(deltas)[len(deltas)//2]:.0f} max={max(deltas):.0f}")
    if within:
        sw = sorted(within)
        say(f"within-run deltas (s): n={len(within)} min={sw[0]:.0f} "
            f"med={sw[len(sw)//2]:.0f} max={sw[-1]:.0f} "
            f"ge300={sum(1 for d in sw if d >= 300)} ge600={sum(1 for d in sw if d >= 600)}")
    # topic error/skip census
    stat = Counter()
    skip = Counter()
    for r in rows:
        for name, val in r["topics"].items():
            v = str(val)
            if v.startswith("ERR "):
                stat[f"{name}:ERR"] += 1
            elif v.startswith("skip"):
                skip[name] += 1
            else:
                stat[f"{name}:ok"] += 1
    say("topic outcomes:")
    for k, v in sorted(stat.items()):
        say(f"  {k} = {v}")
    say("topic skips:")
    for k, v in sorted(skip.items()):
        say(f"  {k} = {v}")
    # last heartbeat full row (what live output looks like)
    say("last heartbeat row (pretty):")
    say(json.dumps(rows[-1], indent=1)[:2200])

# ---- work queue ------------------------------------------------------------
wq = ROOT / "state" / "fuel" / "stealth_work_queue.jsonl"
wrows = []
for line in wq.read_text(encoding="utf-8").splitlines():
    if line.strip():
        wrows.append(json.loads(line))
say(f"\nwork queue rows: {len(wrows)}")
open_rows = [r for r in wrows if not r.get("done_ts")]
sensed = [r for r in wrows if r.get("status") == "sensed"]
selffed = [r for r in wrows if r.get("selffed_ts")]
done = [r for r in wrows if r.get("done_ts")]
say(f"  open (no done_ts): {len(open_rows)}")
say(f"  sensed: {len(sensed)}  done: {len(done)}  selffed-origin: {len(selffed)}")
say(f"  distinct ids: {len(set(r.get('id') for r in wrows))}")
tiers = Counter(r.get("tier") or "free" for r in wrows)
say(f"  tiers: {dict(tiers)}")
for r in wrows:
    tag = "SELFFED" if r.get("selffed_ts") else "manual  "
    st = r.get("status", "open")
    say(f"  [{tag}] {r.get('id')}: status={st} tier={r.get('tier')} "
        f"ask={str(r.get('ask'))[:60]!r}")

# ---- selfimp queue ---------------------------------------------------------
sq = ROOT / "state" / "fuel" / "stealth_selfimp_queue.jsonl"
srows = []
if sq.is_file():
    for line in sq.read_text(encoding="utf-8").splitlines():
        if line.strip():
            srows.append(json.loads(line))
sopen = [r for r in srows if not r.get("done_ts")]
say(f"\nselfimp queue rows: {len(srows)} open={len(sopen)}")
for r in srows[:6]:
    say(f"  {r.get('id')}: done={bool(r.get('done_ts'))} "
        f"task={str(r.get('task'))[:60]!r}")

# ---- work state (lanes) ----------------------------------------------------
ws = ROOT / "state" / "fuel" / "stealth_work_state.json"
if ws.is_file():
    st = json.loads(ws.read_text(encoding="utf-8"))
    lanes = st.get("last_lane_ts", {})
    errs = st.get("lane_errors", {})
    cache = st.get("cache_stats", [])
    say(f"\nwork_state: lanes touched={len(lanes)} lane_errors={len(errs)} "
        f"cache_stats_rows={len(cache)}")
    for k, v in sorted(errs.items()):
        say(f"  ERR {k}: {v[:110]}")
    fin = Counter(str(c.get("finish")) for c in cache)
    say(f"  cache_stats finishes: {dict(fin)}")
    ct = [c.get("cached_tokens") for c in cache if c.get("cached_tokens")]
    if ct:
        say(f"  cached_tokens seen: n={len(ct)} min={min(ct)} max={max(ct)}")

# ---- mined findings --------------------------------------------------------
mf = ROOT / "watch" / "inbox" / "STEALTH_MINED_FINDINGS.jsonl"
mrows = []
for line in mf.read_text(encoding="utf-8", errors="replace").splitlines():
    if line.strip():
        mrows.append(json.loads(line))
say(f"\nmined findings rows: {len(mrows)}")
lane_c = Counter(r.get("lane") for r in mrows)
fin_c = Counter(str(r.get("finish")) for r in mrows)
say(f"  by lane: {dict(lane_c)}")
say(f"  by finish: {dict(fin_c)}")
pa_total = 0
pa_ok = 0
for r in mrows:
    audit = r.get("ponytail_audit") or {}
    for v in audit.values():
        pa_total += 1
        pa_ok += 1 if v else 0
say(f"  ponytail audit path checks: total={pa_total} ok={pa_ok} "
    f"({(100*pa_ok/pa_total):.0f}% exist) " if pa_total else
    f"  ponytail audit path checks: total=0")
tail_banked = sum(1 for r in mrows if "reasoning" in str(r.get("finish")))
say(f"  reasoning-tail banked rows: {tail_banked}")

print("\n".join(OUT))
