# OUROBOROS R4 MEMORY/BOOT SURFACE - accuracy lens (2026-10-05)

Instrument-and-moment grammar throughout. Everything below was read or run this sitting
(2026-10-05, ~23:0x-23:4x Z window) unless tagged carried. No em-dashes.

## What landed tonight (verified in bytes, credit where due)

- The e03-rib-vault lane (run 2026-10-05-exec) landed the r06 pack:
  mag/rib_boot.py:79-99 mounts the vault (live census, 5 law ribs as law-head bytes),
  the "51 frozen ribs" constant is retired (mag/rib_boot.py:16-20), and the three
  POST-DATUM rib amendments exist on disk: RIB_INFERENCE_BUDGET_20261001.md:119
  ("THE LAW IS NOW: omission is a MEASURED ON state"), RIB_MODEL_GATES_20261001.md:108-126
  (mechanism + scoped exception), RIB_FREE_USAGE_POLICY_20260823.md:47-58 (D3 resolved
  by the 13-lane re-probe, verdict appended). Register row 3 (width law as code) also
  landed: 21 max_concurrency hits in tools/workflow_gate.py, tier-2 verified in
  corpus/steal/MASTER_EXECUTE_REGISTER.md:71-73.
- The quantizer staleness gate landed: mag/context_pack.py:413-415 renders a one-line
  debt pointer instead of silently serving old law.
