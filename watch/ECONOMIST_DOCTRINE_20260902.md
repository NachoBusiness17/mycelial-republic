# ECONOMIST DOCTRINE — 24-72h LANE TABLE (2026-09-02, deepseek pipe)
*Summoned by operator for the long-haul ride. Raw verdict below, receipts in room.jsonl + CONVO.md. Claude lane fact folded per operator receipt 09-02. Adapt note: zai_burn_guard shape is right — wire it through covenant.json (single source) + providers.py tier gate, not env-blanking.*

---

## VERDICT: Reset is a 24-72h gift. Spend it on **deepseek pennies + Claude cache-mining**, NOT zai-pro. Zai-pro is your **judgment-beat escape hatch** only. One gate: **`zai_burn_guard.py`** at cron+entrypoint. One meter: **`/tmp/zai_burn_meter.json`** posted to operator webchat every 15min.

---

### (1) LANE PER SURFACE — 24-72h TABLE

| Surface | Lane | Why | Cap (per 24h) | Notes |
|---|---|---|---|---|
| **Operator interactive** | deepseek (primary) | 917ms, zero aborts, pennies | 2M tok | Keep zai-pro as manual fallback ONLY if deepseek 429s >3x in 5min |
| **Seat-farm labor** (cron, bulk) | **Claude** (NEW) | Cheapest cache-read at bulk; see §3 | 5M tok read / 500K write | Verify auth/model/caps FIRST (see §5 debts) |
| **Bulk drains** (Rashomon rebuild, steer-gate) | deepseek (batch) | 42M tok = $0.84 vs zai $14.4K | 10M tok/day | Split into ≤2M chunks, 5min apart |
| **Judgment beats** (hard eval, one-shot) | **zai-pro Max** | $0 marginal, 1600 prompts/5hr | 50 prompts/day | NEVER cron. Manual only. Operator types "JUDGE" |
| **Free lanes** (zai-2/3/4) | idle | 429 reset landed; don't touch | 0 | Let them cool 24h. They're your 429-1310 canary |

---

### (2) ZAI LANE SPEND — WITHOUT RE-TRIGGERING 429-1310

| Lane | Hourly cap | Daily cap | Safe spend pattern |
|---|---|---|---|
| zai-2/3/4 (coding) | 200 prompts/hr | 1,600 prompts/day | **ZERO for 24h**. Then 50/hr max, spread 5min apart |
| zai-pro Max | 1600 prompts/5hr | ~7,600/day | **≤10 prompts/hr**, only for JUDGE beats. Never batch |
| zai Lite | unknown | unknown | **Do not use** until verified (see §5) |

**429-1310 wall math:** The 12:52 reset gives you ~1,600 prompts on zai-2/3/4. If you burn >200/hr, you hit the wall again. **Rule: 50/hr max, 5min spacing, hard stop at 200/day.** The wall is per-hour AND per-day — both reset independently. Treat the daily as the binding constraint.

---

### (3) ZAI-PRO MAX vs DEEPSEEK PENNIES vs CLAUDE

| Metric | zai-pro Max | deepseek | **Claude** (NEW) |
|---|---|---|---|
| Marginal cost | **$0** (Max plan) | ~$0.02/M tok | ~$0.005/M tok read (cache) |
| Cache read | N/A (no cache) | N/A | **~$0.005/M** (vs $0.03 write) |
| Cache write | N/A | N/A | ~$0.03/M (expensive — batch writes) |
| Latency | ~1-2s | 917ms | ~1.5s |
| Rate limit | 1600/5hr | none known | ~100 req/min (verify) |
| **Bulk-cron fit** | ❌ (rate wall) | ✅ (cheap, no wall) | ✅✅ (cheapest cache-read) |
| **Judgment fit** | ✅✅ (only use) | ❌ (weak on hard evals) | ⚠️ (good but unproven) |

**Claude economics:** Cache reads at ~$0.005/M tok are **4x cheaper than deepseek** for bulk cron. But cache writes are 6x more expensive. **Pattern: write cache once (Rashomon invariant), read 100x.** This is your bulk-drain lane for the rebuild docket.

---

### (4) ONE MECHANICAL GATE — `zai_burn_guard.py`

