# STEAL CARD: inference-efficiency (frontier_olm 2026-10-10, round 2 REVISE applied)

Round 1 was REVISED on one blocking ground plus four lesser defects, all verified against bytes
this sitting: a false NEW claim (round 1 asserted "Both finds' NEW claim holds" while both finds
were already banked in this workflow family's own prior runs under watch/inbox, the root round
1's overlap grep omitted), an OWED line already paid by a superior held read, an endurance
thesis held since 09-30 that round 1 presented as fresh, two sweep cite errors, and an unbanked
returned JSON. This round corrects all five. What the reviewer verified clean under their own
runs (every code cite, the probe arithmetic, the meter counts, the disk identity, both arXiv
pages) is carried forward labeled as such, not redone; everything new below was run or read by
this seat this sitting.

## Overlap (rerun at the demanded scale; the round-1 NEW claim was FALSE)

Round 1 grepped catalog + memory/rib only and missed the root where every frontier bank lives.
This sitting's full-scale rerun: `grep -rln "Lachesis\|EdgeAgent\|2610\.08378\|2610\.03394"`
over ALL twelve `watch/inbox/frontier_olm_*` runs (20260928, 09-30, 10-01..10-10) hit 13 files,
10 of them outside this run's own 10-10 directories:

- 2026-10-05: `sweep/evals-self-improvement-arxiv.md:36` notes EdgeAgent (1.77x, Apple M4,
  "not deep-read"); `sweep/inference-efficiency-arxiv.md:28` banks EdgeAgent 2610.03394 in its
  banked list (abstracts pulled via export.arxiv.org id_list, that file :20).
- 2026-10-07: `sweep/kv-cache-context-engineering-arxiv.md:9` lists 2610.08378v1 among ELEVEN
  end-to-end arxiv.org/html full-text reads, and `:38-40` is a FULL Lachesis entry (see Steal
  1); `sweep/inference-efficiency-arxiv.md:43` lists EdgeAgent (1.77x on M4);
  `sweep/kv-cache-context-engineering-reddit.md:203,251` names Lachesis in a banked axis;
  `steal/inference-efficiency.md:4-5` is the LITIGATED PRECEDENT: that run's round 1 was forced
  to revise for "a false zero-overlap receipt... the grep omitted watch/inbox, the root where
  every frontier bank lives". Round 1 of this card repeated the identical mistake.
- 2026-10-08: `sweep/kv-cache-context-engineering-x.md:59` names Lachesis among prior banks.
- 2026-10-09: `sweep/inference-efficiency-arxiv.md` entry 5 is a FULL EdgeAgent bank, one of
  "7 banked as new" (that file :16), carrying the exact quote "the UMA-aware execution alone
  contributes a 1.29x speedup over batched speculative decoding. Adding the agent-aware
  scheduling lifts the full EdgeAgent system to a 1.77x speedup" and an estate mapping
  (gemma:2b janitor + gemma4 worker; Apple silicon, not the estate's AMD/Windows, so
  patterns-not-numbers); `sweep/kv-cache-context-engineering-arxiv.md:13,37` carry Lachesis in
  census and tiering lines; `sweep/swarm-orchestration-arxiv.md:11` lists the EdgeAgent ID in
  pass-1.
- This run's own 10-10 files (round-1 card, sweeps) are self-references.

Verdict, correcting round 1: BOTH FINDS ARE RE-CONFIRMED, HELD, NOT NEW. EdgeAgent has been
held since 10-05 and fully banked 10-09; Lachesis has been held at FULL-TEXT depth since 10-07,
a better read than this seat's abstract-level one. The ask's and this run's sweep's NEW claims
(`sweep/inference-efficiency-arxiv.md:13` "the 8 banked items have zero catalog hits") are true
of catalog/ and false of watch/inbox, the same root-omission family the 10-07 card litigated.
The catalog/memory greps from round 1 still hold (0 hits, rerun then; catalog re-check 0 this
sitting). Scope limit carried: no recursive grep of all 13G memory/.

## Headline steals (mechanisms; Steal 1 upgraded to full-text grade)

1. LACHESIS (arXiv:2610.08378), RE-CONFIRMED, held full-text since 10-07: placement priced in
   medium lifetime. A serving stack spilling KV to flash is absorbable only if WRITES are
   budgeted in device-years of write endurance, a budget class separate from capacity.
   Full-text mechanism (all from the held 10-07 bank, `frontier_olm_2026-10-07/sweep/
   kv-cache-context-engineering-arxiv.md:38-40`, fetched end-to-end that sitting): between
   harness and engine, KV pages are placed by PREDICTED LIFETIME on two paths - a deterministic
   path using harness-reported segment boundaries ("the harness knows whether a segment is
   discarded at the boundary or retained past it. A short-lived context segment has priority
   for HBM.") and a predictive path ranking worker-segment lifetimes with ridge regression
   (Kendall's tau 0.53). Agentic-session measurements that define the workload class: agent
   peak contexts are 29x chatbot workloads; reasoning segments hold 66-83% of a turn's KV yet
   live one turn; lead-agent segments outlive workers 4.0-6.1x and are unread 71-88% of their
   lifetime, so read-to-write ratio (the prior-work criterion) is a poor proxy. Result:
   "extends HBF lifetime by 1.19-3.13x over HBM-first placement, reaching 3.3-12.2
   device-years" (ask-verbatim; this run's sweep:30); tight-SLO configs outlast the five-year
   warranty. Caveat, now with its evidence: trace-driven simulation only (tau3-bench, BFCLv4,
   AppWorld, SWE-bench Verified, TerminalBench, WebArena traces; Llama-4-Maverick and
   Qwen3-235B-A22B), no end-to-end latency on real hardware (10-07 bank).
   PRIOR ESTATE SIGNAL THIS PROMOTES (held 09-30, never promoted): "SSD wear + thermals are the
   real overnight-inference ceiling, not just wall-clock. Estate angle: our janitors run from
   RAM/NVMe on Windows; anything streaming from disk overnight must budget write endurance"
   (`frontier_olm_2026-09-30/sweep/inference-efficiency-hn.md:50-52`, with :39 "SSD-wear
   ceilings apply at exactly our scale"). Verified never promoted this sitting: grep for
   endurance/SSD-wear/slotstream/TBW over that run's steal cards, DIGEST.md and
   percolator_candidates.jsonl = 0 hits. What the held signal lacked, and what this steal adds,
   is the MECHANISM: the two-floor budget class (capacity + write-endurance) and a placement
   policy that routes by which floor binds, plus the lifetime observables (harness boundaries,
   one-turn reasoning KV, unread lead-agent segments) that make the routing decidable.

2. EDGEAGENT (arXiv:2610.03394), RE-CONFIRMED, held since 10-05, fully banked 10-09: the
   scheduler is the organ and stall is the signal. On one shared-memory device running many
   small agents, tool-call stalls rather than compute are the first-order loss. Mechanism:
   UMA-aware zero-copy tensor parallelism, async suspend-and-yield evicting agents stalled on
   tool calls, and speculative draft budgets set per-sequence by observed real-time
   predictability; "Adding the agent-aware scheduling lifts the full EdgeAgent system to a
   1.77x speedup under extreme tool-use latencies" (ask-verbatim; the held 10-09 bank's fuller
   quote adds "the UMA-aware execution alone contributes a 1.29x speedup over batched
   speculative decoding"; Apple M4 evaluation). Measurement box is Apple silicon, not the
   estate's AMD/Windows host, so patterns transfer and numbers do not (10-09 bank's own
   mapping). The two portable scheduler laws: evict-on-stall, budget-by-observed-predictability.

## Estate map (organ + concrete port moves)

Lachesis feeds the WATER GRAPH, metered by DISK SMITH, and PROMOTES the held 09-30 endurance
thesis into mechanism.

- W1, ENDURANCE AS A SECOND ETA AXIS IN DISK SMITH (promotion of the 09-30 thesis, not a fresh
  idea). Today smith prices ONE axis: capacity. projection() (`tools/disk_smith.py:354-400`)
  computes median pairwise daily free-space burn with IQR honesty and eta_days to the 15.0GB
  floor (`:95`, `:398`); the DISK ETA alert (`:192-194`) fires on that axis alone; no TBW/wear/
  endurance/device-year string exists anywhere in the file (reviewer-verified, carried forward).
  Port: a second column pricing the same volume in device-years against rated TBW. Live
  denominator (round 1, reviewer-reproduced): C: is disk 0, a Samsung SSD 990 EVO Plus 2TB,
  rated 1,200 TBW / 5 years (Samsung warranty page, semiconductor.samsung.com). The subtlety
  the held thesis named and Lachesis now formalizes: smith's net delta UNDERCOUNTS writes. A
  pagefile that balloons and shrinks daily has near-zero net delta and heavy write churn; the
  ledger's last snap reads pagefile 63.95GB the morning after the 135-to-64GB shrink
  (`logs/disk_smith.jsonl` row 2026-10-09T12:50:02Z). And Lachesis's own observables warn
  against the naive proxy: read-to-write ratio is a poor lifetime predictor (10-07 bank), so
  the endurance axis must be metered by the wear counter, not inferred from read traffic.
- W2, THE WATER GRAPH ALREADY RUNS THE PHYSICS; ADD THE WEAR PRICING. The fracture law
  (`mag/water_graph.py:25-31`, stress field `:144`) has a pipe running full bore accumulate
  `stress += flow` and FRACTURE, closed forever, at a cumulative-throughput threshold: that IS
  write endurance as mechanics. Port: a wear-priced edge class where stress accumulates bytes
  written and the threshold is the TBW rating, so the standing-wave question (does a local
  serving stack spilling KV to this volume survive) is simulated on the water computer before
  it is paid on hardware. Lachesis's placement policy (writes to the absorbing medium, reads
  from the capacity medium) is the existing check-valve routing law (`mag/water_graph.py:14`,
  one-way, no backflow), and its deterministic path maps 1:1 onto estate structure: the harness
  already knows segment boundaries our scheduler also knows (a gopher ask's lifetime, a
  workflow child's cache, a janitor's re-read corpus), so "short-lived segment has priority for
  HBM" becomes "short-lived lane output stays in RAM; only lead-agent-class long-lived state
  pays the flash write".

EdgeAgent feeds the GOPHER FLEET and the INFERENCE BUDGET surface (mapping first drafted by
the held 10-09 bank: gemma:2b janitor + gemma4 worker across queue/lanes).

- E1, STAMP THE STALL AXIS FIRST. The meter slot exists but is dead AT THE SOURCE: the usage
  row hardcodes "latency_ms": 0 (`mag/gopher_lite.py:115`), and all 23 ZAI_GOPHER_KEY2 rows
  carry 0 (round 1, reviewer-reproduced). The field itself is live estate-wide: this sitting's
  count over `logs/provider_usage.jsonl` = 57,170 rows carrying latency_ms, 53,813 nonzero
  (range 359 to 237,318 ms), 3,357 zero - so other writers measure real latency and only
  gopher_lite's slot is dead, which makes this a one-line fix at the blocking call site
  (_post_json, `mag/gopher_lite.py:120-127`, timeout=180), not a meter build.
- E2, EVICT-ON-STALL IN THE CHORE LOOP. gopher_lite runs one chore per tick and a stalled
  chore holds the loop for the full timeout (`mag/gopher_lite.py:120-127`; the loop sleeps at
  `:261`). Port the suspend-and-yield law: a chore stalled past a threshold yields its tick to
  the next chore in the deterministic rotation and is resumed later, not abandoned. No
  evict-on-stall exists anywhere in mag/ or tools/ (reviewer-verified, carried forward;
  mag/act.py eviction is attention.md records, unrelated). Same law at larger width: the
  workflow fan-out lanes treat a stalled child as a held slot; stall-yield is the
  scheduler-level sibling of the 429-HOLD signal in the max-concurrency law (AGENTS.md).
- E3, PREDICTABILITY-PRICED BUDGETS. FAMILY_TABLE (`mag/inference_budget.py:71`) is the ONE
  source every fire path imports (`memory/rib/RIB_INFERENCE_BUDGET_20261001.md:46`), but every
  row is a STATIC per-family recipe (no adaptive/observed/acceptance logic in the file,
  reviewer-verified, carried forward). The rib's jacket census is the unpriced-divergence
  disease: re-fires after empty content made "$20.53 of $29.91 was re-fire theater" (rib:33)
  and one cold call ran 234s (rib:36). Port EdgeAgent's per-sequence predictability: a family
  row's budget (max_tokens floor, draft spend) adapts to the observed emptiness/acceptance
  history of that ask class, so a sequence class that keeps diverging gets its speculative
  spend cut instead of being re-fired at full price. Lachesis's ridge-regression lifetime
  ranking (tau 0.53, cheap and online) is the same statistical shape: a tiny regressor pricing
  a placement decision by predicted future use.

## Probe (one, falsifiable, cheap; attempted round 1, sharpened round 2)

PRIMARY, the wear axis. The non-elevated attempt failed honestly (PowerShell
Get-StorageReliabilityCounter -> "Access to a CIM resource was not available to the client";
reviewer's alternate WMI door unproven on shell quoting, theirs, stated). The probe is one
elevated run: implied wear rate = Wear% / (PowerOnHours/24); remaining device-years =
(100 - Wear%) / rate. Compare against smith's capacity ETA (days, when trending) and the
round-1 movement proxy (3 ledger rows over 0.5 days: net +254.6GB, sum|delta| 327.0GB = 653
GB/day of absolute movement, which if all writes spends 1,200 TBW in ~5.0 years;
reviewer-reproduced to the decimal). Falsifiers: (a) the counter stays PermissionDenied even
elevated, so the wear axis stays OWED and the movement proxy is the only endurance signal;
(b) wear-implied device-years exceed ~2 years while capacity ETA trends in days, meaning
endurance is NOT the binding constraint on this volume today and W1 demotes honestly to
promotion of the 09-30 thesis as water-graph planning vocabulary (W2) with no live alert
class; a wear rate at or above 0.1%/day promotes the DISK ETA endurance axis immediately.
NEW WATCH ITEM this sitting (folded from the reviewer's gift, now with data): the smith
ledger's 3 rows are all 2026-10-09 UTC (00:48, 02:16, 12:50), smith v1.1 landed 2026-10-10
02:24:09-04:00 (git e5c5d0057), so the round-1 discrepancy is RESOLVED - no post-v1.1 snap
exists yet, and the stamp code at `tools/disk_smith.py:458-461` (curr["projection"],
curr["top_movers"]) will fire on the next snap. But the MagDiskSmithDaily task DID run today
(PowerShell Get-ScheduledTaskInfo: LastRunTime 10/10/2026 8:50:50 AM, LastTaskResult 267014)
and NO row was appended (ledger still ends 2026-10-09T12:50). The daily 08:50 task fired dark;
that is a task-darkness incident for the smith owner (why did the snap not append: bare-python
venv law, script path, or the 267014 result), not a smith code bug.

SECONDARY (EdgeAgent, one line): after E1 stamps real latency_ms, test the heavy-tail premise
on one week of gopher rows (does the top decile of calls hold >50% of wall time); a tight
distribution falsifies evict-on-stall for this fleet and E2 stays unported.

## Verification receipt

Round 2 (this sitting, this seat):
- Full-scale overlap grep over all twelve frontier_olm runs (command in the Overlap section):
  13 files, enumerated above with pinned lines.
- Reads: 10-09 sweep EdgeAgent entry + banked-as-new line; 10-07 kv-cache sweep html-read list
  (:9) and Lachesis entry (:38-40); 10-07 steal card lines 1-5 (the precedent); 10-05 evals:36
  and inference-efficiency:20,28; per-file line pins for the remaining 10-08/10-09/10-10 hits.
- 09-30 endurance prior: read hn:39,50-52; promotion grep (endurance|SSD wear|slotstream|TBW)
  over that run's steal/, DIGEST.md, percolator_candidates.jsonl = 0 hits.
- GIFT 1: git log e5c5d0057 = 2026-10-10T02:24:09-04:00; tools/disk_smith.py:458-461 stamp
  code read; ledger recount = 3 rows, last 2026-10-09T12:50;
  Get-ScheduledTaskInfo MagDiskSmithDaily = State Ready, LastRunTime 10/10/2026 8:50:50 AM,
  LastTaskResult 267014, NextRunTime 10/11/2026 8:50:50 AM.
- mag/gopher_lite.py:113-118 read ("latency_ms": 0 hardcoded at :115);
  logs/provider_usage.jsonl full-lane latency census = 57,170 fields, 53,813 nonzero
  (359-237,318 ms), 3,357 zero.
- Sweep cite repairs: this run's sweep quote lives at sweep:30 (Read: abs line, quote verbatim;
  sweep:31 is estate-fit + caveat); abstract-only evidence for items 3 and 7 is the per-item
  "Read: abs" at sweep:30 and sweep:46 plus the pass-2 note at sweep:9 (only 2610.03228 and
  2609.31619 got html full text); the round-1 cite of sweep:79 named the wrong line (it lists
  items 2,4,5,6,8).
- Returned-card JSON banked to `steal/inference-efficiency.json` beside this file (defect 5).

Round 1 (reviewer-reproduced under their own runs, carried forward, not redone): all code cites
(disk_smith :95,:192-194,:354-400,:362; water_graph :14,:25-31,:144; gopher_lite :120-127,:261;
inference_budget :71; rib :33,:36,:46); probe arithmetic (3 rows, +254.6GB, 327.0GB, 653
GB/day, 5.03 years, pagefile 63.95GB); 23x gopher rows latency_ms 0; disk identity
(DeviceId 0, 990 EVO Plus 2TB); TBW 1,200/5yr on Samsung's warranty table; both arXiv pages
live-fetched (titles, quotes, axes, M4, suspend-and-yield, predictability-driven budgets).
Round 1, run by this seat: PermissionDenied wear-counter attempt; Get-Partition/Get-PhysicalDisk
mapping; catalog + memory/rib greps (0/0); ledger computation; Samsung TBW web check.

## OWED

- The elevated wear read (needs operator elevation; the 267014 daily-task result code is
  reported raw, not decoded against MS docs).
- The MagDiskSmithDaily darkness cause (why the 08:50:50 run appended no row): for the smith
  owner; this seat reports the observable only.
- Lachesis numbers remain trace-driven simulation (trace list and models now cited from the
  10-07 full-text bank); EdgeAgent numbers remain Apple M4, not this host's AMD/Windows.
- No recursive grep of all 13G memory/ (scope limit, unchanged).