- knowledge_graph v2 rebuild landed (memory/knowledge_graph.json ts 2026-10-05T07:15:34Z,
  schema knowledge_graph.v2); my independent read-only census reproduces the heal claims
  exactly: 2,919 nodes / 1,143 edges / 1,204 orphans / 29 dangling edges, all 29 dangling
  of rel already_inside (was 834 dangling pre-heal per the ask; my numbers confirm the
  residual, CONVERGENT with the ask's own figures).

## RANKED MEMORY-AMENDMENT TABLE

| # | Organ | Exact edit | What a fresh seat gets wrong today | Evidence row |
|---|-------|-----------|-----------------------------------|--------------|
| 1 | mag/rib_boot.py:76,93-96 (LAW_HEAD_CHARS=1200) | Mount each law rib as head 1200 PLUS every POST-DATUM/AMENDMENT section (5 ribs total 28,615 B; mounting full bytes is cheaper than the bug) | The seat boots PRE-amendment law: thinking-off mandate without the omission-is-ON mechanism, free-usage "never force" without the 10-05 instrument verdict. The mount cured "vault invisible" and re-created "amendment invisible" in the same sitting | Measured this sitting: POST-DATUM at normalized-char offsets 5905/7707 (MODEL_GATES), 6397/8465 (INFERENCE_BUDGET), 2836/4038 (FREE_USAGE); all > 1200, so law_head cuts them |
| 2 | tools/zknot.py (logon recap) | (a) add the day-4-mine no-silent-truncation gate at tools/zknot.py:273 (`real[:3]` still silently drops); (b) wire a real logon trigger (AGENTS.md claims "rewritten at logon" but rg over scripts/ githooks/ mag.cmd found zero zknot wiring); (c) print LATEST age in the header so staleness is loud | The boot recap a seat reads FIRST ends 2026-10-03 19:35 ET: it silently omits the 10-04 night shift, R1-R4, the rib amendments, and the mesh bank, while presenting as "last 3 real ZCode sessions"; the meter line (129/1000) is a closed window | memory/zknot/LATEST.md:5 (Written 10-03 19:36 ET); memory/runs/zknot/runs.jsonl last row ts 2026-10-03T23:36:53Z status "stopped" (stop file since removed, no run since); rg "zknot" scripts/ githooks/ mag.cmd = zero hits |
| 3 | memory/warm_state.json + mag/rib_boot.py:137-144 | rib_boot should regenerate warm state (or read memory/biography/verkle_tip.json live) and stamp an age-debt line when the file is >24h old | rib_boot.json (regenerated tonight 23:32:47Z) carries chain index 11203 / root 41f3b807 while the live tip is 11355: the boot surface asserts a tip 152 leaves stale as the chain-is-truth anchor | warm_state.json:3-9 (generated 2026-10-03T22:55:40Z, index 11203) vs verkle_tip.json (n_leaves 11355, updated 2026-10-05T23:06:17Z); rib_boot.py reads WARM without regenerating |
| 4 | quantizer packs (memory/corpus/quantized_thought/) | Recompile now (content-stale) AND register a scheduler (CURRENT.md:90 already files "quantized packs expire 2026-10-06T15:18Z with no scheduler") | The ONLY law layer most seats see (context_pack L0b Compiled laws) is compiled 2026-09-29T15:18:39Z v0.4, 12 flash rows, ZERO rows naming the d4 thinking law or the width law (rg "thinking" and "max_concurrency|width" = 0 matches); after 10-06T15:18Z the debt pointer hides ALL law, so seats boot law-less | compile_report.json (compiled 2026-09-29T15:18:39Z, v 0.4); instructions_flash.jsonl = 12 rows; PACK_STALE_DAYS=7 (mag/constants.py, imported at mag/context_pack.py:14) |
| 5 | memory/rib_boot.json consumers | Make something READ it: context_pack should mount the vault law block, or AGENTS.md's load-order table should name `python -m mag.rib_boot --json` | The vault mount is write-only: rg across the tree finds no code consumer (only prose/catalog/dashboard-static references), and the AGENTS.md load order (8 steps) never names rib_boot. The cure exists as bytes nothing loads | rg -ln "rib_boot" (this sitting): corpus/steal/MASTER_READ_ESTATE.md, corpus/steal/MASTER_EXECUTE_REGISTER.md, catalog rows, dashboard static; zero imports/calls in mag/ tools/ scripts/ |
| 6 | mag/rib_boot.py:160-163 (brief block) | Apply the same FROZEN divert mag/lanes.py:227-235 already has: if the body starts "# FROZEN", serve state/CURRENT.md | rib_boot.json's brief.head serves the 2026-09-26 frozen fossil (2101 chars) while lanes.py correctly diverts every pack render to live truth; two organs read "the brief" and disagree | memory/briefs/latest.md first 60 chars = "# FROZEN as-of 2026-09-26"; mag/lanes.py:231-234 diverts; rib_boot.py:160-163 does not; rib_boot.json brief_chars=2101 |
| 7 | mag/knowledge_graph.py edges | Add a knot edge builder (all 400 knot nodes are structurally edgeless: no rel touches kind=knot) and resolve-or-drop the 29 we_have names whose module:{name} targets do not exist | Orphans remain 1204 of 2919 nodes: knots unreachable by graph fan-out (BM25 still sees them), 447 modules with no docstring-law lines, 140 steal + 217 doctrine folds with no edges; 29 already_inside edges dangle on phantom module ids | Read-only census this sitting over memory/knowledge_graph.json: orphans 1204 (kinds: module 447, knot 400, steal 140, doctrine 217), dangling 29 all already_inside (31 total, 29 dangling) |

## BOOT-ORDER VERDICT

The current order (AGENTS.md -> FRAMEWORK -> compass -> zknot LATEST -> state/CURRENT.md ->
context-pack) is right in SHAPE and wrong in WIRING. Keep recap-first (zknot before compass),
but: (1) insert the rib vault mount AFTER the recap and BEFORE the pack, because the pack's
compiled-laws layer is the stale one (table row 4) and the vault is where tonight's amendments
actually live; (2) the recap and the warm state are regenerated by nothing (rows 2-3), so the
order reads fresh-looking stale bytes; (3) state/CURRENT.md is the live truth the brief divert
already targets (lanes.py:231-234) and deserves its load-order slot explicitly (it has one in
prose, not in the 8-step table). One sitting would wire a single logon verb (extend mag.cmd
context-pack to run zknot + rib_boot + warm boot and fail loud on age) and the order becomes
self-refreshing instead of self-trusting.

## Dead organ (no sacred cows)

mag/thought_bank_app.py: 116 lines, last commit 60b1bde7f 2026-09-14, file mtime 2026-09-04,
zero live consumers (rg finds only configs/violation_baseline.json, a dist_audit snapshot,
and temp listings; no import in mag/ or tools/, no wiring in context_pack or the quantizer).
It serves nothing on the boot path; retire or fold into the quantizer lane. I did NOT read
its body, so what it would serve if wired is unverified (blind spot below).

## Where memory dies unregenerated (the ask's fourth question)

Three measured deaths: (1) zknot LATEST (no trigger since 10-03 23:36Z); (2) warm_state
(2 days, 152 leaves behind, nothing regenerates it at seat start despite AGENTS.md prose);
(3) the quantizer packs (compile 09-29, bar expires 10-06T15:18Z, no scheduler). Fourth,
half-verified: fold outcome stamps. The amenti-diff SYNTHESIS.md:25 censused that NO fold
carries a held/falsified outcome stamp estate-wide (grep over watch/salon_receipts/ +
memory/runs/salons/: 2 prose survivors; memory/corpus/LINKS.jsonl carries exactly 2
SUPERSEDED rows total), so superseded conclusions never die visibly. I could NOT locate
the ask's "register row 11" text in any register I searched (MASTER_READ_ESTATE curiosity
register = 10 rows; MASTER_EXECUTE_REGISTER next register = 10 rows; r2-gaps/amenti grep):
the row itself is OWED-unlocated; the demand it names is NOT landed per the amenti census.

