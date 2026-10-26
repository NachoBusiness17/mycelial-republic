# deep-attention-market: a currency for the estate's attention

Banked 2026-09-28, flash50 deep item. Every count and code cite below was read or run in this session. Nothing is copied from memory.

## 1. The measured problem: 9 queues, no common price

The estate's attention is already rationed, but each organ rations itself with a different instrument:

| Organ | Size measured this session | Allocation instrument today |
|---|---|---|
| Driver topics | 5 topics, `configs/research_topics.yaml:11-55` | locked hand priority order, "1 topic/tick, <=2 steals" (`research_topics.yaml:5-6`), frozen since 2026-08-07 |
| Patrol tasks | 8 scheduled tasks (`scripts/register_census_patrol_task.ps1`, `register_corpus_rescan_task.ps1`, `register_day_end_task.ps1`, `register_endpoint_news_task.ps1`, `register_fts_index_task.ps1`, `register_improve_task.ps1`, `register_ratchet_task.ps1`, `register_vision_nightly.ps1`) | fixed cron times, command economy |
| Workflows | 30 gate rows in `memory/workflows/REGISTRY.jsonl` (7 checks G1-G7 each) | submit-time gate, pass/fail, no relative ranking |
| Free lanes / burn waves | 553 numbered B2 lanes in `memory/burns/BURN_WAVE_STATE.json`; holds log records 1302-death clusters at lines 926-976 | dispatcher width caps + holds, landed truth re-derived from disk (the `closed` field: "landed array re-derived from the LANDED RULE ... not self-report") |
| Shared inbox | 1,415 active items over 4,696 events, `watch/inbox/INDEX.json` (shared_inbox.v1, append-only fold, "untrusted_data_until_classified") | manual classification |
| Biography pings | 109 identical "Session record ready" pings, 40,425 chars in `memory/attention.md`; writer truncates at 40,000 (`mag/biography.py:526`), consumers clip to 3,000 (`mag/lanes.py:293`) and 600 (`mag/context_pack.py:620`, tail 400 at :933) | a human triage on 2026-09-28 resolved 127 by hand (triage block in the file itself) |
| Percolator | 1,655 rows in `memory/percolator/explore.jsonl` (wc) | unbounded append |
| Sizing store | 87 rows in `memory/learn/sizing.jsonl`, written by `mag/one_sizer.py:47-59` | mode-vote lookup, no budget |
| Daemon loops | ghost cycle (120s) + autorun loop (5s), both live in `memory/supervisor/state.json` | static timers |

Herbert Simon named this 55 years ago: a wealth of information creates a poverty of attention ("Designing Organizations for an Information-Rich World," 1971). The estate has the wealth: thousands of pending units. It has no price.

## 2. The estate already built the market's parts, separately

None of this is greenfield. Four existing organs are proto-market mechanisms that were never joined:

1. **`mag/attention_ranker.py`** is a central planner with hand-set shadow prices. The score is a fixed linear utility `3*actionability + 2.5*impact + 2*urgency + 1.5*centrality + 1.2*novelty + uncertainty - 1.5*redundancy - wallpaper_cost` normalized to 100 (`attention_ranker.py:89-93`). It already knows the feedback vocabulary of a market, `{"useful", "wallpaper", "pin", "mute", "acted"}` (:17), and already holds the single most important safety property: operator feedback may reorder ordinary items "but cannot hide hard rules" (:250, enforced :234-239).
2. **`mag/run_worth.py`** is a stopping rule with value thresholds (`worth_valuable: 0.55`, `worth_worthless: 0.25`, `run_worth.py:27-34`): it prices whether a long run deserves to keep burning compute.
3. **`mag/one_sizer.py`** learns the cheapest capable tier per (skill, domain, shape) by mode vote over landed rows (`one_sizer.py:62-97`): a learned unit cost.
4. **The intake rubric** (`.agents/skills/agent-harness/SKILL.md:12-16`) scores FIT/PULL/COST/WINDOW/NOVELTY 0-5 each into BUILD NOW / WINDOWED / CALIBRATE / REMEMBER bands. WINDOW ("feeds a starved lane NOW?") is literally a shadow price of scarce capacity; NOVELTY is a redundancy discount the ranker also charges (:90).

The parts are scattered across planner, gate, sizer, and rubric. A market is what you get when you let them trade with each other through one ledger instead of being tuned by hand.

