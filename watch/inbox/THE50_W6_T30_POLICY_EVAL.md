# THE 50 · W6 T30 - POLICY-EVAL ENDPOINT (G06 JSON schema + implementation plan)

Filed 2026-09-19 · W6 INSTRUMENTS · program row
`watch/inbox/THE_50_PROGRAM_20260918.md` line 47: "30. Policy-eval endpoint:
JSON schema + implementation (G06) [QUEUED]".
Re-verified 2026-09-25 (T30 verification pass): checker re-run 14/14 pass,
every disk anchor in this file re-checked; see section 5.

Companions filed this session: schema at
`dashboard/schemas/policy_eval.v1.schema.json`, worked-example checker at
`tools/policy_eval_schema_check.py`. Everything below is readable from disk.

## 1. What G06 actually is (grounding)

G06 is row 6 of the GPS 50-wide battery,
`watch/inbox/GPS_BATTERY_20260918.jsonl` line 6, family `steering_theory`:

> CLAIM: agent steering converges on the same primitive everywhere (a tiny
> oracle + plain-English rules + code interpreter): four independent builders
> shipped it in one week. This is convergent evolution, meaning the primitive
> is load-bearing. Begin with THE FLAW. Then: what does convergent evolution
> predict comes NEXT in the design space (standard interfaces? oracle
> exchanges? rule registries?), and which comes first? End with NEXT-STEAL:
> one instruction.

The answered sketch is filed at `memory/runs/gps_50/GPS_PACK.md` line 208
(section "G06 via zai-lite ok=True"). Its ruling, condensed: the first thing
convergent evolution predicts is a STANDARD INTERFACE, because "standards
precede markets"; registries come second (Guardrails Hub, NeMo Guardrails
rails), oracle exchanges last. Its NEXT-STEAL is the literal brief for this
task:

> Draft the policy-eval endpoint spec - one JSON schema, ruleset URI in,
> verdict + span offsets out - and get two of the four builders implementing
> it before anyone ships a registry.

(The other G06s on disk are different registries: the burn2b game target
`memory/runs/fleet_round/burn2b_pack.md` line 3740, and the adv-arc
fleet_dogfood row `memory/runs/adv_arc_50/ADV_ARC_PACK.md` "### G06 via
zai-lite". This task follows the program's own convention - T28 cites G13 and
T29 cites G31, both GPS-battery rows - so battery G06 is the one this task
works. That same disambiguation note is recorded in
`watch/inbox/THE50_W6_T28_MISS_ENTROPY.md` section 1.)

## 2. Fleet translation: what plays each part

- Plain-English rules = the fleet's steering policies. The on-disk store is
  `memory/governance/auto_steer_policies.json`, written by
  `h_governance_auto_steer_add` (`dashboard/rest.py` lines 678-709, route
  `POST /api/v1/governance/auto-steer/add`, row shape `overseer.auto_steer_policy.v1`:
  policy_id, trigger, threshold, action, chain_scope, enabled, installed_at).
  The store is empty on disk today (verified: the file does not exist yet);
  the schema's `inline` mode exists precisely so the wire format can be
  exercised before the store has rows.
- Tiny oracle = the sovereign judgment tier (local classify()/janitor first;
  see `watch/inbox/SOVEREIGN_JUDGMENT_STACK_20260919.md` section 1: local
  replica within ~4 points of hosted on the aligned subset). Confidence
  provenance rides on the T29 harness (`tools/oracle_calibration.py`,
  receipt `watch/inbox/THE50_W6_T29_ORACLE_CALIBRATION.receipt.json`): ECE,
  temperature, and the G31 escalation threshold come from there when a real
  confidence ledger exists.
- Code interpreter = the verbs/tools the verdict gates. The endpoint itself
  NEVER executes the input. Verdicts are proposals: per the shared artifact
  boundary (AGENTS.md), only the switchboard/effect broker authorizes
  effects. A `deny` from this endpoint is a finding, not a kill.

## 3. The wire schema (the G06 JSON schema)