## Convergence flags

- The graph residuals (1204 orphans / 29 dangling already_inside) match the ask's own
  claimed numbers; independently re-derived this sitting: CONVERGENT.
- The amenti-diff fold-stamp finding and the day-4 mine's no-silent-truncation demand
  converge on the same defect class: continuity artifacts that decay without a gate.

## Blind spots (honest)

- docs/ref/MCP_EPISTEMIC_MESH_AUDIT.md was read only via grep lines (the nine-memory
  mapping header at :53); its full mapping and owed rows are unverified here.
- The ask's "register row 11" source was not found (searched r2-gaps, amenti-diff,
  both Master registers); reported as unlocated, not as nonexistent (QUANTIFIER LAW:
  absence claim scoped to those four locations).
- mag/thought_bank_app.py body unread; the day-3 mine card naming its 09-30 lapse was
  not located; only git log/mtime/consumer census back the dead-organ claim.
- I did not execute `python -m mag.rib_boot` myself (memory/rib_boot.json was
  regenerated by a sibling lane at 23:32:47Z mid-sitting; running it would race);
  its content claims are read from the file bytes, which is the same artifact a seat
  would ingest.
- No pytest run (not asked); the GPS ledger (tools/gps_mcp/gps_ledger.db3) was listed
  but not queried; the operator's 03:00 synthesis is taken as cited by the ask.
- zknot's SQLite source (~/.zcode/cli/db/db.sqlite) was not queried directly; the
  10-03 cutoff rests on LATEST.md bytes + runs.jsonl, not on a session-db census.

---

# ADDENDUM: second accuracy sitting (2026-10-05 ~23:43-23:55Z, independent re-derivation)

Re-asked cold with the same topic; read the organ bytes myself before seeing the table above.
Duplication is emphasis: every row below that re-derives a row above is flagged CONVERGENT and
outranks single-source claims. This pass ran the checks the first pass named as not-run.

## Checks the first pass could not run, now run

- `python -m mag.rib_boot --json` EXECUTED live (ts 2026-10-05T23:43:57Z): read_only true,
  publish_called false, rib_count 26, vault_md_count 52, vault_law_ribs_mounted 5/5,
  chain.index 11203 read from warm_state. CONVERGENT with rows 1/3/5 above and extends them:
  the mount works today on the current tree, not just at the sibling's 23:32:47Z regeneration.
