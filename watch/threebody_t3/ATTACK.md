# ATTACK — T3 (ONI). Calibration words only, ≤200.

## Verdict 1: `mag_authority` redundant → **AMEND**
Patches do NOT jointly close the hole. Patch 2 (`fix_blackboard_post_provenance.json`) only *stamps* `authority: {"status":"UNMESHED"}` onto `bb-*.json` — it adds no gate. It does not route through `switchboard.propose`, no tier check, no DENIED. **`mag/board_directive.py` docstring states the same open gap:** "blackboard_post() writes bb-NNNNN.json DIRECTLY to disk with no switchboard grant, tier check, or budget." Patch 1 gates only `switchboard_v2` internals; the bypass writer never reaches it. Patch 3 (harness) only rewires the AUTHORIZED path — irrelevant to a bypass caller.
**Live escalation:** `blackboard_post(text, kind, owner)` takes caller-supplied `kind`/`owner`. A hostile caller posts `kind="decision"` (pinned forever, anchors mission coherence) under a forged owner → an unprivileged write becomes an authoritative, un-evictable anchor. Probe/read via same writer is visible (good) but NOT blocked. `mag_authority` (gate on bypass writer) is NOT redundant.

## Verdict 2: test implementable → **KEEP**
`/mag/tests/test_agent_state.py` exists (2456 B); pytest `def test_*(tmp_path, monkeypatch)` convention REAL (verified head-20 + `grep` — 20+ files confirm pattern).

## Verdict 3 (improvement): **KEEP** — prompt-only, low-risk.

## Weakest sentence:
Verdict 1 final line — **"no bypass gap"** — byte-falsifiable against `board_directive.py`'s own admission.

## Receipts
`read` of 3 staged patches + `swarm_tools.py:298` + `board_directive.py:1-20` + `ls`/`head -20` `/mag/tests/test_agent_state.py`.