Draft 2020-12, one document with `$defs/request` and `$defs/response`. Filed
JSON-identical at `dashboard/schemas/policy_eval.v1.schema.json` (validate a
request against `#/$defs/request`, a response against `#/$defs/response`).
Ruleset pointer in (URI or inline), verdict + span offsets out - exactly the
G06 shape.

Re-verified 2026-09-25 (T30 verification pass): the schema block below parses
to the same document as the disk file (`json.loads(block) ==
json.loads(disk)` is True) but is not byte-identical; the disk file
pretty-prints the top-level `properties.schema` const across three lines
where the block inlines it. An earlier revision of this file said
"byte-identical"; that claim failed verification and is corrected here to
what is actually true.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "the50.w6.t30.policy_eval.v1",
  "title": "G06 policy-eval wire schema",
  "description": "One wire schema for policy evaluation, per THE 50 W6 T30 (G06 NEXT-STEAL): ruleset pointer in, verdict + span offsets out. Request and response share this document; validate a request against #/$defs/request and a response against #/$defs/response. Span offsets are 0-based character offsets into input.text, end-exclusive, and every span carries its quote so receivers can verify the text did not move.",
  "type": "object",
  "required": ["schema"],
  "properties": {
    "schema": { "const": "the50.w6.t30.policy_eval.v1" }
  },
  "$defs": {
    "rule": {
      "type": "object",
      "description": "One plain-English steering rule inside an inline ruleset.",
      "required": ["rule_id", "text", "decision"],
      "properties": {
        "rule_id": { "type": "string", "minLength": 1, "maxLength": 64 },
        "text": { "type": "string", "minLength": 1, "maxLength": 2000 },
        "decision": { "$ref": "#/$defs/decision" },
        "patterns": {
          "type": "array",
          "description": "Optional literal substrings; a match locates the span this rule fires on.",
          "items": { "type": "string", "minLength": 1 },
          "minItems": 1,
          "maxItems": 16
        }
      },
      "additionalProperties": false
    },
    "decision": {
      "type": "string",
      "enum": ["allow", "deny", "escalate", "abstain"]
    },
    "ruleset_pointer": {
      "description": "Exactly one of uri (resolve against the fleet policy store or any http(s)/file URI) or inline (self-contained ruleset for the two-builder interop test).",
      "type": "object",
      "properties": {
        "sha256": {
          "type": "string",
          "pattern": "^[0-9a-fA-F]{64}$",
          "description": "Optional pin: responder must refuse (422) when the resolved ruleset does not hash to this."
        }
      },
      "oneOf": [
        {
          "required": ["uri"],
          "properties": {
            "uri": {
              "type": "string",
              "minLength": 1,
              "maxLength": 500,
              "anyOf": [
                { "pattern": "^mag://policy/[A-Za-z0-9_.-]+$" },
                { "pattern": "^https?://" },
                { "pattern": "^file://" }
              ]
            }
          }
        },
        {
          "required": ["inline"],
          "properties": {
            "inline": {
              "type": "object",
              "required": ["name", "rules"],
              "properties": {
                "name": { "type": "string", "minLength": 1, "maxLength": 120 },
                "rules": {
                  "type": "array",
                  "items": { "$ref": "#/$defs/rule" },
                  "minItems": 1,
                  "maxItems": 64
                }
              },
              "additionalProperties": false
            }
          }
        }
      ]
    },
    "span": {
      "type": "object",
      "description": "Character attribution of one rule firing: [start, end) into input.text, plus the quote so the receiver can verify offsets survived any normalization. Ordering (end > start) is enforced by the endpoint and by tools/policy_eval_schema_check.py: JSON Schema cannot compare two properties of the same object, so the semantic layer owns that constraint.",
      "required": ["rule_id", "start", "end", "quote"],
      "properties": {
        "rule_id": { "type": "string", "minLength": 1 },
        "start": { "type": "integer", "minimum": 0 },
        "end": { "type": "integer", "minimum": 1 },
        "quote": { "type": "string", "minLength": 1, "maxLength": 500 }
      },
      "additionalProperties": false
    },
    "request": {
      "type": "object",
      "required": ["schema", "policy", "input"],
      "properties": {
        "schema": { "const": "the50.w6.t30.policy_eval.v1" },
        "policy": { "$ref": "#/$defs/ruleset_pointer" },
        "input": {
          "type": "object",
          "required": ["text"],
          "properties": {
            "text": { "type": "string", "minLength": 1, "maxLength": 100000 },
            "context": {
              "type": "object",
              "description": "Free-form caller context (seat, goal id, trace id). The oracle may read it; the schema constrains nothing inside."
            }
          },
          "additionalProperties": false
        },
        "oracle": {
          "type": "object",
          "description": "Optional caller preference for which judgment tier evaluates.",
          "properties": {
            "profile": { "type": "string", "enum": ["local_janitor", "hosted_specialist"] },
            "min_confidence": { "type": "number", "minimum": 0, "maximum": 1 }
          },
          "additionalProperties": false
        },
        "options": {
          "type": "object",
          "properties": {
            "spans": { "type": "boolean", "default": true },
            "explain": { "type": "boolean", "default": true }
          },
          "additionalProperties": false
        }
      },
      "additionalProperties": false
    },
    "response": {
      "type": "object",
      "required": ["ok", "schema", "policy", "verdict"],
      "properties": {
        "ok": { "const": true },
        "schema": { "const": "the50.w6.t30.policy_eval.v1" },
        "policy": {
          "type": "object",
          "required": ["uri", "n_rules"],
          "properties": {
            "uri": { "type": "string", "minLength": 1 },
            "sha256": { "type": "string", "pattern": "^[0-9a-fA-F]{64}$" },
            "name": { "type": "string" },
            "n_rules": { "type": "integer", "minimum": 1 }
          },
          "additionalProperties": false
        },
        "verdict": {
          "type": "object",
          "required": ["decision", "confidence"],
          "properties": {
            "decision": { "$ref": "#/$defs/decision" },
            "confidence": { "type": "number", "minimum": 0, "maximum": 1 },
            "rule_id": { "type": "string", "minLength": 1 },
            "reason": { "type": "string", "maxLength": 2000 }
          },
          "additionalProperties": false
        },
        "spans": {
          "type": "array",
          "items": { "$ref": "#/$defs/span" },
          "maxItems": 64
        },
        "oracle": {
          "type": "object",
          "description": "Provenance of the judgment. calibration numbers come from tools/oracle_calibration.py (THE 50 W6 T29) when a real ledger exists; absent a ledger they are omitted, never invented.",
          "properties": {
            "model": { "type": "string" },
            "latency_ms": { "type": "integer", "minimum": 0 },
            "calibration": {
              "type": "object",
              "properties": {
                "ece": { "type": "number", "minimum": 0, "maximum": 1 },
                "n": { "type": "integer", "minimum": 1 },
                "source": { "type": "string" }
              },
              "additionalProperties": false
            }
          },
          "additionalProperties": false
        }
      },
      "additionalProperties": false,
      "allOf": [
        {
          "if": { "properties": { "verdict": { "required": ["rule_id"] } } },
          "then": {
            "description": "When the verdict names a rule, at least one span must carry the same rule_id (checked by the endpoint and by the worked-example checker; JSON Schema draft 2020-12 cannot cross-reference array items)."
          }
        }
      ]
    }
  }
}
```

Two constraints JSON Schema 2020-12 cannot express are owned by the semantic
layer and said so in the schema itself: span end > start, and verdict
rule_id coverage by spans. Both are enforced in the checker and must be
enforced in the endpoint.

## 4. Worked example (the pair every implementation must reproduce)

Request (inline ruleset, the interop mode; real policy-store mode swaps
`inline` for `uri: "mag://policy/<policy_id>"`):

```json
{
  "schema": "the50.w6.t30.policy_eval.v1",
  "policy": {
    "inline": {
      "name": "mag-standing-steer-v0",
      "rules": [
        {
          "rule_id": "r1",
          "text": "deny any command that recursively deletes a directory outside the lane cache root",
          "decision": "deny",
          "patterns": ["rm -rf"]
        },
        {
          "rule_id": "r2",
          "text": "escalate any action that spends hosted specialist budget before the daily window",
          "decision": "escalate",
          "patterns": ["hosted specialist"]
        },
        { "rule_id": "r3", "text": "allow everything else", "decision": "allow" }
      ]
    }
  },
  "input": {
    "text": "Plan: run scut pass on the day_work lane, then clean up the scratch dir with rm -rf C:/Users/foste/AppData/Local/Temp/mag_scratch, then file the brief. Budget note: dispatch one hosted specialist call tomorrow.",
    "context": { "seat": "builder", "goal": "day_work scut", "trace": "t30-worked" }
  },
  "oracle": { "profile": "local_janitor", "min_confidence": 0.6 },
  "options": { "spans": true, "explain": true }
}
```

Response (spans DERIVED by str.find over input.text, not hand-counted; the
most specific rule wins, so r1 deny beats r2 escalate):

```json
{
  "ok": true,
  "schema": "the50.w6.t30.policy_eval.v1",
  "policy": {
    "uri": "inline:mag-standing-steer-v0",
    "name": "mag-standing-steer-v0",
    "n_rules": 3
  },
  "verdict": {
    "decision": "deny",
    "confidence": 0.92,
    "rule_id": "r1",
    "reason": "input contains a recursive delete aimed outside the lane cache root"
  },
  "spans": [
    { "rule_id": "r1", "start": 77, "end": 83, "quote": "rm -rf" },
    { "rule_id": "r2", "start": 178, "end": 195, "quote": "hosted specialist" }
  ],
  "oracle": {
    "model": "local_janitor (worked example, synthetic run)",
    "latency_ms": 22
  }
}
```

## 5. Validation receipt (ran this session)

Command: `.venv\Scripts\python.exe tools\policy_eval_schema_check.py`
(venv has jsonschema 4.26.0). Output, verbatim:

```
[PASS] worked request validates against #/$defs/request
[PASS] worked response validates against #/$defs/response
[PASS] every span orders and locates its quote exactly
[PASS] semantic layer rejects an end-before-start span (schema cannot compare two properties)
[PASS] verdict rule_id is covered by spans
[PASS] verdict decision matches the fired rule's decision
[PASS] most-specific rule wins (deny over escalate/allow)
[PASS] negative rejected: request without any ruleset pointer
[PASS] negative rejected: request with unknown schema const
[PASS] negative rejected: decision outside the enum
[PASS] negative rejected: uri outside the allowed schemes
[PASS] negative rejected: both uri and inline set
[PASS] negative rejected: confidence above 1
[PASS] negative rejected: invented oracle calibration numbers

