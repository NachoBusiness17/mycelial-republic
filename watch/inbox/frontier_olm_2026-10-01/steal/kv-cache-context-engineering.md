# Steal card: kv-cache-context-engineering (frontier olm 2026-10-01, round 2)

Round 2 draft. Applies the three substantive critique fixes: find 4 re-anchored
to the provider seam the estate already holds (FIX 1), the gapwave OWED flipped
to verified (FIX 2), and the 09-30 prior card attached as reverse-GPS with a
re-bank ledger (FIX 3). Two critique minors folded (24-key caveat, probe input
located); one critique minor is itself corrected below (the subreddit label).
Round-1 text is overwritten by this file; round-1's defects are owned in the
Retractions section, not silently patched. Prior-area card:
`watch/inbox/frontier_olm_2026-09-30/steal/kv-cache-context-engineering.md`
(cited below as "prior card" with its line numbers).

## Checks run THIS ask (round 2)

1. **Provider seam census** (my own instruments, full file, this moment):
   `wc -l logs/provider_usage.jsonl` = 77,627 rows (the prior card's Sep-30
   scan read 77,502 at its :8; file grew +125 rows since). Python full-parse
   census: 57,367 rows with BOTH `cache_hit_tokens` and `cache_miss_tokens`
   non-null; 57,540 rows with `cache_miss_tokens` non-null; 40,843 rows with
   `session_id`; 0 bad-JSON lines among cache-field carriers; 173 lines carry
   the substring `cache_hit_tokens` without the top-level key (nested text),
   which is why the substring instrument (`rg -c` = 57,540) and the
   parsed-key instrument (57,367) disagree. Name instrument and moment before
   comparing counts. Sample first cache-field row keys: ts, provider, model,
   calls, prompt_tokens, completion_tokens, tokens, ok, meta,
   cache_hit_tokens, cache_miss_tokens (11 keys, no session_id in that row
   vintage; the prior card's :9 noted the same schema variance).
2. **Reader verified:** `mag/cost_learn.py:28` is
   `USAGE = ROOT / "logs" / "provider_usage.jsonl"`; its docstring (:3-5)
   states the enriched provider seam "now carries cache_hit/miss, latency_ms,
   session_id". `_detect_spikes` (:144-145) buckets rows by UTC hour and flags
   miss/ratio spikes, skipping ollama/test_provider rows (:149-150) and rows
   without cache fields (:151-152). The hour bucket is the fold point for the
   timescale axis below.
3. **FIX 2 verified, OWED flipped:** the ignore-filtered search reproduces my
   round-1 false negative: `rg --files -g "context_economics*"` returns
   nothing (rc 1). The same search with `--no-ignore` finds
   `memory/runs/gapwave/context_economics_1m.md`. Cause: `.gitignore:102` is
   `memory/runs/**` (exceptions at :103-104). File stat: 10,495 bytes, mtime
   Sep 19 22:41. Line 67 verified verbatim on disk: "compaction itself is the
   largest f-generator in the system." (the f term of the crossover formula at
   :61, keep-horizon lever at :65). The estate's own sweep already cited it:
   sweep:33 (FOLD-vs-KEEP economics at context_economics_1m.md:53-:94, doug.sh
   piece at :46) and sweep:57 (the :67 f-generator line).
4. **Prior card read in full; its claims re-verified where I reuse them:**
   `tests/test_context_freeze.py:56` `test_two_consecutive_repack_outputs_share_prefix_hash`
   (module under test `mag.agent_cli as ac` at :16, so `ac.repack_messages` in
   mag/agent_cli.py): two repacks with different live values (:57-60), both
   system prompts split at EVOLVING_TAIL_MARKER and sha256'd (:64-68),
   equal-prefix-hash assert (:69), registry seam hash covers prefix + NUL seam
   + schema bytes (:74-78), byte-identity against the freeze registry (:79).
