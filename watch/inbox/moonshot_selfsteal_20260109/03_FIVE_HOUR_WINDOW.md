# 03 - THE FIVE HOUR WINDOW (Lane 3): their governor, stolen as our clock

Lane 3, five-lane self-steal wave (this dir): the rolling 5h compute
window - the provider's quota shape - and our stolen version of it.

## What it IS

THEIR window: the provider meters tenant exhaust with a rolling compute
window we see only by its shadow - 429 code 1302 "Rate limit reached for
requests" storms rendered as fake subscription errors
(corpus/steal/TETHERED_LINK_STEAL_20260925.md:12-28); tiered (Max > Pro >
Lite), off-peak concurrency dynamic, quota 0.4x off-peak vs 1.2x peak on
GLM-5.3-Flash (TETHERED_LINK_STEAL_20260925.md:32-52). The 5h width is
the operator's reading of the plan, verbatim in the coinage
(memory/rib/RIB_STANDING_WAVE_BUDGET_20261009.md:4-7).

OUR stolen window: the retention + budget layer recognized as the same
organ evolved on our side, then stolen - "zai's 5 hour compute window...
stolen for our own purposes... flywheel lattice standing wave self steal"
(RIB_STANDING_WAVE_BUDGET_20261009.md:4-12; watch/inbox/disk_audit_20261009/LAW_PACK.md:5-11). Differences that
matter (rib :9-12): theirs denominated in tokens and opaque, ours
tokens-as-disk and readable in our own ledger (smith deltas read the
window's fill level directly); theirs resets opaquely, ours rolls by
construction - 7d retention is the window's width, the free-space floor
its edge (rib :32-33).

Window physics measured on theirs: the limit is ROLLING THROUGHPUT, not
width - 1302 ceiling at 15-16, after a burst even 12 takes 1302s until
the window decays, hold fires ~10 min on any 1302
(watch/inbox/burn_wave_20260926/B2_25_envelope_remeasure_20260926.md:29;
watch/inbox/gala_20260925/AFTERPARTY_CLOSE_20260926.md:8-9) - and the
dispatch shape is the retry strategy: workflow children get maxAttempts 0
and die on the first 429/1302, Task agents ride maxAttempts 11 + driver
backoff (TETHERED_LINK_STEAL_20260925.md:16-17, :58-60, :89-102).

## What we HOLD (measured, with paths)

- Task agents clean at widths 3, 6, 10, 12, ceiling 12-16
  (B2_25_envelope_remeasure_20260926.md:5; AFTERPARTY_CLOSE_20260926.md:8);
  width 10 banked 37,386,533 witnessed tokens in 1229.9 s = 109.4M tok/h,
  10/10 lanes, zero surfaced 1302s; wave 2 fired 176.9 s later, zero 1302
  (B2_25_envelope_remeasure_20260926.md:25)
- 50 workflow children (5 runs x 10) + burn cron + offpeak ran for
  hours; the first 429/1302 contact there is a HOLD, not a loss
  (watch/inbox/ENVELOPE_50W_HIT_20260926.md:3-9)
- Stolen-window ledger: 11079 files, 309.12GiB exec forest, purge prize
  81.22GiB at 7d+, peak 61.2GiB on 10-04; 255.86GiB = 82.8 pct mapped to
  30 named burns, 100 pct of top-20 writers unattended dwf actors
  (RIB_STANDING_WAVE_BUDGET_20261009.md:37-39; LAW_PACK.md:24, :31)
- The burn program inside the window: cron every 2h, 3 parallel topics
  per fire; DeepSeek paid calls fire only off-peak where prices halve
  (memory/burns/MANIFEST.json:5, :21)

## STATE

Landed: the rib is minted, five invariants
(RIB_STANDING_WAVE_BUDGET_20261009.md:14-33); smith organ exists,
dot-dir rows landed (LAW_PACK.md:68, :75); the envelope laws above are
receipts, not plans. Owed: the L2 retention sweep and L3 EXHAUST_BUDGET
gate are spec'd, not code - the rib mounts in rib_boot only with its
carrier (rib :57-58; LAW_PACK.md:96-101); no window-phase announcer or
stagger scheduler exists anywhere; the 15-16 rung stays untested
(B2_25_envelope_remeasure_20260926.md:39).

## COMPOSITION (the window with each sibling asset)

| With | The composition |
|---|---|
| WoW machinery | World ticks scheduled inside the window shape. The family's own counter-examples name wall-clock ticks and MySQL-as-authority as smells (docs/ref/WOW_FAMILY_LINEAGE_20260915.md:93), so the tick loop becomes window-shaped: deterministic tick batches fired as width-bounded burst waves in the window's high-throughput phase; world-persist rebuilds and map re-derivation caged outside it as local janitor work (the re-derivable class already carries keeper scripts, LAW_PACK.md:44-48). Content is not protocol - five years of heaviest custom content changed ~1 pct of verbs (WOW_FAMILY_LINEAGE_20260915.md:3-7) - so ticks tolerate batching without changing the game. |
| Token economics | The window IS the budget's clock. Tokens-are-disk makes the 7d retention width and the free-space floor the same organ as the quota window (RIB_STANDING_WAVE_BUDGET_20261009.md:14-19, :32-33); burn orders declare GB/day and smith deltas adjudicate intended vs actual (LAW_PACK.md:29-34); the burn cadence - every 2h, 3 topics - is the window's heartbeat, and DeepSeek paid climbs align two clocks at once: off-peak halving riding a freshly decayed window (memory/burns/MANIFEST.json:5, :21). |
| The mesh | Windows staggered across devices = a mesh-wide always-on composite window. Chan rows announce each seat's window phase on watch/room.jsonl; rib_bus carries the window law once for every seat (.agents/skills/mesh-comms/SKILL.md:6-12); the mesh's own falsifier already speaks window - a message is justified iff it changes a file, decision, or receipt within one window (.agents/skills/mesh-comms/SKILL.md:34-36). Staggering is just phase publication plus a scheduler that fires each host at its offset. |
| GSTD | Window capacity as the leaseable resource. The GSTD fleet lane pays credits per task execution (docs/ref/GSTD_FLEET_LANE_SPEC.md:1-15); the margin between the standing burn cadence and the measured ceiling is exactly the headroom we lease out as probe / corridor / queue tasks. Its 10s x 30-tries poll (5 min) fits inside one burst phase, and the fail-closed wallet gate keeps the lease honest (GSTD_FLEET_LANE_SPEC.md:27-32, :49-50). |

## MOONSHOT - the mesh-wide composite window

One host with a 5h window is dark 19h/day. Derived arithmetic (nominal 5h
from the coinage, rib :4-7; decay per AFTERPARTY_CLOSE_20260926.md:8-9):
- Coverage per host = W - L (W usable hours, nominal 5; L lost daily to
  the decay shoulder - UNMEASURED, the probe below). Hosts for 24/7 =
  ceil(24 / (W - L)); per-host tolerance at N hosts = 5 - 24/N (derived):
  N=5 (offset 4.8h) tolerates 0.2h - slack 1h, too thin; N=6 (offset
  4.0h) tolerates 1.0h/host; N=7 tolerates ~1.6h.
- Today's fleet is 3 devices (desktop FULL, bob node-lite, pixel
  node-lite, GSTD_FLEET_LANE_SPEC.md:10-11) = 15 window-hours/day =
  62.5 pct of the day (derived); two more devices reach full coverage.
