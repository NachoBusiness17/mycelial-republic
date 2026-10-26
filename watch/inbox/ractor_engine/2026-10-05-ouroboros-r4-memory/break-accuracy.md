# OUROBOROS R4 MEMORY/BOOT SURFACE: break-accuracy (the hostile second pass)

Banked 2026-10-06T00:2xZ (~20:2x ET 2026-10-05). Everything below was read or run by this pass
this sitting unless tagged carried. No em-dashes. Citation grammar: path:line for code, exact
command plus output for checks. Warning stamped up front: the tree moved twice during the lens's
own run and three more times before this pass finished reading; every moment below is pinned to
bytes plus mtime, and any verdict that ignores the moment is wrong by construction (the estate's
own census denominator law, AGENTS.md).

## 1. THE RACE THE LENS LOST (pinned by mtimes, all read this sitting)

| Moment (ET / Z) | Event | Bytes |
|---|---|---|
| ~19:32 ET / 23:32Z | lens sitting-1 reads artifacts | rib_boot.json ts 2026-10-05T23:32:47Z, chain index 11203 (carried in its report) |
| 19:38:34-51 ET / 23:38:34-51Z | ZKNOT REGENERATES | runs.jsonl row `{"ts": "2026-10-05T23:38:34+00:00", "tool": "zknot", "status": "ok", "qualifying": 18, "written": [14 files], "skipped_up_to_date": 4}`; LATEST.md and runs.jsonl mtimes both 19:38:51 ET |
| 19:43-19:55 ET / 23:43-23:55Z | lens sitting-2 window (per its own header; it executed `python -m mag.rib_boot --json` at 23:43:57Z, still warm index 11203) | addendum claims "zknot recap stale since 10-03T23:36Z ... zero runs since" |
| 19:52:07 ET / 23:52:07Z | accuracy.md BANKED with the stale-recap claim | accuracy.md mtime 19:52:07.328 ET |
| 19:58:18 ET / 23:58:18Z | hermes warm boot regenerates warm state | warm_state.json generated 2026-10-05T23:58:18Z, index 11355, 998 B |
| 20:11:19 ET / 00:11:19Z | rib_boot regenerates its json | rib_boot.json ts 2026-10-06T00:11:19Z, index 11355, vault 5/5 mounted |
| 20:12-20:2x ET / 00:12-00:2xZ | THIS PASS reads | verkle_tip.json n_leaves 11358, updated 00:12:12Z |

Kill shot: the zknot regeneration hit disk 13 minutes 56 seconds before the lens banked
accuracy.md (19:38:51 ET write vs 19:52:07 ET bank). Sitting-2's own window began four minutes
after the fresh receipt landed, so the banked "zero runs since 10-03" was byte-false when
written. The lens's own named falsifier (a runs.jsonl row newer than 2026-10-03T23:36:53Z) fired
and was never re-censused at bank time. That is the census-carrier disease applied to the lens's
own evidence chain, by the lens whose whole topic was that disease.

Aftermath shape (addition A2): three of the four regens the lens demanded as wiring were
hand-fired by siblings tonight (zknot 23:38:34Z, warm boot 23:58:18Z, rib_boot 00:11:19Z). The
cures landed as one-off manual regens, which proves the demand while proving the wiring absent.

## 2. VERDICTS ON THE FIVE FINDINGS

### Finding 1 (1200-char law heads cut every amendment): CONFIRMED

Reproduced exactly by this pass's own instrument (repo venv python, same normalization as
mag/rib_boot.py:94, `" ".join(t.split())`):

```
RIB_MODEL_GATES_20261001.md      normchars_total=7707 POST_DATUM_at_normchar=5905 raw_line=108
RIB_INFERENCE_BUDGET_20261001.md normchars_total=8465 POST_DATUM_at_normchar=6397 raw_line=119
RIB_FREE_USAGE_POLICY_20260823.md normchars_total=4038 POST_DATUM_at_normchar=2836 raw_line=47
head_has_POST_DATUM=False head_has_MEASURED_ON=False (all 5 ribs)
```

