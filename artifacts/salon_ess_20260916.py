"""salon_ess_20260916 -- falsifier #1 from the physical-computing pack.

"Salon-ESS: inter-lane decorrelation must predict desk-grade quality in existing
receipts, or 'the fleet is a thermodynamic sampler of judgment space' is struck
from the canon."  (watch/inbox/physical_computing/PHYSICAL_COMPUTING_PACK_20260916.md section 4.1)

Data used (fixed paths, read-only):
  PART 1  watch/inbox/physical_computing/receipts/SALON_FREE_20260916_raw.jsonl
          8 lanes, ONE question, desk ranks 1-8 parsed from the sibling receipt .md
  PART 2  memory/runs/lane_salon/salon_*.json
          33 salons, 2-6 same-question witnesses each; desk-synthesized 'verdict'
  PART 3  memory/runs/salon_50_20260916/raw.jsonl
          salon_50 inventory: 12 lanes x 4 themes, one lane per qid; NEXT-STEAL
          contract-compliance as the only per-answer quality floor

Metrics (stdlib only, no scipy/numpy):
  token-set Jaccard on words (len>=3, lowercased) and difflib SequenceMatcher ratio
  decorrelation(d_i) = 1 - mean similarity of answer i to its peers in the same salon
  Spearman rho with average ranks; exact permutation p for n<=9 (n! <= 362880)

$0, local, read-only over inputs. Run: .venv/Scripts/python.exe artifacts/salon_ess_20260916.py
"""
import json, re, difflib, math, glob, sys
from pathlib import Path
from itertools import permutations, combinations

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
P1_RAW = ROOT / "watch" / "inbox" / "physical_computing" / "receipts" / "SALON_FREE_20260916_raw.jsonl"
P1_MD = ROOT / "watch" / "inbox" / "physical_computing" / "receipts" / "SALON_FREE_20260916.md"
P2_GLOB = str(ROOT / "memory" / "runs" / "lane_salon" / "salon_*.json")
P3_RAW = ROOT / "memory" / "runs" / "salon_50_20260916" / "raw.jsonl"

TOKEN = re.compile(r"[a-z0-9']{3,}")

def toks(text):
    return set(TOKEN.findall(text.lower()))

def jac(a, b):
    A, B = toks(a), toks(b)
    if not A or not B:
        return 0.0
    return len(A & B) / len(A | B)

def seqratio(a, b):
    return difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()

def mean(xs):
    xs = list(xs)
    return sum(xs) / len(xs) if xs else float("nan")

def rankdata(xs):
    # average ranks, 1-based
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    ranks = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        r = (i + 1 + j + 1) / 2.0
        for k in range(i, j + 1):
            ranks[order[k]] = r
        i = j + 1
    return ranks

def spearman(x, y):
    n = len(x)
    if n < 3:
        return float("nan")
    rx, ry = rankdata(x), rankdata(y)
    mx, my = mean(rx), mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    rho = num / den if den else float("nan")
    return rho

def perm_p(x, y, tails=2):
    """exact two-sided permutation p for spearman rho"""
    n = len(x)
    if n < 3 or n > 9:
        return float("nan")
    obs = spearman(x, y)
    cnt = tot = 0
    for perm in permutations(range(n)):
        r = spearman(x, [y[perm[i]] for i in range(n)])
        tot += 1
        if abs(r) >= abs(obs) - 1e-12:
            cnt += 1
    return cnt / tot

def pair_stats(answers):
    """per-answer mean similarity to peers; returns (list, jaccard_all_pairs, seq_all_pairs)"""
    n = len(answers)
    J = [[0.0] * n for _ in range(n)]
    S = [[0.0] * n for _ in range(n)]
    for i, j in combinations(range(n), 2):
        J[i][j] = J[j][i] = jac(answers[i], answers[j])
        S[i][j] = S[j][i] = seqratio(answers[i], answers[j])
    mi = [mean(J[i][k] for k in range(n) if k != i) for i in range(n)]
    ms = [mean(S[i][k] for k in range(n) if k != i) for i in range(n)]
    return mi, ms, [J[i][j] for i, j in combinations(range(n), 2)], \
           [S[i][j] for i, j in combinations(range(n), 2)]

print("=" * 72)
print("SALON-ESS falsifier #1 -- inter-lane decorrelation vs desk-grade quality")
print("=" * 72)

# ---------------------------------------------------------------- PART 1
print("\nPART 1 -- DIRECT TEST: SALON_FREE_20260916 (8 lanes, 1 question, desk rank 1-8)")
rows = [json.loads(l) for l in P1_RAW.read_text(encoding="utf-8").splitlines() if l.strip()]
ok = [r for r in rows if r.get("ok")]
# one answer per lane: earliest ok attempt
best = {}
for r in sorted(ok, key=lambda r: r.get("attempt", 1)):
    best.setdefault(r["lane"], r)
