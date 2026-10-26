# REV 2 scratch: FALSIFIER A at full scale - session-level attribution of write tokens
# over logs/provider_usage.jsonl. Read-only. Zero model calls.
# Pattern (the delete-2 signature): within one session_id, a row with a LARGE uncached
# prompt tail AFTER the session already established cache hits. Thresholds stated inline.
import json
from collections import defaultdict

PATH = r"C:/Users/foste/Documents/projects/local_sovereign_agent/logs/provider_usage.jsonl"
SPIKE_WRITE_FRAC = 0.50   # row write_tok >= 50% of its own prompt_tok
SPIKE_PROMPT_FLOOR = 2000 # and prompt_tok >= 2000 (ignore tiny rows)

def cached_of(r):
    c = (r.get("cache_hit_tokens") or 0) or (r.get("cached_tokens") or 0) \
        or (r.get("cache_read_tokens") or 0) or (r.get("cache_read_input_tokens") or 0)
    ptd = r.get("prompt_tokens_details") or {}
    if isinstance(ptd, dict):
        c = c or ptd.get("cached_tokens") or 0
    return c or 0

sessions = defaultdict(list)
agg_rows = 0
with open(PATH, encoding="utf-8", errors="replace") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except Exception:
            continue
        ts = str(r.get("ts") or r.get("timestamp") or "")
        if not (ts.startswith("2026-09") or ts.startswith("2026-10")):
            continue
        sid = r.get("session_id")
        if not sid:
            continue
        if r.get("ok") is False:
            continue
        if (r.get("calls") or 1) > 1:
            agg_rows += 1
        sessions[(str(r.get("provider") or "unknown").lower(), str(sid))].append(
            (ts, int(r.get("prompt_tokens") or 0), cached_of(r), str(r.get("model") or ""))
        )

stats = defaultdict(lambda: dict(sess2=0, spike_sess=0, coldstart_sess=0, max_spike_write=0))
examples = []
for (prov, sid), rows in sessions.items():
    if len(rows) < 2:
        continue
    rows.sort(key=lambda x: x[0])
    s = stats[prov]
    s["sess2"] += 1
    seen_hit = False
    spiked = False
    for i, (ts, pt, cached, model) in enumerate(rows):
        write = max(0, pt - cached)
        if cached > 0:
            seen_hit = True
        if i > 0 and seen_hit and pt >= SPIKE_PROMPT_FLOOR and write >= SPIKE_WRITE_FRAC * pt:
            spiked = True
            s["max_spike_write"] = max(s["max_spike_write"], write)
            if len(examples) < 12:
                examples.append((prov, sid[:18], ts, pt, cached, write, model[:24]))
    if spiked:
        s["spike_sess"] += 1
    else:
        # sessions with >=2 rows whose writes all sit before any hit = pure cold start
        first_hit = next((i for i, r_ in enumerate(rows) if r_[2] > 0), None)
        all_writes_early = all(
            max(0, rows[i][1] - rows[i][2]) < SPIKE_WRITE_FRAC * rows[i][1] or rows[i][1] < SPIKE_PROMPT_FLOOR
            for i in range(len(rows))
        )
        if all_writes_early:
            s["coldstart_sess"] += 1

print(f"FALSIFIER A, full scale, sessions grouped by (provider, session_id), Sep+Oct 2026")
print(f"thresholds: spike = write_tok >= {SPIKE_WRITE_FRAC:.0%} of row prompt AND prompt >= {SPIKE_PROMPT_FLOOR}, at row index > 0 after an established hit")
print(f"multi-call aggregated rows in scope: {agg_rows}")
print(f"{'provider':12} {'sess>=2rows':>11} {'spike_sess':>11} {'coldstart_only':>15} {'max_spike_write_tok':>19}")
tot2 = totspike = 0
for prov, s in sorted(stats.items(), key=lambda kv: -kv[1]["sess2"]):
    tot2 += s["sess2"]; totspike += s["spike_sess"]
    print(f"{prov:12} {s['sess2']:>11} {s['spike_sess']:>11} {s['coldstart_sess']:>15} {s['max_spike_write']:>19,}")
print(f"{'TOTAL':12} {tot2:>11} {totspike:>11}")
print("\nexample spike sessions (provider, session prefix, ts, prompt, cached, write, model):")
for e in examples:
    print(" ", e)
