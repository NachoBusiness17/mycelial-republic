# ORG SYSTEM V2 - THE LIVE-CLAIM LEDGER

class: DESIGN+RECEIPT; writer: zcode seat (this window); commissioned by operator:
"burn this seat max full width rn on what is useful in parallel using everything
we've learned to help design a better organization system self steal"; moment:
2026-10-18 ~07:20 EDT; instrument: 10 named Explore miners, one parallel volley,
width 10 per the proven Task-agent envelope (receipts: corpus/steal/TETHERED_LINK_STEAL_20260925.md,
watch/inbox/gala_20260925/AFTERPARTY_CLOSE_20260926.md B2-476), ~1.75M subagent
tokens banked; ore distilled below, every claim carries its shelf path.

## The thesis (one recurring failure behind almost every drift receipt)

**Truth decouples from its carrier.** The estate's organizational failures are not
ten diseases; they are one disease wearing ten coats:

- The crown is stale: newest truth (RIB_BOB_PRIMARY_20261017) lives in memory/rib/
  while the row-0a sniff still crowns SOAK_BEACON_20261016, which now states the
  opposite fact about hermes tiering (state/SOAK_BEACON_20261016.md:10-12 vs
  memory/rib/RIB_BOB_PRIMARY_20261017.md:40-42). REDBOARD is 10 days stale but
  still the routed red-patrol page (state/REDBOARD.md mtime vs AGENTS.md:5).
  START_BRIEF says "nothing draining the queue" while SOAK_BEACON says "29 tasks
  registered and firing" (state/START_BRIEF.md:6-8).
- Hand-copied numbers rot: SEATS.md hand matrix says worker gemma4 / Hermes parked,
  live says qwen2.5-coder:7b / parked=false (memory/improve/SEATS.md, FOSSIL-CHECK
  285.8h stale); the census headline class was the founding case
  (tools/census_drift_patrol.py:4-8, "12 days stale, no gate noticed").
- Built organs go dark silently: MagHermesBurn247 disabled 9 days unnoticed
  (watch/inbox/FORGOTTEN_REGISTER_20261016.md); the arch-03 circuit breaker never
  wired in the container copy minted empty knots daily
  (watch/inbox/MORNING_TRIAGE_20261017.md); "29 tasks registered" vs "no framework
  loops alive" contradiction above.
