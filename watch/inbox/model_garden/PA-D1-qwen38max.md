# PA-D1-qwen38max (qwen/qwen3.8-max-prime @ nous, turn 1, channel: content)

# ADVERSARIAL READ: ractor50 doctrine chapters (accuracy, logic, operations)

---

## CHAPTER 1: 00__accuracy.md

### (1) Strongest objection surviving scrutiny

**The chapter's 12 defect classes split into two incompatible temporal categories, but the instrument upgrades treat them as one.**

Landing-time gates (citation resolver, pinned node IDs) can catch defects that exist AT the moment of landing: ok:true-equals-landed, unreceipted premise dispatch, memory-written citations, hand-copied count. But at least four classes are inherently POST-landing: moment-verdict overwritten in place, state-doc verdict decay, race-written numbers, anchor drift. No gate that fires once at landing time can catch a verdict that decays three days later. The chapter's "Instrument upgrade" sections for incidents 3 and 11 (the ones visible before truncation) propose versioned files and scheduled re-runs, but these are never elevated to the same enforcement status as the citation resolver. The result: the chapter's headline deliverable (citation-resolution gate at landing) addresses the easiest half of its own taxonomy while the harder half gets prose, not mechanism.

This beats the cheap seat's objection ("the gate certifies form not truth") because the cheap seat's critique assumes the gate was meant to catch reasoning errors. The chapter explicitly scopes it to transport/citation resolution. The real defect is not that the gate is too weak for its stated purpose - it is that the chapter's own taxonomy proves the gate's stated purpose covers only a subset of the incidents it catalogs, and the chapter never acknowledges this coverage gap.

**Cheap seat verdict:** partially valid, misaimed. The "ritual not law" framing is rhetorically sharp but attacks a strawman (the gate was never claimed to catch inference errors). The temporal-coverage gap is the real wound.

### (2) Line-pinned defects

**Defect A - self-contradiction on code changes:**
Quote: "No code under mag/ or tools/ was touched by this lane, so the conditional ratchet step does not fire."
Location: 00__accuracy.md, method paragraph (line ~5 of body text, after the header block).
Problem: The same chapter prescribes "the ledger append path (the script that writes a LANDED row to memory/burns/LEDGER.jsonl) runs a citation resolver before accepting verdict=LANDED" (Incident 1 instrument upgrade). This IS a code change to a tool path. The chapter simultaneously claims no code was touched and delivers code-change prescriptions as its primary output.

**Defect B - incident 3 fix is unspecified at mechanism level:**
Quote: "versioned fold files + supersession byte census"
Location: 00__accuracy.md, Pattern classes table, row "moment-verdict overwritten in place."
Problem: Every other row in the table names a concrete mechanism ("citation-resolution gate at landing", "pinned failing node IDs from a named receipt before dispatch", "before/after line-count reconciliation in the same process"). This row names a desired state, not a mechanism. Who versions the files? When does the census run? What triggers it? The answer is: unspecified, unlike every other row.

### (3) Landable amendment

Paste into the method paragraph, replacing the "No code under mag/ or tools/ was touched" sentence:

> "This lane touched no code under mag/ or tools/ during its session; its instrument upgrades are prescriptions owed to the next implementation lane. Coverage note: the landing-time gates prescribed here (citation resolver, pinned node IDs) address 8 of 12 defect classes; the remaining 4 (moment-verdict overwritten, state-doc verdict decay, race-written numbers, anchor drift) require scheduled re-verification instruments that fire post-landing, specified per-class in the incident sections but not yet elevated to standing cadence."

**Falsifier for this amendment:** if a future audit shows that one of the "post-landing" four was actually catchable at landing time by the prescribed gates, the coverage split is wrong and the amendment overstates the gap.

---

## CHAPTER 2: 01__logic.md

### (1) Strongest objection surviving scrutiny

**Law 4 (wiring liveness is outside-only truth) is performatively self-refuting within the chapter that states it.**

