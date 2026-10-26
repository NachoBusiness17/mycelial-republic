# LAND L1: the schema door (comics lane, 2026-10-07)

Seat: comics L1 landing lane. Fold: SYNTHESIS.md moves 1+7 (this directory).
Law: repo venv interpreter only, no em-dashes, no git commit (working tree
left for the fence owner).

## 1. What landed in code

tools/free_lane_fleet.py (400 lines, at the ratchet FILE_LINE_CAP exactly):

- fire() gains a typed-schema pass-through keyed off the queue item, never
  hardcoded: `fire(p, prompt, schema=None)`. Openai-kind bodies carry
  `response_format` in the json_schema shape when the item has a schema;
  ollama bodies carry `format` = the json schema itself; cohere is left
  as-is (no response_format on v2, per the fold's instruction).
- cycle() carries `schema` from queue items into fire() and banks a
  `schema` boolean flag on every ok ledger row (all 20 econ2 ledger rows
  read schema True; verified memory/runs/free_lane_fleet/ledger.jsonl).
- The cohere content-block join relocated to the message-content path per
  the fold's :284-293 note: the join now runs AFTER the content fallback
  chain, so the top-level `message.content` blocks cohere v2 actually
  returns are joined instead of str()-ed into a python repr (the arm-A
  a03/a04/a13 defect). d4 reasoning_content fallback preserved.
- Queue contract widened in the module docstring: {id, kind, prompt,
  max_tokens?, schema?}.

Tests: tests/test_free_lane_fleet_schema.py, 8 tests, network-free
(_OPENER stubbed; cycle() runs a stubbed fire() against tmp roots).
Result: 8 passed; plus tests/test_gstd_fleet_provider.py 13 passed
(the queue consumer) = 21 passed, 0 failed, this sitting.

## 2. The restage (13 arm-A subjects as schema trials)

probe_comics_schema_restage.py --stage dropped 13 queue files
(comic:econ2:a01..a13, arm-A subjects byte-identical, arm-B typed schema,
arm-B instruction prompt). One `--cycle` fired 10, banked 10, 0 failures,
providers healthy 5/7 (both openrouter seats fenced at consecutive_fails
6 and 5, the fold's known dead rail). a11-a13 remain queued for the next
hourly cron pass (named pending, not dropped).

Collision note, honestly banked: the hourly fleet schtask fired inside my
window, so each of a01-a10 fired TWICE (ledger ts 20:52:49Z to 20:54:15Z).
Every id's json_ok verdict is identical across both firings (10/10
agreement, checked this sitting), so the graded line is cycle-independent;
scores read the last row per id.

Grades (econ_probe_restage_schema.json, this directory):

| seat | door | fired | json_ok | PASS |
|---|---|---|---|---|
| open-mistral-nemo (mistral) | response_format json_schema | 2 | 2 | 2 |
| qwen2.5:7b (ollama-local) | format = schema | 2 | 2 | 2 |
| meta/llama-3.2-11b (nvidia-1+2) | response_format json_schema | 4 | 0 | 0 |
| command-r7b-12-2024 (cohere) | none (left as-is) | 2 | 0 | 0 |

vs arm-B baseline 10/10 json_ok (econ_probe_results_arm_b.json): the
enforcing seats hold the class (mistral + qwen 4/4 json_ok, 4/4 PASS);
the door is seat-dependent, which is the finding:

- NVIDIA accepts response_format and IGNORES it: 200 OK, then markdown-
  fenced JSON that also violates the schema (pose as arrays, who off-enum
  actor/director/judge; raws banked in econ_probe_restage_schema.json).
- Cohere (no door by design) also fences; its text would parse leniently
  but the register's mechanical gate stays strict parse, like the gauntlet.
- vs arm-A line grammar 2/13 PASS through the same queue door: schema
  items went 4/10 PASS with every json_ok also a full PASS.

## 3. The gemma:2b no-instruction verdict

gemma2b_noinstruction_result.json (this directory): ONE fire at gemma:2b,
schema ON (format = json schema), prompt reduced to the bare subject (the
instruction preamble dropped entirely), temp 0.3. Result: json_ok TRUE,
3 panels, in_vocab TRUE, caps_ok TRUE, verdict PASS, 15985 ms. Banked arm-B
twin with the instruction (econ_probe_results_arm_b.json gemma row 1, same
subject): json_ok TRUE but caps_ok FAIL, 17518 ms.

Verdict: the format door ALONE rescues gemma:2b on this task. With zero
instruction the schema-constrained sampler emitted a fully valid spec, and
the instructed run's caps failure was variance, not instruction-dependent.
The door buys structure, not speed: 15985 ms no-instruction vs 17518 ms
instructed (both cold-ish first calls; arm-B gemma median was 4942 ms), so
instruction removal bought no latency here. Caveat: n=1, temp 0.3, single
subject. Deviation named: fired direct at ollama, not through the queue,
because the fleet's ollama seat is qwen2.5:7b by PROVIDERS law and a queue
item cannot address gemma:2b; the queue pass-through itself is exercised
by the 13 restage items above.

## 4. Erratum landed

accuracy.md (this directory): the phantom discord-api-docs issue #25935
cite in F4(a) is struck inline and a dated ERRATUM section is appended
(amend-never-rewrite). The SVG-non-rendering fact survives on its own
corroboration (docs.discord.com/developers/reference, web fetch, this
fold); only the issue number dies.

## 5. Gates

- One fleet cycle with schema items: clean (fired 10, banked 10, 0 fail).
- pytest: 21 passed across tests/test_free_lane_fleet_schema.py (8, new)
  and tests/test_gstd_fleet_provider.py (13).
- Ratchet: tools/violation_ratchet.py check --changed reports zero NEW
  rows for tools/free_lane_fleet.py and tests/; the NEW rows it does
  report are sibling-seat working-tree files (blast_radius_probe.py,
  classify_probe.py, longrunner_patrol.py), pre-existing, not touched by
  this lane. free_lane_fleet.py sits at exactly 400 lines, under the cap.
- No git commit made.

## 6. Owed forward

- a11-a13 fire on the next hourly cron; rescore with --score after.
- The nvidia ignores-response_format finding wants a second cell before it
  is called law (n=4 here, one sitting).
- gemma:2b no-instruction at n>1 and multiple subjects before the
  rescue-not-latency wording hardens.
