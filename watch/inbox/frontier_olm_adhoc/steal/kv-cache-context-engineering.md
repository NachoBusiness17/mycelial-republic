# STEAL CARD: kv-cache-context-engineering (frontier_olm_adhoc) - rev 3

source-fetched: adhoc · seat: steal-kv-cache-context-engineering · moment: 2026-10-11 · rev 3
(round-2 critique applied the evening of 2026-10-11; rev-3 ledger block below)
Inputs: 2 confirmed finds from the 2026-10-10/11 adhoc sweeps, delivered by the round-1
ask. Source docs read in full at the rev-2 sitting; REV 3 RE-ANCHOR (both cited paths
were replaced at the same path by sibling sittings between the rev-2 landing and the
evening - details in the rev-3 ledger): RR-Evict now cites
watch/inbox/frontier_olm_adhoc/sweep/kv-cache-context-engineering-arxiv.prior-2026-10-10.md
(item 1 at :40-53, re-verified rev 3) and Slow Vale cites the retained raw captures
sweep/_kv_thread_1x0ms0m.xml + sweep/_read_town800_agents.txt (numbers at :11, :83,
:86, re-verified rev 3); the standing prose bank remains
watch/inbox/frontier_olm_2026-10-09/sweep/kv-cache-context-engineering-reddit.md:26-31.

## Revision ledger (round-2 critique -> this rev)

Round 1 claimed both finds "genuinely new". FALSE on both: the estate banked them at
sweep layer days ago, and the round-1 overlap check ran on surfaces that provably
cannot see those banks (catalog/catalog.jsonl + memory/ only; the run dirs are
untracked and unindexed). This rev:
1. Rewrites the overlap verdict with the prior banks cited by path:line and reframes
   the card as the steal-layer distillation of already-banked finds, naming the true
   increments.
2. Corrects the telemetry best-day claim (round 1 said "best day 93.0% (2026-09-30)";
   the file's best is 99.29% on 2026-08-17; 09-30 is only the best of the recent
   window). Method, filter, and calls-vs-rows stated below.
3. Fixes the stale capture citation: models/providers.py:412-416 is the offpeak defer
   block today; the cache capture lives at :558-570 and :847-868. The stale range in
   memory/research_polished/kv_cache_compaction.md:11 and :21 was corrected this
   session (both edits landed).
4. Lands the card JSON next to this .md per the prior-run pattern (watch/inbox/
   frontier_olm_2026-10-08/steal/kv-cache-context-engineering.json is the shape).
5. Records the standing overlap-surface law below.

## Revision ledger (round-2 critique of the combined file -> rev 3, 2026-10-11 evening)

