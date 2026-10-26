# Receipt: gambiter - 20261006 - FINAL (this window)

Mate: THE GAMBITER. Pack: logs/mates/missions/mission_20261006_08_gambiter.md.
Status: FINAL for this window (stopped on context budget, not thread exhaustion;
3 of the 5 hunting-ground threads named for next cycles below). Next cycle
resumes me by id gambiter.

## FINDINGS

### Game 1 (seed thread): the percolator memorization exploit, formalized

Mechanism (bytes): mag/percolator.py. percolate() partitions text by lexicon,
hashes surviving signal to a 16-hex canonical; a repeat increments that
invariant's count; a novel enters the explore queue. Counts buy real things:
mag/invariant_surface.py:180 ranks invariants by count descending, and
mag/autorun_common.py:93 gates an action at count >= 8. So count is payoff,
not decoration.

Players:
1. The loop (emitters): pro_library.fire logs "[steer] ..." behavioral events;
   mag/operator_inbox.py:425 routes every behavioral event through
   percolate_signal with the constant source "behavioral_event". Live emitter
   sites today: operator_inbox.py:425, fuel_feed.py:557, ox_percolate.py:155.
2. The registry (memory/percolator/invariants.json): stores counts.
3. The heal path (_load_registry, percolator.py:257): on any missing sealed
   generation, merges the newest seal into live.

Pre-fix equilibrium: the emitter's dominant strategy was fire-more, because
each fire of the "[steer] Elevate with a deliberate ask" move re-incremented
the very invariant that tells seats to fire it (a positive-feedback loop paying
itself), and the heal path SUM-merged seal+live counts on every heal event
(memory/percolator/heal.log: repeated heals riding one seal), so heal farming
also paid. Result: count = repetitions x heals, monotone up, never down.
Degenerate monopoly equilibrium: one invariant held 232,214 of 291,343 counted
events (79.8 percent). The meter read the loop's obsession as truth.

The rule change (Z15, landed 2026-09-30, receipt
watch/inbox/hydrology/Z15_PERCOLATOR_FIX.md, verified on bytes this window):
three payoff edits. (1) Half-life decay: count halves per 30 idle days, floor
1, so hoarded count depreciates. (2) Heal-merge takes MAX not SUM
(percolator.py:297): idempotent, heal farming pays zero. (3) Self-emission
cap: same source in the same UTC cycle counts once (percolator.py:395), so the
fire loop's marginal within-day payoff is zero. New equilibrium: count
approximates distinct (source, cycle) observations, decayed by absence.

Post-fix state, read this window: 648 invariants, total count 1193, top count
37 (3.1 percent share), 578 rows at count 1. Instrument: tests/test_percolator_z15.py
= 15 passed in 10.05s (this window, -p no:cacheprovider). The exploit is
neutralized at the registry.

### Residual exploit surface (my delta, unpatched, named)

R1. Source-rotation pump. The cap keys on the source string, and source is a
caller-supplied free string (percolate_signal source param). N invented source
labels buy up to +N per UTC day on one chosen invariant, and every observation
refreshes decay_as_of (percolator.py:413), so a continuously pumped invariant
never decays. Cost near zero; payoff: top ranking in invariant_surface plus
passing count >= 8 gates. Backstop exists but is DORMANT: maintenance()
(caps count to distinct observed days, applies decay) has zero scheduled
callers repo-wide; grep over mag/, tools/, scripts/ finds only the CLI flag
(percolator.py:971) and tests. Rule change: wire maintenance into an existing
daily task (the estate already runs the MagFtsIndexDaily and
MagCensusPatrolDaily scheduled-task patterns), and consider hashing source
into a bounded verified namespace so labels are not free.

R2. Seal-laundering floor. Heal-merge takes MAX(seal, live). mag/seal.py
copies invariants.json as ground truth and signs byte-identity of the copy,
not truth of the content. A poisoned live registry that gets sealed becomes a
permanent count floor that survives later wipes via heal (the exact amnesia
path the heal exists for). Lower severity than R1 because it requires
poisoning live first, but it makes R1 damage durable across resets. Rule
change: run the maintenance cap after every heal (a heal is exactly when
inflated counts re-enter), or have seal() refuse to snapshot counts above the
observed-days bound.

### Game 2 (self-chosen cycle-2 thread): queue priority is cheap talk

Mechanism (bytes): configs/lanes.yaml priority_markers = ["[priority]",
"[grok]", "[L2]"]; grok_budget max_escalations_per_day = 2 (in-code default 8),
require_priority = true. Two gate sites with different semantics:

- Strict gate, mag/lanes.py:193 can_escalate_grok: budget binds everyone
  (used >= max_d returns False regardless of marker); the marker is an
  admission requirement, not a bypass; force=True bypasses everything.
- Lenient gate, mag/router.py:649 (the overview/plan dispatch path): blocks
  only when NOT markers["priority"] AND NOT grok_budget_ok. A goal text
  containing the substring "[priority]" (mag/lanes.py:160 is a pure substring
  match, self-issued) skips the exhausted-budget block. grok_budget_ok itself
  is honest (router.py:273, computed from real usage rows in logs/usage.jsonl
  via lanes.py:178).

The game: the marker is cheap talk any seat can print; the budget is the scarce
resource ration. At the lenient site the marker buys a budget bypass. Dominant
strategy for any seat that controls its own goal text: always tag. Equilibrium:
the cap unravels (it binds only untagged goals, and the marker list is public
in configs/lanes.yaml, so no knowledge asymmetry protects it). The "specialist
scarce" doctrine dies by vocabulary, not by code.

