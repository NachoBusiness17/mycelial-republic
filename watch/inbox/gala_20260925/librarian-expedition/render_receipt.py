#!/usr/bin/env python
# cited-missing lane: render the receipt markdown to STDOUT.
# Pipe the stdout to watch/inbox/librarian_exp/cited-missing.md (bash redirect).
# No file writes here. No em-dashes.
import json

LANES = "watch/inbox/gala_20260925/librarian-expedition/lanes"

with open(LANES + "/unique_citations.json", encoding="utf-8") as f:
    data = json.load(f)

rows = {}
for u in data["citations"]:
    val = u["value"]
    if u["kind"] == "github" and val.endswith("."):
        val = val.rstrip(".")
    r = rows.setdefault(val, {"kind": u["kind"], "value": val, "cites": [],
                              "catalog_hits": [], "filename_hits": [],
                              "held": False, "held_durable": False})
    r["kind"] = "arxiv" if "arxiv" in (r["kind"], u["kind"]) else r["kind"]
    r["cites"].extend(u["cites"])
    r["catalog_hits"] = sorted(set(r["catalog_hits"]) | set(u["catalog_hits"]))
    r["filename_hits"] = sorted(set(r["filename_hits"]) | set(u["filename_hits"]))
    r["held"] = bool(r["catalog_hits"] or r["filename_hits"])
    if r["held"]:
        durable = [h for h in (r["catalog_hits"] + r["filename_hits"])
                   if "temp" not in h.lower() and "tmp" not in h.lower()]
        r["held_durable"] = bool(durable)

PLACEHOLDER = {"2407.12345"}

def prio(r):
    if r["value"] in PLACEHOLDER:
        return "n/a (placeholder id)"
    if r["held"]:
        return "held"
    groups = set(c["group"] for c in r["cites"])
    claim = bool(groups & {"drops", "48h_synth"}) or any(
        c["group"] == "olm1001" and "DIGEST" in c["file"] for c in r["cites"])
    n = len(r["cites"])
    if claim or n >= 3:
        return "P1-HIGH"
    if n == 2:
        return "P2-MED"
    return "P3-LOW"

def holding_str(r):
    if not r["held"]:
        return "no"
    return "yes (durable)" if r["held_durable"] else "weak (temp-path only)"

def fetch_str(r):
    if r["value"] in PLACEHOLDER:
        return "yes (HTTP 200; id real but cited as a fabricated-citation artifact)"
    if r["kind"] == "github":
        return "yes (public GitHub; HTTP 200 probe)"
    return "yes (arXiv public; registry verified by probes)"

def cites_str(r, limit=4):
    locs = sorted(set(c["file"].split("watch")[-1].replace("\\", "/").lstrip("/")
                      + ":" + str(c["line"]) for c in r["cites"]))
    locs = ["watch/" + l for l in locs]
    if len(locs) > limit:
        return "; ".join(locs[:limit]) + f" (+{len(locs)-limit} more)"
    return "; ".join(locs)

def holdings_evidence(r):
    parts = [h.split("local_sovereign_agent/")[-1].replace("\\", "/")
             for h in (r["catalog_hits"] + r["filename_hits"])[:3]]
    return "; ".join(parts) if parts else "-"

def sortkey(r):
    order = {"P1-HIGH": 0, "P2-MED": 1, "P3-LOW": 2, "n/a (placeholder id)": 3}.get(prio(r), 4)
    return (order, -len(r["cites"]), r["value"])

ncite_rows = sum(len(set(c["file"].replace("\\", "/") + ":" + str(c["line"])
                         for c in r["cites"])) for r in rows.values())
not_held = [r for r in rows.values() if not r["held"]]
p1 = [r for r in rows.values() if prio(r) == "P1-HIGH"]
p2 = [r for r in rows.values() if prio(r) == "P2-MED"]
p3 = [r for r in rows.values() if prio(r) == "P3-LOW"]
weak = [r for r in rows.values() if r["held"] and not r.get("held_durable")]
held_dur = [r for r in rows.values() if r.get("held_durable")]

