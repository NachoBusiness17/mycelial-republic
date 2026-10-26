# B2-133 Cerebras consumer purge in mag/ code (2026-09-26)

## Verdict

LANDED. The providers.yaml `dormant` flag now gates every mag/ hardcoded lane
list and the cost view. New reader `mag/dormant.py` (one law, one reader) plus
seven gate blocks: fuel_feed FREE_LANES, rotation_harness LANES, lane_salon
WITNESSES, quorum_window FREE_LANES, research_fanout LANES (host match),
cost_truth _PROVIDER_FREE_OR_CREDIT, free_tier FREE_SURFACES. Cerebras (B2-36
dormant, card-gated trial, chat 402 no-credit) is out of all seven; operator GO
flips the flag and every gate restores the lane with no code edit, matching the
GO note carried on the cerebras block itself. The same flag-derived gate caught
nvidia and mistral where they were hardcoded (dormant per B2-61), the exact
general law B2-204 already set at the quota seam. One new test
(tests/test_dormant_gate_b2133.py, 2 cases); 51 tests green across the touched
neighborhoods; ratchet NEW=0 on every file this lane touched.

## Evidence with file:line quotes

- The flag owner, configs/providers.yaml:690 "dormant: true   # card-gated
  trial; operator GO flips this + re-adds to prefer_order" (cerebras block,
  B2-36 landing). Full live dormant roster read from bytes by the new helper:
  saelis providers.yaml:64, gemini :473, mistral :627, cerebras :690, nvidia
  :734 (all "dormant: true").
- Post-gate lists, verified by import after the edit: mag/fuel_feed
  FREE_LANES = ['ox', 'openrouter-a1', 'openrouter-a2', 'groq', 'z_ai3'],
  FAST_LANES = ['groq'], STRONG_LANES = ['ox', 'openrouter-a1',
  'openrouter-a2']; mag/rotation_harness LANES = [('groq', None)];
  mag/lane_salon WITNESSES = ['grok-cli', 'openrouter', 'groq', 'together',
  'deepseek-pro']; mag/quorum_window FREE_LANES = ['groq', 'openrouter'];
  mag/research_fanout LANES = ['groq-qwen', 'groq-oss', 'groq-oss20',
  'zai-lite', 'or-union-alpha', 'or-glm52', 'or-nemotron', 'or-ling3'];
  mag/cost_truth _PROVIDER_FREE_OR_CREDIT = ['groq', 'together'];
  mag/free_tier FREE_SURFACES = ['z_ai3', 'groq', 'openrouter-a1',
  'openrouter-a2', 'ox', 'together', 'ollama', 'coding_plan', 'grok_free',
  'nous']. Cerebras absent from all seven; nvidia gone from fuel_feed /
  lane_salon / quorum_window / cost_truth / free_tier; mistral gone from
  research_fanout (its base_url host api.mistral.ai matches the dormant block).
- Pricing seam, live check: mag/cost_truth._lookup_rate('cerebras',
  'gpt-oss-120b') now returns state 'unpriced'; nvidia 'unpriced'; groq control
  still 'free_or_quota'. Historical cost-truth consequence, counted from bytes:
  logs/provider_usage.jsonl carries 165 cerebras rows and 135 nvidia rows that
  re-price from free_or_quota to unpriced (configs/cost_rates.yaml carries no
  model rates for either provider, only deepseek-v4-flash/pro).