- Throughput: one host bursts at 109.4M tok/h at width 10
  (B2_25_envelope_remeasure_20260926.md:25); a staggered composite keeps
  one host in burst phase at all times, so mesh-wide sustained
  throughput approaches burst rate, not the 5/24 duty-cycle average
  (derived).
- The mesh staggers, the window keeps hosts honest: no unbounded sink per
  host (RIB_STANDING_WAVE_BUDGET_20261009.md:20-22), smith deltas per
  device, phase on the chan, law on the rib_bus.

## SELF-STEAL

- Stole the window SHAPE and inverted ownership: their governor meters
  tenant exhaust for their benefit; ours meters our own exhaust for us,
  ledger readable, refill rolling (RIB_STANDING_WAVE_BUDGET_20261009.md:8-12).
- Stole the meter READING: 429/1302 storms taught us the envelope from
  the outside - the failure mode became the instrument; the retry
  asymmetry was found in our own adapter bytes and corrected into the
  dispatch-shape law (TETHERED_LINK_STEAL_20260925.md:10-18, :89-102).
- The retention contract's shape is stolen prior art converged: Gemini
  CLI's four-field knob, Codex's quota checklist (LAW_PACK.md:24-25,
  :31-32); deepest steal: their window is a cost we pay, ours is
  inventory we lease - the governor became an asset.

## FALSIFIER + PROBE

Falsifiers: a landed cap/retention/budget with a monster regrown behind
it and no organ catching it means the law is prose
(RIB_STANDING_WAVE_BUDGET_20261009.md:44-45); growth diverging from
declared budgets with no smith alert means invariant 3 is decoration
(rib :46-47); if staggered hosts run dark because the shoulder eats the
window, N-host arithmetic is wrong by exactly L x N hours - unmeasured L
is a guess wearing a formula.

PROBE - measure the shoulder L (one evening, all local bytes):
1. Fire one width-10 Task-agent wave (the measured clean rung,
   watch/inbox/burn_wave_20260926/B2_25_envelope_remeasure_20260926.md:5);
   log T0 and last-completion T1.
2. Every 10 min after T1 (the hold interval,
   AFTERPARTY_CLOSE_20260926.md:9) dispatch one single-prompt Task agent;
   record clean completion vs surfaced 1302 per ping.
3. L = T(first clean ping) - T1; two consecutive clean pings end it.
4. Bank L as 03a_shoulder.md in this dir; hosts-for-24/7 =
   ceil(24 / (5 - L)) is then derived arithmetic on banked bytes, not
   folklore. If L exceeds 1.0h the 6-host design dies; N=7+ is the target.