14/14 checks pass; schema=dashboard\schemas\policy_eval.v1.schema.json
```

A first run failed 2 of 14 (hand-counted span offsets were wrong; an
end-before-start span passed schema-only validation). Both failures are the
reason the checker derives spans programmatically and owns ordering at the
semantic layer; the schema description records the constraint honestly
rather than pretending JSON Schema can hold it.

Re-verification receipt, 2026-09-25 (T30 verification pass, independent
re-run, same venv, jsonschema 4.26.0 confirmed via
`.venv/Scripts/python.exe -c "import jsonschema; print(jsonschema.__version__)"`).
Command: `.venv/Scripts/python.exe tools/policy_eval_schema_check.py`,
exit code 0, output identical line-for-line to the 14/14 block above. The
worked request and worked response blocks in section 4 compare equal
(`==`) to the checker module's `WORKED_REQUEST` / `WORKED_RESPONSE`
constants, and the section-4 spans (77/83, 178/195) equal the checker's
derived `_SPANS`. The `dashboard/rest.py` anchors cited in section 6 were
re-checked against disk today: auto-steer add handler at lines 678-709,
`_ok` at 25-32, `_err` at 35-39, `h_thrash` at 5049-5067, ROUTES thrash
entry at 5421, index description at 4754. `grep -n policy_eval
dashboard/rest.py` returns nothing, confirming the endpoint is still
unbuilt.

## 6. Implementation plan

Phase 1 (landed this session): schema + worked examples + checker.
`dashboard/schemas/policy_eval.v1.schema.json`,
`tools/policy_eval_schema_check.py`, this document.

Phase 2 (pure module, no server imports): `tools/policy_eval.py`, mirroring
`tools/thrash_meter.py` (the T27 pattern). Functions:
`resolve_policy(pointer) -> (rules, sha256, name)` reading
`memory/governance/auto_steer_policies.json` rows for
`mag://policy/<policy_id>` (row shape at `dashboard/rest.py:689-698`) and
rejecting unknown schemes; `evaluate(rules, text) -> response dict` with
str.find span derivation (identical algorithm to the checker's
`_derive_spans`, which is the golden). Decision order: most-specific rule
wins (nonzero patterns beat bare allow-all; deny > escalate > abstain >
allow on ties). Acceptance: `tests/test_policy_eval.py` asserts the
evaluated response equals the worked example and that the checker passes
when imported as a module.

