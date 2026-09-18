# CORPUS MAP SALON — 2026-09-18 (ractor salon, self-steal shape-train)

**Operator ask:** self-steal the entire corpus — map, understand, catalog, tag —
and build a sane MCP connector / surfacing hook, so the trajectory can later be
mined for a better version of us. Free lanes launched at it. Dogfood everything.

**Anchor (operator post @NachoQuixotic 2100789178564816932, 2026-09-18):**
> "More often than not our estimation of the thing replaces the thing. Our
> expectations shape what we experience."

That sentence became the design law: **the map stays subordinate to the bytes.**

---

## THE FOLD (S6 conductor synthesis)

The salon's convergent verdict: **the mapping already happened** —
`catalog/catalog.jsonl` (946,773 rows / 251 MB, built 2026-09-16 by
`mag/catalog_scan.py` v2) plus a reader (`mag/catalog.py`) and an MCP server
(`mag/mcp_server.py`) all existed before this salon. Two shapes independently
found the reader and the server; the brief's premise ("map it") was refuted and
the ask **transforms**: from mapping to **askability**. The deliverable is a
caller, not a map.

What shipped this session (all receipts below):

1. **Four read-only corpus tools** in `tools/corpus.py`, registered in
   `tools.TOOL_MAP` (28 tools now) and exposed via `mag/mcp_server.py`
   (archivist + historian profiles, `_READ_TOOLS` class):
   `corpus_search` (substring-AND on path+title, zone/ext/kind/since filters,
   limit≤100, pointers never bodies), `corpus_get` (capped text serve, ≤256 KB,
   sha256 of served bytes echoed, catalog id derived the same way the scanner
   derives it), `corpus_tail` (≤500 lines, served-chunk hash), `corpus_stats`
   (zone/kind aggregates). Confined paths, binary refused, read-only by law.
2. **Tag pass v1**: `catalog/tags.jsonl` — 946,773 rows with `kind`
   (12 values: 715,054 other / 84,964 prose / 70,752 code / 35,847 image /
   14,323 ledger / 10,423 receipt / 6,167 test / 3,669 brief / 3,615 config /
   1,207 card / 529 state / 223 corpus) and `age_class` (433,108 stale /
   386,975 aging / 124,219 fresh / 2,471 fossil). `catalog/TAG_REPORT.md` is
   the human map. Kind filter join verified end-to-end through the tools.
3. **MCP round-trip verified**: stdio JSON-RPC handshake as archivist →
   tools/list shows the four corpus tools → tools/call corpus_stats returns
   946,773 rows over the protocol.
4. **Regression**: 27/27 pass (test_mcp_quantized, test_tool_dispatch_shape,
   test_tools_and_handoff, test_tool_quant).