The chapter's own verification method is: "Quote byte-verification sweep, 11 candidate quotes: 9 byte-hits used" and "Estate grep for the newest vocabulary" (Checks section, items 3 and 4). These are internal searches over the estate's own files. Law 4 states: "wired is a truth only the outside can decide." But the chapter uses internal grep to establish claims about what is wired (the zero-caller finding for mcp_pin.check_drift). If wiring truth is outside-only, then the chapter's own method cannot establish its own law 4 finding. The chapter needs an outside instrument (runtime call tracing, import graph from a live process) to verify wiring, but invokes only text search.

This beats the cheap seat's objection (0/1/2 as two ontologies) because the cheap seat imports "874-drift-rows" which does NOT appear anywhere in the chapter text. The cheap seat is arguing against evidence it brought from outside the chapter, which violates the estate's own citation discipline. The performative contradiction in law 4 is visible entirely within the chapter's own bytes.

**Cheap seat verdict:** the trivalence objection is structurally interesting but UNVERIFIED against this chapter's text. The "874-drift-rows" premise has no source in 01__logic.md. The census-denominator objection (universe re-cut mid-count) is stronger but still relies on external evidence not cited.

### (2) Line-pinned defects

**Defect A - propagation gap asserted without obligation source:**
Quote: "the honest gap is propagation: the newest vocabulary (uncollapsed, never-disproven) has ZERO hits in corpus/steal and memory/corpus"
Location: 01__logic.md, "The system in one sentence" section.
Problem: The chapter presents zero hits as a defect ("the honest gap") but never names the rule or law that obligates propagation. If the vocabulary is three days old (w4-42, dated ~2026-09-27), zero propagation may be normal latency, not a gap. The chapter assumes the obligation without citing it.

**Defect B - law 3 steal presupposes mechanism continuity:**
Quote: "during the next gala wave, witness one sibling lane's grounding_wave claim row under your own seat name"
Location: 01__logic.md, five laws section, law 3 steal.
Problem: The operations chapter (same evidence set) documents that the gala mechanism was substantially rewritten between waves (rate-limit holds, truncation caps, fold-gate guards). A steal that says "during the next gala wave" assumes the next wave runs under the same protocol. If the gala's lane structure changes (as it did between wave5-repair and ball-20260929), this steal is dead on arrival. No condition is stated for when the steal applies.

### (3) Landable amendment

Paste at the end of law 4's row, after "Leverage: high":

> "Verification boundary: this law's claims about wiring (zero-caller findings) were established by text grep, which is an inside instrument. The law's own logic requires that wiring verdicts be confirmed by an outside instrument (runtime import tracing or process-level call logs) before they bank as CORROBORATED. Until that outside confirmation exists, zero-caller findings bank as UNVERIFIED-INSIDE, not CORROBORATED."

**Falsifier for this amendment:** if text grep over the full estate tree (including dynamic dispatch registries, plugin loaders, and config-driven imports) is provably complete for all call paths, then inside search IS sufficient and the amendment's distinction collapses.

---

## CHAPTER 3: 02__operations.md

### (1) Strongest objection surviving scrutiny

**The chapter's ratchet has no release valve: every failure adds a constraint, but no mechanism exists to retire constraints whose triggering condition no longer holds.**

Eight failures produce eight fixes. Each fix tightens: hold before refire (F6), single-writer doctrine (incident 5), --no-register flag (incident 3), fail-loud guards (F4), truncation caps (F10). The chapter never asks: "what does this constraint cost in throughput, and under what conditions do we remove it?" The single-writer doctrine (incident 5 fix) directly contradicts the parallelism that makes 50-wide waves viable. The chapter's own incident 4 shows that width is the binding constraint on throughput. So the fix for incident 5 (single-writer) worsens the condition that caused incident 4 (rate-limit deaths at high width). The chapter contains the evidence for this contradiction but never surfaces it.

This beats the cheap seat's objection (waves may not be discrete) because the chapter explicitly handles non-discreteness: incident 2 addresses journal-order interleaving, incident 5 addresses concurrent writers. The chapter is aware of overlap. What it is NOT aware of is that its own fixes interact with each other to create new failure modes.

**Cheap seat verdict:** the wave-discreteness objection is already addressed by the chapter's own content. The coordination-cost objection ("50-wave budget is really a 50-negotiation budget") is interesting but unanswerable from the chapter's evidence - it is a design question, not a defect in the text.