lanes = sorted(best)
answers = {l: best[l]["answer"] for l in lanes}
print(f"rows={len(rows)} ok={len(ok)} lanes_answered={len(lanes)}")

# parse desk ranks from the receipt md: lines "N. **lane** ..."
md = P1_MD.read_text(encoding="utf-8")
ranks = {}
for m in re.finditer(r"^(\d+)\.\s+\*\*([a-z0-9\-]+)\*\*", md, re.M):
    ranks[m.group(2)] = int(m.group(1))
print("desk ranks parsed (1=best):", ranks)
missing = [l for l in lanes if l not in ranks]
if missing:
    print("!! lanes without desk rank:", missing)

common = [l for l in lanes if l in ranks]
ans_list = [answers[l] for l in common]
mi, ms, Jpairs, Spairs = pair_stats(ans_list)
dec = [1.0 - v for v in mi]          # token-Jaccard-based decorrelation
dec_s = [1.0 - v for v in ms]        # seqratio-based
rk = [ranks[l] for l in common]

print(f"\npairwise similarity across all C(n,2)={len(Jpairs)} pairs:")
print(f"  token-Jaccard: mean={mean(Jpairs):.4f} median={sorted(Jpairs)[len(Jpairs)//2]:.4f} "
      f"min={min(Jpairs):.4f} max={max(Jpairs):.4f}")
print(f"  seqratio:      mean={mean(Spairs):.4f} median={sorted(Spairs)[len(Spairs)//2]:.4f} "
      f"min={min(Spairs):.4f} max={max(Spairs):.4f}")
print("\nper-lane (lane, desk_rank, meanJaccardToPeers, decorrelation=1-J):")
for i, l in enumerate(common):
    print(f"  {l:<15} rank={rk[i]}  J={mi[i]:.4f}  dec={dec[i]:.4f}")

rho = spearman(dec, rk); p = perm_p(dec, rk)
rho_s = spearman(dec_s, rk); p_s = perm_p(dec_s, rk)
print(f"\nSpearman(decorrelation, desk_rank) full n={len(common)}: "
      f"Jaccard rho={rho:+.3f} (perm p={p:.3f}) | seqratio rho={rho_s:+.3f} (perm p={p_s:.3f})")
print("  NOTE negative rho = more decorrelated -> better rank -> SUPPORTS the claim")

# leave-one-out (or-nemotron leaked 9.7k chars of chain-of-thought into its answer,
# per the sibling receipt -- it distorts seqratio especially)
print("\nleave-one-out sensitivity (drop one lane, recompute rho on Jaccard decorrelation):")
for drop in range(len(common)):
    sub = [i for i in range(len(common)) if i != drop]
    d = [dec[i] for i in sub]; r_ = [rk[i] for i in sub]
    print(f"  drop {common[drop]:<15} n={len(sub)} rho={spearman(d, r_):+.3f}")

# trimmed or-nemotron: final 2500 chars (receipt says final bullets are the answer)
ans_t = dict(answers)
if "or-nemotron" in ans_t and len(ans_t["or-nemotron"]) > 2500:
    ans_t["or-nemotron"] = ans_t["or-nemotron"][-2500:]
tl = [l for l in common]
mi_t, ms_t, _, _ = pair_stats([ans_t[l] for l in tl])
dec_t = [1.0 - v for v in mi_t]
rho_t = spearman(dec_t, [ranks[l] for l in tl]); p_t = perm_p(dec_t, [ranks[l] for l in tl])
print(f"\nor-nemotron trimmed to last 2500 chars: n={len(tl)} Jaccard rho={rho_t:+.3f} (perm p={p_t:.3f})")

