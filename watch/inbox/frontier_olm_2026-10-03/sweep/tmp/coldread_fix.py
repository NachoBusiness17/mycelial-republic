# -*- coding: utf-8 -*-
"""Apply the 14 cold-reader fixes to DIGEST.md, amend RECEIPT.md accordingly
(DIGEST size row, self-size fixed point, checks 7-8, cold-reader note), and
regenerate the measurement artifact. Values unchanged except where a fix
corrects an overstatement."""
import json
import os
import re

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_2026-10-03"
DIGEST = os.path.join(ROOT, "DIGEST.md")
RECEIPT = os.path.join(ROOT, "RECEIPT.md")
TXT = "sweep/tmp/fold2_inventory_current.txt"
KGA = "sweep/tmp/kg_reconcile.json"

# ---------- 1. knowledge-graph reconciliation artifact (cold-reader fix 7)
g = json.load(open(r"C:\Users\foste\Documents\projects\local_sovereign_agent\memory\knowledge_graph.json", encoding="utf-8"))
ids = {n.get("id") for n in g["nodes"]}
deg = {i: 0 for i in ids}
dangling_bad = 0
for e in g["edges"]:
    for k in ("source", "target"):
        if e.get(k) not in ids:
            dangling_bad += 1
zero_degree_read = {"nodes_with_degree_ge_1": sum(1 for d in deg.values() if d > 0), "dangling_endpoints": dangling_bad, "of": len(g["edges"]) * 2}
deg = {i: 0 for i in ids}
dangling = 0
dangling_by_rel = {}
for e in g["edges"]:
    s, t = e.get("from"), e.get("to")
    if s in deg:
        deg[s] += 1
    else:
        dangling += 1
        dangling_by_rel[e.get("rel")] = dangling_by_rel.get(e.get("rel"), 0) + 1
    if t in deg:
        deg[t] += 1
    else:
        dangling += 1
        dangling_by_rel[e.get("rel")] = dangling_by_rel.get(e.get("rel"), 0) + 1