- Bus-mount probe the first pass did not do: `python -m mag.rib_bus mount --domain doctrine`
  parsed to 26 ribs; substring probe over the full JSON: thinking False, omission False,
  "measured on" False, width False, max_concurrency False. So neither boot rib surface (bus
  invariants, vault law heads) carries the d4 thinking law, the width law, or the 10-05
  free-usage verdict. The mounted MODEL_GATES law_head ends mid-sentence in GLM pricing text
  ("catalog ~$0.02-0.04/as"), nowhere near the POST-DATUM block at :108. Extends table row 1.
- Live chain measured: `wc -l memory/biography/verkle_chain.jsonl` = 11356 rows (first pass
  read verkle_tip.json n_leaves 11355 minutes earlier; moment delta, consistent). CONVERGENT
  with row 3: warm_state index 11203 is 153 rows behind my count, file exactly 998 B.
- Live pack-offload evidence: tail -1 watch/inbox/PACK_OFFLOAD.jsonl = a full-mode pack
  hard-clipped (stage 4, total_chars 7350 vs max 7200) at 2026-10-05T23:45:14Z, minutes before
  this writing: the shed ladder fires today and IS instrumented at pack level; the field-level
  clips (brief/directives/todo, mag/context_pack.py:685-689) remain uninstrumented.
- The frozen-brief divert independently derived: mag/lanes.py:228-236 serves state/CURRENT.md
  when latest.md starts "# FROZEN" (banner byte-verified in memory/briefs/latest.md head);
  mag/rib_boot.py:160-163 reads latest.md with no such divert. CONVERGENT with table row 6.
- Register row 11: one more location ruled out. memory/percolator/candidates.jsonl = 30 rows;
  row 11 (1-based) is the quantization degradation ladder (ts 2026-10-02T04:17:43Z, Reddit
  qwen source), not a fold-history proposal. CONVERGENT with the first pass: row 11 as the ask
  states it stays OWED-unlocated (now scoped across five locations).
- docs/ref/MCP_EPISTEMIC_MESH_AUDIT.md read IN FULL (first pass had grep only): the audit's
  byte claims spot-check true (mag/seed_seal.py exists, backing the decaying-manifest port
  note at :43-44) and one internal staleness found: :79 says "ouroboros R3 ... RUNNING RIGHT
  NOW" while commit 6f6b1a2d6 already ticked R3 complete. The audit's three structural
  findings (closed loop, identical-cognition confound, mirror-scorer circularity) and the
  no-demotion-path gap are the sharpest memory-law prose banked tonight; the nine-memory
  mapping's engine names verify in the seed repo per the audit's own note (:57-59), not here.
- LINKS registers: `grep -c SUPERSEDED` = 2 at memory/corpus/LINKS.jsonl (the path
  amenti-diff SYNTHESIS.md:25 names, count verified) and 0 at watch/inbox/LINKS.jsonl; both
  exist (320033 B Oct 3 vs 313650 B Oct 5) and have diverged; canonicality unmined.

## Second-sitting ranked deltas (rows that change the fold)

1. CONVERGENT, escalated: the pre-amendment boot surface is now proven on BOTH rib surfaces by
   live execution (vault heads cut every POST-DATUM block; bus carries none of the three laws).
   Move unchanged: mount amendment sections beside heads (table row 1); one sitting.
2. CONVERGENT: vault mount write-only (row 5) re-proven with a zero-hit rg across AGENTS.md,
   FRAMEWORK_LOAD, compass, mag.cmd, scripts/, githooks/ (exit 1). The AGENTS.md load-order
   table edit is the cheapest single sitting on the board.
3. CONVERGENT, quantified: zknot recap stale since 10-03T23:36Z (last ok run) with the stop
   file now ABSENT and zero runs since; silent truncations re-cited at tools/zknot.py:171,184,
   188,192,273; no recall/get; no exit-2 truncation gate (its probe remains not-run: nothing
   to test). Rows-vs-view split: OWED.