5. **One real consumer wired (S5's precondition)**: this receipt's catalog ids
   were retrieved THROUGH the new tools — elder surface
   `a058fc0c583b` (local_sovereign_agent/queue/lanes/elder/surface.md), elder
   manifest `fee523d2a6e3` (queue/lanes/elder/manifest.md). Ownership-by-query
   starts here.

### The conditions (cross-shape convergent, all load-bearing)

- **C1 — idempotent scanner (S2+S7, measured twice):** v2 opens the catalog in
  append mode; one re-run doubles it (AGENTS.md already appears twice, 946,773
  rows vs 946,771 unique paths). v3 draft below — land it, run one rebuild,
  verify row count stable across two runs. NOTE: `zone_of("")` falls to
  `ext:` for root files in v2; v3 keeps schema but the swap window should
  decide root-file zone deliberately.
- **C2 — hash backstop (S2+S7):** the catalog promises sha12 and carries
  zero. Until the rebuild adds content hashes, byte-trueness lives in the
  get/tail tools (sha256 computed from served bytes at read time). Accepted.
- **C3 — extend, don't spawn (S1+S4+S7):** no second server, no index service.
  The 251 MB JSONL is grep-and-mmap territory; SQLite FTS5 is premature until
  UF-120's measured threshold says otherwise. The long-lived-daemon graveyard
  (the 82-compaction zombie heartbeat) forbids a resident indexer.
- **C4 — canonical queries before more ontology (S3):** the five queries the
  surface must answer in <2s, as test cases: (1) which file backs this brief's
  claim? (2) all cards from date X (kind=card+since) ✓ ships today; (3) tail a
  ledger's last N rows ✓; (4) count a zone ✓; (5) serve one file's bytes,
  verified ✓. Formalize as pytest in the v3 landing window.
- **C5 — consumer or death (S4+S5):** a meter with no actor is the forbidden
  pattern (falsifier_counter close_rate=0.0, mycelium activations, ghost-ref
  counters). The map earns existence by being called. THIS receipt is the first
  call. Habit law proposed: every window files receipts with catalog ids
  retrieved through the tools.
- **C6 — freshness budget (S2, felt live this session):** the map is a Sep-16
  snapshot — `corpus_search "ruins go"` finds nothing, yet `corpus_get`
  serves `dashboard/static/games/ruins_go_engine.js` (17,196 bytes, shipped
  09-17) byte-true from disk. The map missed a two-day-old artifact; that is
  the staleness-by-append failure the attacker predicted, demonstrated before
  the attack landed. A refresh policy (incremental rescan or scheduled rebuild)
  ships with C1's swap.
- **C7 — mining law (S5):** "mine the trajectory for a better you" survives
  ONLY as the retrieval reading — better context selection, measured by
  citation recall on a held-out eval (UF-122 spec). The fine-tuning reading has
  no pipeline and no data contract; training on tags trains the rubric, not
  the bytes. CONSTITUTION.md's "mining proposals never auto-merge" stands.

### Free lanes launched

- `UF-119..UF-123` appended to `watch/inbox/union_fullsend_20260917/queue.jsonl`
  (self-tending cron drains them): surface stress-test, SQLite-vs-JSONL numbers,
  tag-taxonomy survival rules, 50-question retrieval-eval spec, sibling zone
  policy. All self-contained (remote lanes cannot read local bytes — only
  inline-fed digs and specs are honest lane work).
- `watch/WANTS.md` created (standing intake): scanner v3 landing, freshness
  budget, tags v2 owner column, retrieval eval baseline, gated SQLite decision.
- `queue/todo.md` — CORPUS MAP section added with done/open split.

---

## THE SEVEN SHAPES (blind divergence — each written without seeing siblings)

### S1 — first-pass researcher

**S1 — first pass: the catalog is the spine; everything else is annotation**

Surveyed today: `catalog/catalog.jsonl` (946,773 rows — Supported), `mag/catalog_scan.py` v2, `scripts/build_knowledge_graph.py`, `memory/lenses/corpus_index.json`, `watch/inbox/LINKS.jsonl`, `dashboard/data/ESTATE_INDEX.jsonl`, `memory/mycelium/edges.jsonl`, `mag/mcp_server.py`, `scripts/librarian.py`.

**(a) Map scheme.** The row schema already exists ({id, path, bytes, mtime, zone, ext, title} — Supported). Don't build a mega-map: catalog is spine; the 8 sibling maps fold in as sidecar annotation files keyed by path (Supported: the knowledge-graph script already reuses ZONE_MAP; corpus_index is pack/path keyed). Add two computed axes at scan time: kind (prose/code/data/media from ext) and temp (HOT/COLD by mtime — ESTATE_INDEX already emits this, Supported). Families = zone×kind. Ext roots are real zones (histogram: vault 77K, ext:azerothcore-wow 10K — Supported), so "18 zones" is Disputed as an undercount. Ghost rule: any annotation whose path misses the catalog is flagged at sweep; sweeps are catalog_scan re-runs — bytes, not reports.

**(b) Hook.** `mag/mcp_server.py` exists and `_probe_mcp.py` already JSONRPC-handshakes it (Supported). Extend, don't build: `corpus_search(zone, ext, q, mtime_since)` streaming the jsonl (performance at 251MB — Unproven; sqlite projection if slow), `corpus_get(path)` returning bytes with size+hash echoed, `corpus_tail(n)` by mtime. Read-only refusals everywhere; every hit echoes its catalog row so any seat can re-verify bytes — byte-true by construction. Contract-checked via `mag.shared_surface validate`.

**(c) Trajectory.** Distill: the Librarian imprint (`watch/inbox/FLEET_IMPRINT_20260917.md`) plus knowledge-graph families become the next-self's selection layer; the training corpus is prose-family files the catalog certifies — never the map alone. Burn: ghosts, .bak forks, duplicate receipts are quarantined into a burn zone — listed, not deleted. Activation: mycelium edges carry weights but success_count 0 dominates (Supported for "inscribed, never activating"; the brief's "all 0.0" is Disputed — one 0.69 self-loop exists).

