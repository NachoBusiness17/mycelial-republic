# THE 50 · W6 T28 - MISS-ENTROPY DASHBOARD (G13 design + minimal JSON data path)

Filed 2026-09-19 · W6 INSTRUMENTS · program row
`watch/inbox/THE_50_PROGRAM_20260918.md` line 45: "28. Miss-entropy dashboard
(G13 design) [QUEUED]".
Re-verified 2026-09-25: generator re-run against the grown corpora (cutoff
moved 2026-09-19 to 2026-09-25); every computed number below is from that run.

## 1. What G13 actually is (grounding)

G13 is row 13 of the GPS 50-wide battery,
`watch/inbox/GPS_BATTERY_20260918.jsonl` line 13, family `cache_os`:

> CLAIM: 99 percent prefix cache hit rate is necessary but dangerous: it
> proves stability but also proves nothing new is being asked. The health
> metric is not hit rate but the ENTROPY of misses. Begin with THE FLAW.
> Then: design the miss-entropy dashboard (what distribution over cache
> misses signals healthy exploration vs drift vs pathology). End with
> NEXT-STEAL: one instruction.

The answered sketch is filed at `memory/runs/gps_50/GPS_PACK.md` line 515
(section "G13 via groq-oss ok=True"), with four panels: Entropy Score
(H = -sum p_i log2 p_i over miss-key buckets), Bucket Distribution (top-k
share), Temporal Variance (sigma_H over a rolling window), Miss-Rate Delta,
plus the NEXT-STEAL (a scheduled job computing miss_entropy + top5_pct per
window). This task turns that sketch into the fleet's design and files the
minimal JSON data path it consumes.

(The other G13 on disk, PRIVLIDGE/`swarm.html`, is the burn2b game gate at
`memory/runs/fleet_round/burn2b/wave_01/N004_G01.md` line 61. It is a
different registry. This task follows the program's own convention: T29
cites G31 and T50 cites G25, both GPS-battery rows. Battery G13 is the one
whose text names this dashboard.)

## 2. Fleet translation: what plays the cache, what plays a miss

The fleet's "prefix cache" is the seat-facing knowledge layer: context pack,
briefs, invariants, corpus, meter registry. A "hit" resolves a seat's ask
against what is already filed. A "miss" is any event where the layer failed
or the ask went past it. Three miss surfaces have real rows on disk today;
each gets a miss-key, and all three share one schema:

| Surface | Miss row | Miss-key bucket | Source (read this session) |
|---|---|---|---|
| prophecy_called_shot | verdict-filed BROKEN row | target_date (the staked horizon) | `watch/inbox/mrpool_export/called_shot_ledger.jsonl` (16), `..._captions.jsonl` (107), `watch/inbox/qdrop_export/called_shot_ledger.jsonl` (3), verdict at `watch/inbox/mrpool_export/CALLED_SHOT_VERDICT.json` |
| ops_fkb_failures | `fkb_failure` training event | input.kind (secondary: action.tool, action.provider) | `training/events.jsonl`, 109,261 fkb rows (2026-09-25 run) |
| jev_meter | packet with meter_correct=false | packet id | `queue/lanes/jev/trail.jsonl` (6 wave rows; meter idempotent by packet id, standing drive re-fires) |

Rule carried over from the W1 T5 payoff matrix
(`watch/inbox/THE50_W1_T05_PAYOFF_MATRIX.md`, cell 2): only verdict-filed
rows enter miss entropy. Ledger v2 (107 rows, no verdict field filed) and
the Q rows (3, all horizons past, no verdict filed) are pending, not misses.
They are reported as unresolved inventory, never as scored misses.

## 3. The panels (design, adapted from the G13 answer)

1. **Entropy Score.** H in bits over the surface's miss-key buckets, plus
   the comparable index H_norm = H / log2(K) so surfaces with different K
   plot on one axis. The G13 answer's healthy band (3.5 to 5.2 bits, about
   20 to 30 buckets) was calibrated on cache workloads and is kept quoted,
   not applied: our surfaces have K = 2 to 15 primary buckets. Fleet bands,
   PROPOSED first calibration from this filing, not law: H_norm below 0.35
   = hot-spot (miss mass concentrated, the Med Bed shape); 0.35 to 0.85 =
   mixed; above 0.85 with rising miss volume = scatter (shotgun).
2. **Bucket Distribution.** top1_share and top5_share per window. The G13
   hot-spot rule (top-5 above 60 percent) maps here to top1_share.