Every number the lens reported (5905/7707, 6397/8465, 2836/4038) matches to the digit; every line
cite is byte-exact (MODEL_GATES:108 "## POST-DATUM AMENDMENT 2026-10-04 to the DEEPSEEK-V4.1-FLASH
row"; INFERENCE_BUDGET:119 "## POST-DATUM AMENDMENT 2026-10-04"; FREE_USAGE:47 "## POST-DATUM
VERDICT 2026-10-05"). The falsifier was tested and held: no law_head[:1200] contains POST-DATUM,
"MEASURED ON", or the R062_FREE_USAGE_RESOLVE marker. The spine survives the current rib_boot.json
(ts 00:11:19Z): the mounted MODEL_GATES head still ends mid-sentence at "catalog ~$0.02-0.04/as",
deep in GLM pricing text, nowhere near the amendment at :108.

One number corrected downward in trust: the lens's "all 5 ribs total 28,615 B" is wrong by
exactly 100. Current truth: 28,715 B by the json bytes fields (4195 + 7801 + 8608 + 4113 + 3998,
python sum this sitting) and 28,776 B by stat (the 61 B gap on FREE_USAGE alone is 61 CRLF pairs;
read_text collapses CRLF). The full-mount-is-cheaper-than-the-bug argument is unaffected.

### Finding 2 (zknot recap two days stale, no regeneration mechanism): WEAKENED

The staleness half is dead, killed by the lens's own falsifier before it banked (see section 1):
the current runs.jsonl tail row is 2026-10-05T23:38:34Z status ok, and the current LATEST.md
reads "_Written 2026-10-05 19:38 ET by tools/zknot.py_" at line 5, covering the fd5ec147 session
through 2026-10-05 19:35 ET, listing the R3 landing commits (6f6b1a2d6, 0bd7357f0 at 10-05 19:29),
and carrying the pending todo row "[in_progress|high] OUROBOROS R4 LIVE (dwfrun-45927560)". The
claim that the recap "silently omits the 10-04 night shift, R1-R4" is false at current bytes: the
covered session windows span 10-04 and 10-05, R3 is in the commit lists, R4 is named LIVE.

What survives, byte-verified by this pass, and it is most of the structural finding:
- tools/zknot.py:273 still `last3 = [cards[s["id"]] for s in real[:3] ...]` with no gate; 18
  qualifying sessions existed at the regen moment and the recap carries 3, silently. The day-4
  mine demand (no-silent-truncation gate, exit 2 on dropped rows) is still OWED, and the mine
  cite is byte-exact ("agent-memory-and-continuity via x.md":21 names zknot.py:273 verbatim).
- No recall()/get() functions exist (def census this sitting: redact, et, fmt_dur, first_line,
  load, template_prefixes, is_template, git_commits, inbox_files, pending, card, meter, receipt,
  main). Rows-vs-view split: still OWED.
- No wired trigger exists at two scopes: full-tree rg (only AGENTS.md:5 prose claiming "rewritten
  at logon by tools/zknot.py", a facts reader in tools/compile_seats.py:171-183, and a note in
  configs/fossil_registry.json; zero invocations in scripts/, githooks/, mag.cmd, configs/) and a
  host schtasks census (`schtasks /Query /FO CSV /NH` piped through rg -i
  "zknot|rib_boot|quantizer|quantized|hermes|context_pack|context-pack|ouroboros" = zero matches).
  A ZCode-side hook or out-of-tree alias would evade both scopes: stated, not excluded.
- Attribution of tonight's 23:38:34Z run: OWED. The receipt carries no actor field, and this pass
  will not invent one.

### Finding 3 (rib_boot.json is a write-only stale snapshot): WEAKENED

The staleness numbers are dead; the structure stands. warm_state.json regenerated at
2026-10-05T23:58:18Z (index 11355, 998 B) and rib_boot.json at 00:11:19Z (index 11355), so at this
pass's read moment the chain block is 3 leaves behind the tip (verkle_tip 11358), not 152. The
"152 leaves behind" and "warm 10-03" claims were true at sitting-1's moment (~23:32Z) and died
mid-run; the addendum re-proved 11203 at 23:43:57Z from a warm state that had not yet been
re-fired. Correct behavior for a hostile pass: report the numbers with their moments, not as
constants.

The surviving byte-truth, all re-verified on the CURRENT json (ts 00:11:19Z):
- No code consumes the artifact. ouroboros.py names rib_boot at :14/:56 but rib_boot_mount() at
  :169-175 runs only `mag.rib_bus mount --domain doctrine` (26 invariants; 16,438 chars probed
  this sitting) and never touches memory/rib_boot.json or the vault; rib_fork.py's mentions are
  prose (:5, :17). The rest of the rg hits are catalogs, receipts, dashboard static, and a
  knowledge-graph node about rib_boot. Zero imports or reads of the json in mag/ tools/ scripts/.
- The brief block serves the fossil: the current json's brief.head begins verbatim "# FROZEN
  as-of 2026-09-26 (Mag P0-1 warm-face) **Status:** FROZEN" while mag/lanes.py:227-235 diverts
  the same file to state/CURRENT.md for every pack render. Two organs read the brief and
  disagree, exactly as the lens said. (Soften by one nuance: the FROZEN banner itself names the
  truth surfaces, so a seat gets a pointer, not just a fossil body.)
- mag/rib_boot.py:136-144 reads WARM without regenerating; AGENTS.md's 8-step load-order table
  has no rib_boot row (rg over AGENTS.md: row 8 is context-pack at :51; the only zknot mention is
  the :5 prose claim). Confirmed at current bytes.

### Finding 4 (quantizer flash pack content-stale, expiry tomorrow, no scheduler): CONFIRMED, with two scope corrections

Load-bearing numbers all re-verified this sitting: instructions_flash.jsonl = 12 rows (wc -l);
`rg -c -i "thinking|max_concurrency|width"` over the file exits 1 (zero matches); compile_report
compiled 2026-09-29T15:18:39Z v0.4; PACK_STALE_DAYS = 7 at mag/constants.py:19 (imported at
context_pack.py:14); the debt pointer at mag/context_pack.py:413-415 ("law hidden until fresh").
The expiry arithmetic holds: the bar crosses 2026-10-06T15:18Z, tomorrow afternoon.

The CURRENT.md owed line EXISTS: state/CURRENT.md:89-90 carries "quantized packs expire
2026-10-06T15:18Z with no scheduler". This pass's first grep missed it because the sentence wraps
across a line break ("quantized\npacks expire"); the second grep ("quantiz") found it. Lesson
taken by this pass about wrapped-line grep patterns; the lens's cite stands.

Scope correction 1: "hides ALL compiled law" overstates. The seam is flash-tier only by
construction (context_pack.py:377-389 docstring: "Flash tier only (<=220-char imperatives ...)");
what goes dark at expiry is the 12-row flash band, not all compiled law everywhere (the local
band, 338 rows, never rode the boot pack at all; its only other consumer is
tools/concept_span_check.py:62-63). The finding's spine (the only compiled-law seam in the boot
pack carries zero of tonight's three laws and expires tomorrow) is unaffected.

Scope correction 2: "no scheduler" needs the patrol nuance. A daily detection patrol exists:
scripts/census_patrol_daily.ps1:160-176 invokes tools/fossil_check.py against
configs/fossil_registry.json:6-12, whose note says the pack bar is 24h, independent of compile
mtime (the comment block at :160-162 even recalls the packs going 9 days fossil with zero
alarms, which is why the patrol is registry-driven now). So the debt will be LOUD, not silent;
what nothing schedules is the auto-RECOMPILE. In-tree plus schtasks scopes both verified zero.
The deeper defect is content, not date: a bare recompile only helps if the 10-03/10-04/10-05 laws
actually land in the new pack; the compile input is the percolator invariant stream, so the move
must assert the three laws' presence, not just freshness (the lens's min-rows assertion move is
right; this pass would make it min-rows-with-pattern).

### Finding 5 (knowledge-graph residual is structural): CONFIRMED, cite corrected

