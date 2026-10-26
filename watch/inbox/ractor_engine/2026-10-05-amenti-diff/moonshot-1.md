# MOONSHOT LENS - the Amenti diff adjudication (2026-10-05, moonshot-1)

Rode the five targets against the estate bytes. Every claim below is either a file/line I read this sitting or a command I ran this sitting. No falsifier was fired; this is adjudication, not the probes themselves.

## 0. Commands run (the receipts for this pass)

1. `./.venv/Scripts/python.exe` over `tools/gps_mcp/gps_ledger.db3`: verdict_log = 703 rows, ts span 2026-09-30T01:24Z to 2026-10-05T07:15Z, verdict mix 323 one / 380 zero, hours lumped into 8 buckets (23h=132, 7h=110, 12h=100, 9h=99, 14h=97, 3h=78, 13h=81, 1h=6).
2. Same DB, day/night split: day(06-20) pass 211/487 = 0.433; night(21-05) pass 112/216 = 0.519. Two-proportion z on my own arithmetic: z about 2.11, p about 0.035, unstratified, confounded by task_shape mix (named below).
3. Tag census: `grep -hoE "(Supported|Disputed|Unproven)" memory/runs/salons/*/SALON_ARTIFACT.md` = 1,222 Supported / 396 Disputed / 665 Unproven (2,282 tokens) across 43 of 53 artifacts; strict pipe-table form only 41 tags. 39 of 53 carry per-seat engine: lines.
4. Fold-outcome tracker search: `grep -rliE "fold.*(falsif|refut|overturn)" memory/runs/ tools/ mag/` returned only raw data and .mimosa hook-state, no organ. The one worked fold re-test is `state/perturbation_battery.json` (2026-09-06, cases P1-P5, per-case caught flags) over `memory/runs/salons/unified_fold_20260906/SALON_ARTIFACT.md`.
5. Tavern organ: `tools/tavern.py:76` (`eff_threshold = max(1, min(5, threshold) - pressure)`), 47 session dirs under `watch/inbox/playground/`, DONE row verified live: `brawl=False spend=2.1141 esc={"Greta Thornwood": 3, "Ilse Marrow": 5, ...} pressure=1 models anthropic/*`.

## 1. Target adjudication

