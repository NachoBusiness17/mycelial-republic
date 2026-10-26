"""B2-464 board apply, REBASED (one-shot, anchored, appends + landing note).

Rebase history: v1 at ~19:24Z aborted on its own count==1 assert because the
B2-464 row had been flipped [x] by a concurrent hand with no landing note (and
B2-465's lane claimed band B2-498..B2-500 at 19:24:30Z); per the claim law this
v2 re-reads fresh bytes, numbers past the highest mentioned id, appends the
CLAIM line BEFORE the brief rows, and appends the LANDED note (receipt
pointer) to the already-checked B2-464 row, retiring the B2-238 exposure the
unpointed flip created. No whole-file restore; single transform+write on bytes
read inside this script; count==1 asserts on every anchor.
"""
import re
from pathlib import Path

QUEUE = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent"
             r"\watch\inbox\burn_wave_20260926\QUEUE.md")
RECEIPT = ("watch/inbox/burn_wave_20260926/B2_464_caller_census_20260926.md")
TS = "2026-09-26T19:28:27Z"

text = QUEUE.read_text(encoding="utf-8")

# --- anchor asserts (count == 1 each) -------------------------------------
row_anchor = "- [x] B2-464 corpus_search caller census after the FTS5 wiring:"
assert text.count(row_anchor) == 1, "B2-464 checked row not uniquely found"
tail_anchor = ("taken mid-lane by a concurrent self-feed, renumbered "
               "highest+1 at apply time per the B2-167 law)")
assert text.count(tail_anchor) == 1, "B2-464 row tail not uniquely found"
assert "LANDED 2026-09-26T19:24:30Z" not in text, "landing note already present"

# --- band: number past the highest id mentioned anywhere on the board -----
ids = [int(m) for m in re.findall(r"B2-(\d+)", text)]
start = max(ids) + 1
band = (start, start + 1, start + 2)
for i in band:
    assert not re.search(r"B2-%d\b" % i, text), "band id collision: B2-%d" % i

foreign = [ln.strip()[:120] for ln in text.splitlines()
           if ln.strip().startswith("- CLAIM ") and "CLAIMED" not in ln[:12]]

briefs = [
    (start, (
      "- [ ] B2-{0} B2_22_fts5_spike.py re-run guard: the B2-464 census proved the "
      "spike misreads the wired corpus_search (baseline arm line 155 calls the "
      "production tool with no scan force, line 159 hardcodes engine=scan, line 196 "
      "classifies the full-scan class by rows_scanned >= rows_indexed, a predicate "
      "only true under pre-wiring lines-read semantics; build_index() first deletes "
      "the production db and rebuilds the meta-less schema so _fts_state() reads "
      "fresh-by-mtime and every baseline call takes the index path, walked rows "
      "never reach 757667, full=[] and all four class medians land None); force the "
      "scan arm (point module FTS_DB at an absent path in-process, the B2-102 A/B "
      "pattern) or classify on res['engine'] + res.get('parity_note') instead of the "
      "hardcoded label, and re-run for fresh post-wiring A/B numbers; falsifier: the "
      "unfixed spike prints full_scan_queries [] with full_scan_median_ms null; "
      "pointers watch/inbox/burn_wave_20260926/B2_22_fts5_spike.py:155,159,196 + "
      "watch/inbox/burn_wave_20260926/B2_464_caller_census_20260926.md Falsifier 1 "
      "(self-fed by B2-464).")),
    (start + 1, (
      "- [ ] B2-{0} the rescan writer silently ages the index into permanent scan "
      "fallback: catalog/catalog.jsonl was rewritten 2026-09-26T19:16:30Z "
      "(133,894,969 bytes, 489,548 total_rows, live stat during B2-464) while "
      "catalog_fts.sqlite still answers from the 18:55:08Z build over the "
      "214,470,472-byte map, so every term query walks the scan arm with "
      "index_state=stale until someone remembers tools/corpus_fts_rebuild.py; "
      "mag/catalog_rescan.py rebuild()/incremental() write the catalog and manifest "
      "but never chain an index rebuild, and B2-465 only arms a daily CHECKER; chain "
      "a rebuild (or an explicit invalidate + scheduled-rebuild note) into the "
      "rescan writer's completion path so a map write never leaves the index stale "
      "past its own run; falsifier: incremental() over a fixture catalog with an "
      "index present must end fresh or exit non-zero naming the stale index; "
      "pointers mag/catalog_rescan.py rebuild/incremental + "
      "watch/inbox/burn_wave_20260926/B2_464_caller_census_20260926.md Evidence 17 "
      "(self-fed by B2-464).")),
    (start + 2, (
      "- [ ] B2-{0} census prose fossils: mag/catalog_rescan.py:9 cites the qdrop "
      "probe as rows_scanned 757667, true only under pre-wiring scan semantics "
      "(post-wiring a fresh-index qdrop search reports rows_scanned 0 walked, and "
      "757667 reappears only on the stale-scan arm where the early-break usually "
      "stops far earlier), and mag/mcp_server.py:14 says dashboard /run_task "
      "dispatches the same TOOL_MAP while the dispatch lives in backend/server.py "
      "/run_task (dashboard/rest.py imports no TOOL_MAP at all); fix both anchors to "
      "the current truth so the next census does not chase them; falsifier: grepping "
      "the two files today finds both fossils, and after the fix the qdrop C6 story "
      "states the engine split explicitly; pointers mag/catalog_rescan.py:9 + "
      "mag/mcp_server.py:14 + watch/inbox/burn_wave_20260926/"
      "B2_464_caller_census_20260926.md Evidence 5 and 12 (self-fed by B2-464).")),
]

claim_line = ("  - CLAIM B2-464 watch/inbox/burn_wave_20260926/QUEUE.md " + TS +
              " (B2-464 self-feed band B2-%d..B2-%d; highest id on fresh bytes "
              "B2-%d; foreign active CLAIMs B2-104, B2-469, B2-465 and B2-489 on "
              "this file honored, appends plus one landing-note append only, no "
              "rewrite; v1 apply at ~19:24Z aborted on its own count==1 assert when "
              "the B2-464 row was found already flipped [x] unpointed and band "
              "498..500 was found claimed by B2-465)" % (band[0], band[2], max(ids)))

lines = text.splitlines()
out = []
for ln in lines:
    if ln.rstrip().endswith(tail_anchor):
        ln = ln.rstrip()[:-len(tail_anchor)] + tail_anchor + \
             " (LANDED 2026-09-26T19:24:30Z receipt " + RECEIPT + \
             "; the [x] flip predates this note on the bytes, this note is the " \
             "landing lane's pointer per the B2-238 law)"
    out.append(ln)
while out and not out[-1].strip():
    out.pop()
out.append("")
out.append(claim_line)
for i, body in briefs:
    out.append(body.format(i))
QUEUE.write_text("\n".join(out) + "\n", encoding="utf-8")

print("APPLIED band B2-%d..B2-%d" % (band[0], band[2]))
print("LANDED NOTE APPENDED to B2-464 row")
print("FOREIGN_ACTIVE_CLAIMS %d" % len(foreign))
for f in foreign:
    print("  ", f)