The round-2 verifier withheld approval on three counts plus three should-fixes; every
one applied this sitting, each verified first-hand before the edit:
1. DANGLING PRIMARY-SOURCE ANCHORS (the blocking one): both adhoc sweep files this
   card cited were replaced at the same path AFTER rev 2 landed. The arxiv sweep's
   own header reads "Supersedes the 2026-10-10 mint of this path (preserved verbatim
   as kv-cache-context-engineering-arxiv.prior-2026-10-10.md, cp this sitting)" -
   the RR-Evict item this card cited at :40-53 now lives in that .prior file
   (verified: prior :40-53 carries the item, quotes intact). The reddit sweep was
   REPLACED at 17:00 with NO prior preserved (its header: "This file REPLACES the
   05:33Z sibling card at the same path"), and the current file carries zero Slow
   Vale / 1x0ms0m content (grep-verified). All adhoc-reddit Slow Vale cites below
   are re-anchored to the retained raw captures (_kv_thread_1x0ms0m.xml; render
   _read_town800_agents.txt :11/:83/:86, all numbers verbatim: 99.9%-resolved,
   ~1,490 extra calls on ~160k decisions = 0.9% call-count overhead,
   Prometheus-checked, daily-summary pass, sub-30-minute gaps). The citation lint
   cannot catch this class (paths exist, line ranges in-EOF); only a content
   re-read can - which is why the standing law below gains the rev 3 clause.
2. TRUE INCREMENT (1) re-scoped: the 10-10 swarm re-bank this card itself cites
   already carries the quantified validation lane verbatim at
   watch/inbox/frontier_olm_2026-10-10/sweep/swarm-orchestration-reddit.md:29
   ("160k completed decisions/day with ~1,450 validation failures and ~1,490
   retry calls (0.9% call-count overhead)") and :34 (Q2: "over 99.9% of cases...
   at 0.9% call overhead"), both verified rev 3. The genuinely unbanked residue
   is only the Prometheus-checked attribution and the daily-summary
   scheduled-compaction cadence; reworded in the Overlap verdict below.
3. 2609.28870 is banked entry 7 of the 09-28 list, not entry 6 (entry 6 is KVSET
   2609.27746; verified at the list itself, :110-111). Both mentions fixed.
4. SHOULD-FIXES taken: the seventh sweep item (1wom3fe) is stolen in card B rev 2
   (the expert-layer eviction twin of this card's rr_tail race); the standing law
   below gains the preserve-.prior-on-replacement clause; the telemetry counting
   rule is now named (the rev-2 figures 851 and 721 reproduce exactly under the
   family+ok rule) with the rev-3 recount stamped into probe 2.
The companion JSON (kv-cache-context-engineering.json) remains the rev-2 submission
record; this .md is the living card at rev 3.

## Standing-law defect this card exposes (the root cause)

Frontier overlap checks that grep only catalog/catalog.jsonl + memory/ are blind to
the estate's real frontier prose: the frontier_olm_* run dirs (untracked, not
catalog-indexed; the only catalog hits for frontier_olm_20260928 are pytest-tmp
fixture copies). The working dedup surface is the sibling runs themselves,
cross-cited by path:line. This is at least the second run in the family to re-bank a
known find. STANDING FIX: every frontier overlap check greps
watch/inbox/frontier_olm_* AND watch/inbox/frontier_olm_adhoc in addition to
catalog + memory/. REV 3 CLAUSE (2026-10-11: today's replacement events proved the
law insufficient - grepping the run dirs is necessary but not enough, because the
run dirs are NOT append-only): any sweep seat that replaces a file at the same
path MUST preserve the superseded bytes as a .prior-<date> sibling (the arxiv seat
did this by its own cp; the reddit seat did not, and its prior survives only as a
catalog mtime line), and cites into a replaced file must be re-anchored to the
.prior or the raw capture at the moment of replacement, not left to dangle.
(Recorded here for the next sweep; wiring it into the sweep skill
cards is an operator/lane call, not this card's.)

## The steal (one mechanism, not a link dump - DISTILLATION LAYER)

Both finds are already banked at sweep layer (see Overlap). What this card adds is
the distilled mechanism with the two banks cross-merged, plus the estate-side race
neither bank ran:

1. Slow Vale, 800+ persistent agents (thread 1x0ms0m): 90%+ cache hit at ~30k mean
   context, 300-400 calls per agent per day, ~5B tokens/day under US$100, won by
   request architecture: stable instructions + reusable history at the frozen front,
   state-dependent action options at the tail; dynamic tool schemas kept OUT of the
   prefix ("Changing the schema prevented the otherwise stable context after it from
   hitting the cache"), replaced by plain-text JSON + backend validation resolving
   99.9% of malformed outputs at ~0.9% call-count overhead (1,490 extra calls on
   160k decisions, Prometheus-checked; raw render _read_town800_agents.txt :86,
   re-anchored rev 3). Cadence law: daily
   per-character summaries plus sub-30-minute call gaps keep the retention window
   warm; compaction is scheduled, never exhaustion-triggered. The 10-09 bank
   (frontier_olm_2026-10-09/sweep/kv-cache-context-engineering-reddit.md:26-31) adds
   the price of materialize-once-vs-reprefill the adhoc sweep did not carry:
   llama-server per-slot KV save/restore is "98 s of prefill vs 67 ms to restore"
   for a 27k-token CPU prefix.
2. RR-Evict (arXiv 2609.32278): LRU's recency-synchronization failure - one agent
   turn refreshes all its cached prefix nodes together, so LRU concentrates eviction
   on a few idle agents' whole histories and the returning agent recomputes nearly
   everything (the P99 TTFT outlier). Fix: round-robin tail-chunk eviction (1,024-
   token chunks) across idle trajectories; no arrival or tool-latency prediction.
   Measured vs LRU: "reduces P99 TTFT by up to 75.4% and P99 uncached prompt tokens
   by up to 65.7%"; 60.5%/56.2% vs LRU+completion signals on coding agents; PD-
   disaggregated 60.7%/60.8%; useful regime na < m < n; limits: short idle intervals,
   HBM only. SGLang on H100, Qwen3-Coder-30B-A3B + Qwen3-8B, tau2-bank (222
   trajectories) + SWE-bench. (Mechanism details beyond the adhoc sweep doc are the
   09-28 bank's, at frontier_olm_20260928/sweep/kv-cache-context-engineering-arxiv.md:80.)

The estate-side move neither bank contains: race round-robin tail eviction against
the estate's own LRU null arm at real pack budgets (the probe below).

## What the estate already has (self-steal check, verified this session)

- freeze_system_prompt + evolving_tail: mag/context_pack.py:948-1021. First call per
  session captures the bytes (system text + canonical tool schemas hashed together,
  :970-984); later calls return the SAME bytes even if inputs drifted, drift belongs
  in the tail (docstring :957-959); a mid-session schema change is either served
  stale or forces refreeze = full-prefix miss (:960-961). ReFold port P5 stamps at
  :39-40 and :1533-1537. Wired live at mag/agent_cli.py:1061-1066; tested by
  tests/test_context_freeze.py.
- The G1 gap law + LRU null arm: any eviction/compaction claim must beat the LRU
  null or it is decoration (tools/lru_null_arm.py:1-17, citing
  memory/research_polished/kv_cache_compaction.md). Instrument:
  tools/prefix_cache_sim.py (sessions keyed by lane+actor, 30-min gap, :73-75 and
  :102-104); banked run memory/runs/lru_null_arm/lru_null_arm_results.json
  (generated 2026-10-04T01:43:42Z, read as artifact this session, NOT rerun): 5000
  rows, 1328 sessions, frozen_append 0.9387 hit at the 8192-block anchor = the
  unbounded ceiling; at the real 1x pack budget (4800 chars) 0.5054; 4x 0.9336.
- rr_tail does NOT exist anywhere: repo-wide rg for "rr_tail" this session returned
  only stderr_tail/stdout_tail substring noise (mag/bash_local.py:241,
  mag/codex_seat.py:135, mag/coding_session_loop.py:201, mag/cooker.py:149,
  mag/roadmap_runner.py:223, mag/seat_probe.py:62, mag/_codex_seat.py:76,
  tools/nightcrew.py:154). The race is genuinely unrun.
- Cache capture wiring (corrected): models/providers.py:558-570 (DeepSeek top-level
  prompt_cache_hit/miss + OpenAI-compat prompt_tokens_details.cached_tokens ->
  record_usage) and the second call site :847-868. The old :412-416 range is the
  offpeak defer block today (read this session). kv_cache_compaction.md:11 and :21
  corrected this session to the real ranges.

## Estate organ map (each find to the organ it feeds, concrete port move)

- Slow Vale -> the context pack organ: mag/context_pack.py:948-1021
  (freeze_system_prompt/evolving_tail) + mag/skills_pack.py:232-268 (skills_for_job:
  config-driven excerpts, stable by construction) + mag/claritas.py:15-52 (vendor
  faces leading the frozen front). PORT MOVES:
  (a) Schema-placement law: only session-stable schemas may enter the frozen block;
      dynamic (MCP-style) schemas render in the evolving tail or become plain-text
      contracts with backend validation (the town's 99.9%-at-0.9% lane). The freeze
      mechanism already pins first-seen schemas into the hash (mag/context_pack.py:
      970-984), so the port is an audit + law, not new machinery.
  (b) Cadence leg: pack builds are cadence-clean (measured below) but provider CALLS
      run 2-3 orders thinner than the town's per-agent rate on quiet days and hit%
      tracks it (measured below). Port: a scheduled same-frozen-prefix warm-keeper
      inside the 30-min window on thin days, priced against the ~50x flash hit/miss
      ratio (kv_cache_compaction.md finding 1).
  (c) Hermes relay compaction lane (the long-session stall class whose
      overflow_reason upstream just bounded, commit f06008308): scheduled summaries
      on the town's daily cadence, not exhaustion-triggered repacks. The 10-09
      bank's 98s-vs-67ms restore number prices the warm-boot side of the same lane.
- RR-Evict -> gopher fleet eviction policy, via the estate's own null-arm instrument
  (tools/prefix_cache_sim.py + tools/lru_null_arm.py). The estate's replay already
  shows the target regime: 1328 interleaved sessions in 5000 rows is genuinely
  multi-agent, and at the real 1x pack budget LRU loses 43 points to eviction
  (0.5054 vs 0.9387 unbounded). PORT: add an rr_tail arm (visit sessions
  round-robin, evict a 1,024-char-class small tail chunk per idle trajectory) and
  race it against the frozen_append LRU null at 1x/2x/4x pack; if it wins, the same
  rotation ports to the relay overflow decision (whose history truncates when the
  window fills: rotate tail chunks, never LRU-drop a whole agent).

Honest tension, carried: the sibling find "When Fancy Eviction Fails" (arXiv
2609.28870, ALSO already banked: 09-28 banked entry 7, same list at
watch/inbox/frontier_olm_20260928/sweep/kv-cache-context-engineering-arxiv.md:105-112,
and reconfirmed by the 10-01 sibling
:20) measured on 20B+ production tokens that recency is unusually predictive and
LRU is a robust baseline. Our own telemetry agrees at volume (99.29% on the
851-call 08-17 day). Our trace is bimodal - bursty-warm on heavy days, thin-cold on
quiet ones - which is exactly why the probe races RR vs LRU on OUR trails instead
of trusting either paper.

## Probes RUN this session (receipts, not claims; both re-run for rev 2)

1. Pack-build cadence read (the town's retention-window law vs the pack lane).
   Command: ./.venv/Scripts/python.exe over watch/inbox/PACK_OFFLOAD.jsonl.
   Result: 35,975 lines total = 35,436 v1 + 538 v2 + 1 bad line (line 13500,
   non-UTF-8 0x80 byte; the sibling finetuning card's "13499" is the same tear
   0-indexed). v1-only gap series n=35,435, span 2026-09-28T07:12Z .. 2026-10-09T
   00:18Z: median 0 s; p99 = 1007 s (nearest-rank) / 991 s (linear interpolation)
   - round 1's "993 s" was a truncated-index nearest-rank, same ~16-17 min band;
   35,276/35,435 = 99.55% of gaps under the town's 30-min threshold; exactly 2 gaps
   over 4 h. The pack lane is cadence-clean. root_short is a tip-root
   (mag/context_pack.py:56-57), NOT a session id, so this ledger cannot key
   per-agent eviction traces; the trails tapes remain the session-keyed instrument.
2. Live provider hit-rate read (corrected; COUNTING RULE NAMED at rev 3 after the
   round-2 verifier's rerun diverged on the calls figures while the token masses
   matched exactly). Command: ./.venv/Scripts/python.exe
   aggregating cache_hit_tokens/cache_miss_tokens in logs/provider_usage.jsonl
   (rev 2 sat on 77,780 rows / 62 cache-days, last 2026-10-10; rev 3 recount, run
   this sitting: 77,800 rows / 63 cache-days, first 2026-08-04, last 2026-10-11 -
   one more day landed between sittings, census-denominator law applies).
   Definitions named: a "cache row" carries
   numeric cache_hit_tokens+cache_miss_tokens; "calls" = cache rows on the
   deepseek*/glm* families with ok=True, each such row calls=1 (the rev-2 shape
   "sums the row calls field over rows-with-cache" was under-specified: at the
   rev-3 recount 2026-08-17 reads 981 under all-cache-rows but 851 under
   family+ok - the rev-2 figure; 2026-09-30 reads 729 all-cache / 728
   family-any-ok / 721 family+ok - the rev-2 figure; the days' hit/miss token
   masses are identical under every rule, so the hit-rate claims are
   rule-invariant). 63 days carry
   cache fields at the rev-3 moment (first 2026-08-04, last 2026-10-11) across 46+ model ids,
   mass concentrated on deepseek-family + glm. Best days overall: 2026-08-17 99.29%
   (67,668,864 hit / 480,585 miss; 851 calls; deepseek-r1:1.5b + deepseek-v4-flash/
   pro), 2026-08-30 98.52% (2,567 calls), 2026-08-10 98.31% (1,010 calls). Recent
   window (>=2026-09-28) best: 2026-09-30 93.00% (3,409,068 / 256,661; 721 rows =
   721 calls; deepseek-v4-flash + glm-4.5-flash) - round 1 wrongly called this the
   file's best because its script only printed the last 12 days. Worst recent:
   2026-10-08 and 10-09 at 0.0% on single calls; 10-10 34.58% (46 calls).
   Conclusion unchanged and strengthened: the estate's ceiling sits ABOVE the
   town's 90%+ (99.29% touched); the failure is HOLDING it across quiet days.
3. Banked null-arm artifact read (read, NOT rerun this session):
   memory/runs/lru_null_arm/lru_null_arm_results.json, generated 2026-10-04T01:43Z -
   the 1x-pack 0.5054 vs unbounded 0.9387 eviction gap the RR probe targets.

## The falsifiable probe for this week (cheap, decisive)

RR-tail arm race on the estate's own trails. Add one eviction arm to
tools/prefix_cache_sim.py (sessions visited round-robin, a small tail chunk evicted
per idle trajectory, all else identical), then rerun tools/lru_null_arm.py with the
grid pinned at 1x/2x/4x/8x the 4800-char pack budget over the same trails
(deterministic, minutes, $0 - instrument, traces, and null arm all exist; the arm
itself is grep-verified absent). FALSIFIER: if rr_tail's hit_rate beats the
frozen_append LRU null by under 2 pp at 1x-2x pack, RR-Evict does NOT transfer to
our trace shape and the eviction steal closes as not-our-failure-mode (capacity
stays the lever, agreeing with the banked 2609.28870); if it recovers 10 pp or more
of the measured 43-point 1x-pack gap, port round-robin tail truncation into the
relay overflow decision and bank the win against the G1 law. Either outcome is
decisive.

## OWED (never asserted as done)

- The rr_tail arm was NOT implemented or run this session (mapping + probe design
  only; absence grep-verified); the 0.5054-vs-0.9387 numbers are the 2026-10-04
  banked artifact, not a fresh run, and the null arm itself was not rerun.
- The schema-placement audit (which tool schemas are session-stable vs dynamic in
  the live request stream) did not run; no evidence yet that estate frozen prefixes
  carry dynamic schema bytes, only that the mechanism would pin them if they did.
- The plain-text-JSON + backend-validation lane is mapped, not ported.
- Both finds' external pages were not re-fetched this session; quotes are the sweep
  seats' verbatim captures (raw XML retained in the sweep directories).
- Hermes relay internals live in the external hermes-agent repo; overflow_reason
  was verified only through commit f06008308's message, not relay code.
- The standing overlap-surface fix is recorded here but NOT wired into the sweep
  skill cards or any gate; that is an operator/lane decision.

## Overlap verdict (corrected this rev; round 1's "genuinely new" was false)

- RR-Evict (arXiv 2609.32278): BANKED 2026-09-28 by
  watch/inbox/frontier_olm_20260928/sweep/kv-cache-context-engineering-arxiv.md:32
  (candidate table, marked "(banked)"), :80 (deep-read mechanism, MORE detailed
  than the adhoc sweep: 1,024-token chunks, tau2-bank 222 trajectories,
  Qwen3-Coder-30B-A3B + Qwen3-8B, analytic regime), :105-106 (banked entry, same
  75.4%/65.7% quote). Reconfirmed NOT-rebanked by the 10-01 sibling
  (watch/inbox/frontier_olm_2026-10-01/sweep/kv-cache-context-engineering-arxiv.md:20,
  "Already BANKED") and listed as banked 2026-09-28 by the 10-10 census
  (watch/inbox/frontier_olm_2026-10-10/sweep/kv-cache-context-arxiv.md:27).
- Slow Vale (thread 1x0ms0m): BANKED 2026-10-09 by
  watch/inbox/frontier_olm_2026-10-09/sweep/kv-cache-context-engineering-reddit.md:
  26-31 (item 1: same load-bearing quote verbatim, same 800+/300-400/~30k/5B/US$100/
  90%+ numbers, same schema-churn and plain-JSON laws, PLUS the 98s-vs-67ms restore
  number), and banked AGAIN 2026-10-10 by the swarm-orchestration lane
  (watch/inbox/frontier_olm_2026-10-10/sweep/swarm-orchestration-reddit.md:25 URL,
  :27 "The single strongest find; answers Q1, Q2, Q3, Q5 at once") - itself a
  re-bank the estate never consolidated.
- The tension sibling 2609.28870: banked 09-28 (entry 7 of the same banked list,
  :105-112) and reconfirmed by 10-01 :20.
- TRUE INCREMENTS of this card over the prior banks (rev 3 re-scope: judged
  against the FULL prior set, the 10-09 bank AND the 10-10 swarm re-bank this
  card cites): (1) only the Prometheus-checked attribution and the
  daily-summary scheduled-compaction cadence - the lane's numbers themselves
  (99.9% at 0.9% overhead, ~1,490/160k) are already banked at
  watch/inbox/frontier_olm_2026-10-10/sweep/swarm-orchestration-reddit.md:29 and
  :34, so the rev-2 wording claiming them as carried "not by the 10-09 bank" was
  true-but-misleading by omission; (2) the rr_tail race + falsifier on the estate's
  own instrument (grep-verified absent everywhere); (3) the organ map and the
  measured estate probes (telemetry ceiling corrected to 99.29%, pack cadence
  99.55%); (4) the overlap-surface standing law. Everything else in this card is
  distillation of the cited banks.

---

# STEAL CARD B: kv-cache-context-engineering, reddit pass-2 batch (six finds + the
seventh item stolen at rev 2) - rev 2

source-fetched: adhoc - seat: steal-kv-cache-context-engineering - moment: 2026-10-11
(evening sitting) - rev 2 (round-2 critique applied: the seventh sweep item 1wom3fe
stolen below, card A re-anchored to rev 3, the telemetry counting rule named; every
critique item verified first-hand before editing - receipt).

FILE STATUS: appended below card A, now at REV 3 (its rev-3 ledger records the
sweep-replacement re-anchors: the arxiv prior preserved at
kv-cache-context-engineering-arxiv.prior-2026-10-10.md, the reddit sweep replaced
with no prior, Slow Vale re-anchored to the raw captures). The sibling cite into
this file (steal/inference-efficiency.md:71-72 at :36-40) still lands on card A's
standing-law paragraph, unchanged in substance plus its rev 3 preserve-.prior
clause. This card covers the six reddit finds of the sweep's second pass PLUS the
seventh item (1wom3fe) the round-2 verifier caught both cards dropping. Its JSON
banks as kv-cache-context-engineering.reddit2.json so card A's rev-2
submission-record JSON at kv-cache-context-engineering.json survives.

## Provenance (nothing fabricated)

Six confirmed finds arrived in the round-1 ask, all source=reddit. All six are
banked at SWEEP layer by watch/inbox/frontier_olm_adhoc/sweep/
kv-cache-context-engineering-reddit.md (the second-pass sweep card; items at
:36-69), raw thread XML retained as sweep/_kvr2_thread_*.xml and rendered reads
as sweep/_kvr2_read_*.txt. This session re-verified every load-bearing number
directly in those raw renders (Receipt); reddit.com itself was not fetched (the
sweep records all three JSON doors walled and the RSS fallback, sweep :5-8).
This card is the steal-layer distillation the sweep bank does not carry: the
per-organ port map, the estate-side gaps each steal exposes, and the probes.

## Overlap (run this session, not inherited)

- Catalog dedup: grep over catalog/catalog.jsonl for all six thread ids
  (1wromzr, 1wlss89, 1wl5hfk, 1whf345, 1wjhk0r, 1wkyny9) returned 0 rows
  (command in Receipt). Matches the sweep's per-item receipts (sweep :39, :49,
  :54, :59, :64, :69).
- Find 1 (1wromzr) is an AMENDMENT, not a new bank: the OP's quant-regime
  logit-penalty table was prior-banked 2026-10-03 at
  watch/inbox/frontier_olm_2026-10-03/sweep/quantization-and-compression-reddit.md:24
  (path corrected this session: the ask's overlap field named the basename
  without its sweep/ segment; line 24 verified first-hand - it carries the full
  BF16 74->84 through Q2_K 12->24 table plus the --logit-bias deprecation
  caveat). This card banks only the comment-layer study that bank
  lacks: the 2.2M-token judge study and the effort-control-without-KV-recompute
  point.
- Find 4 (1whf345) fires a title-only debt: listed unread at the 10-03 kv sweep
  :44 per the ask's overlap field and sweep :59 (that file not re-read here).
- Card A's standing overlap-surface law (:36-40) was honored: the dedup grep
  covers the adhoc run dir where the bank actually lives.

## The six steals, their organs, and the port moves

### 1. Judge-regime dependence, now MEASURED on real agent thinking (1wromzr) -> PERCOLATOR + the marker-penalty arm

Mechanism (raw-verified, sweep/_kvr2_read_1wromzr.txt): u/eightone-81 mined 85
real agent sessions (6,851 thinking blocks, ~8.85M chars = ~2.2M tokens after
fork-dedupe; median block ~500 chars because agent thinking lands in small
chunks between tool calls; :364) of Qwen3.8-Flash-Next W4A16 on vLLM. Only 3
marker families survive contact with agent work - hmm (1,739 uses), wait
(2,888), actually (2,423) - with a ceiling of 1.6-7% of thinking tokens = 1-4%
of all generated tokens, and accuracy NOT measured (:354, :358). The two judges
(model self-judge vs a 35B judge) agree on useful/wasted/ordinary only 61% of
the time (:375); the self-judge calls 8% of hesitations wasted where the 35B
judge says 37% (:376); both-agree waste is ~12%, honest range 12-37% (:378).
The 35B judged ~33% of long thinking blocks skippable, ~48% in blocks with 5+
hesitation markers, 68% of those looping (:371). Constraint: vLLM rejects
logit_bias under speculative decoding (issue #42744, sweep :37). And
u/AlabamaResearcher's point (sweep :37): per-request logit-bias is a
reasoning-effort control that does NOT force the KV recompute a mid-session
template change causes - the steering knob lives at the sampler, prefix bytes
untouched.

Estate side: the estate ALREADY BUILT the cheap leg. mag/marker_penalty.py
(profile loader :41-64, penalty_logit_bias :67-85, RATIO lineage docstring
:1-15) wired into mag/llama_cpp_bridge.py:199-208 (with a profile armed the
only payload delta is the logit_bias key; default-behavior law at :43-49), OFF
by default with the measure-before-trusting law in
configs/marker_penalty_profile.json ("law" field).

PORT MOVES:
(a) Percolator invariant candidate (the true steal): NO SINGLE-JUDGE WASTE
    GATE - any waste/verdict metric that gates fleet behavior needs a second
    judge arm plus a reported agreement score first. This extends the fold's
    refusal-regime law (corpus/steal/CORPUS_FOLD_FRONTIER_OLM_20261001.md:9:
    keyword refusal 98.0 -> 80.5 under KV cache compression at McNemar p~1e-8
    while classifier refusal held 99.0-99.5) into the waste domain with a
    measured instance: 61% agreement, 8%-vs-37% judge spread. Three
    independent instances across two judgment domains (keyword-vs-classifier
    refusal, lexical-vs-semantic phantom-kv, self-vs-35B waste).
(b) marker_penalty profile v2 arm: cut the shipped marker set toward the 3
    agent-validated families, carrying the honest ceiling (1.6-7% of thinking,
    accuracy unmeasured) and the specdec incompatibility note in the profile's
    own metadata. No code change - it is a new profile JSON consumed by the
    existing loader.
(c) Pack law: thinking-effort steering belongs in per-request sampler knobs,
    never mid-session template edits (which flip the frozen-prefix hash and
    re-pay the full miss; mag/context_pack.py:955-962 - drift belongs in the
    evolving tail, either half changing flips the hash).

### 2. Compaction x quantization x KV-precision, plus the first-action gate (1wlss89) -> CONTEXT PACK

Mechanism (raw-verified, sweep/_kvr2_read_1wlss89.txt): OP's postulate -
quantization error propagates across context size (:4), so 128k + compaction
can beat raw 256k/1M on Q4-class models; the chart assumed 8-bit KV and "if
the KV-cache is 4-bit the degradation is much faster than illustrated"
(u/audioen :26); in-thread counter-evidence says degradation may be
context-length per se (~50% of max context rule of thumb, :13). u/audioen
names what OpenCode compaction actually drops: "the compaction step itself is
a full context rewrite. My guess is that reasoning is removed and model only
sees tool calls, tool call results, and assistant and user messages" (:47).
u/Marcus_MSC's scoring rule (:51): inspect the FIRST action after compaction -
does the summary still name the requested files, constraints, and unfinished
work - because a dropped "don't modify this file" instruction makes the
shorter run look coherent while failing the task.

Estate side: the sweep seat fired the reach-ratio probe and found the estate
NEVER compacts on the janitor tier - the ledger that mag/context_compression.py
:409-417 appends to (COMPRESSION_LOG) has never existed on disk (sweep :16,
the sweep's run, not rerun here); the live loss signature sits at the provider
boundary as reset-to-~601-token events (up to 99.4% within-bucket shrink,
sweep :17).

PORT MOVES: install the first-action-after-compaction scoring gate BEFORE
compaction ever fires on the janitor tier (gate-first: the estate's
restart-and-diff law independently reinvented in-thread); when compaction
lands it preserves reasoning bytes (find 3's preserve_thinking), because
reasoning-dropped is exactly the bytes-that-never-reach-the-model-again class
the reach meter must catch; compaction stays scheduled, never
exhaustion-triggered (card A's Slow Vale cadence law).

### 3. The anti-quantized-KV position, with a KV provenance primitive (1wl5hfk) -> SOVEREIGN MIRROR

Mechanism (raw-verified, sweep/_kvr2_read_1wl5hfk.txt): "I am also
anti-quantized KV cache. I have been burned there - I think the tradeoffs
compound, especially at longer contexts" (:4); the config that avoids the
tradeoff - Qwen3.8-27B UD-Q8_K_L on 2x 3090 in TP with FP16 KV "into the 250k+
context with zero sense of degradation" vs 150k comfortable on 3.6 (:5), plus
--ctx-checkpoints 31 (:193) and chat-template-kwargs carrying
"enable_thinking": true and "preserve_thinking": true (:198). In-thread
counter-datapoint: 3.05bpw exl3 Flash-Next with FP16 KV + 24 GB sysmem KV
spillover described as indistinguishable from Q8 (sweep :52).

PORT MOVES: (a) llama.cpp --ctx-checkpoints is a KV snapshot/restore ring - a
continuity-checkpoint primitive. The sovereign mirror organ (the
persistent-continuity surface; docs/ref/LINEAGE_POINTERS.md:19 names "the
v2-hybrid system prompt for the persistent sovereign mirror") can key
provenance to checkpoint ids: a re-audit can name WHICH KV snapshot a given
continuity break rode on - the KV-layer twin of the verkle chain's anchored
leaves. Applicability caveat: the estate's bridge targets llama-cpp-python
0.3.36 (mag/marker_penalty.py:70-76 records that server's wire-shape caution
class) - ctx-checkpoints support there is UNMEASURED (OWED). (b)
preserve_thinking is the same reasoning-bytes-continuity law as find 2's drop
class: what history-keeping preserves determines what the model ever sees
again, and find 3 ties cache survival to keeping it.

### 4. The janitor fleet's KV-budget config pair + trust-bytes verification (1whf345) -> GOPHER FLEET

Mechanism (raw-verified, sweep/_kvr2_read_1whf345.txt): the OP is a QUESTION -
long-running Hermes agentic tasks on Qwen3.8-27B MLX push memory pressure at
64k-128k on a 64 GB Mac Studio M4 Max (:5), and the MLX-vs-GGUF applicability
stayed unresolved in-thread (Claude suggested cache-type Q8 + flash attention,
then self-corrected that those "only work for GGUF models"; :5). The answer
carries the steal: export OLLAMA_FLASH_ATTENTION=1 and
OLLAMA_KV_CACHE_TYPE=q8_0 (:11), verified by "you can check what cache type is
actually loaded with OLLAMA_DEBUG=1 in the server logs" (:22) - env-var intent
is not truth; the loaded cache type is.

Estate side: the janitor fleet IS Ollama (AGENTS.md DNA line: local Ollama
janitors first, gemma:2b scut + gemma4 short worker). Port-gap grep this
session: OLLAMA_KV_CACHE_TYPE / KV_CACHE_TYPE / ctx-checkpoints /
preserve_thinking = ZERO matching rows across mag/, tools/, configs/,
memory/rib/ (Receipt). The estate banks KV economics doctrine for providers
while holding no KV-budget law for its own fleet.

PORT MOVE: a fleet env contract (OLLAMA_FLASH_ATTENTION=1 +
OLLAMA_KV_CACHE_TYPE=q8_0 for GGUF-backed janitors) WITH the verification step
as law: the OLLAMA_DEBUG=1 log line naming the loaded cache type is the accept
gate - the same trust-bytes class as the release-integrity checksum law (commit
e8eedd8eb). The estate fleet is GGUF-class so the MLX ambiguity is probably
moot; UNVERIFIED (OWED).

### 5. KV bytes are a context-length budget, not a model-size property (1wjhk0r) -> QUANTIZER (honest mapping) + the fleet budget table

Mechanism (raw-verified, sweep/_kvr2_read_1wjhk0r.txt): the diagnostic method -
"Run ollama ps while that 260k-context model is loaded and check the Processor
column - Ollama's docs say anything under 100% GPU means part of the model is
in system RAM" (:16); the OP's readout 64%/36% at 17 GB = 7 GB model + 10 GB
for the 260k context (:19); the arithmetic law "That 10GB is the KV cache for
the 260k context - it scales with context length, not model size. If you
rarely need the full window, lowering num_ctx is the direct fix;
OLLAMA_KV_CACHE_TYPE=q8_0 halves the cache bytes at some quality cost" (:22).

PORT MOVE (honest mapping, sibling precedent at steal/inference-efficiency.md
:210-214): the charter organ "quantizer" resolves to mag/auto_quantize.py:1-15
- analytics-resolution quantization (L0-L5 retention buckets), NOT model/KV
quantization; the true port target is the fleet's KV-precision budget. Port =
a KV-budget table for the fleet (bytes as a function of num_ctx and cache
type; the q8_0 halving rule; the Processor-column spill check as the
diagnostic) landing next to the desk Modelfile's num_ctx knob
(mag/desk_model_probe.py:79, today PARAMETER num_ctx 8192 with no budget
contract attached).

### 6. Depth degradation was an engine defect; a warm prefix at 1M answers in 0.55 s (1wkyny9) -> WATER GRAPH + a percolator covariate law

Mechanism (raw-verified, sweep/_kvr2_read_1wkyny9.txt): halogen 0.12.0 vs
0.11.10, same machine, same session, same prompts - decode at 1,004,581 tokens
of context 27.3 -> 38.3 tok/s, prefill 790 -> 937 tok/s, cold 21.2 -> 17.9
minutes (:5-9); "A follow-up turn over the prompt cache at 1M reaches its
first token in about 0.55 s; the numbers above are the cold path" (:12);
conditions Ryzen AI Max+ 395, 128 GB, HALOGEN_ROPE_YARN=4 HALOGEN_CTX=1048576
(:12).

PORT MOVES: (a) Water graph (mag/water_graph.py:1-16, routing as physics):
engine releases re-price the physics - a 40% decode improvement at depth
changes which lanes gravity favors, so lane-routing decisions need an
engine-version stamp or they go stale silently. The 0.55s-vs-17.9-min
cached/cold spread is the freeze-the-prefix economics (the ~50x DeepSeek
hit/miss ratio at memory/research_polished/kv_cache_compaction.md:9) carried
to its extreme - the price of a warm tank at 1M tokens. (b) Percolator
covariate law: any length-axis performance claim must name engine + version,
the same denominator discipline the census law holds for test counts - a
"model degrades at depth" claim measured against one engine build is
unstratified noise.

### 7. The seventh sweep item, stolen at rev 2: q8 KV at 131k context on 16 GB VRAM, with eviction counters (1wom3fe) -> GOPHER FLEET config sheet + card A's rr_tail race at the expert layer

The round-2 verifier caught both cards stealing six of the sweep's seven banked
items and dropping this one (sweep item 2 at :41-44) - the most direct external
evidence bearing on card A's rr_tail race design AND this card's Ollama KV-budget
probe. Mechanism (raw-verified, sweep/_kvr2_read_1wom3fe.txt): AtomicChat
AD-4.27bpw Q4_K_M + the shared Unsloth MTP head + --spec-draft-cpu-moe runs 131k
context on 16 GB VRAM at 16.5 tg / 350 pp with q8_0 KV at ~3.2 GB (:6, :48), and
decode stays flat across context because a MoE with offloaded experts is
DDR-bandwidth-bound, not context-length bound, "as long as the KV cache fits in
VRAM" (:48). The comment duel is the steal: the adaptive expert-cache fork posts
61.68 t/s but its own counters read "16,202 misses and 8,138 evictions per 1k
tokens (~37% miss)" with prefill 95-137 t/s (:82, :83), against the OP's static
pinned-expert placement - 80 slots chosen once by cost model, "zero eviction
traffic", the one property it wins being that "it can't thrash mid-session"
(:73, :74), with the OP's verdict that for agent traffic with recompression
events the churn "can eat the whole decode advantage" (:88). Config-law tails:
quantized V cache needs -fa on "or llama.cpp just refuses" (:143), and the MTP
break-even on this build measures ~0.50 acceptance, not the usual ~0.60 rule of
thumb, because --spec-draft-cpu-moe parks the draft experts in RAM (:147:
15.2 t/s off, 16.5 at 0.55 acceptance, 14.4 at 0.48).

PORT MOVES: (a) this is card A's rr_tail question in miniature at the expert
layer - adaptive wins decode (61.68 t/s) but pays ~37% miss/eviction churn and a
3-4x prefill regression, static wins can't-thrash; the duel in-thread lacks
exactly the judge the estate's null-arm discipline supplies (beat the static/LRU
null or it is decoration, tools/lru_null_arm.py:1-17), so the rr_tail race gains
a second external anchor. (b) It hardens this card's headline probe: the q8_0 KV
budget at long context is MEASURED here (3.2 GB at 131k, flat decode while KV
fits VRAM), and the -fa requirement at :143 is the engine-side twin of find 4's
OLLAMA_FLASH_ATTENTION=1 pair - a fleet copying the cache-type flag without the
attention flag "will think the build is broken".

## The falsifiable probe for this week (headline; cheap, local, decisive)

Ollama KV-budget A/B with the trust-bytes gate, on the estate's own janitor
host:
1. Baseline: load one GGUF janitor model at a fixed num_ctx (e.g. 32768);
   record the ollama ps Processor + size columns and load time.
2. Arm: same model, same num_ctx, OLLAMA_FLASH_ATTENTION=1 +
   OLLAMA_KV_CACHE_TYPE=q8_0; GATE = the OLLAMA_DEBUG=1 server log must name
   the loaded cache type (if no such log line exists, the probe fails the
   verification law itself - a finding, not a config pass).
3. Measure: KV-bytes delta at fixed num_ctx via the ollama ps size column
   (predict ~2x reduction from the halving rule, find 5), Processor-column
   movement if the baseline spilled, and a 10-prompt janitor-scut quality spot
   check.
FALSIFIER: no debug-log cache-type line, OR KV bytes do not drop ~2x, OR scut
quality degrades -> q8_0 KV closes for the fleet and the config becomes FP16
KV + tighter num_ctx (find 3's position, its 250k receipt); a clean ~2x with
intact scut quality -> bank the env contract + the budget table (finds 4+5)
into the fleet config and the desk Modelfile comment. Either outcome is
decisive and costs $0.

Secondary probe (find 1, $0, records-only): re-score an existing banked
verdict/waste surface (e.g. 100 rows) with a second judge arm and report raw
agreement. Falsifier: agreement >= 90% on that surface scopes the second-arm
law as overkill THERE (scoped, not struck); agreement near the 61% precedent
makes the percolator invariant mandatory before any waste gate fires.

## OWED (never asserted as done)

- No Ollama host, model, or server was touched this session: the headline
  probe is designed, not run. The estate's local Ollama install, its backend
  class (GGUF vs MLX), and its engine versions were NOT verified here.
- marker_penalty profile v2 (the 3-family agent-validated cut) is mapped, not
  built; no logit-bias experiment was fired.
- ctx-checkpoints / preserve_thinking support on the estate's llama-cpp-python
  0.3.36 bridge: UNMEASURED.
- The 10-03 OP-table bank cite was corrected and verified first-hand this
  session (watch/inbox/frontier_olm_2026-10-03/sweep/
  quantization-and-compression-reddit.md:24); the 10-03
  kv-sweep :44 title-only line for 1whf345 is still carried from the ask's
  overlap field plus the sweep's receipt (sweep :59) - that file was not
  re-read here.
- The first-action-after-compaction gate is mapped, not built; the
  compression-ledger absence (sweep :16) is the sweep seat's run, not rerun
  here.
- reddit.com was not fetched this session; every quote comes from the sweep
  seat's retained raw renders, re-grepped by this seat (Receipt).

## Receipt (what this session actually ran)

- Raw-capture re-verification greps over sweep/_kvr2_read_*.txt:
  1wromzr -> :354 (only 3 words worth penalizing, small ceiling), :358
  (hmm 1,739 / wait 2,888 / actually 2,423; 1.6-7% of thinking, 1-4% of all
  tokens; accuracy not measured), :364 (85 sessions, 6,851 blocks, ~2.2M
  tokens, ~500-char median), :371 (33% / 48% / 68% skippable-riser-looping),
  :375 (61% agreement), :376 (8% vs 37%), :378 (12% both-agree, honest range
  12-37%), :5/:273 (the ~50-entry --logit-bias id list), :196 (tokenizer-split
  marker caveat), :471 (116 token values comment). 1wkyny9 -> :5-9 (27.3 ->
  38.3 tok/s at 1,004,581 tokens; prefill 790 -> 937; cold 21.2 -> 17.9 min),
  :12 (0.55 s cached follow-up; HALOGEN_CTX=1048576), :34 (cached-follow-up
  restated). 1wl5hfk -> :4 (anti-quantized-KV quote), :5 (250k+ FP16 KV, 2x
  3090 TP), :193 (--ctx-checkpoints 31), :198 (preserve_thinking true).
  1whf345 -> :5 (memory-pressure OP + the MLX-vs-GGUF ambiguity), :11 (the env
  pair), :22 (OLLAMA_DEBUG=1 verification). 1wjhk0r -> :16 (Processor column),
  :19 (64%/36%, 17 GB = 7 + 10), :22 (10 GB KV scales with context length;
  q8_0 halves cache bytes). 1wlss89 -> :4 (error propagates), :13
  (50%-of-max-context counter), :26 (4-bit KV degrades faster), :47 (audioen:
  full rewrite, reasoning removed), :51 (Marcus_MSC first-action rule).
- Catalog dedup: grep -c over catalog/catalog.jsonl with the alternation
  1wromzr|1wlss89|1wl5hfk|1whf345|1wjhk0r|1wkyny9 = 0.
- Estate-side anchors read this session: mag/marker_penalty.py (full; loader
  :41-64, bias builder :67-85, wire caution :70-76), mag/llama_cpp_bridge.py
  (:20-60 and :190-215: profile import, OFF-by-default law, payload builder
  with the logit_bias-only delta), configs/marker_penalty_profile.json (head:
  name/created/law/mechanism fields), mag/auto_quantize.py (:1-30),
  mag/water_graph.py (:1-16), mag/desk_model_probe.py (:70-90, the Modelfile
  writer whose num_ctx knob sits at :79), mag/context_pack.py (:955-965, the
  freeze docstring: same bytes on drift, either half changing flips the hash),
  mag/context_compression.py (:408-418, the COMPRESSION_LOG append writer),
  docs/ref/LINEAGE_POINTERS.md (:15-25, sovereign-mirror naming),
  corpus/steal/CORPUS_FOLD_FRONTIER_OLM_20261001.md (:5-9 via grep: the
  refusal-regime law with McNemar numbers), memory/research_polished/
  kv_cache_compaction.md (full read: the ~50x ratio at :9, the organ lineage),
  watch/inbox/frontier_olm_adhoc/sweep/kv-cache-context-engineering-reddit.md
  (full), steal/kv-cache-context-engineering.md and its .json (card A, full).
- Port-gap grep: OLLAMA_KV_CACHE_TYPE|ctx-checkpoints|ctx_checkpoints|
  preserve_thinking|KV_CACHE_TYPE over mag/, tools/, configs/, memory/rib/ =
  zero matching rows.
- Citation lint (house gate for changed prose records), run twice this
  session: first run FAIL exit 1 (blocking=3: two PATH-MISSING - one inherited
  from card A's abbreviated 09-28 arxiv bank cite, one this card's 10-03 bank
  cite pointing at steal/ where the bank lives in sweep/ - and one
  PHANTOM-NUMBER, a bare num_ctx value duplicated in this receipt). Fixes:
  expanded card A's abbreviation to the full
  watch/inbox/frontier_olm_20260928/sweep/ path (semantics unchanged),
  corrected this card's cite to the sweep dir with line 24 verified first-hand,
  and dropped the duplicate bare number. Rerun: exit 0, blocking=0, 12 WARNs
  (the rev-1 receipt line first miscounted 11; corrected here), all
  TOKEN-MISS/SHORTHAND heuristic class on multi-cite sentences, WARN-only and
  legal under the a05-r2 default.
- Rev-2 verifications (every round-2 critique item checked first-hand before
  the edit landed): the arxiv sweep's supersession header + the .prior file's
  RR-Evict item at :40-53 read directly; the reddit sweep's replacement header
  re-read and its zero Slow Vale / 1x0ms0m content confirmed by grep; the 10-10
  swarm re-bank's validation lane at
  watch/inbox/frontier_olm_2026-10-10/sweep/swarm-orchestration-reddit.md:29 and
  :34; the 09-28 banked list entries 6 (KVSET 2609.27746) and 7 (2609.28870)
  read at :110-111; the Slow Vale raw render _read_town800_agents.txt :11, :83,
  :86 (99.9%-resolved, ~1,450 failures / ~1,490 extra calls on ~160k decisions,
  0.9% call-count overhead, Prometheus, daily-summary pass, sub-30-minute gaps)
  and its raw XML _kv_thread_1x0ms0m.xml; the 1wom3fe raw lines :6, :48, :73,
  :74, :82, :83, :88, :143, :147; and the telemetry recount - three
  ./.venv/Scripts/python.exe aggregations over logs/provider_usage.jsonl giving
  77,800 rows / 63 cache-days / first 2026-08-04 / last 2026-10-11, with
  2026-08-17 = 981 all-cache rows / 851 family+ok and 2026-09-30 = 729
  all-cache / 728 family-any-ok / 721 family+ok - card A's rev-2 figures
  reproduce exactly under the family+ok rule, now named in its probe 2.
- Not run: any pytest, any model load, any probe execution, any reddit or
  external fetch.