4. NEW: quantizer packs carry ZERO of tonight's three laws even while fresh (12 flash rows,
   compiled 2026-09-29T15:18:39Z; the d4 law is 6 days younger than the pack) and the whole
   layer goes dark after 2026-10-06T15:18Z with no recompile scheduler found in-repo
   (state/CURRENT.md Owed already names the expiry). CONVERGENT with row 4; the "law hidden
   until fresh" gate makes the expiry loud, the recompile is still owed.
5. CONVERGENT: graph heal numbers reproduced exactly on my own census (2919/1143/1204/29, all
   29 dangling already_inside with prose targets minted at mag/knowledge_graph.py:237-239);
   757 of 1204 orphans (knot 400 + doctrine 217 + steal 140) are orphans BY CONSTRUCTION
   (edges builder at :223-243 touches only module/landscape/maps_to), and fold() at :574-584
   returns already_present on id collision, so a superseded conclusion is unrepresentable.
   The amenti T5b prospective outcome-stamp law remains unlanded.

Boot-order verdict stands as written above (right shape, wrong wiring); this pass adds the
single-verb proposal's enforcement detail: the logon verb must fail loud on age (zknot age,
warm_state age, pack age) rather than render fresh-looking stale bytes, and must carry the
amendment tails so the mount serves post-datum law on day one.

## Second-sitting blind spots

- Same out-of-tree hole: ZCode-side boot lane and scheduled tasks live outside the repo; all
  "unwired" claims scope to in-repo instruments (scripts/, githooks/, configs/, queue/lanes/,
  mag.cmd), greps listed above.
- thought_bank_app.py body still unread (I only re-ran git log: last commit 60b1bde7f
  2026-09-14); its data-store mtime unlocated, so the 09-30 lapse stays ask-carried.
- The 26 bus invariants were substring-probed, not read in full; a differently-worded bus
  invariant carrying the d4 or width law would evade the probe.
- No pytest, no workflow_gate scenario suite, no session-db query, no live URL fetch this
  sitting; every absence claim above names its grep or read (quantifier law).
- LATEST.md prompt/todo contents read, not re-derived against ~/.zcode/cli/db/db.sqlite.

---

# ERRATUM (third sitting, 2026-10-06 ~00:2x Z, after the hostile second pass)

Two number-claims banked above are STRUCK as byte-false at bank time; the structural
findings survive on bytes re-verified this sitting. This erratum corrects BOTH the
first-sitting table (rows 2-3) and the second-sitting addendum (its delta row 3).

STRUCK:
- "zknot: no run since 2026-10-03T23:36:53Z / recap ends 10-03" (first sitting, table
  row 2; repeated in the addendum's delta row 3 as "zero runs since"). FALSE when
  banked: memory/runs/zknot/runs.jsonl carries a 2026-10-05T23:38:34Z status ok row
  (18 qualifying, 14 cards written), and memory/zknot/LATEST.md:5 reads "_Written
  2026-10-05 19:38 ET"; the fresh recap covers the R3 landing commit (0bd7357f0,
  LATEST.md:52), its receipts (LATEST.md:76-81), and the R4 LIVE todo row
  (LATEST.md:129). Both earlier sittings read a pre-write runs.jsonl tail mid-flight
  (the tail command this sitting returns both rows); the recap staleness half of the
  finding is WITHDRAWN.
- "chain 152 (first sitting) / 153 (addendum) leaves behind; warm_state 2026-10-03"
  (table row 3). TRUE only at those moments, dead on re-read: warm_state.json
  regenerated 2026-10-05T23:58:18Z (index 11355, still 998 B); rib_boot.json
  regenerated 2026-10-06T00:11:19Z and AGAIN 00:22:22Z (index 11355 both); verkle_tip
  n_leaves 11358 at my re-read: 3 leaves behind. The leaf-lag is a moving number that
  measures the DESIGN (rib_boot.py:136-144 reads whatever warm_state last held, never
  regenerates), not a finding; the number claims are struck.

