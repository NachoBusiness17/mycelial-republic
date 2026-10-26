#!/usr/bin/env python
# cross-librarian verification pass: classify every extracted arXiv citation location as
# genuine (URL or explicit 'arxiv' mention on the line) vs score-table false positive
# (markdown table row, no 'arxiv' string, 2+ numeric cells) vs bare-id-prose (no URL but
# non-table context: kept, flagged for the receipt).
import json, io, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = r"C:/Users/foste/Documents/projects/local_sovereign_agent/"
d = json.load(open(ROOT + "watch/inbox/gala_20260925/ouroboros/lanes/_byproducts/fleet_citations.json", encoding="utf-8"))

NUMISH = re.compile(r"\b\d+\.\d+\b")
linecache = {}
def get_line(f, ln):
    k = (f, ln)
    if k not in linecache:
        try:
            linecache[k] = io.open(ROOT + f, encoding="utf-8", errors="replace").readlines()[ln - 1]
        except Exception:
            linecache[k] = ""
    return linecache[k]

cls = {}          # (workflow, value) -> set of classes
for c in d["citations"]:
    if c["kind"] not in ("arxiv", "arxiv-bare"):
        continue
    key = (c["workflow"], c["value"])
    for f, ln, _ in c["locs"]:
        line = get_line(f, ln)
        low = line.lower()
        if "arxiv" in low:
            k = "genuine-url"
        elif line.lstrip().startswith("|") and len(NUMISH.findall(line)) >= 2:
            k = "score-table-fp"
        else:
            k = "bare-id-prose"
        cls.setdefault(key, set()).add(k)

per_wf_fp = {}
per_wf_prose = {}
for (wf, val), ks in sorted(cls.items()):
    if "score-table-fp" in ks:
        per_wf_fp.setdefault(wf, []).append(val)
    if ks == {"bare-id-prose"}:
        per_wf_prose.setdefault(wf, []).append(val)

print("=== ARXIV MATCH VERIFICATION (line-context pass over all %d arXiv uniques) ===" % len(cls))
tot_fp = sum(len(v) for v in per_wf_fp.values())
tot_prose = sum(len(v) for v in per_wf_prose.values())
print("score-table false positives: %d | bare-id-prose (kept, no URL on line): %d | genuine-url: %d"
      % (tot_fp, tot_prose, len(cls) - tot_fp - tot_prose))
for wf, vals in sorted(per_wf_fp.items()):
    print("  FP %s: %s" % (wf, ", ".join(vals)))
for wf, vals in sorted(per_wf_prose.items()):
    if len(vals) <= 12:
        print("  PROSE-ONLY %s: %s" % (wf, ", ".join(vals)))
    else:
        print("  PROSE-ONLY %s: %d ids (sample: %s)" % (wf, len(vals), ", ".join(vals[:8])))
