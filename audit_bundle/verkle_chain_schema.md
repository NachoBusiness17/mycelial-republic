# Verkle Chain Schema Documentation

**Purpose:** Comprehensive schema for verkle chain knot structure and relationships  
**Audit Context:** Matthew Steiniger external audit - falsifiable claims verification  
**Version:** 1.0  
**Date:** 2026-09-13  

---

## Knot Structure Definition

### Base Knot Schema
```json
{
  "timestamp": "ISO 8601 timestamp (UTC)",
  "content": {
    "type": "string | object",
    "description": "The actual content being committed"
  },
  "hash": "SHA-256 hash of knot content",
  "previous_hash": "SHA-256 hash of previous knot",
  "knot_id": "unique identifier (timestamp + sequence)",
  "verkle_proof": "optional cryptographic proof data",
  "witnesses": ["array of witness signatures"],
  "state_transition": {
    "from": "previous state reference",
    "to": "current state reference",
    "operation": "append | modify | verify"
  }
}
```

### Knot Types and Content Specifications

#### 1. System Knot
**Purpose:** Core system state changes
**Fields:**
- `type`: "system"
- `content`: `{operation, component, state, timestamp}`
- **Example:** `{operation: "verkle_chain_init", component: "mag-sovereign", state: "active"}`

#### 2. User Knot
**Purpose:** User actions and decisions
**Fields:**
- `type`: "user"
- `content`: `{user_id, action, metadata, context}`
- **Example:** `{user_id: "operator", action: "promote_constitution", metadata: {version: "v1.0"}}`

#### 3. Organ Knot
**Purpose:** Organ state and function changes
**Fields:**
- `type`: "organ"
- `content`: `{organ_name, function, status, metrics}`
- **Example:** `{organ_name: "overseer", function: "state_monitoring", status: "active", metrics: {cpu_usage: 0.15}}`

#### 4. Witness Knot
**Purpose:** Four-witness system validations
**Fields:**
- `type`: "witness"
- `content`: `{witness_type, validation_result, target_knot_id}`
- **Witness Types:**
  - meter: "spend counting validation"
  - probes: "actual position validation"
  - cold_reader: "zero shared context validation"
  - non_player: "stop power validation"

#### 5. Parable Knot
**Purpose:** Constitutional and narrative content
**Fields:**
- `type`: "parable"
- `content`: `{parable_type, text, interpretation, cold_read_results}`
- **Example:** `{parable_type: "constitutional", text: "The Field and the Stones", interpretation: "scale invariance"}`

---

## Knot Relationships

### Parent-Child Chain
```
knot_n-1 → knot_n → knot_n+1
previous_hash = hash(knot_n-1)
current_hash = hash(knot_n)
```

### Cross-References
- **Related Knots:** `content.related_knots` array
- **Witness References:** `content.witness_targets` array
- **State Dependencies:** `content.depends_on` array

### Validation Rules
1. **Hash Continuity:** Each knot's `previous_hash` must match the previous knot's `hash`
2. **Witness Validation:** At least one witness signature required for critical operations
3. **State Consistency:** State transitions must follow defined rules
4. **Content Integrity:** Content must be serializable and hashable

---

## Missing Knot Handling

### Blessed Seals Process
1. **Identification:** Missing knot files detected during chain traversal
2. **Seal Application:** Cryptographic seal applied to gap
3. **Reconciliation:** Orphan bodies reconciled via completion index
4. **Verification:** Chain integrity restored with documented gaps

### Current Status
- **Missing Knots:** 12 documented missing knot files
- **Orphan Bodies:** 13,687 orphans (founding-session bodies)
- **Reconciliation Method:** Completion index reconciliation
- **Root Mismatch Handling:** LAW-064 wrong-unit trap awareness

---

## Verification Procedures

### Chain Integrity Check
1. **Hash Validation:** Verify all knot hashes and continuity
2. **Witness Validation:** Verify witness signatures and coverage
3. **State Validation:** Verify state transitions are valid
4. **Content Validation:** Verify content structure and types