5. **Sweep label check (one critique minor does not hold):** sweep:41 reads
   "### 4. r/LocalLLM 1wo5552", matching the ask's URL
   (reddit.com/r/LocalLLM/comments/1wo5552). The r/LocalLLaMA labels sit at
   sweep:29 (1wiu7xj) and sweep:35 (1wp5668), different posts. So the card's
   r/LocalLLM label matches both the ask and the sweep and stays. The other
   minor is real and folded: sweep:43 carries "later comment: across 24 API
   keys, not a controlled benchmark" on the 60-88 tok/s figure.
6. **Probe input located (find 1, step 2):** seat transcripts persist at
   `memory/agent_sessions/*.json`: writer `save_session`
   (`mag/agent_cli.py:2965-2970`) writes `messages` into
   `_SESS_DIR = ROOT / "memory" / "agent_sessions"` (:2947) as
   `{session_id}.json` (:2950-2952), fed by `_persist_cli` (:2709-2721, sess
   dict with session_id/provider/model/messages). Real files confirmed by ls:
   cli.json, cursor-bridge-test.json, cursor-phase1-cursor-verify.json,
   deepseek.json, desk-deepseek-test.json, desk-deepseek.json, local.json.
7. **HEAD check:** `git log -1 --format="%h %s"` = 3970fc22b (VONNEGUT FINAL
   CUT). The turn-2 heal is commit 1a1efc67b per the environment git log; it
   is no longer HEAD and this card no longer phrases it as HEAD. The heal
   diff remains unverified by this seat (message-level citation only).
8. **Steer-JSON defect verified first-hand (script owner note):**
   `.zcode/workflows/olm-mine.dwf.ts:383-391` builds the thief ask from the
   finds JSON plus critique only; `card` is in scope at :383 and stashed to
   `lastCard` at :391, but the steer ask at :392-393 interpolates only the .md
   path while telling the reviewer to read "and the returned card JSON".
   Same defect the prior card recorded at its :73 with the then-path
   `.zcode/workflows/../workflow-drafts/frontier-olm-mine.dwf.ts:367-371`; the
   script has since moved to `.zcode/workflows/olm-mine.dwf.ts`. Fix belongs
   to the script owner: interpolate `JSON.stringify(card)` into the steer ask.
   Until then "all confidence 1" on the finds is unverifiable by the steer
   seat from the ask alone.

## Retractions (round-1 defects owned)