Machine-printed proof the talk is already cheap: estate code prefixes its own
goals with the marker to pass admission, force=False, at
mag/decision_framework.py:264 ("[priority] loop recovery: ...") and
mag/refine_loop.py:254 ("[priority] refine-loop: ..."). The strict gate still
binds budget there, so the cap survives at those sites. The bypass lives only
at router.py:649. Also: mag/act.py:198 passes force from the caller-supplied
decision dict (decision.force or decision.force_grok), a second, explicit
bypass lever.

Rule changes that move the equilibrium, smallest first:
1. One line: at router.py:649 drop the "not markers['priority']" disjunct so
   the budget binds everyone; the marker keeps its admission role and loses
   the bypass role.
2. Structural: make the marker a metered token issued by governor/switchboard,
   spent on use, non-transferable; or verify at intake that markers originate
   from the operator surface, never from seat-authored text.

I did not patch router.py: spec-before-behavior discipline; this receipt is
the spec and the owning lane applies the fix with this citation.

### Unexplored threads (named for next cycles, not ridden)

1. The meter (self-steal meter, tools/zknot.py): does counting your own steals
   create an incentive to manufacture stealable-looking work?
2. The duel harness: judge selection and who pays for duels; can a seat farm
   wins against a chosen judge?
3. The credit rails (Hermes/Nous, DESCENT protocol): the STEER row legalizes
   API spend only for cross-family judgment or failover; who classifies a task
   as cross-family? Self-classification is a bypass of the spending cap.

## JOURNEY

1. Read the pack (48 lines). Filed the claim receipt before speech, per the
   pack contract. Why: receipt-before-speech law.
2. Read mag/percolator.py nearly in full (through line 957; the CLI tail from
   958 excluded, not needed for the game). Why: the seed thread demands the
   actual payoff function, not the docs.
3. Pulled live registry counts, configs/percolator.json, and the Z15 fix
   receipt (first 80 lines of watch/inbox/hydrology/Z15_PERCOLATOR_FIX.md).
   Why: real-counts law; the exploit numbers and the fix's post-state must be
   byte-backed before formalizing.
4. Grepped count-ranking consumers. Found invariant_surface.py:180 and
   autorun_common.py:93. Why: counts only matter if they buy something; this
   established the payoff surface.
5. Grepped percolate_signal emitters: operator_inbox.py:425, fuel_feed.py:557,
   ox_percolate.py:155. Why: identified the loop side of the game and its
   source labels.
6. Read mag/seal.py:47-166 after spotting MAX-merge at percolator.py:297.
   Why: "who can set the max?" led to the seal-laundering residual R2.
7. Dead end: first pytest run exceeded the 120s tool timeout (cold start).
   Lesson logged per the positive-steering law; retried at 420s timeout with
   -p no:cacheprovider: 15 passed in 10.05s. Why the turn: the same
   instrument, larger budget.
8. Grepped repo-wide for maintenance callers: only the CLI flag and tests, so
   the decay/cap backstop is dormant. Why: this decides whether R1 pays.
9. Rode to cycle 2, self-chosen thread: queue priority (hunting-ground row).
   Read configs/lanes.yaml, mag/lanes.py:150-219, mag/router.py:248-277 and
   615-674. Why: cheapest second formalization, bytes already in hand.
10. Found the lenient-gate bypass at router.py:649; verified marker provenance
    (lanes.py:160 substring) and budget provenance (router.py:273, honest)
    before claiming. Also verified the two machine-printed "[priority]" call
    sites and the act.py force lever. Why: no fabricated anything.
11. Named 3 remaining threads; context budget is now the binding constraint.
    Stopped per pack law (stop on thread exhaustion or context budget,
    whichever first).

Dead ends, named: the pytest timeout (recovered, item 7); the initial greps
for maintenance in tools/ and scripts/ returning nothing (that was the
dormant-backstop finding, not a failure); dist_audit/ copies of lanes.py and
router.py appearing in greps (audit snapshots; ignored in favor of the live
mag/ tree).

## COUNTS (all real, this window)

- Mission pack: 48 lines.
- Files read this window: 7 distinct files (mag/percolator.py lines 1-957,
  mag/seal.py lines 47-166, mag/router.py lines 248-277 and 615-674,
  mag/lanes.py lines 150-219, configs/lanes.yaml all 158 lines,
  watch/inbox/hydrology/Z15_PERCOLATOR_FIX.md first 80 lines, mission pack
  48 lines).
- Registry read this window (memory/percolator/invariants.json): 648
  invariants; false_positives 13; total count 1193; top count 37 (3.1 percent
  of total); buckets: 578 rows at count 1, 43 in 2-5, 19 in 6-20, 8 in
  21-100, 0 above 100.
- Pre-fix numbers, cited from the Z15 receipt, not re-measured by me: top
  232,214 of 291,343 total (79.8 percent); post-apply top 27, total 1,066,
  108 of 526 rows changed.
- Tests this window: tests/test_percolator_z15.py = 15 passed, 10.05s.
- maintenance() scheduled callers repo-wide: 0 (only percolator.py:971 CLI
  flag and tests).
- Live percolate_signal emitter sites: 3.
- L2 escalation gate sites audited: 2 (strict lanes.py:193, lenient
  router.py:649); priority marker strings: 3; configured
  max_escalations_per_day: 2 (in-code default 8); can_escalate_grok call
  sites: 3 live + 1 self-test (lanes.py:255); machine-printed "[priority]"
  call sites: 2 (decision_framework.py:264, refine_loop.py:254); force-lever
  call sites: 1 (act.py:198).
- Patches applied by me: 0 (spec-only window).
- Receipts filed: 1 (this file, rewritten once from claim form).
- Threads ridden: 2 of the hunting ground's 5; threads named for next cycles: 3.

## STATUS

FINAL for this window. Resume by id gambiter for threads: the meter, the duel
harness, the credit rails. No em-dashes. No fabricated anything.