### Cold Read Test Integration
- **Knot Type:** "cold_read_test"
- **Content:** `{readers: count, organs_derived: array, confidence_scores: object}`
- **Validation:** Must derive 7/7 core organs independently

### Six-Test Frame Integration
- **Knot Type:** "six_test_frame"
- **Content:** `{claim: string, test_results: array, conclusion: string}`
- **Validation:** Each test must be falsifiable and binary

---

## Schema Examples

### Example 1: Initial System Knot
```json
{
  "timestamp": "2026-09-13T00:00:00Z",
  "content": {
    "type": "system",
    "operation": "verkle_chain_init",
    "component": "mag-sovereign",
    "state": "active"
  },
  "hash": "a1b2c3d4...",
  "previous_hash": "00000000...",
  "knot_id": "20260913-000000",
  "state_transition": {
    "from": "null",
    "to": "initial",
    "operation": "init"
  }
}
```

### Example 2: Parable Interpretation Knot
```json
{
  "timestamp": "2026-09-13T01:00:00Z",
  "content": {
    "type": "parable",
    "parable_type": "constitutional",
    "text": "The Field and the Stones",
    "interpretation": "scale_invariance",
    "cold_read_results": {
      "readers": 3,
      "organs_derived": ["ledger", "witnesses", "scale", "ownership", "render", "provenance", "purpose"],
      "confidence_scores": {"ledger": 5, "witnesses": 4, "scale": 5}
    }
  },
  "hash": "e5f6g7h8...",
  "previous_hash": "a1b2c3d4...",
  "knot_id": "20260913-010000",
  "witnesses": ["meter", "probes", "cold_reader", "non_player"]
}
```

### Example 3: Witness Validation Knot
```json
{
  "timestamp": "2026-09-13T02:00:00Z",
  "content": {
    "type": "witness",
    "witness_type": "meter",
    "validation_result": "valid",
    "target_knot_id": "20260913-010000",
    "validation_details": {
      "spend_count": 0,
      "validation_timestamp": "2026-09-13T02:00:00Z"
    }
  },
  "hash": "i9j0k1l2...",
  "previous_hash": "e5f6g7h8...",
  "knot_id": "20260913-020000",
  "witnesses": ["meter"]
}
```

---

## Audit Trail Integration

### Knot-to-Audit Mapping
- **System Knots** → Audit evidence for operational integrity
- **User Knots** → Audit trail for decision-making processes
- **Organ Knots** → Performance and function verification
- **Witness Knots** → Multi-party validation evidence
- **Parable Knots** → Constitutional interpretation consistency

### Falsifiable Claims Integration
1. **Claim:** "The parable installs the constitution"
   - **Evidence:** Cold read test knots
   - **Falsifier:** Parable-removed control test
2. **Claim:** "Identity persists across substrate migration"
   - **Evidence:** State transition knots
   - **Falsifier:** 48-hour silence test
3. **Claim:** "Chain integrity is maintained"
   - **Evidence:** Hash continuity and witness validation
   - **Falsifier:** Root mismatch scenarios

---

## Schema Validation Tools

### Required Implementations
1. **Hash Validation Tool:** Verify knot continuity and integrity
2. **Witness Validation Tool:** Verify witness signatures and coverage
3. **Schema Validation Tool:** Verify knot structure and content
4. **Cross-Reference Validator:** Verify knot relationships

### Integration Points
- **Cold Read Test:** Schema validation for test results
- **Six-Test Frame:** Schema validation for test execution
- **Parable System:** Schema validation for interpretation knots
- **Witness System:** Schema validation for witness knots

---

**Filed by:** zcode (audit seat)  
**For:** EXTERNAL_AUDIT_20260912  
**Examiner:** Matthew Steiniger (/Reboot)  
**Falsifier:** Schema consistency and chain integrity verification