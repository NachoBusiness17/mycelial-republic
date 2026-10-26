# OUROBOROS R4 (memory/boot surface) - break-dogfood hostile pass, second sitting

Banked 2026-10-06 ~02:00Z by the break-dogfood seat (hostile second pass). Scope: byte-check
every evidence cite in the lens report, attack each falsifier, add what the lens missed.
This file previously held the 00:55Z same-seat draft (the draft the lens report cites as its
CONVERGENT prior); this pass supersedes it and is verified independently. Every count names
instrument and moment (census denominator law B2-216). No em-dashes. All subprocess spawning
in this pass rode the shell directly or read-only tools; the one Python subprocess spawn
observed (tools/zknot.py git log call, zknot.py:128) already carries creationflags
CREATE_NO_WINDOW at zknot.py:128, so the win32 law is honored in the bytes I read.

## Instrument log (what this sitting actually ran)

1. `./.venv/Scripts/python.exe -c` census: memory/rib/*.md = 52 files;
   RIB_INFERENCE_BUDGET_20261001.md = 8,608 bytes; RIB_DEEPSEEK_ELDER_SEAT.md = 12,026 bytes.
2. `./.venv/Scripts/python.exe -m mag.rib_boot --json` -> RC 0, ts 2026-10-06T01:40:59Z,
   chain index 11355 (warm_state generated 2026-10-05T23:58:18Z), rib_count 26,
   vault_md_count 52, mounted 5/5. SIDE EFFECT: this run rewrote memory/rib_boot.json
   (tool-owned output, mtime 21:40 local). The INFERENCE_BUDGET law_head ends mid-sentence:
   "...returns empty_content finish=length. memory/continuity/seat_memory_20260927/o".
   The MODEL_GATES law_head ends mid-sentence at "...catalog ~$0.02-0.04/as" (line ~23,
   BEFORE the DEEPSEEK-V4.1-FLASH row at :26-30). Neither head contains "MEASURED ON".
3. `./.venv/Scripts/python.exe main.py context-pack` -> RC 0, 7,465 bytes (exact match to
   the lens's figure), header mode=full (2026-10-06T01:43:50). Pack lines 33-34 verbatim:
   "### L0b Compiled laws (thought quantizer, flash tier -- obey)" / "[compile v0.4
   2026-09-29, weight=recency x shape, counts are provenance only]".
4. Token census on the full pack bytes, case-insensitive: "measured on" 0, width 0,
   descent 0, convergence 0, thinking 0, authorship 0, gstd 0, mesh 0, gps 1 (a single
   path-shaped hit, not the GPS synthesis). Case-sensitive set (adds d4, max_concurrency,
   fold_gate, G8): all 0. The lens named "nine tokens" without listing them; my two sets
   are named here in their place.
5. Janitor mode: `main.py context-pack --mode janitor` -> 4,635 bytes
   (header mode=janitor 2026-10-06T01:50:46), not the lens's 4,416: live-content churn
   (tip/census lines) between the two moments; the law-token census is zero in both.
   SIDE EFFECT: the run refreshed memory/context_pack_latest.md (tool-owned output,
   mtime 21:51 local).
6. `./.venv/Scripts/python.exe tools/freshness_check.py` -> "state/CURRENT.md: 1.7d old
   [untracked-mtime] ok" and overall "FRESHNESS: PASS -- boot docs inside the bar".
7. `schtasks /Query /FO CSV /V | grep -i "quantizer|rib_boot|thought_quant"` -> zero rows
   (this cures the lens's malformed findstr probe). Startup folder listing + grep of
   mag_boot_lane.cmd (63 lines, read whole): runs ollama wait, stealth driver, and zknot
   (mag_boot_lane.cmd:39-45); no quantizer, no rib_boot, no hermes_warm_boot.
8. `grep -rln "thought_quantizer" scripts/` -> empty. `git grep -l rib_boot` over the whole
   tracked tree -> 31 files, all prose/index artifacts (catalog.jsonl, tags.jsonl,
   MASTER_EXECUTE_REGISTER.md, MASTER_READ_ESTATE.md, ESTATE_INDEX jsonl/html, rib_boot.py
   itself, rib_boot.json itself, NIGHT_LOOP_20261005.md, rib_fork.py prose comments at
   tools/rib_fork.py:5,:17, RIB_BOOT_DECISION.md, gala check files); the code-file grep for
   "mag.rib_boot|mag\rib_boot|rib_boot.json" returns only tools/ouroboros.py:14 (a
   docstring). .zcode/ sweep: mentions in execute-register.dwf.ts:99 and
   mickey17-burn.dwf.ts:217 are task-ownership prose, not invocations.
9. `./.venv/Scripts/python.exe -m mag.rib_bus mount --domain doctrine` -> 26 rows: chain
   doctrine invariants + table-merge + operator steer noise; zero d4/width/convergence
   law content (first-hand, closing the lens's carried-claim blind spot).
10. Python compute over memory/knowledge_graph.json (its own ts 2026-10-06T01:01:17Z),
    edge keys from/to: nodes 2,919, edges 1,144, orphans (degree-0) 1,204, dangling
    (from/to not a node id) 29, rel=already_inside 31.
11. `./.venv/Scripts/python.exe -m mag.thought_bank_app --census` (read-only DB query of
    ~/.zcode/cli/db/db.sqlite) -> "117,081 new reasoning parts, 9,305 already banked";
    memory/thinking/app_reasoning.jsonl mtime Sep 30 11:52.
12. Reads: mag/rib_boot.py (whole), mag/lanes.py:210-242, mag/constants.py:1-19,
    mag/context_pack.py grep (stale branch :382-413), mag/knowledge_graph.py grep + sites,
    mag/hermes_warm_boot.py grep (:6,:31,:34,:179,:197), tools/zknot.py (whole, 298 lines),
    tools/ouroboros.py:150-190, tools/thought_bank_app.py (whole), memory/rib/
    RIB_INFERENCE_BUDGET_20261001.md, RIB_DEEPSEEK_ELDER_SEAT.md, RIB_MODEL_GATES_20261001.md,
    RIB_BEHAVIOR_CARDS_20260928.md (whole vault POST-DATUM/AMENDMENT sweep via python),
    state/CURRENT.md:1-100, state/NIGHT_LOOP_20261005.md, memory/zknot/LATEST.md,
    memory/warm_state.json, memory/corpus/quantized_thought/compile_report.json,
    watch/inbox/RIB_BOOT_DECISION.md, watch/inbox/LINKS.jsonl:430-435,
    watch/inbox/frontier_olm_2026-10-04/DIGEST.md:41-43 + register.jsonl zknot rows,
    corpus/steal/MASTER_EXECUTE_REGISTER.md:55-84, memories/session/next-window-handoff.md
    (602 lines, incl. :601), AGENTS.md line probes. NOT RUN: pytest (not asked of this
    pass; R3's 345-test green remains the commit's claim, not mine); the whole-vault
    deepseek law census (banked but unfunded); no direct ZCode session-DB census for the
    zknot claims beyond the thought_bank census query.

## VERDICTS

### Finding 1 (boot contract split against itself: handoff warms the FROZEN fossil, AGENTS.md forbids at :55 and prefers at :59, only the pack path diverts) - CONFIRMED

Every cite byte-checked this sitting: memories/session/next-window-handoff.md:9 step 2 warms
memory/briefs/latest.md first (read; exact line); AGENTS.md:55 ("Then: state/CURRENT.md
(live truth; memory/briefs/latest.md FROZEN 2026-09-26 and must not be consumed as live)")
and AGENTS.md:59 ("- Prefer memory/briefs/latest.md, ...") located by line probe, both
exact; mag/lanes.py:227-235 is the Q1 poison fix diverting FROZEN-banner briefs to
state/CURRENT.md inside latest_brief_text() only (read; the divert is pack-path-only; no
doc writer learns). The fossil is live on disk with its banner (rib_boot brief head,
600 chars: "# FROZEN as-of 2026-09-26 ... Truth instead: verkle_tip.json - state/CURRENT.md
..."). Falsifier test: the banner self-correct does exist, so a doc-path seat reading the
fossil first is redirected by the fossil itself; that mitigates severity, not the split.
The lens undercounted the surface: mag/rib_boot.py:61,:161-163 embeds the FROZEN brief head
in every boot output, and mag/hermes_warm_boot.py:34,:179-189 warms the fossil path into
memory/warm_state.json session_brief (chars 2,101, updated 2026-09-26T18:01:29Z, read from
disk this sitting). Three boot surfaces carry the fossil; two boot surfaces carry the
forbid-and-prefer contradiction. Move stands (repoint handoff step 2 + AGENTS.md:59 at
state/CURRENT.md), add: repoint or banner the rib_boot/warm_state brief legs.

### Finding 2 (fresh seat boots pre-amendment law: 1,200-char heads, d4 amendment outside the mount, ELDER_SEAT:90 unamended, :106 says 51 files) - CONFIRMED, mechanism sharpened

All evidence byte-checked: mag/rib_boot.py:76 LAW_HEAD_CHARS = 1200 and :94
`head = " ".join(t.split())[:LAW_HEAD_CHARS]` (read); the d4 amendment text "THE LAW IS
NOW: omission is a MEASURED ON state." is exactly at RIB_INFERENCE_BUDGET_20261001.md:129
(read); the file is 8,608 bytes (stat); my live rib_boot run proves the mounted head ends
mid-sentence in the 09-17 jacket bullet and contains no amendment text (instrument 2);
RIB_DEEPSEEK_ELDER_SEAT.md:90 rails "thinking OFF (row 8, byte-confirmed)" and :106
hard-codes "every rib (memory/rib/, 51 files)" against my live census of 52 (both read;
whole-file read finds NO POST-DATUM section, so the lens's self-falsifier fails to kill);
corpus/steal/MASTER_EXECUTE_REGISTER.md:63-69 carries e03 rows 7-10 which amended
RIB_INFERENCE_BUDGET + RIB_MODEL_GATES + re-probed FREE_USAGE, never ELDER_SEAT (read).
Sharpening (the lens's harm claim needs one correction): the mount does not serve the
PRE-amendment law, it serves a mid-sentence fragment that carries NEITHER the refuted rail
NOR the cure (MODEL_GATES head truncates before its own DEEPSEEK row at :26; my live head
output ends "...~$0.02-0.04/as"). The stale rail reaches a fresh seat by a different door
the lens did not name: AGENTS.md:54's rib-warm law plus the pack's L0d memweave title
pointer (pack line 87 lists RIB_DEEPSEEK_ELDER_SEAT), and the d4 law DOES ride the doc
path in shorthand (handoff:601 "d4 thinking probes - v4 omission=ON"). The structural
finding is stronger than the lens's: the head-from-byte-0 mount can never serve ANY
amendment (see Addition 2). The contradiction a fresh seat actually hits: warm-rib path
serves ELDER_SEAT:90 "thinking OFF (row 8, byte-confirmed)" while handoff:601 serves
"v4 omission=ON". Move stands (append tail sections whole + ELDER_SEAT erratum), with the
note that RIB_MODEL_GATES_20261001.md:129-133 already carries the SECOND-ORDER note naming
ELDER_SEAT and SHOULDERS as stale-cited, unmounted.

### Finding 3 (quantizer lawlessness: v0.4 09-29 pack carries zero of tonight's laws, goes dark 2026-10-06T15:18Z, no recompile scheduler) - CONFIRMED

Byte-checked: memory/corpus/quantized_thought/compile_report.json compiled
"2026-09-29T15:18:39.593544+00:00", v "0.4" (read); mag/constants.py:19
PACK_STALE_DAYS = 7 (read, with the L3-unification docstring); dark date arithmetic
09-29T15:18Z + 7d = 2026-10-06T15:18Z confirmed, and state/CURRENT.md:90 already names the
same debt ("quantized packs expire 2026-10-06T15:18Z with no scheduler"); the consumer
stale branch is real: mag/context_pack.py:382-413 (docstring "render as a one-line debt
pointer instead of law" + `if age_d > PACK_STALE_DAYS:`) - so after the dark moment every
pack renders debt, confirmed in code; pack lines 33-34 confirmed verbatim (instrument 3);
token census zero (instrument 4, tokens named); full pack 7,465 bytes exactly as the lens
claimed. No scheduler, properly probed this time (instrument 7 + 8): zero schtasks rows,
zero Startup entries, zero scripts/ references, boot lane QUEUE has no compile step.
Janitor-mode size differs (4,635 vs 4,416 chars) - live churn between moments, both named;
the lawlessness half is unchanged. Move stands (compile v0.5 now + stage the weekly
recompile beside MagFtsIndexDaily); note the operator's no-timed-cron law of 09-26
(handoff STATE) means the staged task needs the logon-lane pattern like zknot's
mag_boot_lane.cmd:45 slot, or an operator-gated registration.

### Finding 4 (rib_boot.json finding filed but never wired: zero readers, CURRENT.md stale at 10-04T09:30Z while freshness PASSes on mtime, GSTD convergence amendment unwired) - CONFIRMED

Byte-checked: mag/rib_boot.py:181 writes memory/rib_boot.json (read); zero readers and
zero invokers hold under the instruments the falsifiers demanded (instrument 8):
whole tracked-tree git grep finds no code consumer of memory/rib_boot.json; no schtasks
task action references rib_boot (full /V CSV query, the probe the lens botched); no
Startup entry; tools/ouroboros.py:169-175 mounts the rib BUS (mag.rib_bus) and never the
vault file, its only rib_boot mention being the line-14 docstring. New supporting evidence
the lens missed: watch/inbox/RIB_BOOT_DECISION.md (2026-10-01) explicitly ORDERED the wire
("Next: wire it into the boot chain so every cold-start seat gets doctrine before the
first prompt"; priority 1) and the wire never landed - the gap is five days old against a
written order. CURRENT.md half: state/CURRENT.md:8 stamps updated 2026-10-04T09:30:00Z
(read); the 10-05 day (fold gate commit 55cdaaa4f, GSTD rows, R1-R3 landings, mesh spec)
is absent from the file's Goal/Plan sections (read); my freshness_check run PASSes it on
mtime (1.7d vs 7d bar) - the meter is blind to the content stamp, exactly as the lens
said. GSTD half: watch/inbox/LINKS.jsonl:435 carries the convergence amendment byte-exact
("THE CONVERGENCE LAW ITSELF GAINS AN AMENDMENT ... FAILS under authorship overlap");
the lens's received text was truncated mid-sentence here, so the tail ("zero pre...")
is unverified as written, but its verifiable core stands with one caveat: zknot
LATEST.md:54,:138,:217 do carry the commit subject ("GSTD AMENDMENT: operator is
co-founder - convergence data point RETRACTED...") so a fresh seat learns the amendment
EXISTS from the boot recap, while getting none of its content. Lens blind spot closed:
the 23:58:18Z warm_state writer is attributed by module (mag/hermes_warm_boot.py:31
STATE path, :197 schema hermes_warm_state.v1 matching the disk bytes); who fired the run
remains unwitnessed.

## ADDITIONS (what the lens missed)

### Addition 1 - the freshest handoff block serves the PRE-amendment convergence law

memories/session/next-window-handoff.md:601 (NIGHT WINDOW CLOSE 2026-10-05T23:50Z, written
AFTER the 15:15Z amendment) states: "DOCTRINE BANKED THIS WINDOW: convergence law (same
conclusions + different bugs = real convergence; byte-first-dates settle priority)" with
zero amendment pointer, while watch/inbox/LINKS.jsonl:435 (10-05T19:15:07Z) amends exactly
that law ("FAILS under authorship overlap - one hand ships both sides of the apparent
dialogue... check authorship before counting independence"). A fresh seat executing the
handoff (its own step 2) inhales the refuted doctrine as banked law. Same block also
carries "d4 thinking probes - v4 omission=ON" (correct) - so the handoff simultaneously
serves the corrected d4 law and the uncorrected convergence law.
Falsifier: an amendment pointer appended at handoff:601, or the block's law line edited to
cite LINKS.jsonl:435, kills it.
Move: 10 min - append the amendment citation beside the handoff:601 law line.

### Addition 2 - the mount and the amendment law are structurally incompatible

Whole-vault sweep (python, this sitting): exactly 4 of 52 ribs carry POST-DATUM or
"## AMENDMENT" sections - RIB_FREE_USAGE_POLICY_20260823.md:47,
RIB_INFERENCE_BUDGET_20261001.md:119+146, RIB_MODEL_GARDEN_ROUTING.md:215+245,
RIB_MODEL_GATES_20261001.md:69+108+126 - and every one sits far beyond byte 0's 1,200
whitespace-collapsed chars. The e03 cure (append amendments at file end, the
amend-never-rewrite law) and the mount design (head-from-byte-0) can never meet: the
estate's amendment mechanism is invisible to its own new boot surface by construction.
Falsifier: one amendment section found within the first 1,200 collapsed chars of its rib,
or a mount_vault that appends tail sections, kills it.
Move: 25 min - extend mag/rib_boot.py mount_vault to append every ^## POST-DATUM/^##
AMENDMENT section whole beside the head (the lens's own move, now grounded in a vault-wide
census instead of one rib).

### Addition 3 - the thought bank lapse is measured, not just asserted

The ask's premise (thought_bank_app lapsed since 09-30) is now a number:
memory/thinking/app_reasoning.jsonl mtime Sep 30 11:52, and the census run this sitting
(read-only over the session DB) reports 117,081 unbanked reasoning parts vs 9,305 banked.
The harvester has zero scheduled/logon invokers (instrument 7 class). This is the same
unregenerated-memory species as the quantizer, with a 12x-part backlog accruing silently.
Falsifier: a harvester invocation found outside schtasks/Startup/scripts/.zcode, or a
bank mtime newer than 09-30, kills it.
Move: 15 min - add a bounded incremental harvest to the boot lane QUEUE section
(mag_boot_lane.cmd:39-45 pattern, stop-file guarded).

### Addition 4 - the fold deliverables the lens omitted: the amendment table and the boot-order verdict

The lens report contains neither the ranked MEMORY-AMENDMENT TABLE nor the boot-order
verdict its ask demanded. Both supplied here.

MEMORY-AMENDMENT TABLE (ranked: organ -> exact edit -> what a fresh seat gets wrong today
-> evidence):

1. mag/rib_boot.py mount_vault -> append every ^## POST-DATUM/^## AMENDMENT section whole
   beside the 1,200-char head -> 0 of 4 vault amendment sections reachable at boot; fresh
   seat gets mid-sentence fragments ending inside 09-17-era jacket bullets ->
   mag/rib_boot.py:76,:94 + live run 2026-10-06T01:40:59Z + vault sweep (Addition 2).
2. memories/session/next-window-handoff.md:601 -> append the LINKS.jsonl:435 amendment
   citation beside the convergence-law line -> fresh seat inhales "same conclusions +
   different bugs = real convergence" as banked law, refuted 6 hours before that block
   was written -> handoff:601 vs LINKS.jsonl:435 (Addition 1).
3. AGENTS.md:59 + handoff step 2 (handoff:9) -> repoint the warm path at state/CURRENT.md
   (newest state/*.md by mtime), drop briefs/latest.md -> fresh seat is ordered to prefer
   a FROZEN fossil by the same doc that forbids consuming it as live ->
   AGENTS.md:55 vs :59, mag/lanes.py:227-235, rib_boot.py:61+161-163,
   hermes_warm_boot.py:34+179-189 (Finding 1).
4. tools/thought_quantizer.py recompile -> compile v0.5 this week + logon-lane recompile
   slot (operator-gated registration) -> from 2026-10-06T15:18Z every pack renders a debt
   pointer instead of law; until then the law layer is frozen at 09-29, carrying zero of
   the d4/width/convergence/fold-gate/mesh/GPS amendments ->
   compile_report.json + mag/constants.py:19 + context_pack.py:413 + CURRENT.md:90
   (Finding 3).
5. memory/rib/RIB_DEEPSEEK_ELDER_SEAT.md -> POST-DATUM erratum naming the d4 probe receipt
   (MODEL_GATES:129-133 already names it) -> warm-rib path serves "thinking OFF (row 8,
   byte-confirmed)" against the measured omission-is-ON law and a stale "51 files" census
   -> ELDER_SEAT:90,:106 vs RIB_INFERENCE_BUDGET_20261001.md:119-147 (Finding 2).
6. boot chain wiring of mag.rib_boot -> wire into the boot lane per the standing 10-01
   order -> the vault mount output is a finding nobody reads: zero invokers, zero
   consumers -> mag/rib_boot.py:181, RIB_BOOT_DECISION.md priority 1, instrument 8
   (Finding 4).
7. mag/thought_bank_app.py -> logon-lane bounded harvest -> 117,081 reasoning parts
   accrued unbanked since Sep 30 -> census run (Addition 3).
8. tools/index knowledge-graph B1 cure (already_inside edge binding) -> still owed, count
   crept 29 -> 31 -> fresh seat's graph map carries 31 edges pointing at nodes inside
   their own containers and 1,204 degree-0 orphans ->
   compute this sitting (orphan 1,204 / dangling 29 / already_inside 31, json ts
   2026-10-06T01:01:17Z) vs handoff:601 "knowledge_graph already_inside 29 edges (B1)"
   filed as OWED.

BOOT-ORDER VERDICT: the current order is right-shaped and wrongly fed. AGENTS.md:5 puts
the zknot boot recap first and that rung is the only one refreshed during the 10-05
evening (LATEST.md written 19:38 ET by tools/zknot.py, and the logon wiring is real:
mag_boot_lane.cmd:39-45 runs tools/zknot.py at logon, stop-file guarded - AGENTS.md:5's
"rewritten at logon" claim is TRUE, verified in the script). The load-order table
(AGENTS.md:33-41: FRAMEWORK_LOAD -> compass -> science map -> ... -> AGENTS.md ->
context-pack) is static navigation and costs nothing wrong. The broken rungs are below
it: state/CURRENT.md carries a 10-04T09:30Z stamp with the whole 10-05 day absent while
freshness_check.py PASSes on mtime (1.7d, instrument 6); the handoff's newest STATE block
serves the refuted convergence law (Addition 1); and every 10-05 amendment carrier
(LINKS.jsonl:435, docs/ref/MCP_EPISTEMIC_MESH_SPEC.md 17,533 B + AUDIT 4,847 B, the GPS
synthesis row at LINKS.jsonl:433) sits OUTSIDE the boot order - the fresh seat meets them
only as one-line commit subjects in zknot (LATEST.md:54-58) or as the L0d title pointers
in the pack. Verdict: keep the order (boot recap -> framework -> compass -> AGENTS.md ->
context-pack -> CURRENT -> handoff), fix the feed: a round-close verb that appends a
dated block to state/CURRENT.md and a "latest amendments: LINKS.jsonl tail" pointer to
the warm path would close the delta without touching the load table.
Falsifier: a CURRENT.md refresh landing before the next boot with the 10-05 day, or the
handoff law line carrying the LINKS:435 citation, demotes this verdict to
already-cured.

### Addition 5 - premise checks the ask demanded that the lens never touched

- The four knowledge_graph builder defects the day-4 mine named
  (watch/inbox/frontier_olm_2026-10-04/DIGEST.md:41: knowledge_graph.py:102-104, :123,
  :164-165, :171-173) LANDED: commit e80f48b8f ("knowledge_graph 4 mine-verified defects
  fixed + graph regenerated (orphans 1506->1204, dangling 834->29, 300 case_law ids
  decollided, 804 invariant nodes materialized, 300 maps_to edges live)"), and the module
  bytes carry the fix comments (mag/knowledge_graph.py:248 "invariant added 2026-10-05
  with defect fix 3"). My independent compute from the live json reproduces the heal
  exactly: orphans 1,204 / dangling 29 (instrument 10). The residual surface is the B1
  already_inside cure (still owed, count 31) and the 1,204 orphans.
- zknot rows-vs-view (the day-4 mine demand, DIGEST.md:41): what landed is the rows layer
  (per-session cards memory/zknot/<date>_<session>.md, individually addressable, rewritten
  only when the session grew, zknot.py:252-271) and the view layer (LATEST.md regenerated
  from the last 3 cards, zknot.py:273-285), both logon-wired. What the mine named and did
  NOT land in the module bytes: the propose-accept offline consolidation leg (no registry
  or acceptance path exists in tools/zknot.py's 298 lines) and the no-silent-truncation
  gate as a named mechanism (the cards are complete per-session; the view drops older
  cards by design, unflagged).
- Fold-history superseded-conclusions list as "register row 11": NOT FOUND, asserted by
  nobody. memory/workflows/REGISTRY.jsonl row 11 is the mickey17-v2.dwf.ts gate row
  (2026-09-26); zero of its 105 rows match fold-history/superseded; the same grep over
  corpus/steal/ and watch/inbox/ouroboros_20261005/ returns zero. The ask's premise is
  OWED-verification, not a landed row.
- Behavior-cards rib: memory/rib/RIB_BEHAVIOR_CARDS_20260928.md claims "the seat warms it
  at boot" (its own line 8) but it is not in VAULT_RIBS (mag/rib_boot.py:69-75), not in
  the AGENTS.md:54 warm-ribs law (which names FREE_USAGE_POLICY + DRIVING_LADDER only),
  and reaches a fresh seat only as an L0d title pointer (pack line 81). Self-description
  unwired.

## Blind-spot closures carried forward (still open after this pass)

- The whole-vault LAW census (the deepseek instrument, ELDER_SEAT:105-113) remains
  unfunded and unrun; "50 of 53 ribs carried law content" stays a quoted historical claim
  (mag/rib_boot.py:81) whose current-vault descendant I verified only as: 52 .md files,
  4 carrying amendment sections, 5 mounted.
- No direct ZCode session-DB census of the zknot claims beyond LATEST.md bytes +
  zknot.py source + the one read-only census query (117,081 unbanked parts). The
  three-session selection and the 133-per-1000 meter are accepted on zknot.py's
  deterministic source, not re-derived from the DB.
- pytest not run (not asked of this pass); R3's 345-test green remains the commit's
  claim.
- The lens report's fourth finding arrived truncated mid-evidence ("zero pre..."); its
  citable core was verified above and the tail is marked unverified rather than guessed.