- Law arrives stale: the 1200-char rib mount silently served pre-amendment law to
  the one organ carrying amendments (mag/rib_boot.py:70-79) [CORRIGENDUM 2026-10-18:
  wrong line cite - the head-cut evidence is the docstring AMENDMENT TAILS block at
  mag/rib_boot.py:47-56 ("the 1200-char head cut every POST-DATUM/AMENDMENT section
  off the mounted law"), supporting line 88 and LAW_HEAD_CHARS = 1200 at line 102;
  lines 70-79 are sys.path setup and path constants, no 1200-char content]; the law pack compiler
  fails daily and serves 9.6-day-stale packs "stale-but-good beats empty"
  (watch/inbox/MORNING_TRIAGE_20261017.md); compass section 4 is FROZEN at a
  2026-08 snapshot (docs/ref/REPUBLIC_COMPASS.md).
- Attention floods: memory/attention.md head is machine spam drowning real alarms;
  redboard writes a board nobody is forced to read (tools/redboard.py has no
  consumer, tools/redboard.py:212-218); INDEX folds satiate with nonce-gap warnings
  (watch/inbox/INDEX.json header).

The estate already invented the cure five times, piecemeal: rib_boot's live census
("never hard-code a census again", mag/rib_boot.py:22-26) [CORRIGENDUM 2026-10-18:
  wrong line cite - the verbatim phrase sits at mag/rib_boot.py:149 and the live-census
  doctrine at mag/rib_boot.py:16-20 (COUNT NOTE) and 44-45; lines 22-26 are the
  mounted-laws verbatim quote block], the census patrol's
carrier grammar (tools/census_drift_patrol.py:76-119), the ratchet's
accept-by-name baselines (tools/violation_ratchet.py:284-303), the INDEX event fold
(watch/inbox/index_events.jsonl, 14,905 events [CORRIGENDUM 2026-10-18: moment-drifted
  count - disk read 14,992 events at the 2026-10-18 audit; 14,905 was INDEX.json's derived
  event_count (derived_at 2026-10-17T12:09:10Z). See MOMENT-WARNING in CORRIGENDA below]),
  and B2-338's first-line "ok" law
(tools/census_drift_patrol.py:364-367). V2 generalizes that ONE pattern.

## The design: every durable claim becomes a ledger row with a verifier

### Organ 1 - THE LIVE-CLAIM LEDGER (spine)

A single event-sourced ledger `watch/claims.jsonl` (same append/fold shape as
index_events.jsonl): every prose claim another process might act on - census
counts, the SEATS matrix, redboard tallies, beacon position, version "shipped"
labels, task enabled/disabled states - registers a row
`{id, claim_text, carrier_path, claim_regex, moment, owner, verifier}`.
One generic patrol (`tools/claim_drift_patrol.py`, direct generalization of
census_drift_patrol's frozen-grammar + selftest approach) reruns each verifier on
cadence; STALE/CONTRADICTED rows land on REDBOARD in B2-338 format with owner and
exit named. The carrier grammar law stays: the regex is frozen in the patrol's
selftest, not auto-synced (tools/census_drift_patrol.py:98-116).

### Organ 2 - THE CROWN COURT (canon election with a loud vote)

Replace raw mtime-crown with `state/canon_beacon.json`, written at every window
close and boot: which doc crowns, why (authored vs machinery flag in doc
frontmatter, making the row-0a adjudication machine-checkable), and a freshness
bound. Boot then VERIFYS the crown the way rib_boot does - fail loud (SystemExit,
mag/rib_boot.py:208-211) when the crowned doc is older than the newest law rib or
contradicts a registered claim. The sniff-first violation ("skipped rows 0a-0c and
routed blind all day", state/SOAK_BEACON_20261016.md:46-48) becomes mechanically
visible instead of socially enforced.

### Organ 3 - THE MODE ORGAN (the operator's desktop is a first-class surface)

Today's session proved it: game mode vs burn mode is five manual steps and a
popup plague (watch/inbox/DESKTOP_POPUP_QUIET_20261018.md,
DESKTOP_PAUSE_20261017.md). One command, `mag mode game|burn`: pause/unpause the
sovereign+worker cages, flip the popup-capable surfaces (hidden-launcher
verification across Startup + schtasks actions), and auto-file the pause receipt.
Plus the **no-headed-surface law** as a ratchet rule: any scheduled or agent-spawned
process that opens a visible window on the operator's desktop without a hidden
launcher is NEW debt (the run_hidden.vbs pattern, scripts/run_hidden.vbs:1-16,
becomes enforceable instead of conventional).

### Organ 4 - CONTRACT WIDENING (the boundary covers what actually moves)

The shared surface contract never mentions queue/ or bridge/
(watch/inbox/SHARED_SURFACE_CONTRACT.json, zero hits per SURFACE-MINER): 138
handoff entries are gitignored (".gitignore:47-48"), bridge rows carry no sha256
or receipt, queue jsonl flows bypass classify/receipt entirely, 23,957 files on
disk vs 4,291 indexed with subdirs never orphan-checked (mag/shared_surface.py:~277),
and 44 `%TEMP%*` fossils sit in repo root. Widen the contract: handoff rows get
hash+receipt, the orphan check walks subdirs, a root-temp sweep rule joins the
patrols, and a promotion ledger names where accepted artifacts land.

### Organ 5 - THE CONSUMER LAW (anti-cow clause)

New standing law, derived from the receipts: **an organ without a named consumer
and a named verifier is a cow, not a spore** (the hardy-spores rule,
memory index 10/13, applied to machinery) [CORRIGENDUM 2026-10-18: wrong path struck -
  no repo artifact named "memory index" exists (memory/INDEX.md absent); the hardy-spores
  rule is seat-memory, not a repo artifact. Nearest repo byte: memory/living_map.json:18428
  "the truth is like a hardy spore" (snapshot entry, not an indexed rule). See CORRIGENDA
  C3 below]. Evidence it is needed: redboard has no
consumer (tools/redboard.py:212-218), palace models carry falsifiers nothing ever
checks (tools/palace.py:15-16), behavior cards claimed "mounted at boot" with zero
consumers until a census forced it (memory/rib/RIB_BEHAVIOR_CARDS_20260928.md:77-83),
knot_at_close has no gate that ended sessions reach the chain
(mag/knot_at_close.py:251-253). Every new organ lands WITH its consumer and
verifier named in the same commit, or the pre-push review bounces it.

## What already works (kept as foundations, generalized not replaced)

- Accept-by-name baselines (never loosen the hook): tools/violation_ratchet.py,
  configs/violation_baseline.json, citation_lint_baseline.json, and the per-gate
  clones (githooks/pre-push:399-565)
- Carrier grammar + patrol + fail-closed exit 2 + B2-338 first-line law:
  tools/census_drift_patrol.py, tools/citation_lint.py
- Event-sourced folds: watch/inbox/index_events.jsonl -> INDEX.json
- Knot digests, deterministic, kill-switched, named-omission S1 gate:
  tools/zknot.py:10-44, mag/knot_at_close.py
- Amend-never-rewrite and append-only demotion: memory/fold_history/SUPERSEDED.md:8-10
- Hidden launchers: scripts/run_hidden.vbs, watch/docker_watchdog.vbs
- Measured width laws: Task agents clean at 3/6/10/12, width 10 = 109.4M tok/h,
  workflow children maxAttempts 0 = 429 storm (corpus/steal/TETHERED_LINK_STEAL_20260925.md:10-19,94-97)
- Named-actor lanes with row-index quoting, never ordinals:
  corpus/steal/MASTER_MICKEY17_V2.md FOLD NOTES

## Builds ON the sibling 10-18 docs (no duplication)

- EULER_PHASOR_STANDING_WAVE_20261018.md: immutable checkpoint nodes as
  drift-proof anchors -> the Claim Ledger's rows hash-anchor into that chain
  rather than inventing a second integrity store.
- TWEET_RELIC_ONTOLOGY_20261018.md: the 7 Mirror Tools mapping ->
  Organ 1's claim_drift_patrol slots in as the 8th mirror (verify_knot_v2 kin).
- THE_BACKUP_BRAIN_MANIFESTO_20261018.md: WAL/offline-first queue ->
  Organ 4's widened boundary adopts the same lease/dead-PID reaper shapes for
  handoff rows.
- CONTINUITY_ENGINE_SYNTHESIS_20261018.md: living archive, tripartite canon ->
  Organ 2's Crown Court is the local-hardware leg of that canon.

## Build order (smallest pour first; each is a spore with a falsifier)

1. **Claims seed (hours):** claims.jsonl schema + the 5 worst rotting claims
   registered (census headline, SEATS matrix, redboard tally, SOAK_BEACON position,
   version-registry shipped labels). No new code to register - the rows are prose.
2. **claim_drift_patrol.py (a day):** generalize census_drift_patrol (same
   grammar-freeze + selftest + exit-2 discipline) over the ledger. WARN-only
   first, flip-to-enforce is an operator call (t40 precedent).
3. **canon_beacon.json + loud boot check (a day):** frontmatter flags
   (machinery/authored), boot compare vs newest rib, SystemExit on stale crown.
4. **mag mode organ (a day):** script wrapping today's proven pause/popup moves,
   receipt auto-filed; no-headed-surface ratchet rule second.
5. **Contract widening (a week, no urgency):** hash+receipt on handoff rows,
   subdir orphan walk, root-temp sweep, promotion ledger.

## Falsifiers (the index that kills this design if it lies)

- **F1:** if six months from now a hand-copied headline (any count in a .md that a
  process acts on) rots more than 7 days unnoticed, Organ 1 is a cow - kill it and
  take the receipts as the lesson.
- **F2:** if a window boots past a stale crowned doc without the boot failing loud,
  Organ 2 is a cow.
- **F3:** if the next popup plague requires manual archaeology again (no `mag mode`
  one-command cure), Organ 3 is a cow.
- **F4:** if handoff rows still cross surfaces hashless a month after widening,
  Organ 4 is a cow.
- **F5:** if any organ lands in this repo without consumer+verifier named and the
  push is not bounced, the Consumer Law is theater - strike it from AGENTS.md.

## Miner shelf map (ore provenance, one line each)

- RIB-VAULT: memory/rib/ (60+ files; boot mounting, descent protocol, unbuilt
  light-maze router + rib_dispatcher + grammar-seed compiler)
- INBOX: watch/inbox/ 2026-10 receipts + the four 10-18 sibling docs
- STATE: state/ authored docs + REDBOARD + crown adjudication history
- DOCS: docs/FRAMEWORK_LOAD.md, docs/DNA.md, docs/ref/ (compass, direction, operator card)
- SURFACE: watch/inbox/SHARED_SURFACE_CONTRACT.json + queue/ + bridge/ structures
- SEAT: memory/improve/SEATS.md + HABIT.md + memory/zknot/ + memory/attention.md
- MECHANISM: mag/ (governor_autorun, lane_runner, estate_bridge, knowledge_graph,
  rib_boot, context_pack, warm_surface)
- TOOLS: tools/ (zknot, redboard, census_drift_patrol, citation_lint,
  violation_ratchet) + mag/knot_at_close.py + tools/palace.py
- CORPUS: corpus/steal/ (operating playbook, Mickey17 gopher law, tethered link)
- CONFIG: configs/ (lanes, mag, mates, workflow_gate_scenarios G1-G8, baselines)
  + githooks/pre-push full stack

## Owed (operator calls, in pour order)

1. Pick the first pour (recommendation: pour 1+2 together, the claims seed plus
   its patrol - it cures five of the ten friction classes in one move).
2. Confirm or veto the Consumer Law as standing AGENTS.md text.
3. t40-style decision on WARN-first vs enforce-first for the claim patrol.

## CORRIGENDA (2026-10-18, lane i12-corrigenda-self, GENE g07+g08)

Amend-in-place, named, per the amend-never-rewrite law
(memory/fold_history/SUPERSEDED.md:8-10): every original line above stands exactly as
minted; each correction is an appended [CORRIGENDUM 2026-10-18: ...] marker at its
affected claim, restated here. Instruments: the two G0 audit lanes
memory/runs/genetic_burn/20261018/G0/lanes/g07-ore-audit-1.md and
memory/runs/genetic_burn/20261018/G0/lanes/g08-ore-audit-2.md (g07: 30 checks, 3 misses;
g08: 40 checks, 1 wrong-path, 3 drifted counts). Every corrected cite below was re-read
at the named lines before this section was written.

### C1 - wrong line cite, the rib-mount head-cut (thesis, "Law arrives stale")

Original claim stands as minted: "...the 1200-char rib mount silently served
pre-amendment law to the one organ carrying amendments (mag/rib_boot.py:70-79)".

[CORRIGENDUM 2026-10-18: the cite names the wrong lines. The head-cut evidence is the
docstring AMENDMENT TAILS block at mag/rib_boot.py:47-56 ("the 1200-char head cut every
POST-DATUM/AMENDMENT section off the mounted law ... served PRE-amendment doctrine");
supporting: line 88 (boot-time deck-size comment) and LAW_HEAD_CHARS = 1200 at line 102.
Lines 70-79 are sys.path setup, path constants, and a comment - no 1200-char content.]

### C2 - wrong line cite, rib_boot's live census (thesis, "the cure five times")

Original claim stands as minted: "rib_boot's live census ('never hard-code a census
again', mag/rib_boot.py:22-26)".

[CORRIGENDUM 2026-10-18: the cite names the wrong lines. The verbatim phrase sits at
mag/rib_boot.py:149 ("...never hard-code a census again"); the live-census doctrine is
the docstring COUNT NOTE at mag/rib_boot.py:16-20 and the vault-mount paragraph at
44-45 ("the full vault is censused live so no count can rot again"). Lines 22-26 are
the mounted-laws verbatim quote block (chain=record, window=reasoning).]

### C3 - wrong path struck, the hardy-spores rule (Organ 5, Consumer Law)

Original claim stands as minted: "...an organ without a named consumer and a named
verifier is a cow, not a spore (the hardy-spores rule, memory index 10/13, applied to
machinery)".

[CORRIGENDUM 2026-10-18: the citation "memory index 10/13" is STRUCK as a wrong path.
No repo artifact named "memory index" (with 13 entries) exists; memory/INDEX.md is
absent. The hardy-spores rule is seat-memory, not a repo artifact. Nearest repo byte:
memory/living_map.json:18428, "the truth is like a hardy spore" (a snapshot entry, not
an indexed rule). The Consumer Law claim itself survives this strike; only its
citation does not.]

### C4 - MOMENT-WARNING: live counts drift; counts were true at mint (~07:20 EDT)

This doc hand-copies several live counts. Each was byte-true at its mint moment
2026-10-18 ~07:20 EDT; several have already moved. This is not a refutation of the
thesis - it is the thesis working. A count in prose is a snapshot of one tree at one
moment, never a constant (the census denominator law, AGENTS.md B2-216); only Organ 1's
ledger + patrol makes such numbers self-checking. Read every count below with its
moment, not as a constant:

- "14,905 events" (index_events.jsonl, thesis "the cure five times"): disk read 14,992
  events at the 2026-10-18 audit (14,992 lines, zero blank, first seq 1). 14,905 was
  INDEX.json's derived event_count (derived_at 2026-10-17T12:09:10Z) - a hand-copied
  derived carrier: the doc's own disease in its own text (g07 verdict 23).
- "138 handoff entries are gitignored" (Organ 4): live queue moved since mint - now
  529 recursive / 122 top-level / 136 git-ignored porcelain rows in queue/handoff;
  138 not reproducible at any current scope (g08 check 3).
- "23,957 files on disk vs 4,291 indexed" (Organ 4): 4,291 EXACT (INDEX.json path
  items); 23,957 was watch/inbox recursive at mint, now 23,987, +30 live drift
  (g08 check 5).
- "44 `%TEMP%*` fossils sit in repo root" (Organ 4): now 27 - 20 swept since mint
  (g08 check 6).

Correction discipline: the original numbers above stand as minted and are NOT edited;
fresh counts belong to a live read (INDEX fold, `git status --porcelain`, find), never
to another hand-copy. The audit lanes also logged soft notes that need no correction:
census_drift_patrol.py:4-8 is a compressed paraphrase of lines 4-7;
mag/rib_boot.py:208-211 catches only the SystemExit tail (tighter cite 205-209);
palace.py's falsifier sentence spans 14-15; SUPERSEDED.md's law text spans 10-12.