out = []
A = out.append
A("# CITED-BUT-MISSING sweep (librarian-expedition, division B)")
A("")
A("Date: 2026-10-01. Lane: cited-missing. Ask: extract every primary-source citation from the")
A("last-48h receipts and check whether the actual primary is held in the estate (catalog + corpus +")
A("loose bytes) or only fetched-at-runtime with bytes never retained.")
A("")
A("## Method")
A("")
A("- Surfaces swept (all banked in the last 48h): watch/inbox/48h_synth (6 chapters),")
A("  frontier_olm_2026-09-30/steal (6 cards), frontier_olm_2026-10-01/steal (5 cards + DIGEST + RECEIPT),")
A("  spiking_wide (7 cards), localfirst (7 cards + LOCALFIRST_MEMORY_LANDSCAPE_20261001.md), drop")
A("  receipts (SPIKINGBRAIN, STRATA, DOUBLE_DROP, x_intel_drop, model_mating_paper_dig, ABLITERATUS_DROP),")
A("  ractor50 (8 chapters).")
A("- Extraction: regex for arxiv.org URLs, bare arXiv ids (YYMM.NNNNN month-validated), and github.com")
A("  owner/repo pairs, per receipt line. Scripts: watch/inbox/gala_20260925/librarian-expedition/")
A("  extract_citations.py + holdings_check.py + render_receipt.py; raw data lanes/citations_raw.json")
A("  (205 rows) and lanes/unique_citations.json.")
A("- Holdings test: (a) id substring in any catalog/catalog.jsonl path or title (691,789 rows);")
A("  (b) id substring in any FILENAME under corpus/, watch/, memory/, docs/, mag/, tools/, state/")
A("  (state/arxiv/ holds 4,010 dated fetched-text files). Catalog-only hits whose sole path is a")
A("  %TEMP%/tmpdir file are classed WEAK (bytes outside the durable estate), not held-durable.")
A("- Fetchability: HTTP HEAD probes (curl -I -L): 3 arXiv ids + 13 github repos + the placeholder id,")
A("  all returned HTTP 200 (raw probe log in lanes/cited-missing.check.txt).")
A("")
A("## Counts")
A("")
A(f"- Unique citations extracted: {len(rows)} "
  f"({sum(1 for r in rows.values() if r['kind']=='arxiv')} arXiv ids, "
  f"{sum(1 for r in rows.values() if r['kind']=='github')} GitHub repos)")
A(f"- Cite locations (file:line): {ncite_rows}")
A(f"- HELD (durable estate): {len(held_dur)}")
A(f"- HELD (weak, temp-path only): {len(weak)}")
A(f"- NOT HELD (cited-but-missing): {len(not_held)}")
A(f"- Priority split of the missing: P1-HIGH {len(p1)}, P2-MED {len(p2)}, P3-LOW {len(p3)}, placeholder n/a 1")
A("")
A("## Verdict")
A("")
A(f"The estate's memory is leaking: {len(not_held)} of {len(rows)} primaries "
  f"({100.0*len(not_held)/len(rows):.0f} pct) cited by banked receipts are NOT held anywhere in")
A("catalog/corpus/loose bytes AT THE MOMENT OF THIS SWEEP (2026-10-01 ~19:37Z). The pattern is")
A("systematic, not random: receipts that fetched a primary kept only their own prose about it; the")
A("only citations held are ones a holding pass (state/arxiv ingest, training_pdfs, olm0928 sweep _raw)")
A("happened to catch.")
A("")
A("MOVING ESTATE WARNING: the holdings numbers above are a snapshot of a live tree. Mid-sweep the")
A("holdings grew twice: (a) the spiking-wide gala lane banked ev_arxiv_2509_05276_abstract.md")
A("(1,461 bytes, mtime 18:33Z), and (b) a sibling gathering_expedition lane has been landing fetched")
A("primaries into memory/runs/gathering_expedition/ DURING this check: at final render the dir holds")
healer_dir = "memory/runs/gathering_expedition"
import os as _os
try:
    healer_n = len(_os.listdir(healer_dir))
except OSError:
    healer_n = -1
A(f"{healer_n} files (27 arXiv PDFs were already there by 19:36Z, more may have landed since), healing")
A("a large slice of the gap in flight. The counts in the table are honest for the named moment; a")
A("re-run of this lane's scripts after the healer finishes will read a smaller missing set.")
A("")
A(f"## HELD (durable) - {len(held_dur)}")
A("")
A("| citation | kind | cited-where | holding evidence |")
A("|---|---|---|---|")
for r in sorted(held_dur, key=lambda x: x["value"]):
    A(f"| {r['value']} | {r['kind']} | {cites_str(r, 3)} | {holdings_evidence(r)} |")
A("")
A(f"## HELD (weak: temp-path only) - {len(weak)}")
A("")
A("| citation | kind | cited-where | holding evidence |")
A("|---|---|---|---|")
for r in sorted(weak, key=lambda x: x["value"]):
    A(f"| {r['value']} | {r['kind']} | {cites_str(r, 3)} | {holdings_evidence(r)} |")