ge1 = sum(1 for d in deg.values() if d > 0)
kg = {
    "file": "memory/knowledge_graph.json",
    "schema_keys_on_edges": ["from", "rel", "to", "text"],
    "bugged_read_source_target_keys": {"nodes_with_degree_ge_1": zero_degree_read["nodes_with_degree_ge_1"], "dangling_endpoints": "%d of %d" % (zero_degree_read["dangling_endpoints"], zero_degree_read["of"]), "note": "reproduces the sweep seats' 2086/2086 zero-degree and 825/825-dangling read; caused by parsing nonexistent source/target keys"},
    "correct_read_from_to_keys": {"nodes": 2086, "edges": 825, "nodes_with_degree_ge_1": ge1, "edge_orphans": 2086 - ge1, "dangling_endpoints": "%d of %d" % (dangling, len(g["edges"]) * 2), "dangling_by_rel": dangling_by_rel, "resolving_endpoints": len(g["edges"]) * 2 - dangling, "resolving_decomposition": "825 edge-source endpoints plus the 2 target endpoints of family:readable_first's two edges (the only edges resolving on both ends)"},
    "repair_planning_verdict": "use the lens read (lens/graph.md); the zero-degree read was a field-name bug, now reproduced and identified",
}
with open(os.path.join(ROOT, "sweep", "tmp", "kg_reconcile.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(kg, f, ensure_ascii=True, indent=1)
assert ge1 == 602 and dangling == 823, (ge1, dangling)
print("kg reconcile: ge1=%d dangling=%d" % (ge1, dangling))

# ---------- 2. DIGEST edits
text = open(DIGEST, encoding="utf-8").read()

def sub(old, new):
    global text
    count = text.count(old)
    assert count == 1, "target found %d times: %r" % (count, old[:70])
    text = text.replace(old, new)

# fix 6: header bullet distinct-finds restatement
sub("- `register.jsonl` - 42 confirmed finds, one row each (area, source, title, url, date, quote, why, overlap, confidence); rows 1-23 are the round-1 fold, rows 24-42 the round-2 append",
    "- `register.jsonl` - 42 rows covering 41 distinct finds (row 38 deep-reads the paper of round-1 row 23, so arXiv 2609.04098 appears twice by design; see the row-38 note under the round-2 confirmed table), one row each (area, source, title, url, date, quote, why, overlap, confidence); rows 1-23 are the round-1 fold, rows 24-42 the round-2 append")

# fix 9: exec point 2 headline + tail
sub("2. **The free-lane throttling contradiction resolved at the mechanism level.**",
    "2. **The free-lane throttling contradiction is mechanism-mapped, not resolved.**")
sub("only per-dispatch tank accounting decides RQ2 (steal/open-and-local-language-models.md, lens/laws.md:78).",
    "only per-dispatch tank accounting decides RQ2, so the CONTRADICTION OPEN row stays open until that probe fires (round 2 re-owed it unrun; round-2 exec point 10) (steal/open-and-local-language-models.md, lens/laws.md:78).")

# fix 7: knowledge-graph reconciliation addendum
sub("The definitional gap between the two instruments (edge-orphan vs zero-degree, endpoints vs edges) is unresolved and OWED a reconciled parse before any repair run; either way the graph is mostly unlinked and the repair targets are the same.",
    "(Round-2 fold addendum, run this sitting: the gap is closed as a field-name bug, not a definitional one. This fold first reproduced the zero-degree read byte-for-byte, then found its cause: the edge objects key on from and to, and the 2,086/2,086 zero-degree with 825/825-dangling read parses nonexistent source/target keys, yielding 0 nodes with degree 1 or more and 1,650 of 1,650 endpoints dangling. Re-parsed with from/to, the correct read is the lens's: 602 of 2,086 nodes carry degree 1 or more, leaving 1,484 edge-orphans; 823 of 1,650 endpoints dangle (794 has_invariant targets at invariant pseudo-ids never materialized as nodes, plus 29 of 31 already_inside targets at mangled prose-pasted ids); and the 827 resolving endpoints decompose exactly as the 825 edge-source endpoints, since every edge has a real source node, plus the 2 target endpoints of family:readable_first's two edges, the only edges resolving on both ends. Repair planning uses the lens numbers; the parse command and output are recorded in RECEIPT.md's round-2 checks and kept at " + KGA + ". Either way the repair targets are the same.)")

# fix 10: round-1 door health pullpush annotation
sub("(old.reddit login walls, www/api 403, pullpush 429, r.jina.ai 403, redlib dead)",
    "(old.reddit login walls, www/api 403, pullpush 429 rate-limited rather than dead, since a round-2 paced single request later succeeded, see round-2 unconfirmed item 4; r.jina.ai 403, redlib dead)")

# fix 8: steal 2 import status + scope
sub("first imported at tools/stealth_driver.py:275 _work_lanes / :245 work_payload (closing one of the seven fire surfaces that bypass the EMPTY_REASONING guard by hand-rolling fire params instead of importing mag/inference_budget.py: stealth_driver, duel_harness, tesuji_fire, lane_runner, lite_scale, wave_fire, ds_workhorse; lens/laws.md:83);",
    "first import PROPOSED at tools/stealth_driver.py:275 _work_lanes and :245 work_payload, since no such import exists today: this fold's grep -c inference_budget over the seven named surfaces returned zero in every file (tools/stealth_driver.py, tools/duel_harness.py, mag/tesuji_fire.py, mag/lane_runner.py, mag/lite_scale.py, mag/wave_fire.py, tools/ds_workhorse.py), so all seven presently bypass the EMPTY_REASONING guard by hand-rolling fire params instead of importing mag/inference_budget.py (lens/laws.md:83). Scope: this steal wires stealth_driver first; the other six remain in bypass scope until the same import lands in each;")

# fixes 3 + 12: round-2 intro banking shape + item count
sub("The mine's second same-day pass: all 32 lanes re-ran their doors and appended their round-2 banks to the same sweep/ files (every round-1 section preserved verbatim above its round-2 section), a fresh confirmation pass resolved 24 candidates to 19 confirmed finds plus 5 held with evidence, and 4 steal cards landed (three round-2/3 refinements of round-1 areas plus one new olm arxiv+hf card).",
    "The mine's second same-day pass: all 32 lanes re-ran their doors and banked 227 round-2 lane-banked items counted by this fold from the round-2 sweep results (per area: open-and-local 31, quantization 28, memory 29, swarm 27, finetuning 31, kv 28, evals 28, inference 25), a fresh confirmation pass resolved 24 candidates to 19 confirmed finds plus 5 held with evidence, and 4 steal cards landed (three round-2/3 refinements of round-1 areas plus one new olm arxiv+hf card). Banking shape varied by lane, each variation declared in that lane's own bank note: most lanes appended a round-2 section below a preserved round-1 section; several rebuilt the file while carrying the prior pass attributed or in an appendix (per their notes: the olm-arxiv, memory-hn, memory-x, inference-arxiv and kv-x lanes); the quant-x lane preserved its earlier pass as a sibling .pass0.md file; the olm x lane wrote a new sibling file, sweep/open-and-local-language-models-x.round2.md, rather than overwrite the morning bank; and the round-2 swarm lane replaced sweep/swarm-orchestration-arxiv.md outright without preserving round-1 content, so round-1 bytes for that one file survive only in git history. Round-1 citation targets therefore hold their cited bytes only where the lane preserved them; the one round-1 anchor the replacement broke was re-anchored, and the repair is disclosed in RECEIPT.md's round-2 section.")

# fix 6: register growth sentence
sub("This section is the round-2 fold of that mine. The register grew in place from 23 to 42 rows (rows 24-42 below; row 38 deep-reads the same paper as round-1 row 23 and its overlap field states the upgrade).",
    "This section is the round-2 fold of that mine. The register grew in place from 23 to 42 rows, which is 41 distinct finds (rows 24-42 below; row 38 deep-reads the same paper as round-1 row 23, its overlap field states the upgrade, and 18 of the 19 appended rows are new to the register).")

# fix 14: 6 GB headline scoping
sub("4. **The 6 GB reality check closed.** No post-2026-10-02 release at janitor VRAM class ships measured agentic capability in its card; the measured class exemplar remains",
    "4. **The 6 GB reality check closed for everything the lanes could fetch.** No post-2026-10-02 release at janitor VRAM class ships measured agentic capability in its card; the only post-10-02 release-track bytes the round-2 lanes found were the jfan LiteRT-LM WebGPU mirror uploads of 2026-10-03, whose cards assert everything and measure nothing (lane-banked: sweep/open-and-local-language-models-x.round2.md), and the post-10-02 arXiv sub-window itself read empty from announcement lag (gap 5), so the check reopens if the owed 48-hour re-query or a fresh feed lands a measured 6 GB-class card; the measured class exemplar remains")

# fix 11: exec point 6 referents
sub("an independent Jev research report measured MMLU-Pro 82.7 percent for about $0.28 total with a roughly 4x order-of-options primacy bias any routing use must randomize against (lane-banked: sweep/open-and-local-language-models-reddit.md); Gevva0 shows single-prefill logit-scored routing works on stock Gemma 26B while janitor-class E2B/E4B hit a hard wall (lane-banked: sweep/inference-efficiency-reddit.md).",
    "an independent third-party measurement dossier of the TypeSafe Jev decision-model API (jevresearch.github.io/Jev-Research, a research site, not the vendor) measured MMLU-Pro 82.7 percent for about $0.28 total with a roughly 4x order-of-options primacy bias any routing use must randomize against (lane-banked: sweep/open-and-local-language-models-reddit.md); Gevva0 (github.com/solvingSteve/Gevva0, a community project that answers Jev-style choice questions by direct logit readout on stock Gemma 26B in one prefill) shows that pattern working at 26B while janitor-class E2B/E4B hit a hard wall (lane-banked: sweep/inference-efficiency-reddit.md and sweep/inference-efficiency-hn.md).")

# fix 5: exec point 7 hypothesis phrasing
sub("7. **Continuity's exporter went from nice-to-have to P0.** The vendor session store reaps on a roughly 30-day horizon (146 sessions older than 30 days at the card's census read; steal/agent-memory-and-continuity.md), and the transcript-as-leaf law",
    "7. **Continuity's exporter went from nice-to-have to P0.** The card's P1 hypothesis is a vendor reap horizon near 30 days; today's census shows 146 sessions older than 30 days still present (steal/agent-memory-and-continuity.md), so the horizon is not enforced-destructive at read time and the weekly census (P1 shrink versus P2 hold) is the instrument that decides, with the exporter landing at background priority under either branch. The transcript-as-leaf law")

# fixes 1 + 2: exec point 8 censuses and probe-1 disposition
sub("Two independent estate censuses found zero quota or limit kill rows in any lane trail, so the redo-vs-resume fraction is unmeasurable until a death-event writer exists (sweep/swarm-orchestration-hn.md, sweep/swarm-orchestration-reddit.md).",
    "Three round-2 censuses classified the round-1 card's raw marker hits (elder 15, harvest 12, research 722): the research hits are arxiv-source-down MONITOR observations, not kills; elder's rows are 14 to 15 daily CYCLE_FAIL lane-down rows spanning 09-20 to 10-03 (the 15-versus-14 spread is an instrument and moment difference, left unreconciled per the counts law); harvest's 12 are strict-429 lane-cycle deaths; all 26 fatal rows were re-done by the next cadence with zero resume markers, and the code-1005 workflow-quota wall left no trail row at all. At the level steal 4 and 5 target, workflow children, genuine limit-kill rows number zero, so round-1 probe 1's own fewer-than-5 branch fires and those two ports are DEFERRED as instrumented, while the redo-vs-resume fraction stays unmeasurable until a death-event writer exists (sweep/swarm-orchestration-arxiv.md, sweep/swarm-orchestration-hn.md, sweep/swarm-orchestration-reddit.md).")

# fix 5: steal 8 hypothesis phrasing
sub("- **Steal:** the vendor session store reaps on a roughly 30-day horizon, so the thought-bank continuity exporter is the only durable copy of estate session history and lands at background priority either way; resume the reasoning harvest,",
    "- **Steal:** the vendor session store may reap near a 30-day horizon (P1 hypothesis; today's census shows 146 sessions older than 30 days still present, so P2, no reaper, is not excluded), making the thought-bank continuity exporter the estate's only durable copy under P1 and cheap background-priority insurance under P2; resume the reasoning harvest,")

# fix 4: steal 9 OUI-1 wiring clarification
sub("configs/mirrors.json takes the OUI-1 primary numbers to move the burns UNVERIFIED flag.",
    "configs/mirrors.json takes the OpenUI team's own measured numbers from the 1wavhij thread (register row 34) to RETIRE the OUI-1 card's UNVERIFIED flag, not to wire the unverified OUI-1 claims, which stay unwired until a primary lands (round-1 gap 6 and round-2 unconfirmed item 5 both leave that primary owed).")

# fixes 1 + 2: gap 4 reconciliation
sub("4. The redo-vs-resume census does not replicate on the estate corpus because no subagent-granularity death ledger exists; two independent censuses over the lane trails this pass found zero quota or limit kill rows (tallies taken at different moments over different lane sets: one read 7,492 trail rows with 748 strict-429 rows and 26 fatal, the other read CYCLE 3,119, MONITOR 2,852, CYCLE_FAIL 735, HEARTBEAT 605); answering it needs a death-event writer (attempt count plus redone, resumed, or salvaged disposition) (sweep/swarm-orchestration-hn.md, sweep/swarm-orchestration-reddit.md).",
    "4. The redo-vs-resume census does not replicate on the estate corpus because no subagent-granularity death ledger exists. Reconciliation with round 1's card-counted marker hits (elder 15, harvest 12, research 722): those were raw marker greps, and the round-2 classified reads attribute them as research = arxiv-source-down MONITOR observations, not kills; elder = 14 to 15 daily CYCLE_FAIL lane-down rows from 09-20 to 10-03 (the 15-versus-14 spread is an instrument and moment difference, unreconciled per the counts law); harvest = 12 strict-429 lane-cycle deaths. Totals: 26 fatal rows, zero resumed, all re-done by cadence, zero code-1005 rows anywhere (the BUILD-IT-ALL quota wall left no trail row). So the marker scan was unclassified rather than false, and at the workflow-child level the ports target, genuine limit-kills number zero: round-1 probe 1's fewer-than-5 branch fires and the steal 4 and 5 ports are deferred as instrumented (tallies taken at different moments over different lane sets: one census read 7,492 trail rows with 748 strict-429 rows and 26 fatal, another read CYCLE 3,119, MONITOR 2,852, CYCLE_FAIL 735, HEARTBEAT 605). A future re-opener needs a death-event writer (attempt count plus redone, resumed, or salvaged disposition) (sweep/swarm-orchestration-arxiv.md, sweep/swarm-orchestration-hn.md, sweep/swarm-orchestration-reddit.md).")

# fix 10: unconfirmed item 4 pullpush reconciliation
sub("An independent archive (api.pullpush.io) holds the full post",
    "An independent archive (api.pullpush.io, the same pullpush service round-1 lanes logged at 429: rate-limited under burst rather than dead, and this pass's single paced request succeeded) holds the full post")

# fix 13: quant probe ordering
sub("2. Reasoning-quant ladder (percolator row 7): $0 plus one 1.9 GB pull on the operator's box, one afternoon; also mints the q8_0 arm owed since the 09-30 round's steal card.",
    "2. Reasoning-quant ladder (percolator row 7): $0 plus one 1.9 GB pull on the operator's box, one afternoon; first of the two quant probes (smaller pull than round-1 probe 5's 8.1 GB, one arm already on box, and it adds the thinking-token and empty-content channels); it mints the deepseek q8_0 arm owed since the 09-30 round's steal card, which is a different debt from round-1 probe 5's qwen2.5:7b A/B.")

# fixes 1 + 13: probe-status ledger
sub("Round 1's five probes (fold recommendation above) stand unchanged; the round-2 lanes re-owed round-1 probe 3's tank accounting and probe 5's A/B without firing them.",
    "Probe-status ledger after round 2: round-1 probe 1 (salvage census) has been fired by the round-2 swarm lanes, and its fewer-than-5 branch fires at the workflow-child level, so the steal 4 and 5 ports are deferred as instrumented (exec point 8 and gap 4). Round-1 probe 3 (tank accounting) and probe 5 (qwen2.5:7b Q4-vs-Q8 A/B) were re-owed unrun; probe 5 stays second in the quant order behind the reasoning-quant ladder and is not discharged by it (different model family, and the cache-divergence prior at arxiv.org/abs/2609.04748 is qwen2.5-7b-specific). Round-1 probes 2 (imagined-grader census) and 4 (takeover A/B) stand unchanged.")

# fix 6: confirmed table header
sub("### Confirmed finds, round 2 (19; register rows 24-42)",
    "### Confirmed finds, round 2 (19 rows, 18 new finds; register rows 24-42)")

with open(DIGEST, "w", encoding="utf-8", newline="\n") as f:
    f.write(text)
digest_size = os.path.getsize(DIGEST)
print("DIGEST.md bytes now:", digest_size)

# ---------- 3. RECEIPT edits
rtext = open(RECEIPT, encoding="utf-8").read()

def rsub(old, new):
    global rtext
    count = rtext.count(old)
    assert count == 1, "receipt target found %d times: %r" % (count, old[:70])
    rtext = rtext.replace(old, new)

rsub("Round-2 fold of the same run: DIGEST.md gained the Round 2 fold section (and its header counts were updated), register.jsonl grew from 23 to 42 rows (rows 24-42; row 38 deep-reads the paper of round-1 row 23, overlap stated in-row), percolator_candidates.jsonl grew from 5 to 9 rows (rows 6-9). Line 1 of this receipt is unchanged.",
     "Round-2 fold of the same run: DIGEST.md gained the Round 2 fold section (and its header counts were updated), register.jsonl grew from 23 to 42 rows (rows 24-42; row 38 deep-reads the paper of round-1 row 23, overlap stated in-row), percolator_candidates.jsonl grew from 5 to 9 rows (rows 6-9). Line 1 of this receipt is unchanged. Amended the same sitting after a cold-reader review: 14 fixes applied to DIGEST.md (probe-status ledger for round-1 probe 1, census reconciliation with the round-1 marker counts, banking-shape correction with the round-2 item count, OUI-1 wiring clarification, reap-phrasing moved to hypothesis, 42-rows-over-41-distinct restatement, knowledge-graph reconciliation by parse, bypass-import status and scope, contradiction-headline softening, pullpush door annotation, referent expansions for the Jev dossier and Gevva0, 6 GB headline scoped to the fetched window, quant-probe ordering, confirmed-table count restatement).")

rsub("6. Self-size fixed point: placeholder substituted at equal width, re-measured equal (assertion in script).",
     """6. Self-size fixed point: placeholder substituted at equal width, re-measured equal (assertion in script).
7. Cold-reader fix 8 bypass-import check: grep -c inference_budget tools/stealth_driver.py tools/duel_harness.py mag/tesuji_fire.py mag/lane_runner.py mag/lite_scale.py mag/wave_fire.py tools/ds_workhorse.py returned 0 in all seven files (the four mag/ paths located by a filename walk this sitting; the card's bare names tesuji_fire, lane_runner, lite_scale and wave_fire live under mag, not tools). tools/stealth_driver.py:275 and :245 verified as the _work_lanes and work_payload definitions by sed.
8. Cold-reader fix 7 knowledge-graph reconciliation: two .venv/Scripts/python.exe parses of memory/knowledge_graph.json this sitting, output kept at sweep/tmp/kg_reconcile.json. With source/target keys: 0 nodes with degree 1 or more, 1,650 of 1,650 endpoints dangling, reproducing the 2,086/2,086 zero-degree read as a field-name bug (the schema keys edges from/to). With from/to: 602 nodes with degree 1 or more, 823 of 1,650 endpoints dangling (has_invariant 794 plus already_inside 29), 827 resolving endpoints, matching lens/graph.md's 1,484 edge-orphans (2,086 minus 602). Repair planning uses the lens numbers.""")

# DIGEST size row + self size row -> placeholders
rtext = re.sub(r"\| DIGEST\.md \| \d{5} \| \(" + re.escape(TXT) + r"\)", "| DIGEST.md | 00001 | (" + TXT + ")", rtext, count=1)
rtext = re.sub(r"\| RECEIPT\.md \| \d{5} \| \(" + re.escape(TXT) + r"\)", "| RECEIPT.md | 00002 | (" + TXT + ")", rtext, count=1)

final_digest = None
final_receipt = None
for _ in range(5):
    open(RECEIPT, "w", encoding="utf-8", newline="\n").write(rtext)
    ds = os.path.getsize(DIGEST)
    rs = os.path.getsize(RECEIPT)
    nt = rtext.replace("| DIGEST.md | 00001 | (" + TXT + ")", "| DIGEST.md | %05d | (" % ds + TXT + ")")
    nt = nt.replace("| RECEIPT.md | 00002 | (" + TXT + ")", "| RECEIPT.md | %05d | (" % rs + TXT + ")")
    if nt == rtext:
        final_digest, final_receipt = ds, rs
        break
    rtext = nt
open(RECEIPT, "w", encoding="utf-8", newline="\n").write(rtext)
final_receipt = os.path.getsize(RECEIPT)
final_digest = os.path.getsize(DIGEST)
rbody = open(RECEIPT, encoding="utf-8").read()
assert ("| DIGEST.md | %05d | (" % final_digest) + TXT + ")" in rbody, "digest row mismatch"
assert ("| RECEIPT.md | %05d | (" % final_receipt) + TXT + ")" in rbody, "receipt row mismatch"
print("final: DIGEST.md=%d RECEIPT.md=%d" % (final_digest, final_receipt))

# ---------- 4. regenerate measurement artifact at final state
claims = [
    ("steal/agent-memory-and-continuity.md", "chars", 16124),
    ("steal/open-and-local-language-models-arxiv-hf.md", "bytes", 24852),
    ("steal/quantization-and-compression.md", "chars", 22856),
    ("sweep/agent-memory-and-continuity-hn.md", "bytes", 15259),
    ("sweep/evals-and-self-improvement-x.md", "bytes", 21603),
    ("sweep/open-and-local-language-models-arxiv.md", "bytes", 18525),
    ("sweep/quantization-and-compression-hn.md", "bytes", 34342),
    ("sweep/swarm-orchestration-hn.md", "bytes", 16729),
    ("sweep/swarm-orchestration-reddit.md", "bytes", 35621),
    ("sweep/swarm-orchestration-x.md", "bytes", 31487),
]
entries = []
total = 0
for dirpath, dirnames, filenames in os.walk(ROOT):
    for fn in filenames:
        p = os.path.join(dirpath, fn)
        rel = os.path.relpath(p, ROOT).replace("\\", "/")
        entries.append((rel, os.path.getsize(p)))
        total += os.path.getsize(p)
entries.sort()
size_map = dict(entries)
with open(os.path.join(ROOT, "sweep", "tmp", "fold2_inventory_current.txt"), "w", encoding="utf-8", newline="\n") as f:
    for rel, sz in entries:
        f.write("%9d  %s\n" % (sz, rel))
    f.write("TOTAL files=%d bytes=%d\n" % (len(entries), total))
    f.write("claimed-versus-measured (regenerated at the round-2 fold close):\n")
    for rel, unit, claimed in claims:
        f.write("  %-55s claimed %s=%d measured=%d match=%s\n" % (rel, unit, claimed, size_map.get(rel, -1), str(size_map.get(rel) == claimed).lower()))
    f.write("round-1 fold files (historical, from the round-1 receipt): 30695 24640 15161 15190\n")
    f.write("round-1 cross-check values for files since grown by round-2 lanes (historical): 20931 12374 16905 14506 16674 19205\n")
inv_body = open(os.path.join(ROOT, "sweep", "tmp", "fold2_inventory_current.txt"), encoding="utf-8").read()
assert str(final_digest) in inv_body and str(final_receipt) in inv_body
print("inventory regenerated: files=%d bytes=%d" % (len(entries), total))
