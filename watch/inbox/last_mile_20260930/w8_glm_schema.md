## 1. The schema (JSON Schema draft 2020-12)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://local.sovereign.agent/schemas/router_families_entry_v1.json",
  "title": "Router family entry v1",
  "type": "object",
  "required": ["family_id", "model_id", "prices", "duel_record", "quality_gate", "provenance", "derived_at_ts"],
  "additionalProperties": false,
  "properties": {
    "family_id": {"type": "string", "pattern": "^[a-z][a-z0-9-]{1,31}$"},
    "model_id": {"type": "string", "minLength": 3},
    "prices": {
      "type": "object",
      "required": ["input_per_M", "output_per_M", "as_of", "source"],
      "additionalProperties": false,
      "properties": {
        "input_per_M": {"type": ["number", "null"], "minimum": 0},
        "output_per_M": {"type": ["number", "null"], "minimum": 0},
        "blend_1_to_1": {"type": ["number", "null"], "minimum": 0},
        "as_of": {"type": "string", "format": "date"},
        "source": {"type": "string", "minLength": 1}
      }
    },
    "duel_record": {
      "type": "object",
      "required": ["shapes", "totals"],
      "additionalProperties": false,
      "properties": {
        "shapes": {
          "type": "object",
          "propertyNames": {"enum": ["adversarial-review", "schema-design", "planning", "code-analysis", "grading", "other"]},
          "additionalProperties": {"$ref": "#/$defs/shapeRecord"}
        },
        "totals": {"$ref": "#/$defs/shapeRecord"}
      }
    },
    "quality_gate": {
      "type": "object",
      "required": ["metric_name", "metric_value", "decided", "decided_min", "gate_passed"],
      "additionalProperties": false,
      "properties": {
        "metric_name": {"const": "win_rate_lower_bound_95"},
        "metric_value": {"type": ["number", "null"], "minimum": 0, "maximum": 1},
        "decided": {"type": "integer", "minimum": 0},
        "decided_min": {"type": "integer", "minimum": 1},
        "gate_passed": {"type": "boolean"}
      },
      "if": {"properties": {"decided": {"minimum": 1}}},
      "then": {"required": ["metric_value"]}
    },
    "provenance": {
      "type": "object",
      "required": ["ledger_path", "ledger_sha256", "row_count", "receipts"],
      "additionalProperties": false,
      "properties": {
        "ledger_path": {"const": "logs/duel/duels.jsonl"},
        "ledger_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        "row_count": {"type": "integer", "minimum": 0},
        "row_range": {"type": ["array", "null"], "items": {"type": "integer"}, "minItems": 2, "maxItems": 2},
        "receipts": {"type": "array", "items": {"type": "string"}, "minItems": 1},
        "zero_cost_note": {"type": "string", "minLength": 10}
      }
    },
    "derived_at_ts": {"type": "string", "format": "date-time"}
  },
  "$defs": {
    "shapeRecord": {
      "type": "object",
      "required": ["wins", "losses", "ties", "unparsed", "rows_judged", "decided"],
      "additionalProperties": false,
      "properties": {
        "wins": {"type": "integer", "minimum": 0},
        "losses": {"type": "integer", "minimum": 0},
        "ties": {"type": "integer", "minimum": 0},
        "unparsed": {"type": "integer", "minimum": 0},
        "rows_judged": {"type": "integer", "minimum": 0},
        "decided": {"type": "integer", "minimum": 0}
      }
    }
  }
}
```

It relies on the ledger fields a_model, b_model, winner, rubric, ts, mode, and judge_cost, and on the price receipt for input_per_M and output_per_M.

## 2. Edge case decisions

- Zero-duel family: entry is valid with every count 0. quality_gate.metric_value is null (unknown, not 0.0) and gate_passed is false; an unknown gate must never read as a failed skill test. The router treats such a family as ungated and never auto-picks it.
- UNPARSED winner rows: counted in unparsed and rows_judged, excluded from wins, losses, and decided. They are judge failures, not contender evidence.
- TIE rows: counted in ties and rows_judged, excluded from decided. A tie is evidence of parity, not dominance, so it must not inflate or deflate win_rate.
- Missing price: input_per_M and output_per_M are nullable, but as_of and source stay required so the null is attributable. A null price disqualifies the family from cost ranking; the router must error on null, never default it to 0.
- Cost of exactly zero: allowed (legitimate case: reused already-paid content), but provenance.zero_cost_note becomes mandatory. JSON Schema expresses this with an entry-level conditional: if any duel in the receipt set was banked with a_cost or b_cost of 0, require zero_cost_note. Kept as a documented if/then sibling of the one shown for quality_gate; omitted from the block above only for brevity.
- Unknown task shape: classification happens at derivation from the ask_id prefix and mode; anything unclassifiable lands in the "other" bucket, and the propertyNames enum rejects typo'd shape keys like "adversarial-reviews" at validation time.

## 3. Idempotent migration

derive(ledger_bytes) -> entries is a pure fold over the whole ledger: read every row, classify shape, credit the logical winner's family (remapped through the swap field when needed), recompute all counts, gate metric, and derived_at_ts from scratch, then write. There is no incremental update path, so re-running can never double count: identical ledger bytes always produce identical entries. The belt-and-braces check is provenance.ledger_sha256: before rewriting an existing router_families.json, if the stored sha256 matches the freshly computed one, skip the write entirely (byte-stable output). rows are never merged in place; the file is always fully derived state.

## 4. Validation predicates (tests, not just schema checks)

1. The worked example below validates against this schema (jsonschema validate, draft 2020-12 validator).
2. An instance whose duel_record.shapes carries a typo key "adversarial-reviews" FAILS validation (propertyNames enum does the work).
3. An instance with prices.input_per_M = -1 FAILS validation (minimum 0); a null price passes only when prices.source is present.
4. Structural invariant beyond schema power: for every shapeRecord, rows_judged == wins + losses + ties + unparsed and decided == wins + losses. This is not expressible in vanilla JSON Schema and is asserted in the test suite for every derived entry (schema checks types and enums; the fold checks arithmetic).

## 5. Worked example instance

```json
{
  "family_id": "glm",
  "model_id": "z-ai/glm-5.3-prime",
  "prices": {"input_per_M": 2.8, "output_per_M": 8.8, "blend_1_to_1": 5.8, "as_of": "2026-09-30", "source": "V9_NOUS_PRICES.md"},
  "duel_record": {
    "shapes": {
      "adversarial-review": {"wins": 4, "losses": 3, "ties": 1, "unparsed": 0, "rows_judged": 8, "decided": 7},
      "schema-design": {"wins": 4, "losses": 2, "ties": 0, "unparsed": 0, "rows_judged": 6, "decided": 6},
      "planning": {"wins": 4, "losses": 3, "ties": 0, "unparsed": 0, "rows_judged": 7, "decided": 7}
    },
    "totals": {"wins": 12, "losses": 8, "ties": 1, "unparsed": 0, "rows_judged": 21, "decided": 20}
  },
  "quality_gate": {"metric_name": "win_rate_lower_bound_95", "metric_value": 0.52, "decided": 20, "decided_min": 8, "gate_passed": true},
  "provenance": {"ledger_path": "logs/duel/duels.jsonl", "ledger_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "row_count": 21, "row_range": [0, 20], "receipts": ["watch/inbox/last_mile_20260930/W8_MULTIFAMILY.md"]},
  "derived_at_ts": "2026-09-30T12:00:00Z"
}
```
