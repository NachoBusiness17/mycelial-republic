# W5 T22 verifier: recompute the urgency density curve from raw corpora and
# diff against the filed artifact memory/runs/the50/w5_t22_urgency_curve.json.
# Run: .venv/Scripts/python.exe _w5_t22_verify.py
import json, re, sys
from collections import defaultdict

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
QDROPS = ROOT + r"\watch\inbox\qdrop_export\qdrops.jsonl"
# the filed artifact's pool_reproduction_check.pool_ledger names ledger.jsonl
POOL = ROOT + r"\watch\inbox\mrpool_export\ledger.jsonl"
POOL_FULL = ROOT + r"\watch\inbox\mrpool_export\ledger_full.jsonl"
ART = ROOT + r"\memory\runs\the50\w5_t22_urgency_curve.json"

TERMS = ["near", "soon", "final", "countdown", "it begins", "happening",
         "no more time", "finish", "storm", "judgment", "release", "alive",
         "tick tock", "end draws"]
WORD_PATS = [re.compile(r"\b" + re.escape(t) + r"\b", re.IGNORECASE) for t in TERMS]
SUB_PATS = [re.compile(re.escape(t), re.IGNORECASE) for t in TERMS]

def month_of(ts):
    return ts[:7]

def density_rows(rows, variant):
    """rows: list of (month, text). variant: 'word'|'sub'."""
    pats = WORD_PATS if variant == "word" else SUB_PATS
    per = defaultdict(lambda: [0, 0])  # month -> [n_posts, n_urgency]
    for m, text in rows:
        per[m][0] += 1
        if any(p.search(text) for p in pats):
            per[m][1] += 1
    return {m: {"n_posts": v[0], "n_urgency": v[1],
                "density": round(v[1] / v[0], 4) if v[0] else 0.0}
            for m, v in sorted(per.items())}

def summarize(monthly):
    tot_p = sum(v["n_posts"] for v in monthly.values())
    tot_u = sum(v["n_urgency"] for v in monthly.values())
    dens = [v["density"] for v in monthly.values()]
    mx = max(monthly.items(), key=lambda kv: kv[1]["density"])
    return {"months": len(monthly),
            "first_month": min(monthly), "last_month": max(monthly),
            "total_posts": tot_p, "total_urgency_posts": tot_u,
            "overall_density": round(tot_u / tot_p, 4) if tot_p else 0.0,
            "max_month": mx[0], "max_density": mx[1]["density"],
            "mean_density": round(sum(dens) / len(dens), 4) if dens else 0.0,
            "months_over_10pct": sorted(m for m, v in monthly.items() if v["density"] > 0.10),
            "months_at_zero": sorted(m for m, v in monthly.items() if v["density"] == 0.0)}

def diff(label, mine, filed):
    """Month-level diff; returns (max_abs_delta, mismatches)."""
    keys = set(mine) | set(filed)
    missing = sorted(k for k in keys if k not in mine or k not in filed)
    maxd, bad = 0.0, []
    for k in sorted(set(mine) & set(filed)):
        for f in ("n_posts", "n_urgency"):
            d = abs(mine[k][f] - filed[k][f])
            if d > maxd:
                maxd = d
            if d:
                bad.append(f"{label} {k} {f}: mine={mine[k][f]} filed={filed[k][f]}")
        dd = abs(mine[k]["density"] - filed[k]["density"])
        if dd > maxd:
            maxd = dd
        if dd > 1e-9:
            bad.append(f"{label} {k} density: mine={mine[k]['density']} filed={filed[k]['density']}")
    if missing:
        bad.append(f"{label} month keys not in both: {missing}")
    return maxd, bad

out = {"checks": [], "failed": False}