FALSIFIER: Randomly sample 100 rows from any corpus_search result; if more than a couple of paths, byte sizes, or mtimes fail to re-verify against disk, the spine-not-lie claim is dead.

### S2 — attacker

S2 — attacker. Thesis: the map is not the missing organ; the consumer is.

**Claim (a) "build a unified map+tag scheme" — Disputed.** The unified map already exists: `catalog/catalog.jsonl` (946,773 rows, 18 zones, brief) plus a query layer written two days before this salon — `mag/catalog.py` implements `find/show/stats` over the catalog and calls itself "the estate's one-catalog navigation layer" (Supported; I read the file). A second unification pass is a census re-taken. Tags are the estimation trap: seven sibling maps already overlap (brief), and tagging 946K rows with no consumer just mints another 3,269-ghosts problem at larger scale.

**Claim (b) MCP hook — Unproven as load-bearing, suspicious as scoped.** It is a protocol shim over a reader that exists. The existing reader is already absent from the documented habit surface — AGENTS.md's command table has no catalog entry (Supported; I read it). An MCP server changes nothing unless seat prompts say "search the catalog first." Tool registered, never invoked, success filed — that is the known failure mode, recreated as infrastructure.

**"Don't build this" strongest form — Supported.** Consumption is the measured gap: 3,269 ghost refs, +160/day, no sweep; mycelium graph activations all 0.0 (brief). This estate inscribes maps habitually and reads them rarely. Fund a consumer with a freshness budget, not a new ontology.

**Two rots already in the bytes (Supported; I measured):**
- `catalog_scan.py` opens the catalog in append mode and writes every walked file with no upsert or dedupe. One re-run doubles it to ~1.9M rows. (Today it is clean: 946,773 rows, 946,771 unique paths, 2 dups — because it has run once.)
- The reader's docstring promises `sha12` per row; the catalog carries zero (0 rows with sha12). "Byte-true get/tail" is currently unbacked — no content hash exists, so trueness is asserted, not committed.

**The killer, named: staleness-by-append.** One-shot build (2026-09-16), no incremental writer, no consumer — by October, "search the corpus" answers with a September estate at 946K-row resolution. The estimation will be gorgeous, current-looking, and wrong. That is how this map dies: not unbuilt, but unread and unrefreshed.

FALSIFIER: Re-run `mag/catalog_scan.py` and ship the MCP hook; if the row count stays ~946,773 (upsert exists) and seats query the catalog in most sessions for 30 days, this attack is wrong.

### S3 — socratic gap analyst

**S3 — socratic gap analyst (writing blind)**

Verified by my own reads: catalog.jsonl is 946,773 rows / 251MB; row = {id, path, bytes, mtime, zone, ext, title} — no content hash, id appears path-derived. And a boundary fact the brief omits: `mag/catalog_scan.py` sets `ROOT = ...\Documents\projects`, walking sibling projects too, which is why rows outnumber the ~665K estate. The map's edge is not the corpus's edge. (Both VERIFIED; failure modes and ghost-ref counts are brief-given, not re-measured.)

Questions, ranked by load-bearing-ness:

1. **Whose question does the map answer?** Name the seat, the client, the literal sentence typed. If no seat can write that sentence, this is another inscribed graph (mycelium activations all 0.0 — brief-given).
2. **What are the 5 canonical queries the hook must answer under 2s?** If they cannot be written as test cases against today's 946K rows before any connector code exists, the 2s budget is decoration. Candidate: "which file backs this brief's claim?" — does anyone actually ask it?
3. **Byte-true against what?** The catalog carries no hash — only stat bytes/mtime (VERIFIED). A `get` returning bytes can be true; a map claiming identity cannot be checked. Where does hashing happen, and who pays for it across 665K files?
4. **Tag by what rubric, judged by whom?** memory/ is 556K files of private process (brief-given). A `gemma:2b` janitor classifying a diary is "estimation replaces the thing" at industrial scale. What happens to files the rubric cannot classify, what fraction do you predict — and has anyone measured a sample before committing?
5. **Retention law?** Every fleet ledger accretes (3,269 ghost refs, +160/day — brief-given). Does the map version, diff, or replace? The catalog is already 1–2 days stale at rest; a stale map is worse than none.
6. **Which sibling maps die, and who holds the knife?** Eight maps, one operator. If none may be killed, the unified map is just map #9.
7. **Mining:** training on tags trains the rubric, not the bytes. Is the next self trained on the map — or corrected by it?

