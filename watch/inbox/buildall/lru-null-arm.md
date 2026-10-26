# LRU null arm - the G1 gap law's demanded measurement (M3, gala build-it-all)

Lane: m3-lru-null-arm (division B). Moment: 2026-10-03T22:01Z.
Ask: replay the most recent 5,000 dashboard/static/trails rows through a
prefix-cache simulator at the real 4,800-char pack budget; measure the hit
rate curve; bank it as the G1 null before any eviction policy is trusted.

## Law and ask this closes

- memory/research_polished/kv_cache_compaction.md:13 (gap-fold G1): "any
  eviction/compaction claim must beat LRU/ARC/PBKV/Belady-MIN arms or it is
  decoration."
- watch/inbox/gala_20260925/fillball-1001/lanes/work/48h.src.md:60-74 (M3
  steals row): falsifiable claim "radix-leaf LRU at the estate's real budget
  achieves 80%+ hit (external reference 83.48% at 8k blocks on the AgentX
  subset)". The external number is carried from the ask's source card
  (watch/inbox/frontier_olm_20260928/steal/quantization-compression via
  hn.md, agentic-kv-cache via HN item 49643543); not re-fetched this session.
- memory/runs/gapwave/context_economics_1m.md:46 (doug.sh): "compaction
  invalidates the whole prefix", cached share 55% -> 95% - why the null is a
  PREFIX-cache measurement, not a generic cache one.

## What was built

- tools/prefix_cache_sim.py (365 lines): radix tree of full char blocks with
  leaf-only LRU eviction (vLLM/SGLang RadixAttention semantics: internal
  prefix blocks survive while a descendant is cached; a parent that loses its
  last child stays cached as the shorter prefix), request-granularity LRU
  clock, lazy heap eviction, partial trailing block never caches. Tape
  loaders and three prompt arms: frozen_append / frozen_window / volatile.
- tools/lru_null_arm.py (265 lines): CLI, capacity sweep, claim verdict.
- tests/test_lru_null_arm.py: 10 tests pinning the simulator semantics.
- Split note: the first merged draft was 602 lines and the ratchet flagged
  NEW file-too-long on it; the split put both files under the 400-line bar
  and the flag is gone (check log cmds 4 vs 9). House law honored: fixed, not
  baselined; hook never loosened.

## Serving model (pinned, deterministic, no RNG)

