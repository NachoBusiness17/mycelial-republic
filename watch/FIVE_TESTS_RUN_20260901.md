# FIVE TESTS RUN (S3) — 2026-09-01

> **[AUDIT-TYPED 2026-09-08]** status: STAGED · claims: the Five Hypervisor Tests runner exists and is staged; the blocker is host apply + pytest, not missing test code — SUPPORTED (patch-13 presence + grep-0-hits receipts on disk; runtime 5/5 explicitly UNVERIFIED) · falsifier: host applies patch 13 and pytest fails, or test_hypervisor tests are absent from the applied file

**Stage:** S3 07:00–09:00Z · **Runner window:** 06:49Z (ticker advanced early — stage seat was silent, no runner receipt existed)
**Author:** sancho/main (night-shift ticker)
**Burn gate:** $0 spent on this stage (verification is host-venv pytest; no API paid this turn)

## Verdict: BLOCKED-ON-HOST-APPLY (not a code gap)

The Five Hypervisor Tests **runner already exists and is staged** — the blocker is
**host apply + pytest**, not missing test code.

| item | state | path |
|---|---|---|
| Five Tests source (canonical) | **STAGED, awaiting host apply** | `/patches/patch-five-hypervisor-tests.json` (PATCH 13, staged 2026-08-31 17:50Z) |
| Target test file | present, **LACKS** the Five Tests block | `/mag/tests/test_switchboard.py` (dated 08-31 04:54; grep `test_hypervisor` = 0 hits) |
| Applied marker | **absent** for patch 13 | `/patches/applied/` (only `self_steal_switchboard_v2.json` present) |
| Hermetic supplement (this tick) | written, in-cage `staging/` only | `/root/.openclaw/workspace/staging/test_switchboard_hypervisor.py` (optional isolated variant, NOT patched) |

## Why the cage cannot close S3 itself
- The Linux ticker cage has **no Python** (`python3` not found) and no docker/podman.
- `/mag` is read-only; edits route via `/patches` and the **host Mag venv** applies them.
- The Five Tests import `mag.switchboard_v2` / `mag.policy_engine` / `mag.effect_broker` —
  those resolve only under the host venv, not in this cage.

## What the staged Five Tests cover (patch 13 — MEASURED from source read)
1. **bypass** — pinned-kind refusal with switchboard down (charter ONI-corrected invariant:
   pinned kinds refuse; non-pinned legacy writes flow by design).
2. **capability-attenuation** — `untrusted-instruction` / `external-content` labels fail
   DENIED at `grant()`; high-impact effects (fs_write/lane_spawn/model_call/tool_invoke/
   network_access) refuse self-grant regardless of label.
3. **noisy-neighbor** — 8 concurrent `propose`+`grant` → 8 independent verdicts, no starvation.
4. **replay** — same `event_id` twice → not two independent AUTHORIZED grants.
5. **confused-deputy** — 5 malformed authority shapes fail closed in `validate_authority`.

## Desk-check notes (honest, UNVERIFIED-runtime)
Author read the staging `switchboard_v2.py` + `policy_engine.py` source:
- `grant()` gate order (explicit-deny → TTL → budget → confirmation → authority) and
  `validate_authority` (status → capability → revocation → TTL → budget) confirm the
  **attenuation and confused-deputy** failure paths the staged tests assert should DENY.
- **CAVEAT (scorer must read):** `validate_authority` does **not** inspect `authority_label`;
  it keyed only on `status`, `granted_capabilities`, revocation, TTL, budget. An untrusted
  actor who fabricates `status=AUTHORIZED` + `["board_write"]` could pass the *effect layer*
  check. The staged attenuation test closes this via the `grant()` gate (which uses
  `_implicit_authority` + label), not via `validate_authority` itself. **This is a real
  boundary to verify either way when pytest runs.**
- Rusted-iron honesty: these are desk-checks from source; **the 5/5 green claim is UNVERIFIED
  until the host applies patch 13 and runs pytest.** The cage cannot measure it.

## Required host action (operator / host venv)
1. `python -m mag.openclaw_patches apply` (applies patch 13 → Five Tests into
   `/mag/tests/test_switchboard.py`).
2. Run the file's tests on host venv, e.g.: `...\.venv\Scripts\python.exe -m pytest tests/test_switchboard.py`
   or `python -m pytest /mag/tests/test_switchboard.py`.
3. Paste the `5/5 passed` (or actual) result here; scorer tags the receipt MEASURED.

## Gate impact
Per charter M2 + brief S3: **Codex convergence gate — no 32×32 until Five Tests green.**
Holding that gate correctly until host pytest confirms green.

## Labels
- Patch existence + target-file gap (grep 0 hits) : **MEASURED** (disk).
- Five-Tests semantics (source read) : MEASURED.
- 5/5 green at runtime : **UNVERIFIED** (host must run).
- $ spent this stage: $0.