SURVIVING (re-verified this sitting, commands and moments):
- zknot regeneration is BY HAND, NOT BY LAW: the 23:38:34Z run's receipt row carries
  no actor field (attribution OWED); no in-repo trigger exists (rg over mag/ tools/
  scripts/ githooks/ configs/ mag.cmd: only AGENTS.md:5 prose plus a card-counting
  facts reader at tools/compile_seats.py:171-183); no host scheduled task
  (schtasks /Query /FO CSV piped through rg -i "zknot|rib_boot|quantizer|hermes|
  context.pack|ouroboros" = zero matches). Tonight's freshness was one manual run,
  so the 2-day staleness class recurs the next time nobody runs it.
- tools/zknot.py:273 still `real[:3]` (rg this sitting); no truncation gate, no
  recall/get in the def census; the day-4 mine's exit-2 gate and rows-vs-view split
  remain OWED (its line-21 cite re-read byte-exact).
- memory/rib_boot.json still has no code reader: rg over mag/ tools/ scripts/
  githooks/ configs/ mag.cmd returns only tools/ouroboros.py (whose rib_boot_mount()
  at :169-175 runs `mag.rib_bus mount --domain doctrine` ALONE, never mag.rib_boot,
  never the json), tools/rib_fork.py (prose), and mag/rib_boot.py itself.
- The 2026-10-06T00:22:22Z rib_boot.json brief_head still serves "# FROZEN as-of
  2026-09-26" verbatim while mag/lanes.py:227-235 diverts the same file to
  state/CURRENT.md for pack renders; the AGENTS.md 8-step load table still has no
  rib_boot row.

Unchanged by this erratum: table rows 1, 4, 5's structure, 6, 7; the boot-order
verdict; the dead-organ call; the convergence flags.

## Fourth-sitting confirmation (2026-10-06 ~01:30Z, the lens whose F3/F4 were verdicted weakened)

Non-duplicative bytes only; the third sitting's strikes and survivals are adopted as written.

- Stale-tip mechanism reproduced BY THIS LENS's own hands: `python -m mag.rib_boot --json` at
  2026-10-06T01:30:35Z emitted chain.index 11355 / generated 2026-10-05T23:58:18Z while the
  live chain measured 11361 rows (`wc -l memory/biography/verkle_chain.jsonl`, this sitting)
  and memory/biography/verkle_tip.json read n_leaves 11361, updated_minute 2026-10-06T01:15:15Z.
  Lag at my moment: 5-6 leaves, and the boot surface asserted the stale tip as chain-is-truth
  during the check. Lag is time-since-last-manual-run, unbounded above (2 days this week).
- The hermes_warm_boot reference triage completed at my scope (rg over mag/ tools/ scripts/
  configs/ docs/ githooks/ queue/ AGENTS.md mag.cmd main.py): tools/ouroboros.py:14 is
  docstring prose listing organs, tools/ask_bank_seed.py:166 and
  configs/ask_bank/v1/manifest.json:32 are provenance/exclusion path lists - zero call sites
  anywhere; schtasks grep for zknot/warm zero (exit 1). Manual-only stands.
- View-cap wording fix banked precisely: the four caps are LABELED, not silent -
  tools/zknot.py:180-181 ("earlier prompts omitted"), :185-186, :189-190, :193-194 ("+N more"
  variants). The ungated defect is exactly :273 (`real[:3]`, 18 qualifying -> 3, header
  declares "last 3", no gate); rg "def (recall|get)|exit\(|sys.exit" tools/zknot.py = zero
  hits, so the exit-2 gate and rows-vs-view split remain OWED.
- The 23:38:34Z zknot row's full field set re-read: ts/tool/status/qualifying/written/
  skipped_up_to_date/templates/meter - no actor field; attribution OWED confirmed.