# --- Q corpus ---
q_all, q_auth = [], []
with open(QDROPS, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        m = month_of(r["ts"])
        text = r.get("text") or ""
        q_all.append((m, text))
        if (r.get("name") or "").strip() == "Q":
            q_auth.append((m, text))

out["rows_total"] = len(q_all)
out["rows_q_authored"] = len(q_auth)

# --- Pool corpus ---
pool = []
with open(POOL, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        pool.append((month_of(r["date"]), r.get("text") or ""))
out["pool_rows"] = len(pool)

# --- recompute all series ---
mine_q_word = density_rows(q_auth, "word")
mine_q_sub = density_rows(q_auth, "sub")
mine_all_word = density_rows(q_all, "word")
mine_pool_word = density_rows(pool, "word")
s_q_word, s_q_sub = summarize(mine_q_word), summarize(mine_q_sub)
s_all_word, s_pool_word = summarize(mine_all_word), summarize(mine_pool_word)

art = json.load(open(ART, encoding="utf-8"))
fs = art["primary_series"]["monthly"]
fcx = art["context_series"]

def check(name, cond, detail):
    out["checks"].append({"check": name, "pass": bool(cond), "detail": detail})
    if not cond:
        out["failed"] = True

# 1. corpus row counts vs receipt/filed
check("q_rows_total_6242", len(q_all) == 6242, f"loaded {len(q_all)}")
check("q_authored_4705", len(q_auth) == 4705, f"name.strip()=='Q' -> {len(q_auth)}")
check("pool_rows_3663", len(pool) == 3663, f"loaded {len(pool)}")

# 2. primary series month-level diff
d1, bad1 = diff("q_authored_word", mine_q_word, fs)
check("primary_series_month_match", d1 == 0 and not bad1, f"max_abs_delta={d1}; issues={bad1[:8]}")

# 3. primary summary vs filed
fsum = art["primary_series"]["summary"]
for k in ("months", "total_posts", "total_urgency_posts", "overall_density",
          "max_month", "max_density", "mean_density"):
    check(f"primary_summary.{k}", s_q_word[k] == fsum[k], f"mine={s_q_word[k]} filed={fsum[k]}")

# 4. context series: q_full_corpus_word
d2, bad2 = diff("q_full_corpus_word", mine_all_word, fcx["q_full_corpus_word"]["monthly"])
check("context_q_full_corpus_word", d2 == 0 and not bad2, f"max_abs_delta={d2}; issues={bad2[:8]}")
d3, bad3 = diff("q_authored_sub", mine_q_sub, fcx["q_authored_sub"]["monthly"])
check("context_q_authored_sub", d3 == 0 and not bad3, f"max_abs_delta={d3}; issues={bad3[:8]}")
d4, bad4 = diff("pool_word_reproduction", mine_pool_word, fcx["pool_word_reproduction"]["monthly"])
check("context_pool_word", d4 == 0 and not bad4, f"max_abs_delta={d4}; issues={bad4[:8]}")

# 5. filed-claim rechecks (recomputed here)
never_over = all(v["density"] <= 0.10 for v in s_q_word and mine_q_word.values())
mx = max(mine_q_word.items(), key=lambda kv: kv[1]["density"])
check("claim_never_over_10pct", never_over, f"max {mx[0]}={mx[1]['density']}")
check("claim_drop_rate_collapse", mine_q_word["2020-05"]["n_posts"] == 345 and mine_q_word["2020-12"]["n_posts"] == 1,
      f"2020-05={mine_q_word['2020-05']['n_posts']} 2020-12={mine_q_word['2020-12']['n_posts']}")

# 6. Pool reproduction anchors from the cadence file (baseline mean ~0.10 for 2023-09..2024-12)
base = [v["density"] for m, v in mine_pool_word.items() if "2023-09" <= m <= "2024-12"]
base_mean = round(sum(base) / len(base), 4) if base else None
check("pool_baseline_mean_anchor", base_mean is not None and abs(base_mean - 0.10) <= 0.02,
      f"2023-09..2024-12 mean={base_mean} vs filed ~0.10")

out["recomputed_summary_primary"] = s_q_word
out["pool_baseline_mean_word"] = base_mean

# 7. info: ledger_full.jsonl carries fuller text and yields more matches; the
# filed context series used ledger.jsonl (its declared pool_ledger). Reported, not failed.
pool_full = []
with open(POOL_FULL, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        pool_full.append((month_of(r["date"]), r.get("text") or ""))
mf_full = density_rows(pool_full, "word")
out["info_ledger_full_word_urgency_total"] = sum(v["n_urgency"] for v in mf_full.values())
out["info_note"] = ("context_pool_word series matches ledger.jsonl (the artifact's declared "
                    "pool_ledger); ledger_full.jsonl fuller text yields "
                    f"{out['info_ledger_full_word_urgency_total']} urgency posts vs 510 - "
                    "ledger-pair divergence, reported not failed")

print(json.dumps(out, indent=1))
sys.exit(1 if out["failed"] else 0)
