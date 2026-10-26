# Assemble pass 2 (named roster) and append to BLIND_JUDGE_FULL.md, keeping pass 1 text intact (everything before MARK).
import os, re, json, itertools, collections
D = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(D, "raw")
SUBJ = ["who_we_are","what_we_are","the_invariants","standing_wave_gate","parable_as_spec","six_lane_run",
        "water_governor","the_congress","moto_cron","keyed_verse","rib_renderman_mapping","dirac_loops"]
LN = ["diogenes","fermat","foucault","plato_kirk","baudrillard","bernays","ellul","freud","hall","jung","mcluhan","wallas"]
LENSKW = {"baudrillard":["baudrillard","simulacr","hyperreal"],"bernays":["bernays","propaganda","public relations","pr "],
 "diogenes":["diogenes","cynic"],"ellul":["ellul","technique"],"fermat":["fermat","proof","margin"],"foucault":["foucault","panopt","discipline","surveil"],
 "freud":["freud","psychoanal","repress","unconscious"],"hall":["stuart hall","hall","encoding/decoding","encoding","decoding"],
 "jung":["jung","archetyp","shadow","persona"],"mcluhan":["mcluhan","medium is","media"],"plato_kirk":["plato","kirk","cave","philosopher-king","republic","star trek"],
 "wallas":["wallas","incubation","illumination","creative process","stages of thought"]}
MARK = "\n\n# PASS 2: NAMED ROSTER"
W = {"fostertron_max": "MAX", "agy_pc": "Gemini"}
def pj(t):
    for x in reversed(re.findall(r"```json\s*(.*?)```", t, re.S)):
        try: return json.loads(x)
        except Exception: pass
    return None
def pair_acc(ids, truth, pred):
    ok = n = 0
    for a, b in itertools.combinations(ids, 2):
        n += 1; ok += ((truth[a] == truth[b]) == (pred.get(a) == pred.get(b)) and pred.get(a) is not None)
    return ok / n if n else None
def norm(l):
    l = (l or "").lower().strip().replace(" ", "_").replace("-", "_")
    for k in LN:
        if l == k or l.startswith(k) or (k == "plato_kirk" and ("plato" in l or "kirk" in l)) or (k == "hall" and "hall" in l): return k
    return l or "?"
def load(prefix, s):
    mp = os.path.join(RAW, "%s_%s_meta.json" % (prefix, s))
    if not os.path.exists(mp): return None
    meta = json.load(open(mp)); M = json.load(open(os.path.join(RAW, "%s_%s_map.json" % (prefix, s))))
    cp = os.path.join(RAW, "%s_%s_content.md" % (prefix, s)); C = open(cp, encoding="utf-8").read() if os.path.exists(cp) else ""
    return meta, M, pj(C)