```python
#!/usr/bin/env python3
# /usr/local/bin/zai_burn_guard.py — run at cron START and entrypoint
import json, os, time, sys

METER = "/tmp/zai_burn_meter.json"
DAILY_LIMIT = 200  # prompts on zai-2/3/4, hard stop
PRO_LIMIT = 50     # zai-pro Max, manual only

def load():
    try:
        with open(METER) as f: return json.load(f)
    except: return {"date": time.strftime("%Y-%m-%d"), "zai": 0, "pro": 0}

def check():
    m = load()
    if m["date"] != time.strftime("%Y-%m-%d"):
        m = {"date": time.strftime("%Y-%m-%d"), "zai": 0, "pro": 0}
    # Gate: if zai > DAILY_LIMIT, force deepseek
    if m["zai"] >= DAILY_LIMIT:
        os.environ["ZAI_API_KEY"] = ""  # blank it — cron falls to deepseek
        print("ZAI_BURN_GUARD: daily limit hit, forcing deepseek")
        sys.exit(1)  # cron sees non-zero, aborts zai path
    # Gate: pro only if JUDGE env var set (operator types it)
    if "JUDGE" not in os.environ and m["pro"] >= PRO_LIMIT:
        os.environ["ZAI_API_KEY_Pro"] = ""
        print("ZAI_BURN_GUARD: pro limit hit, manual only")
        sys.exit(1)

def increment(lane):
    m = load()
    m[lane] += 1
    with open(METER, "w") as f: json.dump(m, f)

if __name__ == "__main__":
    if sys.argv[1] == "check": check()
    elif sys.argv[1] == "inc": increment(sys.argv[2])
```

**Cron wiring:** `*/5 * * * * /usr/local/bin/zai_burn_guard.py check && /path/to/job` — if guard exits 1, cron aborts before touching zai. **Entrypoint:** add `python3 /usr/local/bin/zai_burn_guard.py check` before any agent spawn. This is structural — no prose, no "remember to check."

---

### (5) THE ONE METER — POST TO OPERATOR WEBChat EVERY 15MIN

**Meter:** `/tmp/zai_burn_meter.json` (same file as gate). **Poster:** cron `*/15 * * * *` runs:

```bash
python3 -c "
import json
m = json.load(open('/tmp/zai_burn_meter.json'))
msg = f'ZAI BURN: {m[\"zai\"]}/200 daily | PRO: {m[\"pro\"]}/50 | deepseek: OK | Claude: OK'
# POST to operator webchat (existing webhook)
curl -s -X POST https://operator-webchat/webhook -d '{\"text\": \"'$msg'\"}'
"
```

**Why this meter:** It's the same file the gate reads — **one source of truth**. If the gate blanks the key, the meter shows it. Operator sees the number every 15min, never dark. Post it to the **same webchat the operator pinged at 13:08Z** — that's the proven channel.

---

### CLAUDE LANE VERIFICATION DEBTS (cheap, next steps)

| Debt | Action | Cost | Time |
|---|---|---|---|
| Auth | Verify ANTHROPIC_API_KEY in .env, test `curl /v1/messages` | $0.01 | 2min |
| Model IDs | Confirm `claude-3-5-sonnet-20240620` (or latest) accepts cache_control | $0.01 | 2min |
| Quota/rate | Check `/v1/models` + docs; test 100 req/min burst | $0.05 | 5min |
| Bounded completion | One 1K-tok completion with cache write, then read — measure $ | $0.05 | 5min |

**Total: ~$0.12, 15min.** Do this BEFORE any bulk cron. If Claude fails auth, the lane table collapses — deepseek absorbs until fixed.

---

### 24-72H ACTION SEQUENCE

| Time | Action |
|---|---|
| **Now** | Deploy `zai_burn_guard.py`, wire cron+entrypoint, start meter poster |
| **+15min** | Claude verification debts (4 steps above) |
| **+1h** | Rashomon rebuild on deepseek (2M tok chunks, 5min apart) |
| **+24h** | If zai-2/3/4 stable (no 429), start 50/hr test on coding lanes |
| **+48h** | Claude bulk-cron cache-mining live (write once, read 100x) |
| **+72h** | Review meter: if zai < 50/day, keep guard; if >150, tighten to 100/day |

**Bottom line:** The reset is a 72h window. Deepseek + Claude do the heavy lifting. Zai-pro is your scalpel for judgment beats only. The guard is the wall. The meter is the light. Operator never goes dark again.