Re-censused by this pass's own read-only venv-python instrument at moment 2026-10-06T00:14:57Z
(the graph's own ts; the file was rebuilt mid-sitting, moving tree): nodes 2921, edges 1144
(+2/+1 since the lens's census, no claim affected), orphans 1204 (module 447, knot 400, doctrine
217, steal 140: exact), dangling 29 of 1144, all rel already_inside: exact; already_inside total
31: exact; knot nodes 400, all 400 orphaned: exact.

Causal cite corrected: the absence lives in _edges() at mag/knowledge_graph.py:223-243, which
branches only on kind==module (has_invariant, :226-235), kind==landscape (already_inside,
:236-239), and any node carrying maps_to (case_law, :240-242). No branch emits from a knot, steal,
doctrine, or invariant node; they can only be TO-targets, and nothing targets them. The lens's
":104-122 knots carry no edge builder" points at the collector (_nodes_verkle), not the builder;
the claim is right, the address is one function off. This pass also confirms fold() at :574-584
returns already_present on id collision, so a superseded conclusion is unrepresentable in the
graph today (convergent with the audit's no-demotion-path gap, AUDIT.md:22-24). The dangling 29
are the landscape we_have fan minting module:{name} targets that do not exist as module nodes:
the resolve-or-drop move stands. Pre-heal baselines (1506 orphans, 834 dangling) are ask-carried;
this pass did not re-run the b1 receipt.

## 3. WHAT THE LENS MISSED (additions, each with falsifier and move)

### A1. The convergence rib contradicts tonight's banked law, and the lens never mentions it

This is the ask's own question ("which rib contradicts tonight's banked laws?") left unanswered by
the accuracy lens, which never greps the vault for convergence at all. RIB_MOSAIC_SEED_20260921.md:37
carries, verbatim: "The mosaic doctrine GENERALIZES its convergence clause: convergence receipts are
not rare validations, they are the expected behavior of coworkers at different fidelity (Papailiopoulos
was one; the prophecy cluster is the standing field)." Tonight's commit 1693dd2ad retracted the
convergence data point as evidence under authorship overlap (the Sybil form: one hand shipping both
sides of the dialogue). The rib carries no amendment marker (rg "POST-DATUM|1693dd" over the file =
zero matches), and it is not one of the 5 mounted law ribs (mag/rib_boot.py:69-75 names DRIVING_LADDER,
MODEL_GATES, INFERENCE_BUDGET, FREE_USAGE, DESCENT), so the contradicted law sits in the vault as
unmarked truth, findable by any seat that greps for "convergence" and trusted on read.
- Falsifier: a POST-DATUM amendment block on the MOSAIC rib, or a machine-readable superseded stamp
  on it anywhere a boot reads. Neither exists at this moment (greps above, plus LINKS census below).
- Move: one sitting, two edits on the amend-never-rewrite model: (1) append the Sybil-form exception
  to RIB_MOSAIC_SEED_20260921.md as a POST-DATUM block; (2) mint the superseded-conclusions list
  (A3) so the retraction is boot-readable, not commit-message-only.
- CONVERGENT: logic.md:22 in this same folder independently found the same rib and quote; a second
  run's independent derivation. Duplication is emphasis: this row outranks any novel single-source
  row this pass could add.

### A2. The regen race plus the hand-crank cascade: the wiring gap is now proven by its own cure

Three regens landed tonight after the lens read their targets stale (zknot 23:38:34Z, warm boot
23:58:18Z, rib_boot 00:11:19Z; section 1 table). None has a trigger in-tree or in schtasks
(section 2, finding 2 and finding 4 scopes). So the estate's current continuity mechanism for all
three organs is "a sibling remembered to re-run it", which is precisely the class of memory that
dies on the first quiet night. The lens demanded a single logon verb; tonight's bytes are the
falsifier experiment for its absence: every cure was a one-off.
- Falsifier: a wired logon verb or scheduled task firing any of the three (both censuses zero; a
  ZCode-side hook outside the tree would need to be shown).
- Move: one sitting (~30 min): extend mag.cmd context-pack to fire zknot + warm boot + rib_boot as
  one idempotent chain, stamp ages in each header, and fail loud (exit 2) on age or on any
  truncation, per the day-4 mine's gate demand.

### A3. "Register row 11" is located, not unlocated: the superseded-conclusions list exists as lane raw material nothing boots

The lens banked "OWED-unlocated" after searching four registers plus the percolator. But the
mickey17_v2 row-address grammar makes row 11 a LANE: r11-fold-history (row grammar "r04#1 is the
second row of lane r04", corpus/steal/MASTER_READ_ESTATE.md:7). The lane files exist at
memory/runs/mickey17_v2/runs/2026-10-04-0/lanes/r11-fold-history.json and .checks.json, and each
carries 5 "SUPERSEDED" mentions (grep -c, this pass). Meanwhile the only registers a boot could
read carry 2 SUPERSEDED rows total (memory/corpus/LINKS.jsonl) and 0 (watch/inbox/LINKS.jsonl).
So the demand is located, its raw material is counted, and the minting is the owed edit. Five
sibling lenses in this folder (logic, economics, dogfood, moonshot-1, moonshot-2) converged on
this interpretation; the accuracy lens was the outlier and stayed outlier.
- Falsifier: an existing boot-readable superseded-conclusions file (rg
  "superseded-conclusions" over AGENTS.md, FRAMEWORK_LOAD, compass, context-pack inputs: zero).
- Move: one sitting: mint memory/fold_history/SUPERSEDED.md from the r11 lane rows plus the
  1693dd2ad retraction as row 1, and wire a pointer into zknot LATEST and rib_boot so a fresh seat
  can ask "what did the estate used to believe and why did it stop".

### A4. The ouroboros driver's own docstring over-claims its boot surface

tools/ouroboros.py:14 claims the fresh-seat boot surface includes "mag.rib_boot + mag.rib_bus
mount (doctrine domain)" but rib_boot_mount() at :169-175 runs only mag.rib_bus. The driver of the
self-enhancement loop mounts 26 doctrine invariants, zero vault law, zero amendment tails. Its
substrate probe this pass: bus mount = 16,438 chars; "thinking"=0, "omission"=0, "measured on"=0,
"max_concurrency"=0, "width law"=0 (convergent with the lens sitting-2's own probe). So the
instrument running the trust-the-bytes rounds reads bytes that do not contain this week's laws.
- Falsifier: a second rib_boot invocation elsewhere in ouroboros.py (rg: hits only at :14/:56/:169/:313).
- Move: one line plus one test: make rib_boot_mount() execute the module (or its mount_vault())
  and assert the amendment markers appear in what the driver mounts; ~20 min.

### A5. The banked mesh canon maps the nine memories onto SEED engines, and names zero of this estate's continuity organs

rg -i "zknot|warm_state|rib_boot|quantized_thought|memory/rib" over docs/ref/MCP_EPISTEMIC_MESH_SPEC.md
= zero matches (17,533 B, mtime 14:17 ET today). The audit's nine-memory mapping
(docs/ref/MCP_EPISTEMIC_MESH_AUDIT.md:51-59) maps onto seed engines (spine_walk, librarian_catalog,
estate_atlas, estate_smith_chart, cooker, task_wall, phone_relay, MANIFEST.sha256, ledger) and says
explicitly: "these engine names live in the seed repo, not this repo - the mapping is for the
pushable package, and its claims verify there, not here". So the ask's premise that the mapping
"names the estate organs" is not byte-true in the banked canon; the estate-side mapping from the
nine memories onto the organs that actually boot a seat tonight (zknot, warm_state, rib_boot,
quantizer packs, the rib vault, the knowledge graph, the LINKS registers) exists nowhere in bytes.
The audit also banked the no-demotion-path gap (:22-24: "a one-way promotion ladder accumulates
once-true-now-false sediment") which this pass verified converges with the MOSAIC rib (A1), the
LINKS census (A3), and fold()'s already_present return (finding 5): four instruments, one defect,
no decay function landed anywhere.
- Falsifier: any file mapping the nine memories onto this repo's continuity organs.
- Move: one sitting: write the estate-side mapping table (nine memories onto the eleven real
  organs, each with its freshness instrument and its demotion path or the explicit lack of one)
  into the audit's companion, so the mesh build inherits the boot surface instead of inventing a
  second memory stack.

## 4. CORRECTED RANKED MEMORY-AMENDMENT TABLE (the fold's table, re-ranked after the breaks)

| # | Organ | Exact edit | What a fresh seat gets wrong today | Evidence row (this pass) |
|---|-------|-----------|-----------------------------------|--------------------------|
| 1 | mag/rib_boot.py:76,93-96 | Mount head 1200 PLUS every POST-DATUM/AMENDMENT section (5 ribs = 28,715 B json-bytes / 28,776 B stat, not 28,615 B) | Boots PRE-amendment law: thinking-off mandate without the omission-is-ON mechanism or its scoped exception, free-usage law without the 10-05 instrument verdict | offsets reproduced exactly (5905/7707, 6397/8465, 2836/4038); falsifier tested and held |
| 2 | RIB_MOSAIC_SEED_20260921.md:37 | Append the Sybil-form exception as POST-DATUM; mint SUPERSEDED list (A3) and wire its pointer into the recap surfaces | Trusts convergence receipts as expected behavior with no independence gate: the exact claim 1693dd2ad retracted tonight; superseded memory dies nowhere a boot reads | rib bytes verbatim; rg POST-DATUM/1693dd on the rib = 0; CONVERGENT with logic.md:22 |
| 3 | tools/zknot.py:273 plus trigger wiring | Gate the [:3] (exit 2 on dropped rows), wire the logon trigger AGENTS.md:5 already claims, wire recall/get over the session store | The recap is fresh tonight but by sibling hand-crank, not mechanism; 18 qualifying sessions silently become 3; next quiet night it rots again and the prose claim is the only thing that says otherwise | runs.jsonl 23:38:34Z row; def census shows no recall/get; rg plus schtasks both zero triggers |
| 4 | rib_boot.json consumers (mag/context_pack.py and/or AGENTS.md load order) | Mount the vault law block inside the pack, or give rib_boot a table row; add the lanes.py FROZEN divert at rib_boot.py:160-163; point chain at verkle_tip.json | The cure is write-only: no code reads the json; the brief block serves the 2026-09-26 FROZEN head verbatim; the chain block can assert any tip a sibling last fired (11203, then 11355, next quiet night: anything) | ouroboros.py:169-175 bus-only; current json brief.head FROZEN verbatim; lanes.py:227-235 diverts |
| 5 | quantizer packs (memory/corpus/quantized_thought/) | Recompile WITH a pattern assertion (the three laws must appear), then register the auto-recompile beside MagFtsIndexDaily; scope the claim to the flash band | The boot pack's only compiled-law seam carries zero of tonight's laws (12 rows, 0 pattern hits) and the seam goes dark behind the debt pointer 2026-10-06T15:18Z; detection is daily and loud (patrol at 24h bar), recompile is nothing | wc -l 12; rg exit 1 both patterns; constants.py:19; CURRENT.md:89-90; census_patrol_daily.ps1:160-176 |
| 6 | mag/knowledge_graph.py:223-243 | Add a knot (plus steal/doctrine) edge builder; resolve-or-drop the 29 phantom we_have targets | 1204 of 2921 nodes are unreachable by graph fan-out: all 400 knots, all 140 steals, all 217 doctrine folds; 29 already_inside edges dangle on phantom module ids; superseded conclusions are unrepresentable (fold() already_present) | census at 00:14:57Z reproduces every residual number exactly |
| 7 | mag/thought_bank_app.py | Retire it or wire it: the dead-organ verdict stands | Nothing (it serves nothing): 4257 B, mtime 2026-09-04, last commit 60b1bde7f 2026-09-14, importers = one violation-baseline token | stat, git log, importer census this sitting; body still unread by anyone this run |

## 5. BOOT-ORDER VERDICT (this pass, against the lens's)

The lens's verdict (right shape, wrong wiring; insert the vault mount after the recap and before
the pack; a single logon verb; fail loud on age) is directionally confirmed by this pass with two
corrections from tonight's bytes:

1. The order's live failure tonight was amendment-blindness, not staleness. zknot regenerated,
   warm state regenerated, rib_boot regenerated, and STILL no law surface a seat mounts carries
   any of the three laws: bus probe 0/5 patterns, vault heads cut all three POST-DATUM blocks,
   flash pack 0/2 patterns. Re-firing the regens harder fixes nothing about that; carrying the
   amendment tails does. Rank the wiring fix below the content fix accordingly (table rows 1-2
   over rows 3-4).
2. The single logon verb must absorb tonight's hand-crank cascade (zknot, warm boot, rib_boot as
   one idempotent chain with age assertions), else the estate keeps the manual path that worked
   tonight and will not work on a quiet night.

The recap-first placement (zknot before compass) stands: AGENTS.md:5's "Boot recap first" prose is
the right shape and its "rewritten at logon" clause is the wrong wiring; either wire the clause or
delete it, because a prose claim that nothing executes is the exact class of rot this round was
fired to find. state/CURRENT.md deserves its explicit table slot (the FROZEN divert at
lanes.py:232-234 already names it as truth; the table still routes through a fossil's pointer).
And the ouroboros driver itself should join the boot order's enforcement surface (A4): the round
that audits the mount should not be able to lie-by-docstring about its own mount.

## 6. CONVERGENT FLAGS

- Offset run (5905/7707, 6397/8465, 2836/4038) and KG residual census (1204/29/31, 400/400):
  independently reproduced by this pass, matching the lens and the ask's own figures.
- MOSAIC rib contradiction: found by logic.md:22, re-derived here from rib bytes plus commit
  1693dd2ad. Two runs, one finding, CONVERGENT, and outranking any novel single-source row.
- r11 lane interpretation: five sibling lenses in this folder versus the accuracy lens's
  "unlocated". The lane files exist and count 5 SUPERSEDED mentions each.
- No-demotion-path gap: AUDIT.md:22-24 converges with the LINKS census (2/0), fold()'s
  already_present, and the MOSAIC rib: four instruments, one defect.
- Bus probe: this pass's 0/5 pattern re-run converges with the lens sitting-2's probe.
- The AUDIT's internal staleness (":79 says ouroboros R3 RUNNING RIGHT NOW while 6f6b1a2d6 already
  ticked complete"): found by the lens's addendum, confirmed in this pass's full read (RULINGS item
  2 at AUDIT.md:79-81).

## 7. NOT-RUN / OWED (blind spots, scoped)

- Attribution of tonight's three regens (zknot 23:38:34Z, warm 23:58:18Z, rib_boot 00:11:19Z):
  OWED. Receipts carry no actor field. This pass will not guess a lane identity.
- zknot's source store (~/.zcode/cli/db/db.sqlite) was not queried; the 18-qualifying and
  14-written counts ride the runs.jsonl receipt, not an independent session census.
- KG pre-heal baselines (1506 orphans / 834 dangling) are ask-carried; the b1 receipt was not
  re-run. Current residual is fully re-censused.
- The day-3 mine card naming thought_bank's 09-30 lapse was not located (same as the lens);
  the dead-organ verdict rests on mtime, last commit, and importer census, not the card.
- Absence claims scopes: "no wired trigger" for zknot and the quantizer recompile covers full-tree
  rg plus a host schtasks census at ~00:2xZ; a ZCode-side hook, an out-of-tree alias, or a task
  created after the census would evade both. "No code reads rib_boot.json" covers rg over
  mag/, tools/, scripts/, configs/, githooks/, mag.cmd at this moment.
- No pytest, no workflow-gate suite, no GPS-ledger query, no session-db query, no live URL fetch
  this sitting; none were asked of this pass.
- mag/thought_bank_app.py body still unread (both passes): the retire-or-wire verdict is on the
  consumer census; what it would serve if wired remains unverified.
- This pass did not re-run the full 52-rib vault census per rib; the 5 law ribs plus the 26 bus
  invariants are the surfaces probed. vault_md_count 52 is rib_boot.json's own census at 00:11:19Z
  (the ask's "53" and the docstring's "52 or 53 depending on instrument and moment" both stand).

*Folded by the break-accuracy seat. Pass the two sharpest rows upward with the race: the amendment
tails are still cut from every surface a seat mounts, and the convergence law the estate retracted
tonight is still minted as standing doctrine in the vault.*

---

# HOSTILE SECOND PASS, SECOND SITTING (2026-10-06 01:0x-01:2xZ, after the erratum)

A fresh break-accuracy seat re-ran the whole byte-check cold after the lens's erratum above.
Everything below was read or run THIS sitting; nothing is inherited without re-derivation.
Instruments: repo venv python (.venv/Scripts/python.exe), rg 15.2.0, Git Bash on win32.
Moving-tree pins: rib_boot.json was observed regenerated at 23:32:47Z, 00:11:19Z, 00:55:15Z and
~01:07Z (mtimes pinned each read); memory/knowledge_graph.json rebuilt at ts 01:01:17Z; the
chain grew 11,356 -> 11,359 rows between reads. Quantifier law applied to THIS PASS too: my
first zknot wiring census piped through `head -30` and truncated; re-run untruncated (97 files
mention zknot repo-wide; code readers = tools/zknot.py + tools/compile_seats.py only). My own
`python -m mag.rib_boot --json` run at 01:18:32Z rewrote memory/rib_boot.json (the module
writes OUT unconditionally, mag/rib_boot.py:181); that regen is MINE, pinned.

## VERDICTS ON THE FIVE HANDOFF FINDINGS

### F1 pre-amendment law on both rib surfaces: CONFIRMED

Every number byte-exact on my own instruments. Offsets (normalization replicated from
mag/rib_boot.py:94, `" ".join(t.split())`): MODEL_GATES POST-DATUM at normchar 5905 of 7707
(raw line 108), INFERENCE_BUDGET 6397 of 8465 (raw line 119), FREE_USAGE 2836 of 4038 (raw
line 47); DRIVING_LADDER and DESCENT carry no POST-DATUM at all. LAW_HEAD_CHARS=1200 at
mag/rib_boot.py:76, slice at :94. Amendment text read at the cited lines: MODEL_GATES:108-126
("## POST-DATUM AMENDMENT 2026-10-04 to the DEEPSEEK-V4.1-FLASH row", omission-is-MEASURED-ON
mechanism + scoped exception), INFERENCE_BUDGET:119-141 ("THE LAW IS NOW: omission is a
MEASURED ON state" at :129), FREE_USAGE:47-61 (10-05 instrument verdict, 13 lanes / 52 asks).
Bus probe re-run: `python -m mag.rib_bus mount --domain doctrine` = 26 ribs, 16,384 chars,
thinking/omission/"measured on"/width/max_concurrency ALL False. Live module run at
01:18:32Z: rib_count 26, vault_md_count 52, vault_law_ribs_mounted 5/5, and the mounted
MODEL_GATES head still ends mid-sentence at "catalog ~$0.02-0.04/as" with POST-DATUM in NO
head. The falsifier was tested in counterfactual form (I never edit files): max normchars_total
across the five ribs is 8465 < 8700, so a raised cap WOULD carry every amendment block; the
shipped 1200 does not. One trust correction, same as the prior pass: lens byte-total 28,615 B
is wrong; stat sum is 28,776 B (json bytes fields sum 28,715 B, CRLF collapse explains the 61 B
delta on FREE_USAGE). CONVERGENT: now re-derived by three runs (lens sitting-2, prior break
pass, this pass).

### F2 the vault mount is write-only: CONFIRMED

The lens's exact scope re-run zero (rg -n "rib_boot" over AGENTS.md, docs/FRAMEWORK_LOAD.md,
docs/ref/MAG_MYCELIAL_REPUBLIC_COMPASS.md, mag.cmd = exit 1; scripts/ + githooks/ = exit 1).
Full-tree untruncated re-census: hits only in catalogs/dashboard static/receipts/run reports,
mag/rib_boot.py itself, memory/rib_boot.json, memory/knowledge_graph.json, tools/rib_fork.py
(prose), and tools/ouroboros.py, whose rib_boot_mount() at tools/ouroboros.py:169-175 runs
ONLY `mag.rib_bus mount --domain doctrine` (:170) and never mag.rib_boot nor the json. The
AGENTS.md load-order table has 8 rows (row 8 = `mag.cmd context-pack` at AGENTS.md:51) and no
rib_boot row; the only zknot mention is the :5 prose claim. No boot doc, hook, or logon verb
invokes the cure. Falsifier (a consumer anywhere) not found at either scope this sitting.

### F3 the boot recap is stale and unregenerated: WEAKENED

The staleness half is dead at current bytes and stays dead on re-read: memory/zknot/LATEST.md:5
reads "_Written 2026-10-05 19:38 ET by tools/zknot.py_", and memory/runs/zknot/runs.jsonl's
tail row is 2026-10-05T23:38:34Z status ok (qualifying 18, written 14, skipped_up_to_date 4,
meter refreshed to 133/7d). The lens's own named falsifier (a runs.jsonl row after 10-04 with
written cards) fired and was never re-censused before banking. What survives, byte-verified
this sitting: (1) regeneration is by hand, not law: untruncated rg + a host schtasks census
(`schtasks /Query /FO CSV /NH` piped through rg -i "zknot|rib_boot|quantizer|quantized|hermes|
context.pack|ouroboros|warm.boot" = zero matches) find no trigger; the only code that touches
zknot besides the tool itself is tools/compile_seats.py:171-183 zknot_facts(), a card-counting
facts reader for SEATS.md (ZKNOT constant at :43); AGENTS.md:5's "rewritten at logon" prose is
executed by nothing. (2) tools/zknot.py:273 is byte-exact (`real[:3]`), 18 qualifying sessions
became 3 in the recap with no gate; the def census shows no recall/get and rg shows zero
sys.exit/exit() calls, so the day-4 mine's exit-2 no-silent-truncation gate and rows-vs-view
split remain OWED. (3) Nuance the lens lost: the four view caps at zknot.py:171 ([-30:]),
:184 ([:15]), :188 ([:15]), :192 ([:15]) each emit an explicit "+N ... omitted/more" line
(:181, :186, :190, :194), so "silent truncations" overstates those four; the ungated :273 cut
and the missing exit-2 gate are the real defect. (4) state/zknot.off is ABSENT while the
10-03T23:36:53Z row names it as the stop file: the stop story changed with no receipt.
(5) Attribution of the 23:38:34Z run: OWED (no actor field in the receipt).

### F4 the boot chain tip serves 153-stale knots: WEAKENED

The number is moment-dead, exactly as the erratum ruled: warm_state.json (998 B) now carries
generated 2026-10-05T23:58:18Z, chain.index 11355, n_leaves 11356; the live chain measured
11,359 rows (wc -l) with verkle_tip.json n_leaves 11359 (updated_minute 2026-10-06T00:48:13Z).
At my moments the lag is 3-4 leaves, not 152/153. But the DESIGN finding is live and I caught
it in the act: my own `python -m mag.rib_boot --json` run at 01:18:32Z read WARM
(mag/rib_boot.py:136-144) and emitted chain index 11355 while the chain was at 11,359, i.e.
the boot surface asserted a 4-leaf-stale tip as the chain-is-truth anchor DURING the check.
Nothing regenerates warm_state by law: full-tree rg for hermes_warm_boot shows only prose/
catalog/test hits (no scripts/, no githooks/, no scheduled-task registration), the host
schtasks census is zero, and AGENTS.md:7 carries it as manual prose. The verdict: the
staleness NUMBER was never a constant (census denominator law); the stale-serving MECHANISM
is confirmed and reproduced live.

### F5 the knowledge-graph residual is structural: CONFIRMED (cite corrected)

My read-only census at graph ts 2026-10-06T01:01:17Z: 2,921 nodes / 1,144 edges / orphans
1,204 (module 447, knot 400, steal 140, doctrine 217) / dangling 29 all rel already_inside /
already_inside total 31 / all 400 knot nodes orphaned. Stable across three sittings' rebuilds
(2919/1143 -> 2921/1144 -> same residuals). The causal cite the lens gave (:104-122) points at
the collector; the absence lives in the builder _edges() at mag/knowledge_graph.py:223-243,
which branches only on kind=="module" (has_invariant, :226-235), kind=="landscape"
(already_inside via we_have[:4] minting `module:{Path(m).name}` targets, :236-239), and
n.get("maps_to") (:240-242): no branch ever emits FROM a knot, steal, doctrine, or invariant
node. fold() at :574-584 returns already_present on id collision (:578-579) AND appends the
new node with zero edges, so superseded conclusions are unrepresentable and any fold is
orphan-by-construction. Pre-heal baselines (1506 / 834) stay ask-carried; not re-run here.

## ADDITIONS (what both lens sittings and, where noted, the prior pass missed)

### A1. RIB_MOSAIC_SEED_20260921.md contradicts tonight's retracted convergence law, unmarked, booting nowhere: CONFIRMED (CONVERGENT)

The rib carries verbatim (lines 36-38): "The mosaic doctrine GENERALIZES its convergence
clause: convergence receipts are not rare validations, they are the expected behavior of
coworkers at different fidelity (Papailiopoulos was one; the prophecy cluster is the standing
field)." rg "POST-DATUM|1693dd" over the file = exit 1 (no amendment marker). Commit
1693dd2ad (Oct 5 15:15:08 -0400) retracts the convergence data point and amends the
CONVERGENCE LAW (the Sybil form), and `git show --stat` proves it touched ONLY
watch/inbox/LINKS.jsonl (1 file, 1 insertion): the retraction exists in a commit message plus
a LINKS row no boot reads (watch/inbox/LINKS.jsonl = 0 SUPERSEDED rows, grep this sitting).
The rib is not in VAULT_RIBS (mag/rib_boot.py:69-75) and not in the 26-invariant bus, so the
contradicted law is also INVISIBLE at boot; a seat that greps the vault for "convergence"
trusts it on read. This answers the ask's "which rib contradicts tonight's banked laws" for
the convergence amendment. CONVERGENT with logic.md:22 and prior-pass A1; third derivation.
- Falsifier: a POST-DATUM block on the MOSAIC rib or a machine-readable superseded stamp any
  boot reads. Neither exists this sitting.
- Move: append the Sybil-form exception as POST-DATUM on the rib; mint the superseded list
  (A3) and wire its pointer into zknot LATEST + rib_boot. ~30 min.

### A2. The hand-crank cascade, fourth regen observed: CONFIRMED (CONVERGENT, moments updated)

Tonight's regens were all hand-fired: zknot 23:38:34Z, warm boot 23:58:18Z, rib_boot.json
observed at 23:32:47Z, 00:11:19Z, 00:55:15Z, ~01:07Z (four regens pinned by mtime), plus MY
own 01:18:32Z. None has an in-tree trigger (untruncated rg: zero in mag/, tools/ minus the
facts reader, scripts/, githooks/, configs/, mag.cmd, queue/) or a host scheduled task
(schtasks census zero). So the regenerator is OUT-OF-TREE (a sibling session loop or
ZCode-side hook: the lens's own named blind spot, now evidenced by churn with no owner). The
wiring gap is proven by its own cure: the cures land as one-offs, and the first quiet night
they stop.
- Falsifier: an in-tree or schtasks trigger firing any of the three, or an actor field on any
  receipt. Neither exists this sitting; attribution of all four regens OWED.
- Move: one idempotent logon verb (extend `mag.cmd context-pack`) firing zknot + warm boot +
  rib_boot, stamping ages in each header, exit 2 on age or dropped rows, creationflags carried
  per A7. ~30 min.

### A3. "Register row 11" is LOCATED: the lane grammar reads it as r11-fold-history: CONFIRMED (CONVERGENT)

corpus/steal/MASTER_READ_ESTATE.md:7 defines the grammar ("Row addresses: `lane#N` indexes
the lane file's `rows` array, 0-based. `r04#1` is the second row of
`r04-estate-index-anatomy.json`."), which makes row 11 a LANE. The lane files exist:
memory/runs/mickey17_v2/runs/2026-10-04-0/lanes/r11-fold-history.json (9,335 B, Oct 4 18:59)
and .checks.json (7,104 B, Oct 4 19:08), 5 SUPERSEDED mentions each (grep -c this sitting).
The register the lens DID search, memory/percolator/candidates.jsonl, has 30 rows and its
1-based row 11 is the quantization-degradation ladder (ts 2026-10-02T04:17:43Z, Reddit qwen
source), not a fold-history proposal: byte-read this sitting, matching the lens sitting-2's
ruling. The only boot-readable superseded lists carry 2 rows (memory/corpus/LINKS.jsonl) and
0 rows (watch/inbox/LINKS.jsonl). So the demand is located, its raw material counted, the
minting owed. CONVERGENT with five sibling lenses plus prior-pass A3; the accuracy lens was
the outlier and its "OWED-unlocated" was a search-scope failure, not an estate fact.
- Falsifier: an existing boot-readable superseded-conclusions file. rg
  "superseded-conclusions" over AGENTS.md/FRAMEWORK_LOAD/compass/context-pack inputs = zero.
- Move: mint memory/fold_history/SUPERSEDED.md from the r11 lane rows + 1693dd2ad as row 1;
  wire pointers into zknot LATEST and rib_boot. ~45 min.

### A4. The ouroboros driver's docstring over-claims its boot surface, and ALSO names a nonexistent directory: CONFIRMED, second error added

tools/ouroboros.py:14 claims the fresh-seat boot surface includes "mag.rib_boot + mag.rib_bus
mount (doctrine domain)" while rib_boot_mount() (:169-175) runs only the bus; :313 calls it;
rg shows rib_boot mentions only at :14/:56/:169/:313. NEW second error this pass: :12 says
`memory/ribs/*.md (rib bus domain registry)` and `ls memory/ribs` = No such file or
directory; the real dirs are memory/rib/ (52 .md vault) and memory/rib_bus/ (domain JSONs,
mag/rib_bus.py:48 RIB_DIR). The instrument running the trust-the-bytes rounds misdescribes
its own mount twice in eight lines.
- Falsifier: a second rib_boot invocation in ouroboros.py (none), or memory/ribs/ existing
  (it does not).
- Move: make rib_boot_mount() execute the module (or mount_vault()) and assert the amendment
  markers appear in what the driver mounts; fix the :12 path. ~20 min.

### A5. The banked mesh canon maps nine memories onto SEED engines and zero estate organs: CONFIRMED (CONVERGENT)

rg -in "zknot|warm_state|rib_boot|quantized_thought|memory/rib|knowledge_graph" over
docs/ref/MCP_EPISTEMIC_MESH_SPEC.md (17,533 B) = exit 1, zero matches. The mapping lives in
docs/ref/MCP_EPISTEMIC_MESH_AUDIT.md:51-59 onto seed engines with the disclaimer "these engine
names live in the seed repo, not this repo ... its claims verify there, not here". AUDIT:22-24
banks the no-demotion-path gap ("a one-way promotion ladder accumulates once-true-now-false
sediment"); AUDIT:78-79 still says ouroboros R3 "RUNNING RIGHT NOW" after 6f6b1a2d6 ticked it
complete. The estate-side mapping (nine memories onto zknot, warm_state, rib_boot, quantizer
packs, rib vault, knowledge graph, LINKS registers) exists nowhere in bytes: four instruments
(one-way promotion: MOSAIC rib, fold() already_present, LINKS 2/0, AUDIT's own gap), zero
decay functions landed.
- Falsifier: any file mapping the nine memories onto this repo's continuity organs.
- Move: write the estate-side mapping table (each organ: freshness instrument + demotion path
  or explicit lack) into the audit's companion. ~45 min.

### A6. The behavior-cards rib boots nowhere while claiming to be warmed at boot: NEW (both lens sittings silent; the ask named the organ)

memory/rib/RIB_BEHAVIOR_CARDS_20260928.md says, verbatim: "This rib is the card deck; the seat
warms it at boot." No boot surface does: it is not in VAULT_RIBS (mag/rib_boot.py:69-75), not
in the AGENTS.md load-order table (:44-51), not consumed by mag/context_pack.py, and rg
"BEHAVIOR_CARDS" over mag/ tools/ docs/ configs/ scripts/ queue/ AGENTS.md = only
tools/behavior_cards_x.py (the miner that extends the deck, feeding
RIB_BEHAVIOR_CARDS_X_20261004.jsonl, schema behavior_card.v1, 52 .md census excludes it: the
vault also holds the .jsonl deck). This is the THIRD prose-boot-claim with no executor, after
AGENTS.md:5 ("rewritten at logon") and AGENTS.md:7 ("run python -m mag.hermes_warm_boot at
session start"). The operator's warmed-invocation surface ("the seat recognizes the SHAPE and
runs the warmed lane without re-teaching") is vault bytes nothing mounts.
- Falsifier: a boot-surface consumer of RIB_BEHAVIOR_CARDS (rg zero this sitting, scopes
  listed above; a ZCode-side hook would evade).
- Move: add the deck to mount_vault()'s law mounts (or a cards block in context_pack), and
  correct the rib's boot claim to name the real consumer. ~25 min.

### A7. mag/rib_boot.py spawns a subprocess without CREATE_NO_WINDOW: NEW

mag/rib_boot.py:121-122 calls subprocess.run(...) with no creationflags on win32, violating
this run's stated law ("any subprocess spawn on win32 carries creationflags CREATE_NO_WINDOW")
and the estate convention carried by at least eight modules (rg -c "CREATE_NO_WINDOW":
mag/afk_loop.py, mag/amd_window_guard.py, mag/autonomous_research.py, mag/batch_drain.py,
tools/citation_lint_io.py, tools/code_execution.py, tools/cold_boot_test.py,
tools/derived_dag.py, among others). The freshly-landed boot organ is the outlier; a GUI-
invoked seat booting via this module pops a console window per mount.
- Falsifier: creationflags present in rib_boot.py (grep -c = 0 this sitting), or a ruling that
  the law scopes to workflow scripts only (none banked).
- Move: one line at :121 (creationflags=CREATE_NO_WINDOW on win32) + a convention grep in the
  pre-push ratchet. ~10 min.

## BOOT-ORDER VERDICT (this pass)

The current documented order is right in SHAPE, wrong in WIRING, and now provably wrong in a
third place: the 8-step table (AGENTS.md:44-51) has no rib_boot row, no state/CURRENT.md row,
and no vault mount; zknot (:5) and warm boot (:7) ride prose that nothing executes; the
behavior-cards rib (:A6) claims boot-warming nothing performs. Keep recap-first; insert the
rib vault mount after the recap and before the pack (the pack's only compiled-law seam, the
12-row flash band, carries ZERO of the three fresh laws and its debt pointer hides even that
after 2026-10-06T15:18Z: re-verified this sitting, instructions_flash.jsonl = 12 rows, rg
patterns exit 1, compile_report v0.4 2026-09-29T15:18:39Z, PACK_STALE_DAYS=7 at
mag/constants.py:19, debt pointer at mag/context_pack.py:413-415, flash-only docstring
:377-389, CURRENT.md:89-90 owed line wraps exactly as the prior pass found); give
state/CURRENT.md an explicit table slot (lanes.py:231-234 already diverts the FROZEN brief to
it); wire ONE logon verb (zknot + warm boot + rib_boot as an idempotent chain, ages stamped,
exit 2 on age or dropped rows) and the order stops reading fresh-looking stale bytes. Content
outranks recency: tonight every regen fired and STILL no surface a seat mounts carries the
three laws or the retraction; carrying amendment tails (F1) and the superseded list (A3)
beats re-firing the hand crank again. The ouroboros driver joins the enforcement surface
(A4): the round that audits the mount must not lie-by-docstring about its own mount.

## NOT-RUN / OWED (this pass)

- The zknot session store (~/.zcode/cli/db/db.sqlite) was not queried; 18-qualifying/14-written
  ride the runs.jsonl receipt, not an independent census.
- KG pre-heal baselines (1506 / 834): ask-carried, not re-run. The b1 receipt was not opened.
- The GPS ledger (tools/gps_mcp/gps_ledger.db3, 782,336 B, mtime Oct 5 03:15) was stat-pinned,
  not queried; the operator's 03:00 synthesis stays ask-carried.
- mag/thought_bank_app.py body still unread by ANY pass this run (4,257 B, mtime Sep 4 23:37,
  last commit 60b1bde7f 2026-09-14; importer census re-run: exact-name refs in code = itself
  only; mag/lane_runner.py:720 and mag/single_feed.py:29 reference the ALIVE mag/thought_bank
  module, a near-name collision that would fool a loose grep; the day-3 mine card naming a
  09-30 lapse remains unlocated).
- Attribution of tonight's four rib_boot regens, the zknot run, and the warm-boot run: OWED
  (no actor fields anywhere).
- No pytest, no workflow-gate scenario suite, no live URL fetch this sitting; none were asked
  of this pass.
- Absence scopes: "no trigger" covers untruncated full-tree rg + a host schtasks census at
  ~01:1xZ; a ZCode-side hook or a task created after the census would evade both. "No code
  consumer of rib_boot.json" covers the same rg scopes at the same moment.

*Second pass folded. The three rows that survive every sitting so far: amendment tails cut
from both rib surfaces (F1), the MOSAIC convergence law unmarked and retracted only in a
commit message (A1), and three continuity organs whose only regenerator is a sibling's
memory (A2). Pass those upward first.*