rows = []; sec = []; conf = collections.Counter(); calib = []; tot = collections.Counter(); cell = collections.defaultdict(lambda: [0, 0])
hw = []; cues = collections.defaultdict(list); models = collections.Counter()
for s in SUBJ:
    p1 = load("blind_full", s); p2 = load("blind_roster", s)
    p1lens = p1voice = "n/a"
    if p1 and p1[2]:
        meta, M, J = p1; ract = {x["id"]: x["ractor"] for x in M}; truth = {x["id"]: x["mouthpiece"] for x in M}
        h = sum(any(any(k in (g.get("thinker_guess","")+" "+g.get("label","")).lower() for k in LENSKW[ract[i]]) and i in g.get("ids",[]) for g in J.get("lenses",[])) for i in ract)
        lr = sum(any(any(k in (g.get("thinker_guess","")+" "+g.get("label","")).lower() for k in LENSKW[r]) and set(i for i in ract if ract[i]==r) & set(g.get("ids",[])) for g in J.get("lenses",[])) for r in set(ract.values()))
        p1lens = "%d/%d (par %d/%d)" % (lr, len(set(ract.values())), h, len(ract))
        p1voice = "%.3f" % pair_acc(list(ract), truth, {i: v for v, l in J.get("voices", {}).items() for i in l})
    if not p2: rows.append([s, p1lens, p1voice, "not run", "", "", "", "", "", ""]); continue
    meta, M, J = p2; models[meta.get("model")] += 1; tot["calls"] += len(meta["attempts"])
    if not J: rows.append([s, p1lens, p1voice, "no JSON", "", "", "", "", meta.get("model"), str(len(meta["attempts"]))]); continue
    A = J.get("assign", {}); ract = {x["id"]: x["ractor"] for x in M}; truth = {x["id"]: x["mouthpiece"] for x in M}; ids = [x["id"] for x in M]
    ok = 0; byw = collections.Counter(); lines = []
    for i in ids:
        a = A.get(i, {}); pl = norm(a.get("lens")); t = ract[i]; c = a.get("confidence"); good = pl == t
        ok += good; conf[(t, pl)] += 1; byw[(truth[i], good)] += 1; cell[(t, s)][0] += good; cell[(t, s)][1] += 1
        tot[("w", truth[i], good)] += 1
        if isinstance(c, (int, float)): calib.append((float(c), good, truth[i]))
        cues[(t, good)].append((s, W[truth[i]], i, pl, c, a.get("cues"), a.get("missing")))
        lines.append("| %s | %s | %s | %s | %s | %s | %s | %s |" % (i, t, W[truth[i]], pl, "Y" if good else "n", c, " / ".join('"%s"' % q for q in (a.get("cues") or [])).replace("|", "/"), (a.get("missing") or "").replace("|", "/")))
    used = collections.Counter(norm(A.get(i, {}).get("lens")) for i in ids)
    hwcell = []
    for L in ("hall", "wallas"):
        for w in sorted(set(truth.values())):
            mine = [i for i in ids if ract[i] == L and truth[i] == w]
            for i in mine:
                pl = norm(A.get(i, {}).get("lens")); hw.append((s, L, W[w], i, pl == L, pl, A.get(i, {}).get("confidence")))
                hwcell.append("%s/%s:%s" % (L, W[w], "hit" if pl == L else "miss->" + pl))
    pv = pair_acc(ids, truth, {i: v for v, l in J.get("voices", {}).items() for i in l})
    tot["ok"] += ok; tot["n"] += len(ids)
    rows.append([s, p1lens, p1voice, "%d/%d (%.0f%%)" % (ok, len(ids), 100 * ok / len(ids)),
                 "MAX %d/%d" % (byw[("fostertron_max", True)], byw[("fostertron_max", True)] + byw[("fostertron_max", False)]) + ("; Gemini %d/%d" % (byw[("agy_pc", True)], byw[("agy_pc", True)] + byw[("agy_pc", False)]) if byw[("agy_pc", True)] + byw[("agy_pc", False)] else ""),
                 "; ".join(hwcell), "%.3f" % pv, "unused: %s; over: %s" % ([l for l in LN if not used[l]] or "-", {k: v for k, v in used.items() if v > -(-len(ids) // 12)} or "-"), meta.get("model"), str(len(meta["attempts"]))])
    sec += ["## P2 %s" % s, "", "- Served `%s`, finish=%s, attempts=%s, %s -> %s, usage=%s" % (meta.get("model"), meta.get("finish"), meta["attempts"], meta["start"], meta["end"], json.dumps(meta.get("usage"))), "",
            "| ID | true lens | writer | judged | ok | conf | cues (verbatim) | missing |", "|---|---|---|---|---|---|---|---|"] + lines + [""]
O = ["# PASS 2: NAMED ROSTER (blind_roster.py; same anonymization+shuffle as pass 1 via blind_full.build; judge given 12 lens names + one neutral line each, must assign one lens per parable, <=ceil(n/12) uses per lens)", "",
     "## Side by side: pass 1 (blind) vs pass 2 (named roster)", "",
     "| Subject | P1 lens recovery (groups; per-parable) | P1 voice pairwise | P2 exact lens acc | P2 by writer | P2 Hall/Wallas | P2 voice pairwise | P2 roster use | P2 served | P2 HTTP |", "|---|---|---|---|---|---|---|---|---|---|"]
O += ["| " + " | ".join(r) + " |" for r in rows]
if tot["n"]:
    mx = (tot[("w","fostertron_max",True)], tot[("w","fostertron_max",True)] + tot[("w","fostertron_max",False)]); gm = (tot[("w","agy_pc",True)], tot[("w","agy_pc",True)] + tot[("w","agy_pc",False)])
    O += ["", "**P2 overall exact lens accuracy: %d/%d (%.1f%%)**; MAX %d/%d, Gemini %d/%d. Chance with 12 lenses ~8.3%%. Served models: %s. DeepSeek HTTP attempts: %d." % (tot["ok"], tot["n"], 100 * tot["ok"] / tot["n"], mx[0], mx[1], gm[0], gm[1], dict(models), tot["calls"])]
    miss = [x for x in hw if not x[4]]
    O += ["", "**Do Hall and Wallas appear correctly on all subjects? %s.** Hall hits %d/%d, Wallas hits %d/%d. Misses: %s" % ("YES" if not miss else "NO",
          sum(1 for x in hw if x[1]=="hall" and x[4]), sum(1 for x in hw if x[1]=="hall"), sum(1 for x in hw if x[1]=="wallas" and x[4]), sum(1 for x in hw if x[1]=="wallas"),
          "; ".join("%s %s/%s %s -> %s (conf %s)" % (x[0], x[1], x[2], x[3], x[5], x[6]) for x in miss) or "none"), ""]
    O += ["## 12x12 confusion matrix (rows = true lens, cols = judged; all writers, all subjects)", "", "| true \\ judged | " + " | ".join(LN) + " | other | recall |", "|---" * 15 + "|"]
    for t in LN:
        r = [conf[(t, p)] for p in LN]; oth = sum(v for (a, b), v in conf.items() if a == t and b not in LN); n = sum(r) + oth
        O.append("| **%s** | " % t + " | ".join(("**%d**" % v if p == t else str(v or "")) for v, p in zip(r, LN)) + " | %s | %s |" % (oth or "", "%d/%d" % (conf[(t, t)], n)))
    O.append("| precision | " + " | ".join("%d/%d" % (conf[(p, p)], sum(v for (a, b), v in conf.items() if b == p)) for p in LN) + " | | |")
    O += ["", "## Lens x subject cells (correct/total, all writers)", "", "| lens | " + " | ".join(SUBJ) + " | total |", "|---" * 14 + "|"]
    for t in LN:
        O.append("| %s | " % t + " | ".join("%d/%d" % tuple(cell[(t, s)]) if cell[(t, s)][1] else "-" for s in SUBJ) + " | %d/%d |" % (sum(cell[(t, s)][0] for s in SUBJ), sum(cell[(t, s)][1] for s in SUBJ)))
    O += ["", "## Calibration (judge confidence vs correctness)", "", "| conf bin | n | correct | acc | MAX acc | Gemini acc |", "|---|---|---|---|---|---|"]
    for lo, hi in [(0, .3), (.3, .5), (.5, .7), (.7, .85), (.85, 1.01)]:
        b = [x for x in calib if lo <= x[0] < hi]
        f = lambda w: ("%d/%d" % (sum(x[1] for x in b if x[2] == w), sum(1 for x in b if x[2] == w))) if any(x[2] == w for x in b) else "-"
        O.append("| [%.2f,%.2f) | %d | %d | %s | %s | %s |" % (lo, min(hi, 1), len(b), sum(x[1] for x in b), ("%.0f%%" % (100 * sum(x[1] for x in b) / len(b))) if b else "-", f("fostertron_max"), f("agy_pc")))
    if calib:
        mc = lambda g: sum(x[0] for x in calib if x[1] == g) / max(1, sum(1 for x in calib if x[1] == g))
        O += ["", "Mean confidence when correct %.3f vs wrong %.3f (n=%d with numeric confidence)." % (mc(True), mc(False), len(calib))]
    json.dump({"conf": {"%s>%s" % k: v for k, v in conf.items()}, "cell": {"%s|%s" % k: v for k, v in cell.items()}, "hw": hw, "calib": calib,
               "cues": {"%s|%s" % k: v for k, v in cues.items()}}, open(os.path.join(D, "BLIND_ROSTER_STATS.json"), "w"), indent=1)
an = os.path.join(D, "ANALYSIS_FOR_MAG.md")
if os.path.exists(an): O += ["", open(an, encoding="utf-8").read()]
O += ["", "# PASS 2 PER-SUBJECT DETAIL (judge cues verbatim)", ""] + sec
fp = os.path.join(D, "BLIND_JUDGE_FULL.md"); base = open(fp, encoding="utf-8").read().split(MARK)[0]
open(fp, "w", encoding="utf-8").write(base + "\n\n" + "\n".join(O))
print("\n".join(O[:60]))
