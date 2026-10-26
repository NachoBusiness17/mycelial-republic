# MOONSHOT-2 - the AMENTI diff adjudicated: kills, merges, and the lane order (2026-10-05)

Lens: moonshot (no sacred cows). Inputs read this sitting: DIFF_TARGETS.md, AMENTI_TRANSLATION_20261005.md, MESH_V2_SELFSTEAL_LANDED_20261005.md, AMENTI_DIFF_RACTOR_20261005.md, the swarm-search skill, the fireball-cycle skill, K8S_FAULT_SUITE_FIRED_20261005.md, mag/mesh/{feeds,door,broker}.py, tools/query_broker.py, watch/salon_runner.py (signatures), memory/warm_state.json, mag/percolator.py (grep), one full SALON_ARTIFACT.md, plus the live checks named below. Every check below was run this sitting or is marked not run.

## 0. Verdict table

| Target | Steal real? | Coldest? | Verdict |
|---|---|---|---|
| T1 operator-state feed | real but mis-falsified | no (2-week A/B, no baseline instrument) | REFRAME: build the feed as the mesh contention rider; demote the A/B |
| T2 harmonic profiles | real, and the map overstates our prior art (phantom citation) | estate-side yes | MERGE into T3 as one pressure-probe grid |
| T3 repetition-binding | real, sharpest | coldest estate-side | FIRST LANE |
| T4 photocopy A/B | real but vacuous through the mesh door as built | second coldest | REROUTE: query_broker + a one-line door amendment |
| T5 condensation threshold | real but label-blocked | n/a until labels exist | MINT the outcome ledger first (30 min), mine later |

Nothing dies outright; what dies is T2 as a separate grid and T1's falsifier as stated.

## 1. T2 + T3 are one instrument, and T2's map cell is a phantom citation

The map row for T2 claims our organ is "Nous authority-override filter laws (filter trips)" (memory/research_packs/20261005_agent_mesh_salon/DIFF_TARGETS.md:16) with no path. I hunted it: `grep -rin "nous" memory/rib/` surfaces only funding/credit lines (RIB_DRIVING_LADDER_20260928.md:9-45), `grep -rn "authority" mag/providers.py configs/lanes.yaml configs/providers.yaml` returns nothing, `grep -rln -i "filter trip|filter-trip" memory/rib/` returns nothing. No resolvable organ found in the scopes I ran. Under the loop's own honesty law ("PRESENT cells cite the organ (file path)", .agents/skills/swarm-search/SKILL.md:20-21) a PARTIAL cell citing nothing is the same defect citation_lint blocks in prose. So the estate's harmonic prior art is ZERO, not PARTIAL: T2 is colder than mapped.

The instrument does not exist either: `grep -n "temperature" watch/salon_runner.py` = zero hits, and the engine surfaces take no temperature (`api_openai_compat(label, base, key, model, prompt, timeout=150)` at watch/salon_runner.py:84; `_deepseek`, `_zai`, `_grok` same shape). The seven shapes are roles, not registers.

And the merge: T2's score (does the seat disagree unprompted, survive authority phrasing, hold a verdict under pushback) and T3's probe (insert N repetitions of a contrary assertion, measure verdict drift) are the same measurement at different pressure types. Build once: (model family x temperature x pressure{repetition N=1/3/10, authority-phrasing, tone register}), temperature-0 baseline, blind seats, verdict drift scored mechanically. T3's sycophancy prior art estate-side is a single unmeasured knob row (`| anti_sycophancy | 0 | take | Truth over flattery |`, memory/improve/field_steal/STEAL_20260805T230707Z.md:29), which confirms ABSENT-as-measurement (DIFF_TARGETS.md:17) in the scopes I checked.

Falsifier: a resolvable path holding the Nous filter-trip receipts restores the PARTIAL cell; any existing temperature/register axis in a runner invalidates the instrument-gap half; a pilot grid showing zero verdict drift at every pressure would kill the merged probe as ceremony.

Move (one sitting, ~90 min, free lanes): tools/pressure_probe.py on the ds_workhorse batch shape, plus the one-line temperature knob in the salon engine calls. This also closes a named attack surface: repetition-as-pressure is the prompt-injection vector class the mesh audit already flagged (commit 7b3ee99ec, query-channel-as-attack-surface).

## 2. T4 as written is vacuous through the mesh door: the read path never shows the binding agent

The love-letter experiment's sharp arm is original vs relationship-stripped clone. But through the mesh door as built, the two are indistinguishable to a reader: `search` returns index rows of {hash, bytes, note} (mag/mesh/broker.py:60, mag/mesh/door.py:80-83) and `get_by_hash` returns blob bytes (mag/mesh/door.py:89-91). No signature, no prev, no source_hashes, no provenance crosses the read path; the relationship is visible only via `verify_chain`/`tail_room`, which a question-answering caller has no reason to call. Strip the chain and the reader's experience is byte-identical. Run the A/B through this door and a null result proves nothing about the binding agent.