1. Round-1 claimed the estate "records no cache hit/miss split" and proposed a
   one-field extension to the hermes burn row schema. WRONG: the provider seam
   `logs/provider_usage.jsonl` has carried cache_hit/miss tokens since at
   least 2026-08-30 (earliest cache+session row in the prior card's scan),
   read by `mag/cost_learn.py:28`. The proposal is retracted as re-banked
   work; the round-1 find-4 falsifier (gap-vs-miss correlation on
   `memory/runs/hermes_burn/usage.jsonl`) was unrunnable as written, because
   that ledger's 8 fields carry no cache split (verified round 1: `rg -i
   "cache"` over `tools/hermes_burn.py` returns zero matches; row schema read
   at `memory/runs/hermes_burn/usage.jsonl:1-3`).
2. Round-1's OWED on `context_economics_1m.md` was a false negative caused by
   an ignore-filtered rg (`.gitignore:102`); the file exists and line 67 is
   verbatim as the find metadata claimed. Lesson banked: an absence verdict
   from a gitignore-respecting search over an ignored tree is not an absence.
3. Round-1 never cited the 09-30 prior card on this same area key; fixed by
   the re-bank ledger below.

## Re-bank ledger (prior card as reverse-GPS)

Re-banked, already estate-held (labeled, not re-derived):

- Find 2's prefix-stability mechanism: built as `mag_context_freeze.v1`
  (sorted serialization, per-session sha256 over prefix + NUL seam + schema
  bytes, `mag/context_pack.py:505-526`) and PROVEN by the landed test
  (`tests/test_context_freeze.py:56-79`). The prior card's :35 already split
  this exact probe into banked (the test) and open (live-provider) halves;
  this card adopts that split instead of re-deriving it.
- Find 4's measurement substrate: `logs/provider_usage.jsonl` cache fields
  (census above) + the prior card's primary probe (:62-64), which already
  specs the inter-request-gap miss decomposition on the session-tagged
  cache-field subset with the denominator law attached. This card adds only a
  timescale readout on that same subset; it does not re-spec the probe.

Genuinely new in this round's five finds:

- Find 1's 61-day reach-ratio instrument (emitted-vs-transcript byte diff),
  the resident/paged/interrupt regime taxonomy, the 10k-unit hook-output
  ceiling with the 5-slice fix shape. Nothing estate-side meters reach;
  arch-01's 0/6 core-reach measurement (`mag/context_pack.py:54-61`,
  :1176, :1377) was a one-off, not a standing meter.
- Find 3's SoulScript mechanism with field numbers: 1.8 years of per-turn
  retrieval of 1-2k sectioned tokens beating a static 15k blob, per-section
  SHA-256 manifest for drift attribution, and the small-model caveat landing
  on gemma:2b. The sweep's own overlap note (:51) says memweave holds the
  doctrine without external field numbers; this supplies them.
- Find 4's slow-timescale attribution lever (misses concentrate in
  human-review gaps) plus the 85% input-savings anchor: a causal lever
  framing the prior card's mechanical gap bucketing does not claim.
- Find 5's restart-and-diff post-compaction correctness gate: the prior card
  holds compaction economics, not a correctness gate; window-1's carrier
  defect (`watch/inbox/hermes_burn/WINDOW1_STATE.md:30-34`, turn-2 echo +
  force-refire duplicate $0.25) gives the gate a live target.
- Find 2's remainder: the capacity-side envelope (2B tokens/week, 0
  preemptions, 38.6% peak KV, 60-88 tok/s per user across 24 API keys, not a
  controlled benchmark per sweep:43; FP8 KV, 262K max per request, shared
  pool) and the unmetered-behavior corollary for the fleet burn profile.

## Find-by-find estate map

### 1. The 61-day instrumentation (r/LLMDevs 1wu24sc, 2026-09-30)

Find: 96.6% of context removed in one compaction (607,378 to 20,766 tokens), 8
of 36 pre-summary messages left no trace; a project-map hook reported success
while only ~11% of its 18,057 bytes reached the model (output above 10,000
units goes to a file, only a ~2KB preview reaches the model); the only check
that caught it was byte-by-byte emitted-vs-transcript comparison; fix shape:
ship the map in 5 slices under the ceiling; resident/paged/interrupt taxonomy.
Sweep: `watch/inbox/frontier_olm_2026-10-01/sweep/kv-cache-context-engineering-reddit.md:25`.
Organ: context pack (`mag/context_pack.py`). Anchor: arch-01 measured the
mandated core reaching the model 0/6 live renders and the old janitor budgets
(1200/1800 chars) were smaller than the uncapped objective alone (2.2k)
(`mag/context_pack.py:54-61`; measured-tier notes :1176, :1377). The emit is
already hashed and counted per session (`prefix_hash`/`prefix_chars`,
`mag/context_pack.py:516-524`) and sheds are logged (`PACK_OFFLOAD.jsonl`,
`mag/context_pack.py:17,35-50`). Port: turn the one-off into a standing reach
meter (probe below) and redesign MODE_CONFIG (`mag/context_pack.py:62-90`)
around resident (always rendered), paged (rendered on open), interrupt
(rendered on event) regimes; slice any payload over the 10k-unit class ceiling.

### 2. 2B shared-prefix tokens on one card (r/LocalLLM 1wo5552, 2026-09-23)

Find: 96GB card, 2B tokens/week, 0 preemptions, 38.6% peak KV, 60-88 tok/s per
user across 24 API keys (later comment: not a controlled benchmark, sweep:43),
FP8 KV shared pool; "most of the prefill never gets recomputed"; unmetered
users stop trimming context. Sweep: :41-45. Organ: context freeze + quantizer.
Mechanism RE-BANKED (test landed, prior card :35); the capacity envelope and
the behavioral corollary are the new halves. Port: verify every rendered
janitor turn keeps the freeze byte-stable (the freeze already covers the tool
schema layer, `mag/context_pack.py:511-515`, answering the template-mutation
warning at sweep:73), then measure the local envelope (KV occupancy, tok/s
under N concurrent janitor sessions). Local numbers OWED until measured. Probe
(adopted from prior card :35, open half): run the same session_id through
`repack_messages` against a live provider twice and assert the second call's
row in `logs/provider_usage.jsonl` shows hit-classed cache fields; falsifier:
prefix_hash stable but hit ratio unmoved means the freeze sits in a dead path
or cache identity includes more than bytes. The round-1 Ollama timing A/B
(10 identical-prefix vs 10 mutated-prefix gemma:2b requests) stays as an
optional local-tier complement, not the primary.

### 3. Soul script: per-turn retrieval over a sectioned manifest (r/LLMDevs 1wu780a, 2026-09-30)

Find: "A 15k-token character bible dilutes itself. The model treats all of it
as equally important, which in practice means none of it is."; rebuild the
prompt every turn in layers, retrieve the right 1-2k tokens of a heading-split,
per-section embedded script; manifest.json indexes every section with a
SHA-256 hash so drift attributes to edits vs model; stated limit: smaller
local models follow injected sections less reliably. Sweep: :47-51. Organ:
memweave + context pack. Memweave holds the law with a falsifier
(`.agents/skills/memweave/SKILL.md:13-15,26-28`); the find adds the field
numbers and the governance mechanism. Port: extend the pack to a per-section
sha256 manifest (hashlib already in use, `mag/context_pack.py:4,512`),
retrieve 1-2k tokens per turn by mode instead of one full render, log
retrieved section ids + hashes beside the shed log, and A/B on gemma:2b
before any default flip (the small-model caveat). Probe: 20-task A/B on
gemma:2b, full-blob pack vs 1.5k-token sectioned retrieval, graded on
compliance checks (em-dash law obedience, correct rib citation); falsifier:
blob matches or beats sections on the local tier means sectioning stays
remote-tier only.

### 4. When prompt caching pays off (r/LLMDevs 1wug1mo, 2026-09-30)

Find: ~85% input token cost savings from prompt caching; misses concentrate
in the slow timescale (human review of output), not the fast agentic loop;
levers: work-pattern pacing, non-default cache expiry, trimming mean
slow-timescale time. Sweep: :53-57. Organ: water graph cost instrument
(`mag/cost_learn.py`). Substrate ALREADY BANKED (round-1 retraction above):
`logs/provider_usage.jsonl` carries the cache split (census in Checks), read
by `mag/cost_learn.py:28`. The gapwave anchor is VERIFIED this ask:
`memory/runs/gapwave/context_economics_1m.md:67` verbatim ("compaction itself
is the largest f-generator in the system"), crossover formula at :61,
keep-horizon at :65; already cited by sweep:33 and :57. Port: pacing levers in
the descent protocol (batch premium turns so human-review gaps do not land on
cache expiry; non-default cache expiry as a named spend lever) plus the
timescale readout below folded into `_detect_spikes`
(`mag/cost_learn.py:144-145`, hour bucket today; ollama/test_provider and
cache-less rows already excluded :149-152). Probe (timescale readout on the
prior card's subset, not a new probe): on rows with session_id and both cache
fields non-null (prior card's Sep-30 joint scan: 40,842 rows, 1,926 distinct
sessions, its :8; today's session-tagged count 40,843, joint count not
recomputed this ask), group by session_id, order by ts, bucket consecutive
intra-session gaps (<=10s / 10s-5min / >=5min), and compute per-bucket
miss share = sum(cache_miss_tokens) / sum(cache_hit_tokens +
cache_miss_tokens). Prediction (the find): the >=5min human-review bucket
holds the dominant miss share. Falsifier: miss share flat across buckets, or
concentrated in the <=10s bucket, which would instead support the prior
card's tight-loop capacity reading (its field data: 33.1% of recompute
inside 10 seconds, 17.5% past the 5-minute TTL, its :16,:23). Denominator
law per prior card :64: report on the subset only, name the moment.

### 5. The post-compaction restart-and-diff test (r/LocalLLM 1wutse7, 2026-10-01)

Find: "A summary can read fine and still lose 'we already sent that email'";
test: restart from the summary and see if any completed action gets repeated.
Sweep: :59-67. Organ: gopher fleet verification gate (workflow-gate scenario
cards, `configs/workflow_gate_scenarios`). Estate anchor: window-1 named the
defect class in its own carrier, turn-2 revision empty with assistant-echo
suspected and force-refire re-running turn 1 (B2 duplicate $0.25)
(`watch/inbox/hermes_burn/WINDOW1_STATE.md:30-34`); the heal landed as
turn-2 no-echo + turn2_only with a 3/3 revision pass (commit 1a1efc67b per
the environment git log; not HEAD, HEAD is 3970fc22b; heal diff not
independently re-verified by this seat). What the estate lacks is the
gradable check. Port: add a post-compaction scenario card: replay the seat
from the summary, diff the executed-action list against pre-compaction, FAIL
on any repeated completed action. Probe: replay the window-1 carrier from its
turn-1 output with the echo heal in place, count duplicated completed actions
across replays; falsifier: zero repeats proves the heal holds or shows the
test is insensitive at this session length, either way a banked gate-design
result.

## The one probe this week

Reach-ratio meter (find 1), because every input now has a named source and it
costs zero new spend:

1. Run `mag.cmd context-pack` for the janitor mode; capture the emitted bytes
   and the frozen `prefix_hash`/`prefix_chars` (`mag/context_pack.py:516-524`).
2. Read one existing seat transcript, e.g.
   `memory/agent_sessions/desk-deepseek.json` (confirmed on disk this ask;
   writer `mag/agent_cli.py:2965-2970`), and extract the byte content of its
   first system+user messages.
3. Reach ratio = transcript-contained bytes / emitted bytes; log it next to
   the PACK_OFFLOAD row (`mag/context_pack.py:17,35-50`).
4. Falsifiable prediction, stated before running: reach ratio at or above 90%
   on the janitor tier means the find's ~11% does not transfer to this stack
   and the meter stays a spot-check; materially lower and the 10k-unit slice
   ceiling plus the resident/paged/interrupt MODE_CONFIG redesign
   (`mag/context_pack.py:62-90`) becomes the week's implementation lane.

## OWED / not run

- Reddit bodies were NOT re-fetched in either round (miner's archive-API
  degradation recorded in the ask); all five finds cross-checked against the
  estate's own sweep bytes at sweep:25,43,49,55,67,73,75.
- No probe EXECUTED; the only executions this ask are the censuses, greps,
  and file reads listed under Checks. All probes are specced with falsifiers.
- Local-tier KV occupancy and tok/s envelope: never measured (find 2).
- The joint cache+session row count for TODAY was not computed (only the
  prior card's Sep-30 figure 40,842 and today's session-tagged 40,843);
  the find-4 probe must run its own joint count before reporting shares.
- Heal diff for commit 1a1efc67b: cited from the commit message, not re-read.
- Script-owner note (not a card defect): interpolate `JSON.stringify(card)`
  into the steer ask at `.zcode/workflows/olm-mine.dwf.ts:392-393` so the
  reviewer can check the returned card against the write-up; recorded by the
  prior card at its :73 for the previous script path as well.
