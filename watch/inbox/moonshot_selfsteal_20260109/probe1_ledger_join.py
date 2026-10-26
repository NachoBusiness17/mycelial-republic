"""PROBE 1 - the three-ledger join (moonshot build order #1).

Joins hermes_burn usage.jsonl (cost) + burns LEDGER.jsonl (verdicts) +
disk_smith.jsonl (GB deltas) by UTC day and prints the first internal price
rows: dollars per green verdict vs dollars per vacuous day, plus GB/day.
Falsifier (Lane 2): if this cannot run in one sitting, tokens-are-disk is
poetry, not plumbing. Receipt-space; mint no tool until the join shape is
proven.
"""
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
USAGE = ROOT / "memory" / "runs" / "hermes_burn" / "usage.jsonl"
LEDGER = ROOT / "memory" / "burns" / "LEDGER.jsonl"
SMITH = ROOT / "logs" / "disk_smith.jsonl"
OUT = ROOT / "watch" / "inbox" / "moonshot_selfsteal_20260109" / "PROBE1_LEDGER_JOIN.md"

def day(ts):
    try:
        return datetime.fromisoformat(str(ts).replace("Z", "+00:00")).astimezone(timezone.utc).strftime("%Y-%m-%d")
    except Exception:
        return None

def load(path):
    try:
        return [json.loads(x) for x in path.read_text(errors="replace").splitlines() if x.strip()]
    except FileNotFoundError:
        return []

cost = defaultdict(float)
tokens = defaultdict(int)
for r in load(USAGE):
    d = day(r.get("ts"))
    if d:
        cost[d] += float(r.get("cost_usd") or 0)
        tokens[d] += int(r.get("prompt_tokens") or 0) + int(r.get("completion_tokens") or 0)

verd = defaultdict(lambda: defaultdict(int))
for r in load(LEDGER):
    d = day(r.get("ts"))
    if d:
        verd[d][str(r.get("verdict"))] += 1

smith = load(SMITH)
gb = {}
for i, r in enumerate(smith):
    d = day(r.get("ts"))
    if not d:
        continue
    gb[d] = r.get("free_gb")

days = sorted(set(cost) | set(verd) | set(gb))
lines = [
    "# PROBE 1 - three-ledger join - first internal price rows",
    f"moment: {datetime.now(timezone.utc).isoformat()}",
    f"rows: usage {sum(1 for _ in load(USAGE))}, ledger {sum(1 for _ in load(LEDGER))}, smith {len(smith)}",
    "",
    "| day | cost_usd | tokens | steal | green | vacuous | other | free_gb |",
    "|---|---|---|---|---|---|---|---|",
]
for d in days:
    v = verd.get(d, {})
    lines.append(f"| {d} | {cost.get(d, 0):.2f} | {tokens.get(d, 0)} | {v.get('steal', 0)} | {v.get('green', 0)} | {v.get('vacuous', 0)} | {sum(n for k, n in v.items() if k not in ('steal', 'green', 'vacuous'))} | {gb.get(d, '')} |")

green_days = [d for d in days if verd.get(d, {}).get("green", 0) > 0]
vac_days = [d for d in days if verd.get(d, {}).get("vacuous", 0) > 0]
tot_cost = sum(cost.values())
tot_green = sum(verd.get(d, {}).get("green", 0) for d in days)
tot_steal = sum(verd.get(d, {}).get("steal", 0) for d in days)
tot_vac = sum(verd.get(d, {}).get("vacuous", 0) for d in days)
lines += [
    "",
    "## The first price rows",
    f"- total measured cost: ${tot_cost:.2f} over {len(days)} days",
    f"- green verdicts: {tot_green}, steal: {tot_steal}, vacuous: {tot_vac}",
    f"- dollars per GREEN verdict (all-time): ${tot_cost / max(1, tot_green):.2f}",
    f"- dollars per STEAL verdict (all-time): ${tot_cost / max(1, tot_steal):.2f}",
    f"- cost on green-verdict days only: ${sum(cost.get(d, 0) for d in green_days):.2f} across {len(green_days)} days",
    f"- cost on vacuous-bearing days: ${sum(cost.get(d, 0) for d in vac_days):.2f} across {len(vac_days)} days",
    "",
    "## Gaps (a missing column is itself the finding)",
    "- smith rows exist only from 2026-10-09: GB/day rates need the daily cadence to accumulate",
    "- usage ledger covers Hermes-paid dispatch only; free-lane and account burn are separate ledgers (the join shape holds, the source list widens)",
]
OUT.write_text("\n".join(lines))
print("\n".join(lines[-12:]))
print("receipt:", OUT)