# ---------------------------------------------------------------- PART 2
print("\n" + "=" * 72)
print("PART 2 -- PROXY TEST: lane_salon corpus (33 salons, witnesses vs desk verdict)")
files = sorted(glob.glob(P2_GLOB))
salon_rows = []
pairs_all_J, pairs_within = [], []
for f in files:
    d = json.loads(Path(f).read_text(encoding="utf-8"))
    wit = [w for w in d.get("witnesses", []) if w.get("ok") and (w.get("answer") or "").strip()]
    verdict = (d.get("verdict") or "").strip()
    if len(wit) < 3 or not verdict:
        continue
    ans = [w["answer"] for w in wit]
    mi, ms, Jp, _ = pair_stats(ans)
    # distinct-lane pairs only (dedupe surfaces: witnesses may repeat a provider)
    names = [w.get("surface") or w.get("provider") or "?" for w in wit]
    distinct = len(set(names)) >= 2
    sim_verdict = [jac(a, verdict) for a in ans]
    dec_i = [1.0 - v for v in mi]
    rho_i = spearman(dec_i, sim_verdict)
    salon_rows.append({
        "file": Path(f).name, "k": len(wit), "distinct": distinct,
        "meanJ": mean(Jp), "medianJ": sorted(Jp)[len(Jp) // 2],
        "rho_dec_vs_verdict": rho_i,
        "p": perm_p(dec_i, sim_verdict) if len(wit) <= 9 else float("nan"),
    })
    pairs_all_J.extend(Jp)

print(f"salons with >=3 ok witnesses + verdict: {len(salon_rows)} of {len(files)} files")
kp = [r for r in salon_rows if r["k"] >= 4]
print(f"salons with >=4 witnesses (Spearman stable): {len(kp)}")
print(f"\npooled same-question cross-lane pairs: n={len(pairs_all_J)} "
      f"mean Jaccard={mean(pairs_all_J):.4f} median={sorted(pairs_all_J)[len(pairs_all_J)//2]:.4f}")
print("\nper-salon: decorrelation vs verdict-agreement (Spearman; only k>=4):")
neg = pos = defined = 0
for r in kp:
    if not math.isnan(r["rho_dec_vs_verdict"]):
        defined += 1
        if r["rho_dec_vs_verdict"] < 0: neg += 1
        elif r["rho_dec_vs_verdict"] > 0: pos += 1
    sig = " *" if (not math.isnan(r["p"]) and r["p"] < 0.10) else ""
    print(f"  {r['file']:<28} k={r['k']} meanJ={r['meanJ']:.3f} "
          f"rho(dec,verdict)={r['rho_dec_vs_verdict']:+.3f} p={r['p']:.3f}{sig}")
print(f"\nsign count (k>=4, defined): rho<0: {neg}  rho>0: {pos}  (coin flip expectation ~50/50)")
rhos = [r["rho_dec_vs_verdict"] for r in kp if not math.isnan(r["rho_dec_vs_verdict"])]
if rhos:
    # pooled estimate: mean of per-salon rho (Fisher-z would need weights; honest simple mean)
    print(f"mean per-salon rho = {mean(rhos):+.3f} over {len(rhos)} salons")

# ---------------------------------------------------------------- PART 3
print("\n" + "=" * 72)
print("PART 3 -- salon_50 inventory (memory/runs/salon_50_20260916/raw.jsonl)")
rows3 = [json.loads(l) for l in P3_RAW.read_text(encoding="utf-8").splitlines() if l.strip()]
ok3 = [r for r in rows3 if r.get("ok")]
first_ok = {}
for r in sorted(ok3, key=lambda r: r.get("attempt", 1)):
    first_ok.setdefault(r["qid"], r)
uniq = list(first_ok.values())
themes = {}
for r in uniq:
    themes.setdefault(r["theme"], []).append(r)
ns_total = sum((r.get("answer") or "").count("NEXT-STEAL:") for r in ok3)
ns_answers = sum(1 for r in ok3 if "NEXT-STEAL:" in (r.get("answer") or ""))
ns_uniq = sum(1 for r in uniq if "NEXT-STEAL:" in (r.get("answer") or ""))
print(f"lines={len(rows3)} ok_rows={len(ok3)} unique_qids_answered={len(uniq)}")
print(f"lanes={len({r.get('lane') for r in ok3})} themes={len(themes)}")
print(f"NEXT-STEAL: total_occurrences_across_ok_rows={ns_total} "
      f"answers_with>=1={ns_answers}/{len(ok3)} unique_qids_with>=1={ns_uniq}/{len(uniq)}")
print("\nper-theme cross-question similarity baseline (CAVEAT: different questions, "
      "confounds topic with lane):")
for t, rs in sorted(themes.items()):
    ans = [r["answer"] for r in rs]
    _, _, Jp, _ = pair_stats(ans)
    lanes_t = sorted({r.get("lane") for r in rs})
    print(f"  {t:<20} n={len(rs)} pairs={len(Jp)} meanJ={mean(Jp):.4f} "
          f"medianJ={sorted(Jp)[len(Jp)//2]:.4f} lanes={len(lanes_t)}")
# per-lane contract compliance + volume (quality floor signals)
from collections import Counter
lane_cnt = Counter(r.get("lane") for r in uniq)
lane_ns = Counter(r.get("lane") for r in uniq if "NEXT-STEAL:" in (r.get("answer") or ""))
print("\nper-lane (unique qids answered / with NEXT-STEAL):")
for l in sorted(lane_cnt):
    print(f"  {l:<15} answered={lane_cnt[l]:>2} with_next_steal={lane_ns.get(l,0):>2} "
          f"compliance={lane_ns.get(l,0)/lane_cnt[l]*100:.0f}%")

print("\n" + "=" * 72)
print("done.")