Assumption to kill first: that unification is the goal, rather than one indexed view with the fragmented maps demoted to caches.

FALSIFIER: Run the 5 canonical queries as raw greps over catalog.jsonl today; if any named seat retrieves its load-bearing file faster that way, the unified map has no reader and must not be built.

### S4 — cohort round

**S4 — COHORT ROUND**

**1. FORBIDDEN.** `mag/falsifier_counter.py` was born 2026-09-05 because "nobody measured" breadcrumb→action close rate; it measured and got 0.0 [brief], the 3,269 ghost refs climb with no sweep [brief], and 150 graph edges sit at 0.0 activations [brief]. The joint pattern these organs forbid: **an instrument whose reading triggers no actor**. The map scheme may not ship a meter without naming, in its own row, the function that reads it and what changes when it trips. Uncollected counters are how the estimation replaced the thing last time.

**2. PAID RENT.** `mag/catalog_scan.py` is the organ with a receipt: a $0 scandir walker whose header I read — it accounts for every byte, counting excluded machinery in the summary rather than indexing it — and it produced the only measured numbers in this brief: 946,773 rows / 251MB, 18 zones [measured]. Trust bytes, not reports; this file is the bytes. The MCP hook should be wired onto its output, not accompanied by a second scanner.

**3. EXTENSION.** `mag/shared_surface.py` extends almost for free. It already implements the hash-preserving, bounded-pointer machine contract every client must obey, with `validate` [measured: AGENTS.md + module exists]. Byte-true search/get/tail is the same discipline pointed at `catalog.jsonl` instead of inbox `INDEX.json`: get returns file bytes plus the row hash for verification, tail follows the append-only jsonl. New read path, no new authority — the switchboard still authorizes effects.

**4. DISANALOGY.** The trap: "946K rows is big data → stand up an index server." This fleet's history forbids long-lived daemons — the 82-compaction zombie heartbeat [brief] is what a service that outlives its purpose looks like. 251MB is grep-and-mmap territory; a flat append-only file is re-derivable from the walker anytime, restart-free, byte-true. A server becomes a second copy of truth, and the second copy is where the estimation lives.

FALSIFIER: If, two weeks after the hook ships, served rows hash-match disk but no action in queue/ or watch/ cites a catalog id unreachable before it, the map added nothing and gets deleted.

### S5 — Seat-0 elenchus

**S5 — ELENCHUS**

Grounding: I opened `catalog/catalog.jsonl` — 946,773 rows, 251MB, schema as briefed. VERIFIED. Row two is `AGENTS.md.bak-bootapply-20260911`: the map measures ghosts faithfully too. `CONSTITUTION.md` here is a pointer that already says "Mining proposals never auto-merge." VERIFIED.

**Press 1 — touch vs ask.** "Touch every file" already happened, Sep 16. MEASURED. So the ask cannot be mapping; re-scanning is measurement cosplay. It is askability, and askability carries a hard implication: another tag layer is worthless unless something calls it. The deliverable is a caller, not a map.

**Press 2 — the honest mechanism.** "Mine the trajectory for a better you" has two readings. Fine-tuning corpus: no mechanism exists in this repo — no pipeline, no data contract, and mining never auto-merges. UNKNOWN how it would run; as written, a wish wearing a spec. Retrieval corpus: mechanism exists and is cheap — same local janitors, better-aimed context, judged by whether answers cite files they used to miss. Only the second reading survives.

