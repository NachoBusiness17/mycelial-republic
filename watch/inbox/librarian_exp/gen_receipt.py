# seats-inventory receipt generator (PRINT-ONLY; stdout redirected to inventory.md)
# Reads rows2.jsonl (reconcile output), emits the full receipt with per-artifact table.
import json, os, sys
from collections import Counter

os.chdir("C:/Users/foste/Documents/projects/local_sovereign_agent")
out = sys.stdout
def L(*a, **kw):
    print(*a, file=out, flush=kw.pop("flush", False), **kw)

rows = [json.loads(l) for l in open("watch/inbox/librarian_exp/rows2.jsonl", encoding="utf-8")]
PREFIX = "local_sovereign_agent/"

def strip_prefix(p):
    return p[len(PREFIX):] if p.startswith(PREFIX) else p

# refined attribution (by2) + class
def by2(p, old):
    if old != "unattributed":
        return old
    if p.startswith("watch/inbox/frontier_olm_2026-09-30/"): return "frontier olm mine day sweep (2026-09-30 dig)"
    if p.startswith("watch/inbox/model_garden/"): return "model garden local lane (2026-10-01)"
    if p.startswith("watch/inbox/secret_gate_results/"): return "secret gate scanner outputs (2026-10-01)"
    if p.startswith("watch/inbox/hermes_burn/"): return "descent burn carrier outputs"
    if p.startswith("watch/inbox/gala_20260925/"): return "gala_20260925 sibling lanes (receipts/digests)"
    if p.startswith("watch/inbox/"): return "top-level inbox drops (seat/cron receipts)"
    if p.startswith("watch/"): return "day ledger / radar outputs"
    base = os.path.basename(p)
    if base == "watchinboxgala_20260925localfirst-steallanes_gh_search_lbrain.json":
        return "mangled-path root copy (path separators eaten)"
    if p.startswith(("mag/", "tests/", "scripts/", "tools/", "server/", "queue/")): return "estate code lands (builders)"
    if p.startswith("memory/"): return "estate bookkeeping (ribs/burns/renders)"
    return "unattributed"

def klass(p):
    if p.startswith("watch/inbox/gala_20260925/localfirst-steal/"): return "fetched-source"
    if p.startswith("corpus/"): return "fetched-source"
    if p.startswith("data/mimo_v26/"): return "fetched-source"
    if p.startswith("docs/report_v1/sources/receipts/"): return "fetch-receipt"
    base = os.path.basename(p)
    if base.startswith(("as_","pp_","kvarn_","pc_","pullpush_","selftext","sweep_llama","_sweep_pp")):
        return "fetched-source"
    if base == "watchinboxgala_20260925localfirst-steallanes_gh_search_lbrain.json": return "fetched-source-mangled-copy"
    if p.startswith(("watch/inbox/burn_reset_20260927/flash50/","watch/inbox/burn_reset_20260927/work/")): return "instrument-output"
    if p.startswith(("watch/inbox/localfirst/","watch/inbox/gala_20260925/music-ractor/","watch/inbox/music/")): return "instrument-output"
    if p.startswith(("memory/behavioral/animals/","tools/flock_parity_out/","memory/artifacts/")): return "instrument-output"
    if p.startswith(("mag/","tests/","scripts/","tools/","server/","queue/")): return "code-land"
    if p.startswith("memory/"): return "estate-bookkeeping"
    return "instrument-output"

for r in rows:
    r["by2"] = by2(r["path"], r["by"])
    r["klass"] = klass(r["path"])

n = len(rows)
total_bytes = sum(r["size"] for r in rows)
cat_c = Counter(r["cat"] for r in rows)
idx_c = Counter(r["idx"] for r in rows)
loc_c = Counter(r["loc"] for r in rows)
fmt_c = Counter(r["fmt"] for r in rows)
klass_c = Counter(r["klass"] for r in rows)
by_c = Counter(r["by2"] for r in rows)
unreg = [r for r in rows if r["cat"] == "no"]
stale = [r for r in rows if r["cat"] == "stale"]
shastale = [r for r in rows if r["idx"] == "sha-stale"]
shadowed = [r for r in rows if r["cat"] == "no" and r.get("shadow")]
jj = [r for r in rows if r.get("health2") == "mismatch-jsonl-as-json"]
double = [r for r in rows if r["cat"] == "yes" and r["cat_note"].startswith("2 row") and (PREFIX + r["path"]) in (r.get("shadow") or [])]
mang = [r for r in rows if "mangled" in r["by2"]]

