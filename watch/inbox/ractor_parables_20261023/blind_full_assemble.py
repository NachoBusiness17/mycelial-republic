import os, re, json, itertools, collections
D = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(D, "raw")
from blind_full import SUBJ, LENSKW, PROG
def pj(t):
    b = re.findall(r"```json\s*(.*?)```", t, re.S)
    for x in reversed(b):
        try: return json.loads(x)
        except Exception: pass
    return None
def pair_acc(ids, truth, pred):
    ok = n = 0
    for a, b in itertools.combinations(ids, 2):
        n += 1; ok += ((truth[a] == truth[b]) == (pred.get(a) == pred.get(b)) and pred.get(a) is not None)
    return ok / n if n else None
def purity(ids, truth, pred):
    g = collections.defaultdict(list)
    for i in ids: g[pred.get(i, "?")].append(truth[i])
    return sum(collections.Counter(v).most_common(1)[0][1] for v in g.values()) / len(ids)
rows = []; tot = collections.Counter(); out = []
prog = json.load(open(PROG)) if os.path.exists(PROG) else {}
for s in SUBJ:
    mp = os.path.join(RAW, "blind_full_%s_meta.json" % s)
    if not os.path.exists(mp): rows.append((s, "not run")); continue
    meta = json.load(open(mp)); M = json.load(open(os.path.join(RAW, "blind_full_%s_map.json" % s)))
    cp = os.path.join(RAW, "blind_full_%s_content.md" % s); C = open(cp, encoding="utf-8").read() if os.path.exists(cp) else ""
    J = pj(C); truth = {x["id"]: x["mouthpiece"] for x in M}; ract = {x["id"]: x["ractor"] for x in M}; ids = [x["id"] for x in M]
    sec = ["## %s" % s, "", "- n=%d (%s). Served model: `%s`, finish=%s, attempts=%s, %s -> %s, usage=%s" % (len(M), dict(collections.Counter(truth.values())), meta.get("model"), meta.get("finish"), meta["attempts"], meta["start"], meta["end"], json.dumps(meta.get("usage")))]
    if not J: sec.append("- **No parseable JSON block in output.**"); out += sec + [""]; continue
    pred = {i: v for v, l in J.get("voices", {}).items() for i in l}
    nmp = len(set(truth.values()))
    pa = pair_acc(ids, truth, pred); pu = purity(ids, truth, pred)
    sec.append("- Voice: judge found %d voices %s; mouthpieces present=%d. Pairwise same/different-author agreement=%.3f; cluster purity=%.3f%s" % (len(J.get("voices", {})), {k: len(v) for k, v in J["voices"].items()}, nmp, pa, pu, " (single mouthpiece: purity trivially 1; voice count is the signal)" if nmp == 1 else ""))
    for k, v in J["voices"].items():
        sec.append("  - %s: %s" % (k, dict(collections.Counter(truth.get(i, "?") for i in v))))
    # lens recovery
    lens_ok = {}; failed = []
    for r in sorted(set(ract.values())):
        mine = [i for i in ids if ract[i] == r]; hit = []
        for g in J.get("lenses", []):
            txt = (g.get("thinker_guess", "") + " " + g.get("label", "")).lower()
            if any(k in txt for k in LENSKW[r]) and set(mine) & set(g.get("ids", [])): hit.append(g.get("thinker_guess"))
        lens_ok[r] = bool(hit)
        for i in mine:
            ok = any(any(k in (g.get("thinker_guess", "") + " " + g.get("label", "")).lower() for k in LENSKW[r]) and i in g.get("ids", []) for g in J.get("lenses", []))
            tot[("lens_par", truth[i], ok)] += 1
        if not hit: failed.append(r)
    sec.append("- Lens recovery (ractor named/evoked in a lens group containing its parable): %d/%d; failed: %s" % (sum(lens_ok.values()), len(lens_ok), failed or "none"))
    sec.append("- Lens groups: " + "; ".join("%s [%s] %s" % (g.get("label"), g.get("thinker_guess"), ["%s/%s" % (ract.get(i), truth.get(i, "?")[:3]) for i in g.get("ids", [])]) for g in J.get("lenses", [])))
    sec.append("- Base rules re-derived (%d):" % len(J.get("base_rules", [])))
    sec += ["  %d. %s" % (n + 1, b) for n, b in enumerate(J.get("base_rules", []))]
    rows.append((s, "%d" % len(M), "%d" % len(J["voices"]), "%.3f" % pa, "%.3f" % pu, "%d/%d" % (sum(lens_ok.values()), len(lens_ok)), ", ".join(failed) or "-", meta.get("model"), str(len(meta["attempts"]))))
    tot["pa_ok"] += pa * len(ids); tot["n"] += len(ids); tot["lens_ok"] += sum(lens_ok.values()); tot["lens_n"] += len(lens_ok); tot["calls"] += len(meta["attempts"])
    if nmp > 1: tot["pa2"] += pa * len(ids); tot["n2"] += len(ids)
    out += sec + [""]
H = ["# BLIND JUDGE FULL: Ractor parables grid (224 = 144 Fostertron MAX glm-5.3 + 80 Antigravity Gemini agy_pc), DeepSeek direct, one call per subject", "",
 "- Carrier: tools.ds_workhorse.load_key (in-process only) -> api.deepseek.com/chat/completions (blind_full.py). Not Hermes. Requested deepseek-reasoner, thinking enabled, max_tokens 65536.",
 "- Anonymized: HTML meta comments + ---KEY--- stripped, roster/model/seat names redacted to [-], IDs shuffled per subject. Maps in raw/blind_full_<subj>_map.json never sent. agy_bob and FAILED files excluded.",
 "- Scoring: voice = pairwise same/different-author agreement vs true mouthpiece, plus cluster purity. Lens = ractor's thinker named/evoked (keyword match) in a lens group containing its parable.", "",
 "| Subject | n | voices found | voice pairwise | purity | lens | lens failed | served model | HTTP attempts |", "|---|---|---|---|---|---|---|---|---|"]
for r in rows: H.append("| " + " | ".join(r) + (" |" if len(r) > 2 else " | | | | | | | |"))
if tot["n"]:
    H += ["", "**Overall**: voice pairwise (weighted) %.3f; on mixed-mouthpiece subjects %s; lens recovery %d/%d; per-parable lens hit MAX %d/%d, Gemini %d/%d; DeepSeek HTTP attempts %d." % (
        tot["pa_ok"] / tot["n"], ("%.3f" % (tot["pa2"] / tot["n2"])) if tot["n2"] else "n/a", tot["lens_ok"], tot["lens_n"],
        tot[("lens_par", "fostertron_max", True)], tot[("lens_par", "fostertron_max", True)] + tot[("lens_par", "fostertron_max", False)],
        tot[("lens_par", "agy_pc", True)], tot[("lens_par", "agy_pc", True)] + tot[("lens_par", "agy_pc", False)], tot["calls"])]
H += ["", "Progress: `%s`" % json.dumps(prog), ""]
O = H + out + ["", "# RAW OUTPUTS (verbatim)"]
for s in SUBJ:
    cp = os.path.join(RAW, "blind_full_%s_content.md" % s)
    if os.path.exists(cp): O += ["", "## RAW %s" % s, "", open(cp, encoding="utf-8").read()]
open(os.path.join(D, "BLIND_JUDGE_FULL.md"), "w", encoding="utf-8").write("\n".join(O)); print("\n".join(H))