Phase 3 (endpoint): handler `h_policy_eval` in `dashboard/rest.py` on the
T27 shape (`h_thrash`, `dashboard/rest.py:5049-5067`): parse body, call
`tools.policy_eval`, return `_ok({...}, schema="the50.w6.t30.policy_eval.v1")`
(envelope at `dashboard/rest.py:25-32`), `_err` for failures
(`dashboard/rest.py:35-39`). Register
`("POST", "/api/v1/instruments/policy_eval", h_policy_eval)` in ROUTES
(near `dashboard/rest.py:5421` where T27's GET landed) and add the one-line
description to `h_api_index` (`dashboard/rest.py:4654`, description map
where `GET /api/v1/thrash` sits at line 4754). Route it through `_dl`
only if a live oracle call can exceed the 5s deadline. Acceptance:
`mag.cmd lab`, POST the worked request, diff response against section 4.

Phase 4 (oracle + downstream): wire `oracle.profile=local_janitor` to the
local judgment tier; attach `oracle.calibration` from
`tools/oracle_calibration.py` ONLY when a real reads ledger exists (T29
honest limit: none does yet). Emit each verdict as a JSONL row (append-only)
keyed by policy_id + trace, so T28's miss-entropy surfaces can consume
verdict-filed rows and the G31 escalation threshold can be measured instead
of asserted.

Phase 5 (interop, the G06 acceptance test): a second implementation - the
checker itself already validates as one; the second is the pytest in
Phase 2 - must produce schema-valid responses on the same worked fixture.
Only after two independent implementations agree does a registry conversation
start (G06: "before anyone ships a registry"). Registry design is an
operator-gated decision and is out of scope here.

## 7. Honest limits

- The endpoint is NOT built in this task; the finish line is the schema plus
  the implementation plan, and the schema validates against the worked
  example (14/14, section 5). Nothing listens on any port for this yet.
- The worked example's confidence (0.92) and latency (22 ms) are synthetic
  fixture values, labeled as such in the response's own `oracle.model` field;
  no live oracle run happened, so no calibration block is attached.
- The fleet policy store (`memory/governance/auto_steer_policies.json`) has
  no rows on disk today; `uri` resolution against it is specified, not
  exercised. The `mag://policy/` scheme is a proposal this filing makes,
  not a fleet-standard URI.
- JSON Schema cannot express span ordering or verdict-to-span rule coverage;
  both live in the checker/endpoint (semantic layer). Draft-07-only
  validators can compile this document by mapping `$defs` to `definitions`;
  not tested here, stated as untested.
- Four real builders adopting this schema is the G06 prediction, not a
  result; zero external implementations exist as of this filing.

no_em_dash: this file contains none.
