# deep-fossil-theory: the FOSSIL-IN-FEED law, formalized

Date: 2026-09-28. Every claim below names what I read or ran in this session. No em-dashes anywhere, per law. Sibling style follows `watch/inbox/burn_reset_20260927/flash50/r-belady-lruk.md` (read this session, lines 1-40), which pins the eviction-side theory (Belady 1966, Mattson 1970, O'Neil 1993); this item pins the recompile-side theory.

**One-line answers.** The optimal k is not a constant: per (artifact, consumer) pair it is k* = clamp( sqrt(2a/(bC)), max(1, R/C), H/C ), an EOQ-shaped interior optimum clamped between a schedulability floor and a harm ceiling. At k=1 you buy read-your-compile and pay R/C per cycle; it is infeasible the moment the rebuild no longer fits inside one consumption period. At k=infinity the artifact is a fossil: admissible only if it simultaneously leaves the feed (sealed, labeled, re-pointed), otherwise it is the estate's measured 12-day census disease. The estate's own sharpening, read out of its gates: violation requires drift, not age alone.

## 0. Receipts: what I read and ran

Read in full this session: `tools/freshness_check.py` (309 lines) and `tools/census_drift_patrol.py` (404 lines); `tools/corpus_fts_rebuild.py` lines 1-150; `mag/hermes_warm_boot.py` lines 1-33; `memory/briefs/latest.md` lines 1-8. Key lines: freshness_check.py:53 STALE_DAYS=7, :54 HEARTBEAT_DAYS=2, :44-51 FROZEN_OK registry, :85 DEFAULT_MAX_AGE_SECONDS=900.0, :160-193 the stale_claim() gate; census_drift_patrol.py:2-7 the measured fossil, :78 CENSUS_STALE_DAYS=7, :125 COLLECT_DRIFT_TOLERANCE=20, :250-288 patrol() with the age-AND-growth conjunction at :265; corpus_fts_rebuild.py:11-15 the meta-table freshness contract, :8-9 the measured 12.35s build over 757,667 rows, :23 exit pattern, :117 atomic os.replace.

Ran this session:

- `.venv\Scripts\python.exe tools\freshness_check.py` → "FRESHNESS: repo heartbeat 0.0d since last commit (alive=yes; bar: stale=7d, heartbeat=2d)", BOOT_4_7.md 2.7d old [frozen-ok], state/CURRENT.md 1.3d old ok, verdict PASS.
- `.venv\Scripts\python.exe tools\census_drift_patrol.py` → "CENSUS-PATROL: ok - census 2026-09-27 (2303 collected / 352 files) ... 1d old of 7d bar, growth noted but inside the window (5 file(s) since census), disk 369 vs carrier 352".
- `findstr /S /I /M "FOSSIL"` over docs/, memory/rib/, configs/ returned zero matches: the law named in the ask is a fresh coinage; nothing below amends an existing in-repo doctrine of that name.
- All seven literature anchors verified against api.crossref.org this session (DOIs in section 6). AGENTS.md clauses are cited from the workspace instructions loaded this session.

## 1. The law, made precise

Let A be a derived artifact (an index file, a census claim, a boot doc, warm state), S the source reality A describes, C the consumption cadence of A's consumer class (mean interval between decision reads), T_R the recompile period, age(A,t) = t minus t_last_compile, and drift the fact that S changed since compile in a way that would change A's bytes. The law states T_R <= k*C.

The structural move is the denomination. k*C is counted in consumer time, not source time and not wall-clock TTL. The same artifact consumed by two seats at different cadences therefore carries two different freshness contracts: a 7-day-old census claim is a fossil for a per-boot consumer (C of one session) and unremarkable for a monthly report. Freshness is a property of the (artifact, consumer) pair, which is exactly what "in-feed" means: the artifact sits in a feed whose loop period is C, and the law caps how many of the consumer's own loops may pass before the artifact is refreshed. A pure wall-clock TTL cannot express this; k*C can.

## 2. What the estate already runs, mapped onto k

Four distinct compiled regimes, all read this session:

1. Per-observation receipts: every tool result carries receipt(observed_at, source_hash) and downstream code gates through stale_claim(), stale past a 900s bar, fail-closed on missing receipts, with a source re-hash that catches drift inside the window (freshness_check.py:85, :160-193). This is the validation/rebuild split: validation per consumption (gate cadence k_gate=1), rebuild on no schedule at all.
2. Boot docs: absolute 7d bar preconditioned on repo heartbeat (alive means a commit within 2d), with a frozen-registry escape (freshness_check.py:53-54, :44-51). Today's live run: heartbeat 0.0d, two docs frozen-ok, rest ok.
3. Census carrier: 7d AND growth (patrol() :250-288, conjunction at :265), plus a magnitude bar of 20 collected items (:125). Conditional and two-dimensional: age AND drift magnitude.
4. FTS index: cheap per-search gate over meta catalog_bytes/mtime, deep sha256 audit tier, one sanctioned writer, atomic swap so a ro reader keeps serving the old index during rebuild (corpus_fts_rebuild.py:11-15, :23-26, :117), scheduled healer at 09:00 daily (AGENTS.md B2-465 bullet; the B2-102 gate "only detects, it never heals" per the same bullet).

## 3. k=1: always fresh

Contract: every consumption sees an artifact compiled within the last C; with a just-in-time scheduler this is read-your-compile, the strong point of the consistency spectrum. Cost: rebuild expense per unit time is a/C, and feasibility requires the rebuild duration R to satisfy R <= C, the classic periodic-task condition (Liu & Layland, section 6). Estate instances: the session warm boot recompiles chain tip, deployments and brief into warm_state.json at session start (hermes_warm_boot.py:1-14, brief path at :32), which is k=1 with C equal to one session and R of seconds, and the 900s receipts bar, which is k=1 for validation with rebuild delegated elsewhere.

Two failure modes, both grounded here. First, schedulability collapse: k=1 claimed while R > C either queues rebuilds into a backlog or silently consumes stale bytes under a fresh label, and the silent cheat is the worse degeneracy because the contract now lies. The estate dodges it explicitly: the deep census check "stays out of the default pre-push path because it needs the venv and a full collection pass" (census_drift_patrol.py:57-61), a recorded refusal to run k=1 on every push. Second, waste below k=1: recompiling more often than anyone reads buys nothing, since both reads fall inside one unchanged interval. Belady's anomaly is the same warning from the eviction side, cross-referenced from sibling r-belady-lruk.md: locally more of a good thing (more memory, more recompiles) is not globally monotone.

## 4. k=infinity: never

Two sub-regimes, and the difference between them is the whole theory of the fossil.

Unlabeled fossil in a feed: the measured event is census_drift_patrol.py:2-7, the hand-copied "1,341 tests / 264 files" headline rode from 2026-09-14 to 2026-09-26 (12 days) while tests/ grew 31 files, because the boot freshness gate watched boot docs and "no gate watched the test-count carrier". Boot-side consumption is roughly daily, so effective k reached 12 and climbing before the tripwire landed. Note the compounding: the number was hand-copied, never byte-backed (AGENTS.md census bullet), so the fossil also severed provenance; staleness rode on top of citation rot.

Labeled fossil, deliberately sealed: memory/briefs/latest.md:1-8 carries a FROZEN banner, "body below is a fossil", names the sealed writers (mag/brief_local.py + mag/session_state_brief.py refuse overwrite), sets the OS read-only bit with an unfreeze instruction, and re-points truth to state/CURRENT.md and siblings. FROZEN_OK in freshness_check.py:44-51 is the registry form of the same move, with reason and date.

The admissible-infinity theorem, stated from these two cases: k=infinity is admissible if and only if the producer simultaneously renegotiates the consumer's contract, that is the artifact leaves the feed (label, re-point, seal writers, register the freeze). A fossil is not a temporal state, it is a contract violation: the producer stopped recompiling while the consumer kept believing. Cost asymmetry explains why sealed fossils are safe and unlabeled ones are incidents: if nobody acts on A, its staleness cost is zero and it is merely an archive; every acting consumer multiplies the harm horizon outward.

## 5. The optimal k

Cost per consumption event: J(k) = a/k + b*(kC/2) + tail. a/k is the amortized rebuild cost (a rebuild every kC costs a/k per consumption); b*(kC/2) is the mean staleness penalty under a uniform consumption phase, since age at consumption is uniform on [0, kC]; tail is harm past the horizon. Setting dJ/dk = 0 gives k* = sqrt(2a/(bC)), the square-root law of lot sizing: freshness is inventory, staleness is holding cost, recompile is the ordering cost. (This is the classical economic-order-quantity transplant; EOQ named from general knowledge, not Crossref-verified this session.)

Three clamps make it operative. Floor: k >= max(1, R/C); below R/C the schedule is infeasible, below 1 it is waste. Ceiling: k <= H/C where H is the harm horizon, the age at which acting on A beats refusing to act; the estate's age-based H is the 7d bar, and its magnitude-based H is COLLECT_DRIFT_TOLERANCE=20 (census_drift_patrol.py:125), because age is only a proxy for drift magnitude and a full law bounds both. Convexity: harm is superlinear in age (the 12-day carrier was an incident; twelve consecutive 1-day lags never were), so the linear holding model underprices large k and the true optimum sits below the EOQ point, which is the argument for pairing a tuned k with a scheduled healer rather than trusting the interior optimum.

The estate's tiered practice is the empirical answer to "what is the optimal k": not one number but a table, receipts at 900s (per observation), boot docs and census at 7d (per session-and-push consumption), FTS rebuild daily with a per-read gate, frozen lineage at infinity (admissible, contract renegotiated). Each row prices a differently: high-b decisions (receipts gate every claim) sit near k=1, low-b archive decisions sit at infinity.

The estate's own sharpening of the law deserves its name: the drift-conditioned freshness bound. patrol() fires only when age exceeds the bar AND the source moved (:265: `stale = age_days > max_age_days and grew`); today's live run shows the AND gate working, 5 files grown since a 1-day-old census, "inside the window", evidence only. Violation is defined against drift visible to an oracle, not age alone, because an old copy of an unchanged source is byte-equivalent to a fresh recompile. k*C is the drift-agnostic envelope you fall back to when watching S is expensive; the conditional form is what you get when a cheap oracle exists (git file-adds since the census date, :219-247; meta bytes/mtime, corpus_fts_rebuild.py:11-15). Oracle strength buys larger k, and weak oracles have measured blind spots: the file-growth signal cannot see items added inside existing files, a 42-item delta measured live (census_drift_patrol.py:53-56), which is why the magnitude bar exists next to the age bar.

## 6. Connections to cache invalidation and eventual consistency

All verified against api.crossref.org this session.

Leases (Gray & Cheriton, SOSP 1989, DOI 10.1145/74850.74870): k*C is a self-expiring lease the artifact holds on its own validity; consumption past expiry forces revalidation. A lease system also has an invalidation channel, the grantor can revoke early. The estate has no invalidation channel, nothing pings the carrier when tests/ grows, so every gate here is the degraded pure-TTL lease: age expiry plus client-side drift polling. The 12-day fossil is exactly the exposure window of TTL-without-channel before the poller existed.

Probabilistically bounded staleness (Bailis, Venkataraman, Hellerstein, Franklin, 2012, DOI 10.21236/ada555882): PBS reports P(staleness <= t) from quorum timing; FOSSIL-IN-FEED is the deterministic limit at t = k*C with probability 1 by construction of the scheduler. The measured 12-day violation carries the same lesson PBS drew from measurements: a staleness bound is a property of the enforcement mechanism, never of the intention.

Crawler freshness (Cho & Garcia-Molina, "Synchronizing a database to improve freshness", SIGMOD 2000, DOI 10.1145/335191.335391): a fixed crawl budget allocated against a changing remote to maximize freshness and minimize age is the same a-budget problem as k, and its central finding, that re-syncing an unchanged page buys zero freshness, is the drift-conditioned refinement rediscovered.

Eventual consistency (Vogels, CACM 2009, DOI 10.1145/1435417.1435432): "eventually" is k=infinity with a promise attached. FOSSIL-IN-FEED converts the promise into a deadline denominated in reader time: convergence within k*C of the consumer's loop. That is strictly stronger than eventual and strictly weaker than linearizability; k=1 with just-in-time compile is the read-your-compile point, k small is bounded staleness, k=infinity is eventual (or never, if the anti-entropy channel is missing).

Nyquist (1928, verified via the Proceedings of the IEEE reprint, DOI 10.1109/5.989875): if the source moves with characteristic period C_S, a recompile period T_R represents source dynamics only up to frequency 1/(2 T_R); beyond that the artifact aliases, reporting plausible stale state. Measured instance: catalog.jsonl appends per trail tick while the index rebuilds at 09:00 daily, within-day aliasing accepted because the failure is graceful, a stale index degrades search to scan fallback, correct but slow (AGENTS.md B2-465 bullet). The Nyquist clamp reads: k must shrink until k*C <= C_S/2 for sources whose drift is not graceful.

Schedulability (Liu & Layland 1973, verified via the reprint DOI 10.1016/b978-155860702-6/50016-8): R <= T is the feasibility floor behind section 3. Cache-invalidation folklore (Karlton's "cache invalidation and naming things") is named as attributed folklore, no primary source verified: FOSSIL-IN-FEED is the TTL-cache answer to it, abandoning coherence messages entirely and budgeting validity in consumer time.

## 7. The enforcement theorem

A freshness law is prose until compiled into four parts, all present and read this session: (1) a detector at consumption with the bar stated in numbers before reading anything (census_drift_patrol.py:9, freshness_check.py:6-7); (2) a healer on a schedule, because B2-102's gate "only detects, it never heals" and MagFtsIndexDaily heals through the one sanctioned writer (AGENTS.md B2-465, corpus_fts_rebuild.py:1); (3) a frozen-registry escape with reason and date, making k=infinity a registered decision instead of a drift (freshness_check.py:44-51, latest.md:1-8); (4) fail-closed cannot-verify paths, exit 2 on git failure or missing carrier or unparseable claim (freshness_check.py:60 "refusing to guess (exit 2)", census_drift_patrol.py:23-28, stale_claim stale on a missing receipt at :170-171), because the fossil's camouflage is precisely a gate that quietly passed. Condensed: a freshness law without a scheduled writer is a memorial, not a mechanism. Detection without healing converges nothing; healing without detection wastes rebuilds; either without fail-closed verification lies.

## 8. Limits of this analysis

The EOQ transplant and the Karlton attribution are named from general knowledge, not verified to primary sources this session. The uniform-consumption-phase assumption in E[age] = kC/2 ignores burstiness (session boots cluster in work hours), which biases the mean age below kC/2 and pushes k* slightly upward. The k=1 reading of the warm boot infers C from the "session start" docstring (hermes_warm_boot.py:2), not from a measured session histogram. No test suite was run: the ask names no suite and this item banks analysis; the two live gate runs and the Crossref verification in section 0 are the checks executed this ask, and the findstr FOSSIL sweep is the completeness check that the law is new.