- Requests: each trail row is one serving request, replayed chronologically.
  5,000 most recent rows of 7,389 then on disk (live tree: 7,343 at survey,
  7,374 and 7,377 at the two intermediate runs, 7,389 at the final run; every
  number in this receipt is from the FINAL run's banked JSON), span
  2026-09-15T07:41:27Z .. 2026-10-03T21:59:24Z, 1,366 sessions
  (lane+actor, 30-min inactivity gap).
- Pack shape: byte-identical frozen prefix (synthetic deterministic, 1,024
  chars, sha256-pinned per lane/actor in the JSON output) + the session's
  append-only transcript of real row bytes, hard-clipped to 4,800 chars with
  the estate clip shape (mag/context_pack.py:1414-1416). Frozen-prefix law:
  mag/context_pack.py:467-526 (freeze_system_prompt, A2). Budget:
  mag/context_pack.py:67 ("max_chars": 4800, janitor).
- db.sqlite: pinned out at probe start (not found at repo root) - the M3
  card's named contingency; trails alone.
- Limitation named: the frozen prefix models a real system prompt's SIZE and
  determinism; it is not the estate's live-rendered prompt.

## The curve (the G1 null, final run)

| cap_blocks | cap_chars | hit_rate | evictions |
|---|---|---|---|
| 2 | 512 | 0.0339 | 55874 |
| 8 | 2048 | 0.1586 | 48264 |
| 16 | 4096 | 0.4142 | 32672 |
| 32 | 8192 | 0.7720 | 10844 |
| 64 | 16384 | 0.9261 | 1414 |
| 128 | 32768 | 0.9381 | 619 |
| 256 | 65536 | 0.9388 | 452 |
| 1024 | 262144 | 0.9388 | 0 |
| 8192 | 2097152 | 0.9388 | 0 |
| UNBOUNDED | - | 0.9388 | 0 |

- **CLAIM HOLDS**: hit rate at the 8,192-block anchor = **0.93876** (banked
  JSON verdict.hit_rate_at_anchor) vs the 0.80 threshold. External reference
  was 83.48% at 8k blocks on the AgentX subset; the estate's boring baseline
  lands above it. Per the M3 card, this measured number is now the G1 null
  every future eviction/compaction claim must beat or be rejected as
  decoration.
- Knee: the null is capacity-starved below 64 blocks - 0.4142 at 16 blocks,
  0.7720 at 32 blocks (below threshold), 0.9261 at 64. Plateau 0.9388 from
  256 blocks equals the unbounded ceiling (zero evictions at 1,024 blocks
  and up, so the anchor read IS the ceiling for this corpus: the estate's
  5,000-request working set fits in a fraction of the anchor).
- Pack-scale: a cache of ONE 4,800-char pack (19 blocks) serves 0.5045; 4x
  pack (76 blocks) 0.9335; 16x pack 0.9388.
- Assembly arms at the same anchor, same eviction policy, same traffic:
  frozen_append 0.93876, frozen_window 0.376234, volatile 0.001283. Pack
  assembly choice spans three orders of magnitude of hit rate - the M3
  card's "lever is pack budget and assembly, not eviction" branch is
  evidenced by the arms even though the primary claim held. Direct support
  for the A2 frozen-prefix law (mag/context_pack.py:467) and against
  re-render-per-call packs (kv_cache_compaction.md:23, "the last live cache
  killer").
- full_hit_rate reads 0.0000 everywhere: STRUCTURAL, not a bug - 4,800 is
  not block-aligned (18.75 blocks of 256), so no request can fully hit at
  this budget/block pairing. Read hit_rate, not full_hit, here.

## Checks (all run this ask; raw outputs in order)

Check log: watch/inbox/gala_20260925/build-it-all/lanes/m3-lru-null-arm.check.txt

1. `.venv/Scripts/python.exe tools/lru_null_arm.py --self-test` - exit 0,
   11 checks green (prefix share, LRU leaf eviction sequence, internal-block
   survival, evicted-leaf miss, append-only hits, estate clip shape,
   capacity floor, determinism).
2. `.venv/Scripts/python.exe -m pytest tests/test_lru_null_arm.py -q -p
   no:cacheprovider` - 10 passed.
3. `.venv/Scripts/python.exe tools/lru_null_arm.py` - the 5,000-row replay,
   exit 0, JSON banked.
4. `.venv/Scripts/python.exe tools/violation_ratchet.py check --changed` -
   exit 1 pre-fix (my NEW file-too-long + 2 sibling findings), exit 1
   post-fix (2 sibling findings remain, both in files this lane did not
   create or modify: tools/cialdini_scanner.py:53 except-pass, untracked
   sibling file; mag/percolator.py GROWTH 580 -> 1022 lines, pre-existing
   modification). Attribution: git status shows those two paths as `??` and
   `M` respectively, untouched by this lane. Debt accepted by no one here;
   the hook was not loosened; the sibling findings stay for their owners.

## Decision ledger

Closes: the G1 gap law's standing demand is now a MEASURED estate null, not
doctrine. Radix-leaf LRU over 5,000 real estate trail rows at the real
4,800-char pack budget holds 93.88% at the 8k-block anchor and at every
capacity >= 64 blocks, and 50.45% at a one-pack cache. Any future
eviction/compaction proposal must beat this curve on estate tapes (the null
is beatable in principle only below the ~64-block knee - that is where a
candidate must win, and where the external finding says capacity, not
policy, is the real enemy) or be rejected as decoration.

## Banked artifacts

- memory/runs/lru_null_arm/lru_null_arm_results.json (schema
  lru_null_arm.v1, generated 2026-10-03T22:01:03Z, 13 curve points,
  pack-scale points, 3 arms at anchor, verdict.holds=true)
- tools/prefix_cache_sim.py + tools/lru_null_arm.py + tests/test_lru_null_arm.py
- Raw check log: watch/inbox/gala_20260925/build-it-all/lanes/m3-lru-null-arm.check.txt
