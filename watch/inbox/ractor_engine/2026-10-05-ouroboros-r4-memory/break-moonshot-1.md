# BREAK PASS - moonshot-1 (OUROBOROS R4 memory/boot surface), hostile second pass, 2026-10-05/06

Breaker seat: break-moonshot-1. Every check below was run this sitting unless named
as lens-run. The lens report I was handed was truncated at its 5th finding; the full
two-sitting report is banked at
`watch/inbox/ractor_engine/2026-10-05-ouroboros-r4-memory/moonshot-1.md` and I
recovered findings F5/F6 and the amendment sitting from those bytes before verdicting.

## Verdicts

### F1 boot mounts heads, law amends at tails: CONFIRMED (CONVERGENT, now 4 independent derivations)

- `mag/rib_boot.py:76` = `LAW_HEAD_CHARS = 1200` and `:94` = the head slice, byte-exact.
- Amendments verified in the ribs: `memory/rib/RIB_INFERENCE_BUDGET_20261001.md:119`
  (POST-DATUM header), `:129` ("THE LAW IS NOW: omission is a MEASURED ON state",
  grep count 1 in the rib), `memory/rib/RIB_MODEL_GATES_20261001.md:126` (SCOPED
  EXCEPTION inside the amendment block that starts at `:108`).
- My own greps on `memory/rib_boot.json`: "omission is a MEASURED ON" = 0 hits,
  "POST-DATUM" = 0 hits. STRONGER than the lens knew: the file's `ts` is
  2026-10-06T00:40:23Z, a THIRD post-amendment regeneration (e03 proof 06:07Z, the
  lens second sitting read 00:11:19Z, mine 00:40:23Z), and the amendment bytes are
  still absent. The falsifier (a fresh run whose law_head carries POST-DATUM) was
  tested three times tonight and held every time.
- PHRASING CORRECTION (does not kill): the lens's "a fresh seat gets the refuted
  pre-amendment mint prose" overstates. Measured head tails: the INFERENCE_BUDGET
  head ends inside the 2026-09-17 jacket-census entry, the MODEL_GATES head ends at
  the GLM-5.3-PRIME row, BEFORE the DEEPSEEK section entirely. The mounted heads
  carry neither the refuted STILL-UNWIRED bullet (`:110-114`) nor the DEEPSEEK
  mandate it amended. The harm is total omission (no d4 law, no deepseek rail at
  all), not served refuted prose.
- CONVERGENT: `break-accuracy.md:35` and `break-communication.md:37` independently
  confirmed the same defect before this pass.

### F2 tonight's law class reaches zero boot surfaces: CONFIRMED