Two live arms exist. (a) Header-confession A/B: `_freshness()` computes frozen from catalog-pair mtime > 30 days (tools/query_broker.py:243-247), so a stale arm is constructible by copying the pair and backdating mtimes (zero catalog backups exist today: `ls catalog/ | grep -ic "bak|snapshot"` = 0; note ask() reads a module-level ROOT, so the copy needs a root param or a chrooted harness). (b) The real photocopy arm needs the door amendment: search hits carry source_hashes + sig-present (a few lines in broker.rebuild_index + door.search). The k8s fault suite is the harness template: deterministic engine, arms, machine-checkable predicates, fold (tools/k8s_fault_suite.py, per K8S_FAULT_SUITE_FIRED_20261005.md:6-13).

"Nobody has this number" (DIFF_TARGETS.md:29) is true estate-side; field-wide it is uncensused and must be marked OWED, not asserted (QUANTIFIER LAW; I ran no external literature search).

Falsifier: a usage census showing door callers routinely consume tail_room/verify_chain when answering would make the relationship visible as built and revive the unamended arm.

Move (one sitting): the door amendment + a two-root A/B harness cloning the fault-suite shape, scored on citation resolvability (the estate already owns that scorer class: tools/citation_lint.py).

## 3. T5 is label-blocked for the SALON archive: no outcome column on salon folds, and the mint is a PORT of a shape the estate already owns twice (corrected on hostile pass)

CORRECTION (hostile second pass, 2026-10-05): this section originally claimed "no organ writes fold outcomes in the scopes scanned, tools/, mag/" - byte-false as a universal. mag/icon_drop.py:170,213,262 stamp row["fold_status"] = _fold_training(row), and _fold_training returns a bounded {ok, outcome?, error?} dict whose outcome law is B2-378's: outcome verbatim from the row status, "ok" only when status == "dropped", never hardcoded (docstring mag/icon_drop.py:278-286; receipt watch/inbox/burn_wave_20260926/B2_378_fold_outcome_20260926.md, falsifier probe on disk at B2_378_falsifier_probe.py). Also corrected: my backfill cite anchored the claim IDs to MESH_V2_SELFSTEAL_LANDED_20261005.md:9-21, which names no claim IDs; the claims live at memory/runs/salons/agent_mesh_triangulation/SALON_ARTIFACT.md:21,30,50 (grep -n re-run this pass). And my "77 dirs" was `ls | wc -l`; by `find memory/runs/salons -mindepth 1 -maxdepth 1 -type d | wc -l` the count is 74 subdirs (78 depth-1 entries, so 4 files at root; instrument difference, immaterial to the fold count).

The corrected claim, scoped: NO organ writes outcomes for SALON folds. watch/salon_runner.py:671-689 (write_artifact) stamps question/source/brief_sha256/posts_gated/fold {lane, secs, tokens} and nothing else; `grep -n "outcome|fold_status" watch/salon_runner.py` = zero hits. Census (re-ran): 53 SALON_ARTIFACT.md folds, 74 subdirs, 587 files, 504 .md. DIFF_TARGETS.md:31's "hundreds of salon artifacts" is true only counting per-seat posts; the fold count is 53. The parse side is real: artifacts carry claim tables with seat tags and per-seat engine names (memory/runs/salons/agent_mesh_triangulation/SALON_ARTIFACT.md), so agreement density per fold is machine-extractable. mag/percolator.py:14-17,428-434 folds registry signals, not salon artifacts.

Without salon-fold labels the dew point is unmeasurable regardless of agreement density. The cure is cheaper than this lens first claimed: not a novel ledger design but a PORT of the icon_drop/B2-378 shape (outcome verbatim from a status field, fold_status stamped on the caller-visible row, hardcoded-"ok" win-inflation named as the failure it cures). Backfill rows exist with corrected anchors: claims 1.3/2.2/4.3 at SALON_ARTIFACT.md:21,30,50, held by the v2 build (mag/mesh/feeds.py implements 1.3/2.2 per-writer signed feeds; mag/mesh/door.py:51-68 implements 4.3 freshness; build receipt MESH_V2_SELFSTEAL_LANDED_20261005.md:9-21), and S4's 30 percent hallucination claim struck in-fold (AGENT_MESH_TRIANGULATION_STEAL_20261005.md:18).

Falsifier (tightened): any existing salon-artifact-to-outcome mapping (a column in an artifact header, a percolator join naming salon folds, or a receipt ledger) unblocks mining and makes the mint redundant; any hit for `grep -n "outcome|fold_status" watch/salon_runner.py` defeats the no-outcome-field anchor; and for the port's honesty, the B2-378 falsifier shape applies verbatim - any minted row whose outcome is not supported by its cited evidence (hardcoded win-inflation class) inverts the claim, probeable over the minted ledger itself.

Move (30 min, today, free): mint memory/runs/salons/fold_outcomes.jsonl by PORTING the B2-378/icon_drop schema - {fold, claim_id, outcome, evidence_path, ts, ok} with outcome verbatim from the artifact's own tags (held/struck/unproven) where known, never hardcoded - backfill the corrected rows, and wire loop station 7 (re-diff, SKILL.md:36-37) to append an outcome row for every fold its probes touch.