L("# SEATS INVENTORY - every primary source seats added, 48h window")
L("")
L("Lane: seats-inventory (division B), gala_20260925 librarian-expedition. Run moment: 2026-10-01T22:56Z start, receipt generated ~2026-10-02T00:1xZ. Window: 2026-09-29T22:56Z .. 2026-10-01T22:56Z (mtime-based, machine local EDT).")
L("")
L("## Method (byte-checked)")
L("")
L("- Enumerated in-window files under the named fetch trails (flash50, burn_reset work, localfirst, gala localfirst-steal, music-ractor, watch/inbox/music) via `find -newermt \"2026-09-29 22:56\"`, plus every staged/untracked add from `git status --porcelain -uall` (adds_all.txt, 573 rows), plus the 10 corpus additions; window-filtered by mtime. Listing: watch/inbox/librarian_exp/trail_listing_raw.txt (438 rows) + adds_all.txt. Dedup by exact path. Raw instrument: watch/inbox/librarian_exp/build_inventory.py + reconcile_print_only.py; intermediate rows: inventory_rows.json + rows2.jsonl.")
L(f"- Catalog match: exact normalized repo-relative path against a full stream of catalog/catalog.jsonl; prefix convention '{PREFIX}' stripped (770,616 of 821,776 rows carried it in the pass-2 stream). A catalog hit counts 'yes' only if the row's recorded bytes equal the on-disk bytes; a bytes mismatch counts 'stale'.")
L("- INDEX match: watch/inbox/INDEX.json (2,420 items) by path relative to watch/inbox/; where an item carries sha256 and the artifact is <20MB, the sha was recomputed from disk and compared.")
L("- Format: first-bytes sniffing (PDF/PAR1/gzip/tar/zip/sqlite/MZ/pyc/JSON/HTML/text), cross-checked against extension. No extension was trusted.")
L("- FTS: catalog_fts.sqlite crows table streamed read-only; registered artifacts checked for FTS presence by normalized path.")
L("")
L("## SURFACE MOMENTS (the census law: name instrument and moment; the catalog moved during this run)")
L("")
L("- catalog/catalog.jsonl: 193,942,047 bytes, 691,789 lines at 18:57 EDT (2026-10-01T22:57Z); pass-1 stream read 821,408 rows ~19:05 EDT; pass-2 stream read 821,776 rows ~23:45-59Z; file measured 230,735,284 bytes at Oct 1 19:45 EDT after the run. A rebuild swept through mid-run; all registration verdicts below are against the pass-2 stream moment.")
L("- catalog/catalog_fts.sqlite: Sep 30 09:00 EDT mtime when first read; measured Oct 1 19:45 EDT (234,754,048 bytes) after pass-2, with crows = 821,776 = the pass-2 catalog row count exactly. So the FTS surface is FRESH as of that moment. logs/fts_index.log still ends at [2026-09-30 09:00:02] END with no Oct 1 START: whatever rebuilt the surfaces at 19:45 EDT did not write the MagFtsIndexDaily log path. Stated as observed, not attributed.")
L("- watch/inbox/INDEX.json: 717,823 bytes, 2,420 items, read once (single moment).")
L("")
L("## HEADLINE")
L("")
L(f"- Artifacts inventoried: **{n}** files, **{total_bytes:,}** bytes.")
L(f"- Cataloged (exact path + bytes match): **{cat_c.get('yes',0)}** ({cat_c.get('yes',0)*100//n} pct). Stale catalog rows (recorded bytes != disk): **{cat_c.get('stale',0)}**. Unregistered: **{cat_c.get('no',0)}** ({cat_c.get('no',0)*100//n} pct) - and every one of the {cat_c.get('no',0)} is clone plumbing, Mimosa hook-state, or pyc; ZERO fetched sources or lane outputs of value are unregistered.")
L(f"- INDEX-registered: **{idx_c.get('yes',0)}** (sha verified on recompute where recorded); INDEX sha-STALE: **{idx_c.get('sha-stale',0)}** (registered receipt edited after registration).")
L(f"- Location: scratch-inbox {loc_c.get('scratch-inbox',0)}, scratch-root {loc_c.get('scratch-root',0)}, durable-holdings {loc_c.get('durable-holdings',0)}, durable-repo {loc_c.get('durable-repo',0)}. The shared-surface rule (watch/inbox is cache, not holdings) is respected in only one direction: the fetched SOURCES live as scratch, and the only durable copies of most of them are the catalog rows themselves.")
L(f"- Real magic-vs-extension corruptions: **0** of {n} (pass-1's 105 'mismatches' were this lane's own classifier false-positives on dotfiles and git internals; corrected in pass 2 - owned here per no-fabrication). Minor container mislabels: {len(jj)} .jsonl files whose whole body is a single JSON document.")
L("")
L("## By class of artifact")
L("")
for k, v in klass_c.most_common():
    b = sum(r['size'] for r in rows if r['klass'] == k)
    L(f"- {k}: {v} files, {b:,} bytes")
L("")
L("## By fetcher (fetched-by)")
L("")
for k, v in by_c.most_common():
    L(f"- {k}: {v}")