A("")
A("## CITED-BUT-MISSING table")
A("")
A("| citation | kind | cited-where | held | fetchable | priority |")
A("|---|---|---|---|---|---|")
for r in sorted(not_held, key=sortkey):
    A(f"| {r['value']} | {r['kind']} | {cites_str(r)} | {holding_str(r)} | {fetch_str(r)} | {prio(r)} |")
A("")
A("Priority legend (claim-weight): P1-HIGH = cited by a drop receipt, 48h_synth steals chapter, olm")
A("DIGEST headline, or 3+ cite locations (a banked claim rests on it in the widest-read surfaces);")
A("P2-MED = 2 cite locations in steal cards; P3-LOW = 1 cite location in a steal card.")
A("")
A("## Named examples of the leak (highest claim-weight)")
A("")
A("1. arXiv 2509.05276 (SpikingBrain) - 13 cite locations across spiking_wide (7 cards) +")
A("   SPIKINGBRAIN_DROP_20261001. At sweep start not one byte was held: the entire wide dig rested")
A("   on prose quotes only. TWO MID-SWEEP HEALS: the spiking-wide gala lane banked abstract bytes")
A("   (watch/inbox/gala_20260925/spiking-wide/lanes/ev_arxiv_2509_05276_abstract.md, 1,461 bytes,")
A("   18:33Z) and the gathering_expedition lane landed the full paper (memory/runs/gathering_expedition/")
A("   p2_2509.05276.pdf, 3.9MB, 19:34Z). The estate healed its biggest leak while this lane measured it.")
A("2. arXiv 2508.16204 (Sakana natural niches) - 10 cite locations in model_mating_paper_dig_20261001")
A("   (MATE_MOE GO-ready verdict). Held at final re-check ONLY via the healer's p2_2508.16204.pdf")
A("   (7.5MB, 19:35Z); no holding existed at sweep start. Repo github.com/SakanaAI/natural_niches")
A("   still not cloned anywhere in the estate.")
A("3. arXiv 2608.10644 - 4 cites in frontier_olm_2026-09-30/steal/agent-memory-continuity.md (the")
A("   agent-memory headline card). Not held at sweep start, while sibling ids from the same sweep")
A("   window (2609.31540, 2609.37902) WERE held in state/arxiv: the old holding pass was partial, not")
A("   principled. The healer's p2_2608.10644.pdf (355KB, 19:34Z) closed this one mid-sweep.")
A("4. github.com/RichSchefren/atlas - localfirst/atlas.md:7 says the card was written from a shallow")
A("   clone at pinned HEAD 229df544944ffb1dadf4d155bcb41334e850da0c, 339 files, read first-hand. The")
A("   clone survives nowhere in the estate: the first-hand-verification claim is unverifiable by bytes.")
A("5. arXiv 2609.27612 (48h_synth/steals.md:204) - catalog hit is a %TEMP% file only")
A("   (%TEMP%/arxiv_2609.27612v1.html). Temp-dir bytes are not a durable estate holding. Classed WEAK.")
A("6. ractor50/accuracy.md:31,33 cites arXiv 2407.12345 as the UF-124/125/126 fabricated-citation")
A("   artifact (the poison canary, accuracy.md:33 falsifier). The id itself resolves (HTTP 200 probe)")
A("   but no banked claim rests on its content; recorded n/a, not counted missing.")
A("")
A("## Instrument proposal (decision ledger)")
A("")
A("ractor50/accuracy.md:35 already specs a citation resolver at the ledger append path (each id must")
A("resolve to fetched bytes in the same session, else the row lands UNVERIFIED, never LANDED). This")
A("sweep extends it to holdings: every LANDED row citing an external primary should leave the primary")
A("bytes in state/arxiv/<date>/<id>v1.txt (the existing 4,010-file archive) or a corpus dir, and cite")
A("that path. A nightly sweep (this lane's three scripts) diffs fresh receipts against holdings and")
A("flags new leaks before the session that held the bytes dies.")
A("")
A("Not run / limits: book-class and non-id primaries (e.g. Wilkes/Wheeler/Gill 1951, already held in")
A("corpus/papers_reference_nonredistributable/) out of scope beyond the extracted id/repo set; unprobed")
A("arXiv ids inherit fetchability from the 3-probe registry verification (same host, same id shape);")
A("content-level checks (does the held text contain the quoted claim) NOT run: held means bytes exist,")
A("not that the quote was re-verified against them.")
A("")
print("\n".join(out))
import sys as _sys
print(json.dumps({"STATS": {"unique_citations": len(rows), "cite_locations": ncite_rows,
                            "held_durable": len(held_dur), "held_weak": len(weak),
                            "not_held": len(not_held), "P1": len(p1), "P2": len(p2),
                            "P3": len(p3)}}, indent=2), file=_sys.stderr)