3. **Temporal Variance.** H per window (calendar month for ops, per wave
   for the meter, per campaign for prophecy) plus the delta of n between
   consecutive windows, in order. G13's pathology rule reads directly:
   falling H with rising miss count = instability, not exploration.
4. **Miss-Rate Delta.** delta-n per window, carried in the curve arrays so
   the renderer computes the delta rather than refetching.

## 4. Minimal JSON data path (filed and computed this session)

- Data: `memory/runs/the50/w6_t28_miss_entropy.json`, schema
  `the50.w6.t28.miss_entropy.v1` (6,793 bytes, reloads as JSON, 0
  em-dashes; cutoff 2026-09-25). Top level: g13_source, cutoff, panels,
  series[3].
- Generator: `scripts/the50_w6_t28_miss_entropy.py`.
  Re-run: `.venv\Scripts\python.exe scripts\the50_w6_t28_miss_entropy.py`
- Endpoint (design, not built in this task): `GET
  /api/v1/instruments/miss_entropy` serving the file through the same
  `_read_json` pattern as `dashboard/rest.py` lines 42-46; render as a
  stacked area of bucket shares with the H_norm line overlaid, one panel
  per surface, per the G13 visualization note.

Computed numbers (from the 2026-09-25 run of the script above, not hand
counts; 2026-09-19 filing values in parentheses where they moved):

| Surface | n | K | H bits | H_norm | top1_share | Reading |
|---|---|---|---|---|---|---|
| prophecy v1 (verdict BROKEN) | 16 | 2 | 0.3373 | 0.3373 | 0.9375 | hot-spot: 15 of 16 misses on target 2026-01-01, 1 on 2026-01-06; the Med Bed campaign is single-claim repetition, G13's over-specialization shape (unchanged since filing) |
| ops fkb by kind | 109,261 | 15 | 1.3621 | 0.3486 | 0.77 | tool_fail dominates (84,127); H_norm sits on the hot-spot boundary (0.35); was 94,922 / H 1.2448 / H_norm 0.3186 / top1 0.7824, tool_fail 74,266; secondary keys: by tool H_norm 0.3089 (K=2705), by provider H_norm 0.4243 (K=8) |
| ops fkb, 2026-08 window | 43,868 | - | 1.7189 | 0.4515 | 0.672 | baseline month (unchanged) |
| ops fkb, 2026-09 window | 65,393 | - | 0.8984 | 0.2995 | 0.8357 | G13 pathology signal live and still holding: miss volume up vs 2026-08, H and H_norm down, top1 share up; failure mass is concentrating on one kind (was 51,054 / 0.6380 / 0.2273 / 0.8772 at filing) |
| jev_meter miss events | 13 (6 waves) | 4 | 1.9501 | 0.975 | 0.308 | near-uniform spread across 4 packet ids (B1-trace, B2-pack, A2-divides, A1-prime); n too small to band (unchanged since filing) |
| ledger v2 pending inventory | 107 rows | 12 expired targets | 2.9941 | 0.8352 | 0.3298 | 94 horizons expired with no verdict filed, 13 still open at cutoff 2026-09-25; inventory only, excluded from miss entropy by the verdict-filed rule |

## 5. What the design adds beyond the G13 answer

- The verdict-filed rule: prophecy misses enter entropy only with a verdict
  on disk, which keeps the retrofit cell (vague x arrives) from inflating
  miss entropy with unresolved rows.
- H_norm as the cross-surface axis, because the fleet's buckets are single
  digits, not cache-scale twenties.
- The pending-inventory block: expired-unverdicted rows are surfaced with
  their own bucket entropy (v2: H_norm 0.8352 over 12 targets, scatter
  shape) so the dashboard shows the backlog without scoring it.
- Meter idempotency respected: the standing drive re-fires packets
  (commit 4ad6eb0d6 pattern), so the meter surface reports both per-fire
  miss events and the deduped unique-packet view.

## 6. Honest limits

- The H_norm bands in panel 1 are a first calibration from three surfaces,
  not doctrine; two ops windows is not a variance estimate, so G13's
  sigma_H panel is carried as windowed H, not sigma.
- v2 and Q verdicts are not filed on disk; any "Pool v2 misses" claim
  would be a guess and none is made here.
- The by-tool K of 2,705 includes sig-suffixed entries; treat tool-level H
  as a census, not a stable index, until keys are normalized.
- The dashboard endpoint and renderer are designed, not implemented; the
  finish line for this task is the design plus the JSON data path, both
  filed above.

no_em_dash: this file contains none.