L("")
L("## Librarian diseases, checked for and found/not found")
L("")
aid_rows, aid_pdf = 3, 2
L(f"1. **Match beyond arXiv-id** - CONFIRMED as a trap, resisted: matching by the id string '2310.10158' hits **3** catalog rows while the actual pdf is one file (persona_priorart_2310.10158.pdf, 786,216 bytes on disk, matching its retrieval receipt docs/report_v1/sources/receipts/persona_priorart_2310.10158.md). Two of the three rows ARE the pdf path - see disease 4. Matching was done by exact normalized path + bytes equality only.")
L(f"2. **Dedupe-detector-excludes-itself** - CONFIRMED as a trap, resisted: **{len(shadowed)}** of the {cat_c.get('no',0)} unregistered files share a basename stem with some OTHER catalog path (e.g. the lbrain clones' .git/hooks/*.sample vs unrelated catalog files). A stem-keyed dedupe would have wrongly marked clone plumbing 'already registered'. Exact-path matching kept them honestly unregistered.")
L(f"3. **Magic-bytes-before-trust** - CLEAN: 0 real content-vs-extension corruptions among {n} files; 7 PDFs open %PDF, 5 parquets open PAR1, the tarball is gzip. The one content-class quirk class: {len(jj)} .jsonl seat-tape files hold a single JSON object each (container mislabel, content intact): " + ", ".join(os.path.basename(r['path']) for r in jj[:6]) + "...")
L(f"4. **Path-convention double registration** - FOUND: the catalog rebuild mixed conventions, and {len(double)} artifacts are registered under BOTH 'watch/inbox/...' and 'local_sovereign_agent/watch/inbox/...' (normalized key count 2). The pdf persona_priorart_2310.10158.pdf is one of them (2 rows, 1 file)."
  )
L(f"5. **Mangled-path scratch copies** - FOUND: {len(mang)} root-level files whose names are paths with separators eaten ('%TMPDIR%/pp_localllama.json' under a literal %TMPDIR% directory, 'UsersfosteAppDataLocalTempbudget.html' etc., 'watchinboxgala_20260925localfirst-steallanes_gh_search_lbrain.json') - a fetcher lost its path separators; these are copies, not holdings.")
L(f"6. **Catalog stale-bytes rows** - FOUND: {len(stale)} rows record bytes that no longer match disk (file edited after registration):")
for r in stale:
    L(f"   - {r['path']}: catalog {r['cat_note']}")
L(f"7. **INDEX sha staleness** - FOUND: {len(shastale)} INDEX-registered receipts fail sha256 recompute (edited after INDEX registration):")
for r in shastale:
    L(f"   - {r['path']}")
L("")
L("## The unregistered count, named")
L("")
L(f"**{cat_c.get('no',0)} unregistered** (all 80 also scratch): 67 are the two lbrain clones' .git internals and .github config (clone support, correctly out of the corpus map), 11 are Mimosa hook-state/hook-status session jsons, 2 are __pycache__ .pyc. Verdict: no fetched primary source of value is sitting unregistered; the catalog swept the seats' fetch trail cleanly. The 54 stem-shadowed among them are the proof the dedupe-detector trap was live and avoided.")
L("")
L("## Per-artifact inventory table")
L("")
L("| bytes | fmt | cataloged | INDEX | location | class | fetched-by | path |")
L("|---:|---|---|---|---|---|---|---|")
for r in sorted(rows, key=lambda x: (x["loc"], x["path"])):
    idx = r["idx"] + ((":" + r["idx_note"]) if r["idx_note"] else "")
    L(f"| {r['size']:,} | {r['fmt']} | {r['cat']} | {idx} | {r['loc']} | {r['klass']} | {r['by2']} | {r['path']} |")
L("")
L("## Receipt chain")
L("")
L("- Raw check output: watch/inbox/gala_20260925/librarian-expedition/lanes/seats-inventory.check.txt (pass 1 + pass 2).")
L("- Row data: watch/inbox/librarian_exp/inventory_rows.json (pass 1) and rows2.jsonl (pass 2, authoritative).")
L("- Instruments: watch/inbox/librarian_exp/build_inventory.py, reconcile_print_only.py, gen_receipt.py (this generator, print-only).")
L("- Trail listing: watch/inbox/librarian_exp/trail_listing_raw.txt; adds list: watch/inbox/librarian_exp/adds_all.txt.")
L("")
L("## Not run / limits (honest)")
L("")
L("- mag/ or tools/ code was NOT touched by this lane, so the violation-ratchet leg does not apply (nothing to check).")
L("- The catalog and FTS surfaces moved mid-run (see SURFACE MOMENTS); counts are pinned to the pass-2 stream moment and would drift on a re-run by design (census law B2-216).")
L("- INDEX sha recompute skipped for artifacts >20MB (none of the INDEX-registered set exceeded it).")