**T1 operator-state feed: steal REAL, mechanism INVERTED.** Nothing types operator state (true, the map's only clean ABSENT). But the specced mechanism (operator writes {sleep, energy, focus} rows daily) dies on writer burden: the operator is the scarcest writer in this estate and self-report surfaces rot here (memory/briefs/latest.md FROZEN 2026-09-26 per AGENTS.md; state/CURRENT.md last updated 2026-10-04, already behind). The mesh side is trivial (`mag/mesh/feeds.py:47` ensure_writer, one call) so the cost is all human. Meanwhile the state is already passively banked: 703 timestamped verdicts. First number, computed this sitting: night verdicts pass 0.519 vs day 0.433 (delta +8.6pp, p about 0.035 unadjusted). The confounder is real (night hours may run easier task_shapes), which is exactly what the next query resolves. Verdict: KEEP, but the falsifier is the stratified cross-tab on banked rows, not a two-week A/B asking the operator to journal.

**T2 harmonic profiles: steal REAL, coldest RUNNABLE vertex, and it is the same instrument as T3.** Family variance is already proven at the filter layer: opus blocks authority-override phrasings 4-for-4 at 16K and 32K, haiku lenient (watch/inbox/RESEARCH_SUMMARY_arena_days_one_two_20261005.md section 4). Nobody anywhere has the sovereignty grid: (family x temperature x register) scored on unprompted disagreement, authority-phrasing survival, verdict-under-pushback. All inputs are free lanes and the arena is a standing harness with an arithmetic cap. Merge T3 into it: pushback-count IS the pressure axis of the same grid.

**T3 repetition-binding: map ERROR found, PARTIAL not ABSENT.** DIFF_TARGETS.md:17 says "sycophancy lore, never measured / ABSENT as measurement." The tavern corpus IS a measured compliance-under-pressure curve: pressure knob in code (tools/tavern.py:76), 47 sessions on disk, DONE rows carrying per-persona escalation 0-5 with model and pressure fields, and the arena receipt section 5 claims monotonicity across 20+ sessions and 4 families (their claim; I verified the artifacts exist and one DONE row, not the curve). What is genuinely cold: repetition-COUNT as the independent variable (the tavern knob is a scalar, not N contrary assertions) and drift on EVIDENCE verdicts rather than persona escalation. So T3 is a new arm of an existing instrument, not a new build. Keep the falsifier (zero drift at N=10 across families = her trance claim has no LLM analog), run it inside the T2 grid.

**T4 photocopy A/B: steal REAL, coldest vertex OF ALL, one design trap.** The freshness header landed today (watch/inbox/MESH_V2_SELFSTEAL_LANDED_20261005.md section 2) and its behavioral effect is unmeasured; nobody in the field has the live-vs-frozen reasoning delta. Trap: `tools/query_broker.py:247` derives frozen from mtime (older than 30 days), so there is no genuine frozen arm yet; an honest A/B pins the catalog pair at a tip (copy) and asks the same N questions through the same seat against pinned vs live. The grader already exists and is deterministic: citation_lint defect-rate and citation resolvability (githooks/pre-push, a05-r2). Dependent variable = lint defect density per arm. $0, machine-checkable.

**T5 condensation threshold: KILLED AS SPECCED (the kill is a finding), salvaged prospectively.** The mine-backward plan assumes an outcome column that does not exist: no organ records fold-later-falsified (command 3/4 above; the single worked instance is the perturbation battery over one salon, state/perturbation_battery.json, 2026-09-06). n=1 outcome rows cannot yield a threshold, and hand-classifying 43 folds against all later receipts is subjective theater. Also the premise "hundreds of salon artifacts" is file-true (587 files) but fold-true it is 53 artifacts, 43 with verdict tags. Salvage (and the eventual honest dew point): (a) parse per-claim agreement density NOW from the fold Evidence columns ("S1, S2, S3 converge" shape verified in memory/runs/salons/agent_mesh_triangulation/SALON_ARTIFACT.md) and the engine lines (39/53 artifacts carry them); (b) mint prospective fold_outcome rows: every new fold gets a 30-day-later mechanical re-test hook in the perturbation-battery shape; the threshold becomes measurable after roughly 20 stamped folds. Stamp now, harvest in a month.

## 2. Free-lane order

1. T1 retro: hour x task_shape (x model) cross-tab on the 703 banked verdicts. Minutes, $0, pure SQL; decides whether the typed feed ever earns its writer burden.
2. T2+T3 unified pressure grid: one harness, arms = register x temperature x family x pushback-count x repetition-count, free lanes + arena, tavern DONE-row shape as the output format.
3. T4 pinned-corpus A/B: pin arm + citation_lint scoring.
4. T5 prospective stamps (parse density vectors today, outcome ledger opens today, threshold harvest ~30 days out).

## 3. The loop itself (.agents/skills/swarm-search/SKILL.md): repeatable, three breaks

- **No falsifier-cost gate at the DIFF station.** Station 5 demands free lanes and minutes, yet T1 shipped a two-week A/B and T5 a subjective archive mine; both had to be retrofitted this sitting to banked-row queries. Law candidate: every falsifier must first be phrased as a query over rows the estate already banks; only if THAT is impossible may it ask for new instrumentation.
- **No map decay.** PRESENT cells never demote when organs retire or rot; the map accumulates like the census carrier before the tripwire law. CONVERGENT: the mesh audit already banked this as the demotion gap (no decay = cannot forget = cannot learn; commit 7b3ee99ec summary). Fix: every PRESENT cell carries a stamp + the cell re-cites a test; a patrol flips stale PRESENT to PARTIAL.
- **Station 7 (re-diff) has no named writer.** This adjudication demoted T3 ABSENT to PARTIAL yet DIFF_TARGETS.md:17 still says ABSENT until a hand edits it; compounding is aspirational without the writer. Cheapest fix: the ractor verdict IS the map patch, landed by the fold.
- **Rider-bias risk (unproven).** Station 1's "one invariant in one sentence" fits a mythos (Amenti = relational carrier) and will distort multi-invariant corpora (a competitor doc set). Falsifier: run the loop on a second rider and see if step 1 forces a false unification. Not run this sitting.

## 4. Blind spots (honest)

- No target's falsifier was fired; every substrate claim is read-or-censused bytes, not a probe outcome.
- The night/day z is my own unstratified arithmetic on 703 rows; task_shape and model mix are uncontrolled, and hour data is lumpy (8 buckets, one bucket n=6).
- Tavern monotonicity and "4 families" are the arena receipt's claims; I verified the organ, the 47 dirs, and one DONE row, not the curve.
- The 2,282-tag census counts tokens, not claims; prose mentions double-count and tag-shape variance (41 strict-table tags vs 2,282 tokens) mean the true per-claim n is somewhere between; the parse must be semantic before T5 vectors are trusted.
- Sibling lenses in this same ractor run were not read; convergence flags (T3 demotion, decay gap) may duplicate theirs, which the fold should score, not me.
- Her system's own empirical claims (fascial, Hz) were not re-verified; out of scope here, already graded MODERN/unmeasured in watch/inbox/AMENTI_TRANSLATION_20261005.md section 2.
