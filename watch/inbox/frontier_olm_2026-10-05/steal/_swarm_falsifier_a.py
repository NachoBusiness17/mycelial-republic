# STEAL CARD swarm-orchestration via x - FALSIFIER A: MODEL-SWITCH CENSUS.
# Read-only over logs/provider_usage.jsonl. Zero model calls. Zero subprocess spawns.
# Question (avichawla find): does the estate's own telemetry show MID-SESSION model
# switches, and do the switch rows carry the cold-rebill signature (write_tok >= 50%
# of prompt on the first row at the new model, prompt >= 2000)? The kv-card
# falsifier (_kv_falsifier_a.py) grouped by (provider, session_id), which by
# construction CANNOT see a model switch inside one session; this script groups by
# session_id ALONE, so a switch is visible as a second distinct model in the group.
import json
from collections import defaultdict

PATH = r"C:/Users/foste/Documents/projects/local_sovereign_agent/logs/provider_usage.jsonl"
COLD_WRITE_FRAC = 0.50   # switch-row write_tok >= 50% of its own prompt
COLD_PROMPT_FLOOR = 2000 # and prompt_tok >= 2000 (ignore tiny rows)

def cached_of(r):
    c = (r.get("cache_hit_tokens") or 0) or (r.get("cached_tokens") or 0) \
        or (r.get("cache_read_tokens") or 0) or (r.get("cache_read_input_tokens") or 0)
    ptd = r.get("prompt_tokens_details") or {}
    if isinstance(ptd, dict):
        c = c or ptd.get("cached_tokens") or 0
    return c or 0

sessions = defaultdict(list)
n_rows = 0
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
        n_rows += 1
        sessions[str(sid)].append(
            (ts, str(r.get("provider") or "unknown").lower(),
             str(r.get("model") or ""), int(r.get("prompt_tokens") or 0),
             cached_of(r))
        )

multi = []          # sessions with >= 2 distinct (provider, model) pairs
switch_cold = []    # switch rows carrying the cold signature
switch_warm = 0     # switch rows WITHOUT the cold signature (cheap switch or no telemetry)
models_hist = defaultdict(int)
for sid, rows in sessions.items():
    if len(rows) < 2:
        continue
    rows.sort(key=lambda x: x[0])
    seen = set()
    distinct = {(p, m) for _, p, m, _, _ in rows}
    if len(distinct) < 2:
        continue
    multi.append((sid, distinct, len(rows)))
    models_hist[len(distinct)] += 1
    seen = set()
    for ts, p, m, pt, cached in rows:
        key = (p, m)
        if key in seen:
            continue
        if seen:  # this row is the FIRST at a NEW model, session already warm elsewhere
            write = max(0, pt - cached)
            if pt >= COLD_PROMPT_FLOOR and write >= COLD_WRITE_FRAC * pt:
                switch_cold.append((sid[:18], ts, p, m[:28], pt, cached, write))
            else:
                switch_warm += 1
        seen.add(key)

print(f"MODEL-SWITCH CENSUS over logs/provider_usage.jsonl, Sep+Oct 2026, ok rows with session_id: {n_rows}")
print(f"sessions (>=2 rows) with >=2 distinct (provider,model): {len(multi)}")
print(f"distinct-model-count histogram: {dict(sorted(models_hist.items()))}")
print(f"switch rows WITH cold signature (write>={COLD_WRITE_FRAC:.0%} of prompt, prompt>={COLD_PROMPT_FLOOR}): {len(switch_cold)}")
print(f"switch rows WITHOUT cold signature: {switch_warm}")
print("\ncold-signature switch rows (session prefix, ts, provider, model, prompt, cached, write):")
for e in switch_cold[:20]:
    print(" ", e)
print("\nall multi-model sessions (session prefix, models, rows):")
for sid, distinct, n in sorted(multi, key=lambda x: -x[2])[:15]:
    print(" ", sid[:18], sorted(distinct), n)