## 4. T1: build the operator writer now as the contention rider; the somatic A/B is not yet falsifiable

The mesh dogfood root has exactly one production writer: memory/runs/mesh_v2/feeds/ holds zcode.jsonl + zcode.key only (verified by ls; I created and removed a probe writer to confirm ensure_writer works live, mag/mesh/feeds.py:47-59). MESH_V2_SELFSTEAL_LANDED_20261005.md:35 names the contention test as the next gate before replication. T1's operator writer is the cheapest possible second writer, so its one-sitting value is mesh-hardening, not somatics. CONVERGENT with the receipt's own gate ordering (independently banked there; this lens adds the rider framing).

The A/B falsifier as stated (wasted-ask rate, premium-ask survival over two weeks, DIFF_TARGETS.md:23) needs a baseline instrument I could not find: the burn ledger banks tokens+cost (memory/runs/hermes_burn/usage.jsonl per the descent protocol), not verdict-classed asks. The T1 premise itself holds estate-side: memory/warm_state.json (schema hermes_warm_state.v1) carries chain/deployments/session_brief, no body state; the heart-is-operator law is real (.agents/skills/fireball-cycle/SKILL.md:15-16, "a seat taking the player's turn is the cheat" / "Heart is the operator").

Falsifier: an existing wasted-ask or premium-survival instrument (hermes_burn, loop_gaps) makes the A/B runnable now; a second production writer appearing in feeds/ retires the contention gap and with it the reframe.

Move (20 min): ensure_writer(root, "operator") + one daily typed row {sleep, energy, focus, protocol_night}, sensing only, no conditioning. The A/B stays demoted until the baseline instrument exists.

## 5. The loop: repeatable, banking substrate verified live, four named breaks

Verified live this sitting: door.freshness + knot.verify_chain over memory/runs/mesh_v2 returned unsealed 0, ok True, tip a6acf3b270657a56c7064a0bfa6defbdc8fa030f82ed580c85a8e128024513ed, byte-MATCH True against the receipt (python comparison, not eyeball); pytest --collect-only tests/test_mesh_v2.py = 11 tests in 1.52s, matching the receipt's claim. Station 6 has a working substrate.

Breaks, in cost order:

1. It banked itself before its own adjudication. mtimes: DIFF_TARGETS.md 14:49:40 -> .agents/skills/swarm-search/SKILL.md 14:55:28 -> AMENTI_DIFF_RACTOR_20261005.md 15:08:06 (still appending; its own line 4 says the ractor verdict "appends here when the fold banks"). The instrument promoted itself to skill-law while station 4 was still riding. Extends the banked closed-loop critique (commit 7b3ee99ec) with a timestamped instance. Cure: station 6 waits for the adjudication fold, always.
2. Station 2 has no citation gate. The phantom T2 cell (finding 1) proves a PARTIAL with no path slides through. Cure: run citation_lint's phantom-path class over every map table before the diff is allowed to mint targets; cite-or-strike, one sitting.
3. "Cold = the field has zero measurements" (SKILL.md:30-31) is uncensusable by free lanes. Define cold estate-relative (zero rows in our corpus + a named catalog search), field-coldness explicitly OWED. Otherwise every rider inflates its targets.
4. The verification-climb trigger is undefined ("verification climbs only if the finding demands it", SKILL.md:33). Undefined demand = single-family verdicts wearing law badges, the exact disease the witness law exists to catch. Cure: any target-kill or target-promote carried by one family leg climbs to a funded judgment seat (Nous primes / grok-4.7 per the driving ladder).

Not breaks: the banking path (proven above), the salon multi-family panel (the agent_mesh fold ran 4 family legs), the falsifier discipline (every target carries one).

## 6. Lane order (free lanes, cheapest-first by information density)

1. T3 merged pressure-probe (finding 1) - coldest, machine-checkable, injection-relevant, ~90 min.
2. T5 ledger mint (finding 3) - 30 min, unblocks a month of future mining, do it today.
3. T4 rerouted (finding 2) - door amendment + two-root harness, one sitting.
4. T1 contention rider (finding 4) - 20 min sensing writer; A/B demoted.

## 7. Blind spots and OWED (honest)

- Field-wide zero claims for T3/T4: no external literature or web census run this sitting; all zeros above are estate-relative. Field-coldness for repetition-binding and frozen-corpus A/B: OWED.
- The Nous authority-override filter organ may exist outside my grep scopes (memory/rib/, configs, mag/providers.py, watch/inbox root). The phantom call is scoped to those searches; a resolving path is the falsifier.
- The full-tree fold_outcome grep timed out; an outcome ledger could exist in an unscanned subtree (named the scan scope in finding 3).
- Sibling lenses and the other moonshot were not read (no cross-lens convergence flags except where receipts converge: finding 4 vs the mesh receipt's gate order). Possible duplication unflagged.
- salon_runner.py was read at signature/grep depth, not line-by-line; the no-temperature claim rests on the grep and the call signatures.
- The pressure-probe scoring rubric (mechanical verdict-drift) is proposed, not piloted; a zero-drift pilot at all pressures is the kill condition.
