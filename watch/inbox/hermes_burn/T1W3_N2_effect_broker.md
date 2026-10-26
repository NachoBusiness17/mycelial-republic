# T1W3_N2_effect_broker (anthropic/claude-opus-5.5, turn 1, channel: content)

# Stranger Audit: effect_broker + switchboard_v2

**Citation note:** the attachment carries no line numbers. Every `file:line` below is therefore UNVERIFIED, and each claim is anchored by function name plus quoted bytes.

## (1) Leaks

| Path | Verdict | Bytes |
|---|---|---|
| Broker trusts a caller-built authority dict | **REAL, worst** | `_authority_ok` checks only `authority.get("status")` and `granted_capabilities`. Self-test 1 hand-builds `"status": "AUTHORIZED"` and expects an fs_write to pass (`cmd_test`). Nothing ties the authority to `grant()`. Provenance inside `policy_engine.validate_authority` is UNVERIFIED (not attached). |
| Self-asserted label plus opt-out flag | **REAL** | `propose(..., authority_label=..., require_confirmation=...)`. Passing `operator-authored` skips the agent gate. Passing `False` makes `proposal.get("require_confirmation", ...)` skip DEFERRED. `_implicit_authority` then returns `status = "AUTHORIZED"` for fs_write. |
| `write_board_note` importable | **REAL** (same root) | `validate_authority(authority, effect)` runs on whatever dict is passed. No `_GRANTED_EVENT_IDS` lookup. |
| Ordinary-label board_write/verkle_link self-grant | **Defended by doctrine, leaky in budget** | The tier gate holds. However, `"budget": budget or dict(...)` is caller-set, and `c == "board_write"` admits the capability even when it was not requested. |
| swarm_cycle `agent-generated` | **Defended** | High-impact effects are refused (`DENIED` branch in `_implicit_authority`). |
| 25,427 direct provider calls | **REAL mediation gap** | They never enter `execute()`. `chat_provider` is importable directly. |

## (2) What 0/25,427 means

- "Every side effect in MAG must route through this broker" (module docstring) is **doctrine, not a control**. Nothing enforces it.
- **Instrument, moment, and context:** the figure comes from `tools/cost_rollup.py` (25,427 calls / $136.19) and `effects.jsonl` (3 rows, 2026-10-01 09:35:42Z to 09:47:16Z, all `owner: state_snapshot`).
- The two numbers do not share a denominator. The 25,427 are model calls. The 3 are board_writes. Model_call coverage is still **0**.
- **Claimable:** "Three state_snapshot notes were broker-admitted and metered."
- **Not claimable:** "The broker mediates MAG side effects," or "coverage is 0.012%" as a safety figure.

## (3) The test (deliverable)

```python
# tests/test_broker_provenance.py
from mag import effect_broker as eb, switchboard_v2 as sb

def test_forged_authority_refused(tmp_path, monkeypatch):
    monkeypatch.setattr(eb, "RECEIPTS_DIR", tmp_path)
    target = eb.ROOT / "memory" / "provenance_probe.txt"
    forged = {"status": "AUTHORIZED", "granted_capabilities": ["fs_write"],
              "event_id": "forge-1", "budget": {"max_calls": 5},
              "ts": eb._now(), "ttl_seconds": 900}
    rec = eb.execute("fs_write", {"path": str(target), "content": "x"}, forged)
    assert not rec.get("result", {}).get("ok")
    assert not target.exists()

def test_granted_authority_still_works(tmp_path, monkeypatch):
    monkeypatch.setattr(eb, "RECEIPTS_DIR", tmp_path)
    d = sb.grant(sb.propose("prov-ok-1", "board_write", ["board_write"]))
    rec = eb.execute("board_write", {"note": {"kind": "test"}}, d["authority"])
    assert rec["result"]["ok"]
```

- **Today:** test 1 fails, because self-test 1 shows a forged fs_write succeeding.
- **After a fix:** test 1 passes once `execute` requires grant provenance, for example an event_id present in the trail or an HMAC.
- **Positive control:** test 2 stops the fix from simply denying everything.
- **Side effects:** `cmd_test` test 1 must then use a granted authority. Test 2 also writes one real blackboard note into the production BB directory.
- **Falsifier:** if test 1 passes on today's tree, then `validate_authority` already checks provenance and the worst-leak claim is wrong.
