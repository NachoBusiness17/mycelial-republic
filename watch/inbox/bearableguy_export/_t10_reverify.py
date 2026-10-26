"""T10 reverification driver - runs the filed census's own replay contract.

Loads BG_SYMBOL_CENSUS.json, imports BG_SYMBOL_counter.py from disk,
replays count_decl / count_text over every reading, recomputes totals,
artworks_present, text_totals, by_month, and reruns the negation checks.
Exits nonzero on any mismatch. Prints PASS/FAIL lines per check.
"""
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CENSUS = os.path.join(HERE, "BG_SYMBOL_CENSUS.json")
COUNTER = os.path.join(HERE, "BG_SYMBOL_counter.py")

with open(CENSUS, "r", encoding="utf-8") as f:
    art = json.load(f)

spec = importlib.util.spec_from_file_location("bg_counter", COUNTER)
bg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bg)

fails = []


def check(name, ok, detail=""):
    print(("PASS" if ok else "FAIL"), name, detail)
    if not ok:
        fails.append(name)


# 1. embedded counter code matches the module on disk
emb = art["counter_code"]
with open(COUNTER, "r", encoding="utf-8") as f:
    disk = f.read()
check("counter_code_matches_disk", emb.strip() == disk.strip())

# 2. replay per-artwork decl + text counts
sym = art["vocab"]["symbols"]
mismatch = []
for r in art["readings"]:
    c, unknown, cancelled = bg.count_decl(r["decl"], sym)
    t = bg.count_text(r["text_decl"])
    want_s = art["counts"]["per_artwork"][r["id"]]["symbols"]
    want_t = art["counts"]["per_artwork"][r["id"]]["text"]
    if c != want_s:
        mismatch.append((r["id"], "symbols", c, want_s))
    if t != want_t:
        mismatch.append((r["id"], "text", t, want_t))
    if unknown:
        mismatch.append((r["id"], "unexpected_unknown", unknown, []))
    if cancelled:
        mismatch.append((r["id"], "unexpected_cancelled", cancelled, []))
check("per_artwork_replay", not mismatch, str(mismatch))

# 3. recompute totals, artworks_present, text_totals
tot = {}
present = {}
for r in art["readings"]:
    for k, v in art["counts"]["per_artwork"][r["id"]]["symbols"].items():
        tot[k] = tot.get(k, 0) + v
        present[k] = present.get(k, 0) + 1
ttot = {}
for r in art["readings"]:
    for k, v in art["counts"]["per_artwork"][r["id"]]["text"].items():
        ttot[k] = ttot.get(k, 0) + v
check("totals_recompute", tot == art["counts"]["totals"])
check("artworks_present_recompute", present == art["counts"]["artworks_present"])
check("text_totals_recompute", ttot == art["counts"]["text_totals"])

# 4. recompute by_month
bm = {}
for r in art["readings"]:
    d = {}
    for k, v in art["counts"]["per_artwork"][r["id"]]["symbols"].items():
        d[k] = v
    for k, v in art["counts"]["per_artwork"][r["id"]]["text"].items():
        d["text:" + k] = v
    bm[r["month"]] = d
check("by_month_recompute", bm == art["by_month"])

# 5. negation checks (rerun live)
nc = art["negation_check"]
_c, _u, canc = bg.count_decl(["no rocket x1 : absent"], sym)
check("decl_negation", len(canc) == 1 and _c == {})
_c, _u, canc = bg.count_decl(["moon x0 : none visible"], sym)
check("decl_x0_cancel", len(canc) == 1 and _c == {})
_c, _u, canc = bg.count_decl(["wibble x2 : not a vocab term"], sym)
check("decl_unknown_flagged", len(_u) == 1 and _c == {})
mt, log = bg.scan_text(nc["freetext_negation_window"]["input"], bg.build_matchers(sym))
live_counts = {k: mt.get(k, 0) for k in
               ["rocket", "moon", "knight", "sword", "king", "crown", "flag"]}
check("freetext_negation_window",
      live_counts == nc["freetext_negation_window"]["counts"]
      and len(log) == len(nc["freetext_negation_window"]["cancelled"]),
      str(live_counts))

# 6. vocab size
check("vocab_term_count", len(sym) == art["vocab"]["symbol_term_count"],
      str(len(sym)))

# 7. corpus: 14 files on disk, register/submissions parse
files = sorted(os.listdir(os.path.join(HERE, "media_full")))
check("media_full_14_files", len(files) == 14, str(len(files)))
ids = [r["id"] for r in art["readings"]]
for i in ids:
    for suf in ("_main.png", "_main_c.jpg"):
        p = os.path.join(HERE, "media_full", i + suf)
        if not os.path.isfile(p):
            fails.append("missing:" + p)
check("all_14_declared_files_exist",
      not any(f.startswith("missing:") for f in fails))

with open(os.path.join(HERE, "submissions.jsonl"), "r", encoding="utf-8") as f:
    subs = [json.loads(l) for l in f if l.strip()]
check("submissions_92_rows", len(subs) == 92, str(len(subs)))

with open(os.path.join(HERE, "media_register.jsonl"), "r", encoding="utf-8") as f:
    reg = [json.loads(l) for l in f if l.strip()]
check("register_parses", len(reg) > 0, str(len(reg)) + " rows")

# 8. em-dash law: none in the artifact text
raw = open(CENSUS, "r", encoding="utf-8").read()
check("no_em_dash_in_artifact", "\u2014" not in raw and "\u2013" not in raw)

print("RESULT", "PASS" if not fails else "FAIL", len(fails), "failures")
sys.exit(1 if fails else 0)