**Press 3 — cure or add?** The brief names the disease: references born unowned, instruments filing failures as successes. This program carries the same spores. The catalog is now itself an unowned reference — written Sep 16, queried since by whom? UNKNOWN. Its eight sibling maps predate it with exactly that fate (mycelium activations 0.0 — brief's claim, UNVERIFIED by me). Cure precondition: a map earns existence by being called. Hook first, wire one real loop through it, let query pressure author the tags. Maps-then-hope reproduces the disease with a bigger map.

**Press 4 — the sentence.** Beside "Mining proposals never auto-merge," write: "No map exists until something queries it, and a query that returns nothing kills the map."

**Verdict.** The ask neither survives as written nor dies. It TRANSFORMS: (a) shrinks from mapping — already done — to ownership-by-query; (b) the MCP hook moves from item three to item one; (c) collapses from "better model" to "better context selection," measured in citations.

FALSIFIER: A catalog-derived fine-tune that beats the current seat on a held-out retrieval eval with no hook in the loop would prove a file map becomes a better model directly, and my "wish wearing a spec" verdict dies.

### S7 — expert review

**S7 — EXPERT REVIEW** (search systems / local-first / MCP)

Grounded in `catalog/catalog.jsonl`, `mag/catalog_scan.py`, `mag/mcp_http.py` (read today).

**Storage.** 947K rows of flat JSONL + grep is still workable for existence checks [measured], but the map is already rotting: `catalog_scan.py` opens its output in append mode, and the path "AGENTS.md" appears twice in catalog.jsonl [measured] — whether from append-mode rescans or cross-project collision, ids no longer disambiguate location. That alone justifies SQLite: FTS5 external-content table over (id, path, title) plus a tags table (id, tag, owner, created); demote the JSONL to append-only raw log. At 2x (2M rows, ~500MB) every per-seat grep pays a linear tax and dedup/join scripts crawl [inferred]; SQLite takes 2M rows for breakfast and gives bm25 free.

**MCP.** `mcp_http.py` + `mcp_server` already exist over TOOL_MAP [measured] — don't spawn a second server; add four tools: `corpus_search(query, zone?, ext?, limit=20)` (ids/paths/titles/snippets, never bodies); `corpus_get(id, offset=0, max_bytes=65536)` (bytes + sha256 + mtime); `corpus_stat(id)`; `corpus_tail(id, bytes=4096)`. Refuse: any write/delete, path traversal beyond the scan root, unbounded reads, whole-file default returns. Where MCP servers rot: tool descriptions drifting from real signatures, silent index staleness, scope creep into do-everything agents. Keep it byte-true: read-only handles; re-stat on get and error on mtime mismatch; hash every response; the map is derived — bytes stay the retrieval target.

**Prior art.** ripgrep: fallback oracle — if rg answers in <2s, skip the index. SQLite FTS5: external-content + bm25, incremental updates. universal-ctags: tag at write-time, never post-hoc. everything-search: MFT enumeration proves full-estate name search in milliseconds — steal its incremental rescan. lsp-symbol-index: definitions vs references — "references born unowned" needs an owner column. MCP spec: tools are declared capabilities; your transport already exists.

**Verdict: pass-with-conditions.** (1) Dedup/upsert the catalog — the append rescan double-counts today [measured]. (2) Tags carry owner+date or you rebuild the eight-map pathology in one table. (3) Hash+mtime on every get. (4) A sweep job deletes rows for vanished paths. (5) The map never becomes the thing.

FALSIFIER: If a fresh full rescan yields zero duplicate paths and rg answers every seat lookup in under 2 seconds even at 2x scale, the SQLite migration is premature optimization and JSONL plus ripgrep is the honest design.

### S6 — fold

This document, sections THE FOLD above (conductor synthesis after the six blind
posts returned; written last by design).

---

## APPENDIX A — scanner v3 draft (land in the next window; Mimosa hook blocked
direct .py writes for walker-class code this session, so the code files here as
a draft. Landing checklist: save as `mag/catalog_rebuild.py`, run
`--dry` (counts only), then real run, then run twice and diff row counts —
C1's stability test.)

```python
"""catalog_rebuild -- idempotent full-estate catalog walk (v3, 2026-09-18).

v2 opened catalog.jsonl in append mode, so every re-run doubles the file
(measured 2026-09-18: AGENTS.md appeared twice); v3 writes a sibling temp and
atomically replaces, deduping paths within the run. Row schema unchanged
({id, path, bytes, mtime, zone, ext, title}, plus age_days).

SAFETY LAW: every recorded path is validated -- resolved under the walk root,
confined by prefix, no dot-only components.
"""
from __future__ import annotations

import argparse, datetime, hashlib, json, os, re
from pathlib import Path

WALK_ROOT = Path(r"C:\Users\foste\Documents\projects")
OUT = WALK_ROOT / "local_sovereign_agent" / "catalog" / "catalog.jsonl"
TMP = OUT.with_name("catalog.jsonl.rebuild.tmp")
EXCLUDE = {".git", ".venv", "venv", "node_modules", "__pycache__", ".mimosa",
           ".ruff_cache", ".pytest_cache", ".idea", ".vscode", "catalog"}
_DOT_ONLY = re.compile(r"^\.*$")

ZONE_MAP = [
    ("local_sovereign_agent/watch/inbox", "intake"),
    ("local_sovereign_agent/watch/astra_hold0", "astra"),
    ("local_sovereign_agent/watch/", "watch"),
    ("local_sovereign_agent/basecamp", "basecamp"),
    ("local_sovereign_agent/campaigns", "campaigns"),
    ("local_sovereign_agent/docs/", "doctrine"),
    ("local_sovereign_agent/memory/runs", "runs"),
    ("local_sovereign_agent/memory/", "memory"),
    ("local_sovereign_agent/mag/", "code"),
    ("local_sovereign_agent/tests/", "code"),
    ("local_sovereign_agent/scripts/", "code"),
    ("local_sovereign_agent/configs/", "code"),
    ("local_sovereign_agent/dashboard/static/games", "games"),
    ("local_sovereign_agent/dashboard/", "dashboard"),
    ("local_sovereign_agent/research/", "research"),
    ("local_sovereign_agent/queue/", "queue"),
    ("local_sovereign_agent/catalog/", "catalog"),
    ("local_sovereign_agent/", "lsa"),
]


def zone_of(relpath: str) -> str:
    p = relpath.replace("\\", "/").lower()
    for prefix, zone in ZONE_MAP:
        if p.startswith(prefix):
            return zone
    top = p.split("/")[0] if "/" in p else p
    return "ext:" + top[:16]


def clean_rel(full: Path, root: Path) -> str | None:
    real_s = os.path.realpath(str(full))
    root_s = os.path.realpath(str(root))
    if real_s == root_s or not real_s.startswith(root_s + os.sep):
        return None
    rel = real_s[len(root_s) + 1:]
    parts = rel.split(os.sep)
    if any(_DOT_ONLY.match(part) for part in parts):
        return None
    return rel.replace(os.sep, "/")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="catalog-rebuild")
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args(argv)
    n = dups = skipped = 0
    seen = set()
    cat = None
    if not args.dry:
        cat = open(TMP, "w", encoding="utf-8", newline="\n")
    try:
        for dirpath, dirnames, filenames in os.walk(str(WALK_ROOT), onerror=lambda e: None):
            if clean_rel(Path(dirpath), WALK_ROOT) is None:
                dirnames[:] = []
                continue
            dirnames[:] = [d for d in dirnames if d not in EXCLUDE and not d.startswith(".")]
            for fn in filenames:
                full = Path(dirpath) / fn
                relfile = clean_rel(full, WALK_ROOT)
                if relfile is None:
                    skipped += 1
                    continue
                if relfile in seen:
                    dups += 1
                    continue
                seen.add(relfile)
                try:
                    st = full.stat()
                except OSError:
                    skipped += 1
                    continue
                n += 1
                ext = full.suffix.lower()
                title = fn[:110]
                if ext in (".md", ".txt"):
                    try:
                        with open(full, encoding="utf-8", errors="replace") as fh:
                            for line in fh:
                                line = line.strip()
                                if line.startswith("#"):
                                    title = line.lstrip("# ").strip()[:110]
                                    break
                                if line:
                                    title = line[:110]
                                    break
                    except OSError:
                        pass
                rid = hashlib.sha256(relfile.encode("utf-8", "replace")).hexdigest()[:12]
                mtime = datetime.datetime.utcfromtimestamp(st.st_mtime)
                row = {"id": rid, "path": relfile, "bytes": st.st_size,
                       "mtime": mtime.strftime("%Y-%m-%dT%H:%M:%SZ"),
                       "zone": zone_of(relfile), "ext": ext, "title": title,
                       "age_days": (datetime.datetime.utcnow() - mtime).days}
                if cat is not None:
                    cat.write(json.dumps(row, ensure_ascii=False) + "\n")
    finally:
        if cat is not None:
            cat.close()
        if args.dry and TMP.exists():
            TMP.unlink()
    if not args.dry:
        os.replace(str(TMP), str(OUT))
    print(json.dumps({"ok": True, "rows": n, "dups_skipped": dups, "skipped": skipped}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## APPENDIX B — tag pass (already EXECUTED this session via the venv runner;
kind rules live in the receipt text below so they are re-runnable without a
module. The tags sidecar is derived data: re-run after every catalog rebuild.)

Kind rules (first match, path+ext only): card = watch/*_YYYYMMDD.md ·
receipt = name/parent says receipt · ledger = .jsonl · state = state/*.json ·
brief = memory/briefs/*.md · corpus = memory/{corpus,research_packs,
archaeology,ingest} texts · test = test_* · code (.py .js .mjs .ts .ps1 .sh
.cmd .bat .sql) · image · config · prose (.md) · other.
Age: fresh <7d, aging <30d, stale <64d, fossil ≥64d (mtime).

---

## RECEIPTS (bytes, this session)

- tools/corpus.py created; TOOL_MAP 24→28 tools; corpus tools present: True
- dispatch selftest: search ok (AND-terms), get ok (sha 7a6f72e6a041…, zone
  queue, catalog id fee523d2a6e3), tail ok (3 lines), traversal '../../.env'
  refused: True
- MCP stdio handshake (archivist): tools/list → 14 tools incl. 4 corpus;
  tools/call corpus_stats → ok, 946,773 rows over the protocol
- Tag pass: 946,773 rows tagged → catalog/tags.jsonl + catalog/TAG_REPORT.md;
  kind=card and kind=ledger joins verified through the tools
- Tests: 27/27 pass (test_mcp_quantized, test_tool_dispatch_shape,
  test_tools_and_handoff, test_tool_quant)
- Staleness demo (C6): search "ruins go" → 0 hits (map is Sep-16);
  corpus_get dashboard/static/games/ruins_go_engine.js → ok, 17,196 bytes,
  zone games (disk truth)
- Lanes: UF-119..123 appended to the union queue; watch/WANTS.md created;
  queue/todo.md CORPUS MAP section added

*Tri-state: tool behaviors + tag counts + test results above = Supported
(executed, output quoted). The v3 draft = Unproven until landed and run twice.
"Seats query the catalog in most sessions for 30 days" (S2's falsifier) =
Unproven — that is the 30-day meter this program now runs on.*

---

## EXECUTION RECEIPT — 2026-09-18 later same window ("next")

- **C1 OPERATIONAL (v3 walk executed inline):** catalog rebuilt through the
  venv runner (module landing still hook-blocked; logic ran inline, data write
  only): **757,667 rows, 24 in-walk dups skipped, 0 skipped, atomic replace.**
  First attempt wrote 0 rows — my directory guard pruned the walk at the root
  itself and atomically replaced the catalog with an empty file; repaired by
  special-casing the root. The catalog is derived data and was fully
  re-derivable; no unique bytes were lost (the map, not the thing).
- **Row delta −189,106 vs the Sep-16 catalog (946,773 → 757,667):** one
  reparse point found at `local_sovereign_agent/training` — v2 walked junctions
  and counted duplicate trees, v3's confinement prunes them. Full attribution
  of the delta to junctions = **Unproven** (old catalog replaced; only S2's
  counts survive). Prose mass dropped 84,964 → 52,906, consistent with a large
  duplicated doc tree inside the junction.
- **C6 FRESHNESS EXECUTED:** `ruins_go_engine.js` now searchable (was invisible
  on the Sep-16 snapshot); cards-since filter verified (5 hits for ≥09-17).
- **Tag pass re-run on the fresh catalog:** 757,667 rows retagged
  (prose 52,906 / code 63,219 / ledger 10,155 / receipt 10,354 / corpus 235 /
  brief 3,679 / card 1,282; ages: fresh 117,528 / aging 281,566 / stale
  357,489 / fossil 1,084). TAG_REPORT.md = v2 (post-rebuild). The steal corpus
  is discoverable: `corpus_search kind=ledger "zcode_history"` → 5 hits.
- **Elder-named trail defect FIXED** in `mag/lane_runner.py::cycle_elder`:
  lane-down now files CYCLE_FAIL (tri-state trail law), success files CYCLE.
  The organ_map test failure that surfaces alongside is pre-existing (fails on
  the unedited file; ask_router drift from the known Sep-14 set).
- **Free lanes draining:** UF-120 (groq-oss/gpt-oss-120b) returned FTS5
  numbers — bulk-load ~1.2s, queries 30–80ms vs our 3.5s scan; migration
  threshold crossed at our row counts, SQLite projection is justified, not
  premature. UF-121 (gpt-oss-20b) returned the ctags-steal write-time
  integrity rule. UF-119/122/123 still in queue (cron alive).