- My censused greps (untruncated, whole scopes): memory/rib/*.md (52 files) = 0
  Sybil/different-bugs; AGENTS.md = 0; .agents/skills/operator-corrections/SKILL.md
  = 0; state/CURRENT.md = 0; memory/zknot/LATEST.md = 0.
- `watch/inbox/LINKS.jsonl` carries Sybil = 2, different-bugs = 1 (rows 432/435).
- Commit 1693dd2ad verified (2026-10-05 15:15:08 -0400, the Sybil-form convergence
  amendment); `git show --stat` = 1 file changed, 1 insertion (LINKS.jsonl only),
  matching the second sitting.
- Compile ceiling verified: `state/CURRENT.md:46-47` "66 laws compiled into
  .agents/skills/operator-corrections/SKILL.md", dated 2026-10-03 in context.
- Compounding byte the lens found and I re-verified: `memory/zknot/LATEST.md:54-55`
  serves the retraction row and the unamended "fourth convergence data point this
  week" row adjacent, no erratum coupling.
- NUANCE (not a kill): `docs/ref/MCP_EPISTEMIC_MESH_SPEC.md:615` does contain
  "Sybil attacks", but as one item in a mesh threat list (poisoning, recursive
  misinformation, citation laundering, Sybil attacks, malicious MCP servers), not
  the amended convergence law, and the SPEC is itself unmounted canon. The finding
  stands for boot surfaces.

### F3 the unamended DeepSeek pair: CONFIRMED, with a double-invisibility sharpening

- grep POST-DATUM / conditions-suspect across both
  memory/rib/RIB_DEEPSEEK_SHOULDERS_20261001.md and RIB_DEEPSEEK_ELDER_SEAT.md:
  exit 1, zero hits.
- `memory/rib/RIB_DEEPSEEK_ELDER_SEAT.md:90` reads "RAILS RIDE EVERY ASK: thinking
  OFF (row 8, byte-confirmed)" byte-exact.
- Neither rib is in VAULT_RIBS (`mag/rib_boot.py:69-75` lists five names, none of
  them DeepSeek).
- SHARPENING: the D5 conditions-suspect ruling itself lives only in the
  RIB_MODEL_GATES tail (`:129-133`), which F1 proves is unmounted. The correction
  to the ribs is invisible for the same reason the stale ribs are: two organs deep
  past every boot surface.

### F4 boot chain serves August fossils and contradicts itself: CONFIRMED with one arithmetic correction

- `AGENTS.md:55` (briefs FROZEN 2026-09-26) vs `:59` (Prefer memory/briefs/latest.md):
  exact, four lines apart. Two-firsts at `:2` (load framework first) vs `:4` (Boot
  recap first): exact. Width bullets at `:35` (cap 3) vs `:36` (supersedes, 10-wide):
  exact. NOTE: the live G8 gate probe (exit 2, digest d4fc5e37ae5f) is the LENS's
  run, not mine; I verified the prose bytes only and did not re-fire the gate.
- Git dates verified: OPERATOR_CARD 2026-08-04, PROJECT_PROPOSAL 2026-08-05,
  SCIENCE_MAP and DIRECTION_v2 2026-08-06; SPEC and AUDIT committed 2026-10-05.
- Grep zeros verified: MCP_EPISTEMIC in AGENTS.md + CURRENT.md = 0 each;
  MASTER_READ_ESTATE in AGENTS.md + CURRENT.md + FRAMEWORK_LOAD.md = 0 each.
- Byte arithmetic REPRODUCED EXACTLY: boot chain 124,014 B (load table 95,867 +
  CURRENT.md 7,211 + zknot LATEST.md 20,936); unmounted canon 65,790 B; vault
  216,642 B over 52 .md; 5 x 1200 = 6,000 chars = 2.77 percent; 47 of 52 unmounted.
- CORRECTION: "124,014 bytes of August-era fossils" conflates chain with fossils.
  The four August docs total 47,661 B; the other 76,353 B includes live-era organs
  (compass 09-27, FRAMEWORK_LOAD 09-29, AGENTS.md 10-04, CURRENT, zknot). The
  ranked-above-canon claim stands; the byte framing does not.
- Also serves the fossil actively: rib_boot itself mounts the FROZEN brief head into
  every render (`mag/rib_boot.py:158-163`; brief updated 2026-09-26 per
  warm_state.json session_brief), so the boot organ, not just the prose, hands the
  09-26 fossil to seats.

### F5 thought-bank exporter dark: CONFIRMED, all cites byte-exact

- stat memory/thinking/app_reasoning.jsonl = 22,178,801 bytes, mtime Sep 30 11:52.
- Importer census (my run, all .py under mag/ tools/ tests/ scripts/): zero hits
  outside mag/thought_bank_app.py itself.
- git log -1 -- mag/thought_bank_app.py = 60b1bde7f 2026-09-14.
- Day-3 card row 8 verified at
  `watch/inbox/frontier_olm_2026-10-03/percolator_candidates.jsonl` line 8: "the
  thought-bank continuity exporter is P0", "~30-day horizon (146 sessions...)",
  "lapsed since its 2026-09-30T11:52:39... last write", "Implementation OWED;
  hand-run weekly until it lands", owner MagCensusPatrolDaily ride-along.
- Same-minute echo verified: memory/MEMORY.md mtime is also Sep 30 11:52.

### F6 zknot rows-vs-view attribution: CONFIRMED

- `tools/zknot.py:245-246` = `commits = git_commits(earliest); files =
  inbox_files(earliest)`: the wall-clock window collection, exact.
- Truncations verified: `:171` lines[-30:], `:184` todo[:15], `:273` real[:3].
- Card numbers verified in memory/zknot/LATEST.md: fd5ec147 card "Commits in window
  (476)" at :50, "Receipts written in window (8124 under watch/inbox)" at :68, and
  :11 "Prompts: 55 human (1342 templated cron dropped)". The attribution distortion
  is measured: 55 human prompts head a card claiming 476 estate commits and 8,124
  receipts written inside the window (sibling work included).
- Meter verified at :3: "last 7d 133 ... target <75".
- The rows-vs-view split and any recall/get remain unlanded in the 299-line file
  (my read of :240-258 shows no attribution filter; the lens read the whole file).

## Blind spots the lens left OWED, resolved this sitting

1. Quantized-pack expiry (lens OWED): RESOLVED, and CONVERGENT with the lens's own
   second-sitting UPGRADE (derived independently there and here).
   `memory/corpus/quantized_thought/compile_report.json` compiled =
   2026-09-29T15:18:39.593544Z; `mag/constants.py:19` PACK_STALE_DAYS = 7; sum =
   2026-10-06T15:18Z, the exact CURRENT.md claim. memory/analytics/quantized is a
   different organ (two tiny 2026-08-09 quantum-bucket files, 545/619 B, no expiry
   field) and never owned the expiry.
2. warm_state writer (lens OWED): writer organ identified = mag/hermes_warm_boot.py
   (grep for warm_state.json across mag/*.py: hermes_warm_boot.py writes,
   rib_boot.py reads). Which sibling seat invoked it at 23:58:18Z is not in any
   bytes I can read; the organ is the answer available. warm_state.json = 998 B,
   matching the ask. No live gap at my moment: rib_boot.json chain.index 11355 =
   warm_state chain.index 11355, both generated 2026-10-05T23:58:18Z.
3. MEMORY.md readers (lens OWED): censused this sitting, see Addition 2.

## What the lens missed (additions)

1. THE AUDIT ITSELF BOOTS STALE. rib_boot.json ts = 2026-10-06T00:40:23Z was
   regenerated DURING this R4 memory round by the driver's own mount (only code
   callers found: tools/ouroboros.py:169 def rib_boot_mount, :313 boot =
   rib_boot_mount()), and still carries zero amendment bytes. The memory-audit
   organ reproduces the exact defect it is auditing; the falsifier for "the next
   regeneration picks up the amendment" is dead by triple observation (06:07Z,
   00:11Z, 00:40Z). No new move needed beyond F1's law_tail cure; this row is the
   proof the cure must land in code, not in another regeneration.
2. memory/MEMORY.md IS A SECOND DARK ORGAN. 107,954 B, mtime 2026-09-30 11:52 (the
   same minute the thought-bank died). Sole in-repo code reader:
   mag/divergence_meter.py:37. divergence_meter.py is itself imported by nothing
   (grep across mag/ tools/ scripts/ tests/ .py, scripts/*.ps1, configs/*.json =
   zero references outside its own file). mag/boot_check.py:33 reads a DIFFERENT
   MEMORY.md (the harness-side .zcode path), not this one. Nothing reads it, boots
   it, or schedules it: 108 KB of memory dead since 09-30 beside the exporter.
   Move: 15-minute census of what MEMORY.md was supposed to feed, then mount it or
   mark it frozen in AGENTS.md; same class as F5, cheaper.
3. THE LAW-PACK TIMER FIRES TOMORROW 15:18Z AND THE METABOLISM DOES NOT EXIST.
   CONVERGENT with the lens second sitting (independent derivation), with new
   bytes: no scheduler anywhere references the recompiler (grep thought_quantizer
   across scripts/*.ps1 and configs/*.yaml = 0 hits); consumption flips to a debt
   pointer per mag/context_pack.py:384-389 ("renders as a one-line debt pointer
   instead of law"); the flash tier (12 imperatives, compile_report stats) rides
   every seat's boot pack via _quantized_laws. After 2026-10-06T15:18Z every
   min-token seat loses its compiled-law layer until a human runs the quantizer.
   CURRENT.md:90 already says "no scheduler"; nothing tonight wired one.
4. PACK_OFFLOAD.jsonl IS A 6.3 MB WRITE-ONLY LEDGER. 29,828 rows, 6,283,174 bytes
   (wc and stat this sitting), appended by mag/context_pack.py:17,49 on every
   overflow render (14 rows at 2026-10-06T00:02:44Z; live stage-3/stage-4 rows at
   00:48:12Z during this round). The only code that touches the path outside the
   emitter is a test redirect (tests/test_dirac_loop.py:115-117). No reader, no
   consumer, no prune. The no-silent-truncation demand landed as an emitter: the
   truncation became visible but the visibility itself is an unbounded burn ledger
   nobody reads. Move: 20 minutes, either a rotation (keep last N) or a consumer
   row in the census patrol; a gate that only writes is half a gate.

## Boot-order verdict (asked again)

I confirm REORDER on measured bytes: tonight's canon is referenced by zero boot
docs while 47,661 B of August docs rank above it, the vault serves 2.77 percent,
and the first doc a seat is pointed at (per AGENTS.md:4) is a view that attributes
476 commits to 55 human prompts (F6). zknot-first is still right, but only together
with F6's authored-vs-in-window split; otherwise the reorder amplifies the
misattribution. The lens's proposed order (zknot, CURRENT, AGENTS law block,
rib_boot --json after F1, MASTER_READ_ESTATE steals, SPEC mapping, era-labeled
compass/FRAMEWORK) is consistent with every delta measured here.

## What I ran (instrument list)

python greps over rib_boot.json, the rib vault (52 files), AGENTS.md, SKILL.md,
LINKS.jsonl, CURRENT.md, LATEST.md, the SPEC; stat on app_reasoning.jsonl,
MEMORY.md, warm_state.json, PACK_OFFLOAD.jsonl, quantized dirs; git log -1 per doc,
git show 1693dd2ad (+ --stat); reads of e03-rib-vault.json, r11-fold-history.json
(:4 ask text), the day-3 card line 8, FALSIFICATION_RECEIPT_20261005.md (exists,
760 B, Oct 5 10:32: register row 10 landed, while the superseded-conclusions list
still lives only in the r11 lane artifact and trajectory/steps.jsonl, zero boot
homes, confirming the lens's convergence note). NOT run: pytest (no ask named
tests), the G8 gate probe (lens-run; a gate check appends a REGISTRY row, and the
lens already banked exit 2 digest d4fc5e37ae5f), any live context-pack render (the
stage rows at 00:48:12Z are sibling/driver output, not mine).

---

# SECOND BREAK SITTING (break-moonshot-1 continuation), moment 2026-10-06 ~02:2x-05:1xZ

Appended per amend-never-rewrite; the first sitting above is preserved verbatim. The world
moved between sittings: the R4 synthesis moves hit disk 21:55-22:18 ET (SYNTHESIS.md 21:55,
boot_regen.py 22:10, zknot.py S1 gate + SUPERSEDED.md 22:18), AFTER the first sitting's
00:40Z reads and DURING this one (my first tools/zknot.py read this sitting caught the
pre-gate 299-line file; the 386-line gated file landed mid-sitting). Findings below verdict
the handed lens report (F1-F5 in its order) and the first sitting where bytes moved.

## Verdicts this sitting

### Handed F1 - mount serves pre-amendment law: CONFIRMED, convergent with first sitting F1
- Byte-true again at the later moment: mag/rib_boot.py:76 (LAW_HEAD_CHARS=1200), :94 (slice);
  rib_boot.json ts now 2026-10-06T02:01:19Z (a FOURTH post-amendment regen) and the mounted
  DRIVING_LADDER law_head still ends mid-Invariant-3 (TAIL220: "...sensing is never
  substituted for it ... A fresh seat re-derived what this rib held, and had"). SPEND
  (RIB_DRIVING_LADDER_20260928.md:39-51) + ONE-BUG (:53-76) unmounted. AGENTS.md:34 carries
  the SPEND amendment inline: two boot surfaces contradict each other at boot.
- My amendment census of the five mounted ribs (grep ^## ADDENDUM|^## POST-DATUM): 5 blocks
  across 4 ribs, zero reachable in any head - DRIVING_LADDER:39,:53; MODEL_GATES:108;
  INFERENCE_BUDGET:119; FREE_USAGE_POLICY:47. DESCENT_PROTOCOL: none. Mount = 6,000 of
  28,715 law-rib bytes (~21%), matching the first sitting's 2.77%-of-vault arithmetic.
- Same phrasing correction as the first sitting (independent re-derivation): the mounted
  INFERENCE_BUDGET head carries NEITHER 'thinking-off by construction' NOR 'MEASURED ON'
  (checked in the JSON law_head) - the d4 harm is total omission, not served refuted prose.

### Handed F2 - AGENTS.md:36 width law vs G8: CONFIRMED; the probe the first sitting declined is now fired BOTH directions
- Probe A (my Write + run): unstamped max_concurrency = 10 -> tools/workflow_gate.py
  check --script = exit 2, FAIL G8-width-shape, digest e235d63b7a1d (differs from the
  lens's d4fc5e37ae5f because the script bytes differ; both exit 2). Rule byte-true at
  tools/workflow_gate.py:21-25 (gate table), :165-175 (G8 row), :308-347 (g8_width_check).
- Probe B (falsifier direction, NEW): same script + "# envelope-receipt:
  watch/inbox/gala_20260925/AFTERPARTY_CLOSE_20260926.md" -> G8 row "ok" (other minimal-probe
  gates fail; G8 specifically passes). A stamped 10-wide passes and AGENTS.md:36 still does
  not say so: no stamp instruction in the bullet; last commit aef98066c 2026-10-04 05:39:22
  -0400 predates the 10-05 G8 landing; the uncommitted working diff (git diff AGENTS.md,
  4+/1-) adds boot rows 0a-0c only, :36 untouched.

### Handed F3 - convergence amendment reaches no boot surface: CONFIRMED (untruncated census)
- git show 1693dd2ad --stat = 1 file/1 insertion (LINKS.jsonl row DROP-GSTD-COFOUNDER-
  AMENDMENT at line 433, full amendment text in its title); e5fd04ecf same 1-row shape.
- My census (grep -rni sybil over memory/rib/, .agents/skills/operator-corrections/,
  memory/corpus/quantized_thought/, docs/, mag/, tools/; full output read): only
  docs/ref/GSTD_INCORPORATION_DRAFT.md:53 and docs/ref/MCP_EPISTEMIC_MESH_SPEC.md:615 (the
  threat-list item the first sitting also dismissed as unmounted canon); ZERO in rib/skills/
  quantized. different-bugs|authorship overlap census: only memory/trajectory/steps.jsonl
  (session logs). tools/lawlog.py exists (4,158 B, Oct 3) but is a block-meter only
  (docstring :1-17); no law-delta compile anywhere. Pre-amendment bytes confirmed at
  RIB_MOSAIC_SEED_20260921.md:37 and corpus/steal/DESCENT_DAY1_STEAL_20261001.md:416.
  LATEST.md:54-55 (old recap) carried retraction + retracted claim adjacent; the 02:18Z
  rewrite keeps both commit lines but now adds the demotion pointer (see F4).

### Handed F4 - zknot silent truncation + rows/view unlanded: WEAKENED (cure landed mid-sitting)
- Byte-true at the lens's moment (first sitting F6 also confirmed the 299-line reads).
  Imprecise then: per-section omission notices existed at old :180-181, :185-186, :189-190,
  :193-194; only the [:3] card cut was silent.
- Cured now: tools/zknot.py is 386 lines - OMIT_MARK :65, omission block :229-250,
  return 2 at :371 (S1 gate); run row 2026-10-06T02:18:16Z: qualifying 19, written 5; the
  rewritten LATEST.md carries ":255 - ... 16 qualifying sessions not carded above (newest
  first; cards under memory/zknot/)" plus the demotion register pointer at :5. boot_regen
  fires it before every context-pack (main.py:3512-3543 exit-2 contract; verdict rendered
  at context_pack.py:1215-1231). The day-4 exit-2 demand is LANDED at the caller + producer.
- Still owed: rows/view split + recall(rank)/get(cited-turn) verbs - current zknot.py uses
  sqlite read-only as card source only (:42,:52,:99,:316), no view/verbs. The synthetic
  250-row exit-2 probe: NOT RUN by me (gate verified by code read + landed LATEST bytes).

### Handed F5 - memory dying unregenerated at three points: WEAKENED (1 leg stands, 2 killed by tonight's landings)
- Thought bank leg STANDS: ls -l memory/thinking/app_reasoning.jsonl = 22,178,801 B,
  Sep 30 11:52; wc -l = 9,305 rows (exact match to lens + day-3 card); grep -rl
  app_reasoning scripts/ = empty; mag/thought_bank_app.py unchanged since Sep 4. No
  metabolism found by my named instruments (schtasks CSV mag-filter saw 19 mag tasks;
  only MagLawPackDaily matched the lawpack/zknot/warm/rib filter).
- Pack leg KILLED as of tonight: compile_report.json "compiled": 2026-10-06T02:00:48Z
  (fresh; the first sitting's 2026-09-29T15:18:39Z bytes are gone). The metabolism the
  lens and first sitting called absent is LIVE: scripts/lawpack_daily.ps1 +
  register_lawpack_task.ps1 (SYNTHESIS move 2), schtasks = "\MagLawPackDaily",
  "10/6/2026 9:30:00 AM","Ready", logs/lawpack.log START 22:17:52 exit=0 verdict fresh.
  First-sitting Addition 3 (timer fires tomorrow 15:18Z, no metabolism) is dead bytes now.
  state/CURRENT.md:90's "expire 2026-10-06T15:18Z with no scheduler" is itself stale.
- Superseded-conclusions leg KILLED as of tonight: memory/fold_history/SUPERSEDED.md
  landed (6,874 B, 22:18 ET), minted FROM the r11 lane archive the lens cited
  (memory/runs/mickey17_v2/runs/2026-10-04-0/lanes/r11-fold-history.json, 9,335 B, ask
  text byte-verified), wired into tools/zknot.py:267-269 and mag/context_pack.py:421,
  pointer live in LATEST.md:5. First sitting's "zero boot homes" was true then; not now.
- KG heal CONFIRMED by my own recount with the CORRECT keys (edges are from/to; a sibling
  recount in trajectory/steps.jsonl 61344 used source/target, read 1,144 dangling/2,921
  orphans with None samples - an instrument bug, not estate truth): nodes 2,921, edges
  1,144, dangling 29 (all rel=already_inside), orphans 1,204. Exact match to lens + ask.

## Additions this sitting (new bytes, not in the first sitting)

1. CORE_LAWS constant serves a pre-SPEND law at every boot: mag/rib_boot.py:109 hard-codes
   "rightsized: cheap-first; frontier scarce; human L3 on irreversible." into every boot
   JSON. Compressed-law drift against the SPEND amendment (DRIVING_LADDER:39-51,
   AGENTS.md:34): judgment-class dispatch to the funded tiers is the DEFAULT now. Second
   stale-law surface inside the same boot module as F1. Move: one Edit + regen. ~10 min.
   Falsifier: core_laws in a regenerated rib_boot.json carrying the amended posture.
2. The behavior-cards rib mounts NOWHERE while claiming it does: RIB_BEHAVIOR_CARDS_
   20260928.md:5-6 "This rib is the card deck; the seat warms it at boot", but grep -c
   BEHAVIOR_CARDS memory/rib_bus/doctrine.json = 0, absent from VAULT_RIBS (rib_boot.py:69-75)
   and the load order. An organ that claims boot service and serves none - the ask's
   no-sacred-cows case. Move: add to VAULT_RIBS or the context-pack card tier. ~15 min.
3. Boot-order verdict (the fold's demanded return; sharpened from the first sitting's
   REORDER): order 0a newest state/*.md -> 0b LATEST -> 0c rib_boot.json -> docs 1-6 ->
   AGENTS.md -> context-pack is RIGHT IN SHAPE as of tonight (rows 0a-0c sit uncommitted in
   the working tree; context-pack fires the regen chain first with the exit-2 age gate) but
   WRONG IN CONTENT at three seats: (a) row 0c serves pre-amendment heads + Addition 1;
   (b) rows 1-6 are 08-04..09-29-era canon (git log -1 dates re-measured: FRAMEWORK_LOAD
   09-29, compass 09-27, science map 08-06, direction 08-06, proposal 08-05, operator card
   08-04) with no supersede pointers; (c) tonight's operator canon (MCP_EPISTEMIC_MESH_SPEC
   768 lines, AUDIT, GPS synthesis e5fd04ecf) reaches no boot row. Move: add row 0d
   (operator canon: LINKS load-bearing + demotion register), commit rows 0a-0c. ~20 min.
4. Fresh-seat read delta (the ask's measure): 6,000 of 28,715 normalized law-rib bytes
   (~21%); 0 of 5 amendment blocks; 47 of 52 ribs count-only; 3 of 19 qualifying zknot
   sessions carded (16 now named); 1 of 9 core_laws contradicted; warm_state.json fresh
   (998 B, generated 2026-10-05T23:58:18Z, chain index 11355 ok, matches rib_boot chain
   tip). The boot delta is now a WRONG-BYTES delta, not a freshness delta - except the
   thought bank, the one organ still dying unregenerated.
5. Instrument hygiene note for the fold: the wrong-key KG recount (trajectory 61344) shows
   why recount claims need the key names in the claim - one sibling's "1144 dangling"
   would have poisoned the fold's graph row had the lens's correct-key numbers not existed.

## NOT RUN this sitting
- The day-4 synthetic 250-row truncation probe (exit-2 assertion): not run.
- Full 52-rib amendment census: out of scope; the mount serves only the 5 censused ribs
  (the only law bytes any seat receives from the vault mount). Scope named in the claim.
- Deeper schtasks sweep for a thought-bank task beyond the named filter: not run; the
  lapsed claim stands on file bytes + the empty scripts/ grep alone.
