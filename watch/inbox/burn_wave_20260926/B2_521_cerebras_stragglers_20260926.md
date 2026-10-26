# B2-521 Cerebras straggler consumers gated on the B2-133 dormant flag (2026-09-26)

## Verdict

LANDED. The six remaining hardcoded cerebras consumers outside the B2-133 seven now
gate on the same flag-derived helper (mag/dormant.py), one law, no new machinery:
mag/swarm_worker.py DEFAULT_PROVIDER (was the literal "cerebras", now derived from
the ZAI_LITE_LAW order through dormant_ids: groq while the flag stands, cerebras
returns on operator GO with no code edit), mag/_consensus_witness.py LANES
(cerebras witness seat drops, same filter shape as rotation_harness),
mag/scale_salon.py (api.cerebras.ai out of the SSRF ALLOWED_BASES by dormant-host
match, cerebras-oss architect out of the gophers and writer lenses by resolving
each id through the already-gated research_fanout LANES table), mag/ask_router.py
LANE_TIERS (cerebras and nvidia tier-0 rows drop, so the dormant lane loses its
best cost prior), mag/subscriptions.py free_lanes display row (built from the live
backbone roster: name, note, and keys no longer claim "cerebras 85%" or carry
CEREBAS_API_KEY), mag/seat_corpus.py SEND_LAWS (cerebras and nvidia registry rows
drop, and the stale latest.json artifact that advertised them to OpenClaw was
recompiled: 14 lanes, zero dormant provider rows). One new test
(tests/test_dormant_gate_b2521.py, 1 wiring case with premise assert); 38 tests
green across every test file that imports the six touched modules; ratchet NEW=0
on every file this lane touched.

## Evidence with file:line quotes

- The flag owner, configs/providers.yaml:690 "dormant: true" on the cerebras
  block (B2-36 landing); live dormant roster read from bytes at run time:
  saelis, gemini, mistral, cerebras, nvidia.
- Gated state verified by import after the edit (all six modules, one session):
  swarm_worker.DEFAULT_PROVIDER = 'groq'; _consensus_witness.LANES = [('z_ai',
  'z_ai', 'glm-4.7-flash', ...), ('groq', 'groq', None, {})] (cerebras seat
  gone); ask_router.LANE_TIERS = {groq 0, openrouter 0, ollama 0, deepseek 1,
  zai 2, openai 3, anthropic 3, xai 3} (cerebras and nvidia rows gone);
  subscriptions free_lanes name "Free lanes (groq/z_ai/ollama free)", keys
  ['GROQ_API_KEY'], note "The backbone: groq 91% ok, z_ai 81%, ollama local."
  (cerebras 85%, nvidia credits, CEREBAS_API_KEY gone); seat_corpus.SEND_LAWS
  ids = 14 lanes, no cerebras/nvidia; scale_salon.ALLOWED_BASES = groq, z.ai,
  openrouter bases only (api.cerebras.ai and api.mistral.ai dropped by host
  match), _GOPHERS = ['groq-oss20'] (cerebras-oss architect dropped),
  WRITER_LENSES ids = ['groq-qwen', 'groq-oss', 'groq-oss20', 'or-glm52',
  'or-nemotron', 'or-ling3'] (cerebras-oss dormant-dropped; mistral-min8 and
  mistral-small dropped on the mistral dormant host; zai-air already absent
  from LANES, retired 2026-09-16 per the research_fanout comment, so filtering
  by LANES membership is behavior-preserving: main() could never fire it).
- Gate code locations: mag/swarm_worker.py:63-74 (gate comment, import :70,
  _SWARM_DEFAULT_ORDER :72, derived DEFAULT_PROVIDER :73); mag/
  _consensus_witness.py:26-34 (filter :34); mag/scale_salon.py:30-56 (gate
  comment, import :39, _lane_live :44-48, ALLOWED_BASES comprehension :50-56),
  :145 (_GOPHERS), :162 (WRITER_LENSES filter), :212 (main loops _GOPHERS);
  mag/ask_router.py:29-40 (filter :39); mag/subscriptions.py:51-67 (_LIVE
  _BACKBONE :67) plus the free_lanes row built from it; mag/seat_corpus.py:
  190-200 (SEND_LAWS comprehension :199).
- Every remaining "cerebras" byte in the six files is gated-roster data that
  returns on operator GO (the archived row tuples and the receipt comments),
  not a live path: full grep census filed above in the gate-code listing.
  The falsifier's live-path condition is therefore disproven at import time.
- Tests: tests/test_dormant_gate_b2521.py (premise assert that cerebras is
  still flagged dormant, then: swarm default not dormant and == groq; witness
  LANES disjoint from dormant ids; every scale_salon ALLOWED_BASES host
  non-dormant and every selectable gopher/writer id resolving through the gated
  LANES table on a non-dormant host with cerebras-oss absent; LANE_TIERS
  disjoint; free_lanes row name/note/keys free of dormant claims; SEND_LAWS
  disjoint). Run with every test file importing the six modules:
  tests/test_dormant_gate_b2521.py + test_dormant_gate_b2133.py +
  test_seat_corpus.py + test_swarm_local_drain.py + test_swarm_quota_gate.py +
  test_loop_death_guards.py = 38 passed, 0 failed; test_cost_truth.py (imports
  SUBSCRIPTIONS from mag.subscriptions at :443) = 3 passed.
- Pre-existing failures documented, not this lane's: tests/test_organ_map.py
  test_map_separates_callable_from_live (atlas LIVE promotion wants a recent
  fireball receipt; memory/runs/atlas mtime Aug 30) and
  test_map_and_elder_surface_callable_orphans (elder gap ask_router
  receipt_stale; memory/runs/ask_router/receipts.jsonl mtime Aug 31, 26 days
  before today). Both are receipt-recency rot measured against 2026-09-26; the
  same test file's assert that ask_router callable_imports is True PASSES, so
  the new gate import does not break the organ map. A git index.lock from a
  parallel lane blocked a stash-based clean-tree re-run; the mtime evidence
  stands in its place.