## 3. The currency: RESID, minted only by verified residue

**Unit: the RESID.** Backing is the thing this estate already treats as the only truth: receipt-at-bytes (`.agents/skills/agent-harness/SKILL.md:42-46`: done is a byte fact, "declared on intent = vapor"). A RESID is not backed by operator dollars and not backed by tokens spent; it is backed by downstream consumption of verified work. Spent compute that nobody consumes mints nothing.

**Ledger.** One append-only event log `memory/market/resid_events.jsonl` folded to `memory/market/resid.json`, exactly the Ethereum fold pattern already running in the shared inbox (shared_inbox.v1: "Writers APPEND events; they never rewrite this file or the log", `watch/inbox/INDEX.json`). Event types: MINT, BURN (bid paid for a slot), SLASH (receipt later VOIDed), TRANSFER (must carry a receipt pointer), EXPIRE (demurrage). Nonce discipline per writer, as the inbox already does, and the inbox's own fold_warnings show the failure mode to defend against (observed nonce gaps for writers exp002a and sancho in this session's read).

**Mint rules (the hard part).** Three denominators, because any single one is gameable:

- **Production leg: +1** for a tri-state-labeled finding with a landable receipt (Supported/Disputed/Unproven with evidence attached is already law, `SKILL.md:30-34`).
- **Consumption leg: +1 per distinct consumer per epoch, capped.** A receipt earns again each time it is actually consumed: cited into a context pack, folded into a law or rib, read by a live process (the fossil registry's consumer column is a hand list of exactly this). This is the real backing. It is the academic-citation oracle and it is unforgeable by volume: writing 100 papers nobody cites mints 100 units and nothing more.
- **Wallpaper leg: -1 per operator mute/wallpaper signal** on the emitting organ, wired to the signals `attention_ranker` already collects (`attention_ranker.py:17`).

For judgment-tier claims with no bytes yet (research forecasts), use the estate's own pre-registration habit as a settlement mechanism: mint a small stake at pre-registration, settle the rest on measurement. The SALON_ESS_REPLICATE fold already did this by hand (pre-registration block filed before any generation, per the Q-020 receipt). That is a prediction market in embryo (Hanson's idea futures / futarchy line of work); the market just standardizes it.

**Spend: a generalized second-price slot auction.** The scarce slots are enumerable because they already are: funded-tier sessions (only Hermes is funded, `memory/rib/RIB_DRIVING_LADDER_20260928.md` invariant 1), workflow child width (the burn-wave envelope), patrol wakeups, topic ticks (the "1 topic/tick" bound becomes price-rationed instead of priority-locked). Each window, organs bid RESID for slots; a winner pays at least the bid of the organ it displaced; proceeds are rebated pro rata to all organs. GSP is chosen over full VCG deliberately: the ad-auction literature (Edelman, Ostrovsky, Schwarz, AER 2007) found GSP is what platforms actually run because it is deterministic and simple to audit, and this estate values auditable determinism (verkle chains everywhere) more than full strategy-proofness; VCG is the upgrade if bid manipulation is observed.

