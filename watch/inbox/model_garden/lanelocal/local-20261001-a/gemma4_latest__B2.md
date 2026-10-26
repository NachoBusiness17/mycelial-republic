# garden-v1-B2 | gemma4:latest | series local-20261001-a | instrument=lane-local-script
# finish=length prompt_tokens=4099 completion_tokens=2048 wall_s=78.46 tok_s=26.1 checks=1/5 {'SHAPE': 0, 'CITES-RESOLVE': 0, 'LINES-IN-RANGE': 0, 'NO-EM-DASH': 1, 'DISTINCT-EVIDENCE': 0}

The deliverable outlines the core operational contracts for the Switchboard system module, detailing expected inputs, successful transitions (Positive Examples), and systematic failure modes (Negative Examples) for critical cross-module interactions.

***

## ⚙️ Contract Specification: Switchboard System Interactions

### 1. Board Write Contract (`cmd_write` / `write_board_note`)

**Contract Goal:** To durably record a structured finding or event onto the shared blackboard, ensuring the author possesses both the capability and the required budgetary authority.

| Aspect | Details |
| :--- | :--- |
| **Inputs** | `note` (JSON payload), `authority` (JSON role/budget info) |
| **Prerequisites** | Authority must possess `board_write` capability. |
| **Constraints** | 1. Policy must validate the authority for the `board_write` effect. 2. Budget check must pass (if not prepaid). 3. Maximum note count must not be exceeded. |
| **Output** | `ok: true` with `path` and remaining budget, OR `ok: false` with a specific failure reason. |

---

#### ✅ Positive Example: Successful Board Write (Budget Allocated)

*The operator has sufficient authority and the budget pre-check passes.*

**Sequence:**
1. **Authority:** `{"capabilities": ["board_write"], "budget": {"max_calls": 10, "used": {"board_write": 1}, "remaining_quota": 9}}`
2. **Note Payload:** `{"text": "Source verification completed for Fork Alpha.", "source": "OperatorXYZ", "step_ok": {"pass": true}}`
3. **Command Line:** `mag switchboard_v2 write --note_file <note_payload> --authority <authority_json>`

**Expected Outcome:**
```json
{
  "ok": true,
  "path": "bb-0000X.json",
  "seq": X,
  "budget_remaining": 8 
}
```

#### ❌ Negative Example 1: Insufficient Capability

*The authority has a budget but lacks the required capability.*

**Sequence:**
1. **Authority:** `{"capabilities": ["tool_invoke"], "budget": {...}}`
2. **Note Payload:** (Any payload)
3. **Command Line:** `mag switchboard_v2 write --note_file <note_payload> --authority <authority_json>`

**Expected Outcome:**
```json
{
  "ok": false,
  "err": "capability board_write not granted",
  "authority": { ... }
}
```

#### ❌ Negative Example 2: Budget Exhausted

*The policy engine blocked the write because the allowance for this effect is zero.*

**Sequence:**
1. **Authority:** `{"capabilities": ["board_write"], "budget": {"max_calls": 1, "used": {"board_write": 1}}` (Budget used up)
2. **Note Payload:** (Any payload)
3. **Command Line:** `mag switchboard_v2 write --note_file <note_payload> --authority <authority_json>`

**Expected Outcome:**
```json
{
  "ok": false,
  "err": "board_write budget exhausted",
  "authority": { ... },
  "budget_remaining": 0
}
```

---

### 2. Proposal and Grant Contract (`cmd_propose` $\rightarrow$ `cmd_grant`)

**Contract Goal:** To transition a stated intent (Proposal) into an authorized, actionable resource (Grant).

| Aspect | Details |
| :--- | :--- |
| **Inputs** | `proposal` (Event ID, Effects), `authority` (Granting Entity) |
| **Prerequisites** | Proposal must exist; Authority must validate effects and capabilities. |
| **Constraints** | 1. If $\text{capabilities}$ are restricted (`--granted`), the grant must fail if the required capabilities are missing from the authority. 2. Denying a grant requires a specific reason. |
| **Output** | `ok: true` with the updated decision, OR `ok: false` detailing the rejection. |

---

#### ✅ Positive Example: Successful Grant

*An authorized agent successfully affirms the request.*

**Sequence:**
1. **Propose:** `mag switchboard_v2 propose --event_id T101 --effect tool_invoke --capabilities "log_access,memory_write" ...` (Creates Proposal T101)
2. **Authority:** `{"capabilities": ["log_access", "memory_write"], "budget": {...}}`
3. **Command Line:** `mag switchboard_v2 grant --proposal_file <T101_prop> --authority <auth_json> --granted log_access,memory_write`

**Expected Outcome:**
```json
{
  "ok": true,
  "decision": {
    "event_id": "T101",
    "status": "GRANTED",
    "receipt_status": "GRANTED",
    "authority": { ... }
  }
}
```

#### ❌ Negative Example: Grant Denial (Policy Violation)

*The granted authority fails to meet the required capabilities defined in the proposal.*

**Sequence:**
1. **Propose:** `mag switchboard_v2 propose --event_id T102 --effect tool_invoke --capabilities "advanced_network_read" ...`
2. **Authority:** `{"capabilities": ["basic_network_read"], "budget": {...}}` (Missing `advanced_network_read`)
3. **Command Line:** `mag switchboard_v2 grant --proposal_file <T102_prop> --authority <auth_json>`

**Expected Outcome:**
```json
{
  "