- Tests: tests/test_dormant_gate_b2133.py (helper truth from a synthetic yaml,
  then the live wiring proof "no mag/ lane list carries a currently dormant
  provider"); run with the touched neighborhoods: 15 passed
  (test_cost_truth.py, test_zai_burst.py fuel-feed cache-lane pin,
  test_quorum_p4_selfvote.py) and 36 passed (test_loop_death_guards.py
  lane_salon fail-closed, test_frontier_salon.py, test_room_tags.py); 51 total,
  0 failed.
- Ratchet (tools/violation_ratchet.py check --changed): zero NEW rows on any
  file this lane touched (mag/dormant.py, the 7 consumers, the test). The FAIL
  rows the run prints belong to other lanes' in-flight files
  (mag/shared_surface.py:426, tools/openrouter_free_gate.py:84,
  tools/probe20_run.py:421, tools/queue_dupes_check.py:33,
  tools/transport_precheck.py:134) and are not this lane's debt to accept.
- Em-dash law: zero em-dashes in every line this lane authored (checked by grep
  over the B2-133-marked blocks and the rewritten docstring lines); pre-existing
  em-dashes in untouched legacy lines were left alone.

## Work done

1. Read the pointers (B2-36 receipt, providers.yaml cerebras block) and all 7
   named consumer sites before touching bytes; found the B2-204 precedent
   (models/quota.py:394 "a dormant lane is NEVER pickable") and mirrored its
   general, flag-driven semantics instead of a cerebras-only hack.
2. Wrote mag/dormant.py: dormant_providers/dormant_ids/dormant_hosts/is_dormant
   reading configs/providers.yaml; an unreadable config yields an EMPTY dormant
   set (missing evidence never invents dormancy; dead lanes still down-report
   honestly at call time per each module's own contract).
3. Wired the seven gates at each list's definition, each with a receipt comment
   naming the law (mag/doctor.py:607), the cause (B2-36) and the restore path
   (operator GO flips the flag); research_fanout matches by base_url host
   because its lane ids are lane-local (cerebras-oss, not the provider id).
4. Updated the owning doc lines spec-first: free_tier module docstring
   ("fast -> groq (cerebras dormant-gated via providers.yaml, B2-133)"),
   rotation_harness docstring ("$0: free lanes only, DORMANT-GATED"), fuel_feed
   CEREBRAS WIRED comment ("DORMANT-GATED 2026-09-26").
5. Added tests/test_dormant_gate_b2133.py; ran it plus every test file that
   imports the touched modules: 51 passed, 0 failed.
6. Verified the cost_truth seam change explicitly (cerebras/nvidia unpriced,
   groq control free_or_quota) and counted the historical re-pricing blast
   radius (165 + 135 rows) rather than burying it.
7. Filed this receipt, the LEDGER row, 2 self-feed briefs (B2-521, B2-522), and
   ticked the QUEUE row.

## Falsifier

This lane is inverted if: (a) any gated list serves a dormant provider again
while the flag stands: `from mag import fuel_feed; 'cerebras' in
[l[1] for l in fuel_feed.FREE_LANES]` returning True means a gate block was
removed or bypassed; (b) providers.yaml loses the cerebras dormant flag without
an operator GO record (queue/todo.md P0): the gate then silently re-admits the
lane; the test's premise assert ("B2-133 premise gone") fails loudly at the
next run instead of rotting; (c) operator GO lands and the lanes do NOT come
back (someone deleted entries instead of gating): the same premise assert fires
and the GO restore path is proven dead; (d) the host-match gate over-matches:
a future lane list entry pointing at any base_url whose host equals a dormant
provider's host dies with it (saelis base_url host is 127.0.0.1, so a future
loopback lane in research_fanout would be gated); today no such entry exists
(the 8 surviving fanout lanes are groq/zai/openrouter hosts), but a new
loopback lane must either use a distinct host or carry an explicit exemption.

## Bibliography closed

Brief row: watch/inbox/burn_wave_20260926/QUEUE.md:205 (B2-133). Flag owner:
configs/providers.yaml (cerebras block :662-710; dormant roster :64, :473,
:627, :690, :734; gitignored per B2-35 note, so this landing is the live
file). Laws: mag/doctor.py:607 (dormant is a declared state), models/quota.py:
388-396 (B2-204 dormant never pickable). Reclassify receipt:
watch/inbox/burn_wave_20260926/B2_36_cerebras_reclassify_20260926.md. Sources
edited: mag/fuel_feed.py, mag/rotation_harness.py, mag/lane_salon.py,
mag/quorum_window.py, mag/research_fanout.py, mag/cost_truth.py,
mag/free_tier.py, mag/dormant.py (new), tests/test_dormant_gate_b2133.py
(new). Byte counts: logs/provider_usage.jsonl cerebras rows 165, nvidia rows
135 (grep -c). Test files read for import-time impact:
tests/test_zai_burst.py:67-68 (FREE_LANES/CACHE_LANES pin),
tests/test_loop_death_guards.py:486-496 (lane_salon._witness),
tests/test_quorum_p4_selfvote.py:20, tests/test_cost_truth.py (no cerebras
fixture). LEDGER: memory/burns/LEDGER.jsonl (row appended this date).