**Demurrage: balances halve each epoch** (Gesell's stamped money, 1913). No organ can win windows forever on old glories; the fossil-registry tombstone entries and the dormant jev lane are what hoarding looks like when it is priced at zero. The demurrage rebate is also the funding source for the next rule.

**Explore floor: 15% of every window is not for sale**, allocated UCB-style to high-uncertainty, low-balance organs (Auer et al. 2002). Without a forced exploration band the market is a rich-get-richer ratchet and percolator-class work (which produces nothing consumable for weeks) starves permanently.

**Two liquidity classes, encoding the driving ladder.** Sensing organs (free lanes) earn sensing-RESID and bid only on sensing slots; funded credits convert to judgment-RESID at an operator-set rate. This turns the rib's invariant 2, "sensing may feed judgment, but sensing is never substituted for it," from a rule a seat can forget (three operator corrections minted that rib) into a liquidity constraint the ledger enforces. Cheap-talk theory (Crawford and Sobel 1982) says uncosted signals are ignored; the ladder plus the ledger is how talk gets a cost.

## 4. What prevents gaming

1. **No Sybils: identity is a registry.** Organs are already enumerated in configs (`research_topics.yaml`, the 8 `register_*.ps1` scripts, `REGISTRY.jsonl`, `fossil_registry.json`). Admission follows the existing named-consumer law (`configs/fossil_registry.json:19`: "revive condition = named consumer first"). An unregistered process cannot open a treasury, so the Sybil attack surface is the config commit, which is reviewed.
2. **No self-minting: verification is exogenous.** Every MINT row names the verifier that passed: a mechanical check (pytest green, hash exists, chain tip) or a second-seat cross-sign, the same cross-sign law VOID nominations already use. An organ never grades its own paper. This is the single load-bearing anti-gaming rule; everything else is secondary.
3. **No citation cascades by construction.** The citation-cascade law already exists in prose (`SKILL.md:33-34`: a label that never survives its own fold is a violation). The consumption leg is that law with teeth: an unfunded citation mints nothing for the cited organ unless the citing artifact itself lands verified bytes.
4. **Goodhart's law is answered with denominators, not hope.** Campbell (1979) and Goodhart (1975): any single proxy collapses under optimization pressure; this is the ML specification-gaming census (Krakovna et al., DeepMind 2020) with real compute attached. Production-only farming dies at the consumption leg; consumption farming dies at the wallpaper leg and the distinct-consumer cap; both die at demurrage, which forces re-earning rather than hoarding.
5. **No blind collusion.** TRANSFER must reference a receipt and is public in the fold; the writer rejects pointerless transfers. Trading RESID for favors leaves an audit trail, which is the most a ledger can do and is more than the current system does.
6. **Validator capture is detectable.** The mint row records which verifier paid out; a verifier that mints too easily shows up as an outlier yield and gets the burn-ledger treatment this estate already gives doctrines: named falsifier, operator-gated enforcement.
7. **The rich-get-richer ratchet is bounded by demurrage plus the explore floor**, and hard rules stay outside the market entirely (next section), so no bid can buy silence on a blocker.

## 5. Comparison with the fossil-check approach

Ran it this session: `.venv/Scripts/python.exe tools/fossil_check.py check` returned `0 WARN, 0 HARD, 0 recompiled, 6 registered` (compile_report 3h/168h bar, SEATS.md 42h/168h, jev trail 220h/720h watch, two tombstones at 570h).

Fossil-check (`tools/fossil_check.py`, law at `configs/fossil_registry.json:3`) and a market regulate the same disease, artifact rot in live feeds, with opposite philosophies:

| Dimension | fossil-check | attention market |
|---|---|---|
| Object regulated | time since last write (mtime bars, `fossil_check.py:78`) | value produced and consumed |
| Coverage | 6 hand-registered artifacts; adding one is a named config edit (`fossil_check.py:7-9`) | every receipt in the estate, admitted by the existing event fold |
| Enforcement | WARN-only, fail-open by law ("a broken check never blinds the patrol", `fossil_check.py:14`) | economic: an unfunded organ stops winning slots; safety floors stay outside the market |
| Incentive | none: you can pass forever with a fresh mtime on worthless output | aligned: value is consumption, not freshness |
| Failure mode | the registry itself fossilizes: 6 entries against thousands of artifacts, each bar_hours a hand-set guess; the FKB re-baseline (Q-028: 17 to 1,421 signatures because the registry had never been rebuilt) shows hand-set schedules drift | Goodhart pressure on the mint denominators; mitigated in section 4 |
| Relative ranking | none: cannot say which of 9 organs deserves the next funded hour | that is the entire output |

The honest verdict: **fossil-check is the ground floor of the same building, and the market is the floors above it.** Fossil-check answers "is this named safety-relevant artifact stale?" which is a blocker-class question; the market answers "who gets the next discretionary hour of funded compute?" which is the allocation question fossil-check was never designed for. The composition is already shaped by the ranker's precedent: hard bands cannot be outbid (`attention_ranker.py:234-239,250`), so fossil bars, gate failures, and probe alarms stay command-economy P0/P1 items, and only the discretionary capacity above them is priced. What the market retires is not fossil-check but the hand maintenance of the registry: the consumer column becomes an observation (who actually consumed it this epoch) instead of a declaration, and a tombstone becomes what it economically is, an organ with zero mint rate, discovered rather than decreed.

Concrete proof the market pays for itself on day one: the 109 identical biography pings (40,425 chars) that a human spent a triage block resolving on 2026-09-28 are exactly what a market prices out automatically. The biography organ paid zero to prepend into every boot feed and earned zero consumption (`mag/context_pack.py:620` keeps 600 chars; the pings scroll past it), which is the market definition of wallpaper, caught without a human. Coase (1937) says organs exist while internal transaction beats market cost; the market makes the Coasean test continuous instead of archaeological.

## 6. What the literature pins down (and where this design deviates)

- **Hayek (1945), "The Use of Knowledge in Society":** the case for prices here is not ideology, it is information location. The knowledge of which lane is worth running is scattered across `logs/run_worth.jsonl`, `memory/learn/sizing.jsonl`, the burn ledgers, and the sizing store; today no mechanism aggregates them, so a human dispatcher guesses (the width-24 experiment in `BURN_WAVE_STATE.json` was exactly such a guess, and it cost 8 surfaced 1302 deaths to learn). The bid is the aggregation.
- **VCG (Vickrey 1961, Clarke 1971, Groves 1973) vs GSP (Edelman-Ostrovsky-Schwarz 2007):** truthfulness vs auditability; chosen GSP first for the reason above.
- **Quadratic funding (Buterin, Hitzig, Weyl 2019):** patrol tasks are public goods; the FTS index serves every seat but is biddable by none. Reserve a matching pool (a slice of the operator's funded quota) that matches sqrt of distinct-consumer valuation, which is the consumption leg with square-root aggregation. This is the market's answer for the organs pure bidding starves.
- **Harberger self-assessment (Posner and Weyl, JPE 2017):** the alternative to demurrage, each organ self-assesses a standing valuation and pays tax on it. Rejected as primary here because the estate's organs are few and the always-for-sale property (a competitor can buy your slot at your self-assessed price) has no clean analog for compute slots; kept as an option for the artifact registry only.
- **Peer prediction (Miller, Resnick, Zeckhauser 2005; Prelec's Bayesian Truth Serum, Science 2004):** relevant only where no bytes exist; the estate's advantage is that most value is mechanically verifiable, so peer-prediction payouts are the minority path, reserved for judgment-forecast settlement.
- **Bandits (Thompson 1933; Auer et al. 2002):** the explore floor is UCB; `run_worth` is the matching stopping rule; together they bound the two classic bandit failure modes (never explore, never stop).
- **Simon (1971), Coase (1937), Gesell (1913), Goodhart (1975), Campbell (1979):** named where used above.

## 7. Staging (deliberate-ask shaped, nothing deploys without an operator GO)

- **Stage 0, instrumentation only:** backfill mints from ledgers that already exist on disk (burn LEDGER rows, REGISTRY PASS rows, sizing rows, percolator closes). Output: one table, RESID per funded token per organ over the last 30 days. This is pure measurement; it would have answered the width-envelope questions the burn wave answered by experiment.
- **Stage 1, shadow market:** compute the auction advice-only for one weekly window; report divergence between what the market would have funded and what actually ran. Divergence is the falsifiable claim: if the market's picks do no better on downstream consumption, the whole thesis dies there.
- **Stage 2, gate one lane:** only the flash-window dispatcher (the B2 pattern) switches to bids. Patrols, gates, and hard bands stay cron and command. The operator remains the central bank: mint denominators, the sensing-to-judgment exchange rate, and the explore fraction are operator-set, which is the existing law that only operator gates defer (`SKILL.md:24`).

## 8. Falsifiers (in estate style, named up front)

- If Stage 1 shadow picks match the human dispatchers' picks more than ~80% of the time, the market is decorative; keep the ledgers, drop the auction.
- If consumption-leg mints concentrate in more than half of all mints on a single consumer class (for example context packs alone), the backing is circular and the denominators need reweighting.
- If an organ sustains a positive treasury across three epochs with zero operator `useful` signals, the wallpaper leg has failed and the mint denominators are being farmed.

The deepest point, stated plainly: the estate already ran this experiment in prose. `AGENTS.md` carries hand-written rationing laws (tier ladder superseded by driving ladder, max-concurrency standing law, pile habit), each one a price the operator set by hand after a failure. A market is that law list made continuous, self-updating, and honest about its own denominators. Fossil-check watches six artifacts for rot; the market watches all of them, and pays the watchers in the only coin that cannot be counterfeited: being read.