### (2) Line-pinned defects

**Defect A - census law violated by the chapter's own citations:**
Quote: "896 model.network.failed, 850 429-retryable, 817 the 1302 shape, 11 terminal actors in 2 runs invisible to the tally"
Location: 02__operations.md, incident 4, waves paragraph.
Problem: These numbers are cited from B2_443_dwf_error_census_20260926.md, a receipt from 2026-09-26. The operations chapter ran on 2026-09-30. The logic chapter's census denominator law (same evidence set) states: "never difference two counts taken at different moments." The operations chapter cites a four-day-old count without re-running it, violating the estate's own stated law. The chapter should either re-run the census or explicitly mark these as historical counts with moment attribution.

**Defect B - F6 under-specified against its own evidence:**
Quote: "Refire-once, then bury with whatever banked; every landed lane is reported the moment it banks. Refires into rate-limit-shaped deaths hold ~10 min first (now in code)."
Location: 02__operations.md, fold rules section, F6.
Problem: Incident 4's own evidence states "width 12 after a burst: 1302s until the window decays." If 1302s persist at width 12 even after the hold period, then F6's "hold ~10 min" is insufficient under known conditions. The law should state: "hold ~10 min; if the burst window has not decayed (measured by a probe), extend or abort." As written, F6 prescribes a fixed delay for a variable-duration condition.

### (3) Landable amendment

Paste as a new rule after F10:

> "F11. Constraint retirement: every constraint added by a failure fix carries a sunset condition (the measurable state under which the constraint is no longer needed). At each wave close, the fold reports which constraints' sunset conditions are met. Constraints whose sunset condition has been met for two consecutive waves are candidates for removal; removal requires operator sign-off. The single-writer doctrine's sunset condition is: shared-surface collision rate below 1 per 100 lane-runs for 3 consecutive waves."

**Falsifier for this amendment:** if constraint accumulation is provably monotonic-safe (no constraint can ever worsen throughput or create new failure modes), then retirement is unnecessary and the amendment adds ceremony without value.

---

## (4) THE PATTERN: the fleet's doctrine blind spot

**All three chapters treat instrument upgrades as monotonic improvements with no cost model and no sunset mechanism.**

- Accuracy: gates are added at landing, but no gate is ever evaluated for false-positive rate or for whether it creates false confidence that suppresses downstream re-verification.
- Logic: laws are stated with falsifiers, but no law carries a condition under which it should be retired or weakened. The chapter even notes that "the v4 ladder was designed for a republic of seats and is played by two; its upper rungs are empty" - a law that cannot fire is a dead weight, but the chapter does not propose removing it.
- Operations: every failure adds a constraint (F1-F10), but no rule addresses constraint interaction, constraint cost, or constraint retirement.

The shared blind spot: **the doctrine has a ratchet with no release valve.** It can tighten but never loosen. It can add gates but never evaluate whether a gate's cost exceeds its benefit. It can name falsifiers but never act on a falsifier that fires. The fleet accumulates constraints the way a codebase accumulates dead code - each one justified at the moment of addition, none ever removed.

---

## (5) THE NEXT LEG: three questions for the cheap arm

1. **Does the estate contain any mechanism for constraint retirement?** Searchable: grep for "retire" / "sunset" / "remove gate" / "relax" / "deprecate" across tools/, AGENTS.md, and corpus/steal/. If zero hits, the pattern is confirmed as a structural absence, not an oversight in these three chapters.

2. **How many of the 12 accuracy incidents had citations that would have resolved cleanly at landing time?** Answerable by extracting the original URLs/IDs from the 12 incidents' verbatim quotes, running them through a resolver (HTTP fetch for openreview/arxiv IDs), and counting how many return bytes. This directly tests whether the cheap seat's "gate is a ritual" objection has empirical support.

3. **What is the measured throughput of the shared ledgers under single-writer mode versus concurrent-writer mode?** Answerable by running `python -m mag.shared_surface rebuild` with timing under both conditions (single lane active vs. multiple lanes appending), or by checking whether any existing receipt records such a measurement. This tests whether the operations chapter's single-writer doctrine has a measurable cost that should trigger its sunset condition.