- Ratchet (tools/violation_ratchet.py check --changed): NEW=5, every row in
  other lanes' in-flight tools/ files (tools/openrouter_free_gate.py:84,
  tools/probe20_run.py:421, tools/queue_dupes_check.py:33,
  tools/transport_precheck.py:134, tools/visor.py:131); zero NEW rows on any
  file this lane touched. Not this lane's debt to accept, matching the B2-133
  precedent.
- Em-dash law: zero em-dashes on any line this lane authored (checked by
  pattern scan over every line carrying the new gate identifiers and comment
  markers, plus full-file em-dash census where every hit maps to a legacy line
  carried verbatim or untouched: swarm_worker docstring and 09-05 history
  comment, seat_corpus legacy rows, subscriptions legacy rows, ask_router:238,
  scale_salon none).
- Artifact honesty: memory/runs/seat_corpus/latest.json carried 3 cerebras
  mentions before this lane (stale compile, pre-gate); recompiled via
  python -m mag.seat_corpus compile; now 14 lanes, zero dormant provider rows;
  the single surviving "nvidia" byte is the model id
  nvidia/nemotron-3.5-lightning:free inside the openrouter lane's model
  catalog (served through OpenRouter, not the dormant nvidia provider), left
  correctly.

## Work done

1. Read the pointers (B2-133 receipt, mag/dormant.py, the B2-133 gates in
   fuel_feed and research_fanout) and all six named sites before touching
   bytes; confirmed scale_salon imports the already-gated research_fanout
   LANES and that no other module imports scale_salon's gated symbols
   (mag/lite_scale.py imports only PARABLE, CANON, CONSTRAINTS, WRITER_HEAD,
   OUT, _now).
2. Wired six gates, each with a receipt comment naming the law
   (mag/doctor.py:607), the cause (B2-36, plus B2-61 for the nvidia rows the
   same general gate catches in ask_router, subscriptions, seat_corpus) and
   the restore path (operator GO flips the flag, no code edit). swarm_worker
   derives its default from the ZAI_LITE_LAW order instead of a second
   hardcoded literal; subscriptions rebuilds the free_lanes row from the live
   backbone roster with the key envs carried exactly as the row had them.
3. Spec-first: each gate comment is the spec line for its behavior; the
   seat_corpus pin test premise was updated in the same landing because the
   new law makes the old pin (cerebras, nvidia in SEND_LAWS) false.
4. Added tests/test_dormant_gate_b2521.py; ran it plus every test file that
   imports the touched modules: 38 passed, 0 failed, plus test_cost_truth
   3 passed.
5. Recompiled the seat_corpus artifact so OpenClaw stops reading a cerebras
   drive-law, and counted the one surviving model-id mention rather than
   burying it.
6. Verified the em-dash law and the ratchet over the changed file set; filed
   this receipt, the LEDGER row, self-feed briefs, and ticked the QUEUE row.

## Falsifier

This lane is inverted if: (a) any of the six sites serves a dormant provider
again while the flag stands: `from mag import swarm_worker;
swarm_worker.DEFAULT_PROVIDER == 'cerebras'` returning True while
mag.dormant.dormant_ids() still contains cerebras means the gate was removed
or bypassed (the new wiring test asserts the same and fails first); (b)
providers.yaml loses the cerebras dormant flag without an operator GO record:
the test's premise assert ("B2-521 premise gone") fails loudly at the next run
instead of rotting, and the gates then correctly admit the lanes; (c) operator
GO lands and the rows do NOT come back (someone deleted entries instead of
gating): the same premise assert fires and the GO restore path is proven dead;
(d) scale_salon's _lane_live silently eats a new writer lane: a future
WRITER_LENSES row whose id is absent from research_fanout.LANES drops without a
trace (zai-air precedent). Mitigation: add the lane to research_fanout.LANES
first; the wiring test's laned.get(lane_id) assert then proves it selectable.

## Bibliography closed

Brief row: watch/inbox/burn_wave_20260926/QUEUE.md:206 (B2-521). Flag owner:
configs/providers.yaml (cerebras block, dormant: true at :690; gitignored per
B2-35 note, so this landing is the live file). Laws: mag/doctor.py:607 (dormant
is a declared state), models/quota.py:388-396 (B2-204 dormant never pickable),
mag/dormant.py (the B2-133 one-reader helper). Precedent receipt:
watch/inbox/burn_wave_20260926/B2_133_cerebras_purge_20260926.md. Sources
edited: mag/swarm_worker.py, mag/_consensus_witness.py, mag/scale_salon.py,
mag/ask_router.py, mag/subscriptions.py, mag/seat_corpus.py,
tests/test_dormant_gate_b2521.py (new), tests/test_seat_corpus.py (pin
premise), memory/runs/seat_corpus/latest.json (regenerated artifact). Imports
read for blast radius: mag/swarm_surface.py:84 (rides DEFAULT_PROVIDER),
mag/cost_truth.py:443 (reads SUBSCRIPTIONS), mag/lite_scale.py:21 (scale_salon
prompt constants only), mag/afk_cadence.py:222, mag/api_gateway.py:672,
mag/dogfood_audit.py:192 (import mag.ask_router as a package module, so the
module-level gate import is safe). Test files read:
tests/test_organ_map.py:16,60 (pre-existing receipt-recency failures),
tests/test_zai_burst.py (B2-133 lane-pin precedent). LEDGER:
memory/burns/LEDGER.jsonl (row appended this date).
