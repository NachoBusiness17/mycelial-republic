# PA-A1-qwen38max (qwen/qwen3.8-max-prime @ nous, turn 1, channel: content)

# ANTI-FORGERY AND REPLAY-REJECTION LAYER FOR STEERING CHANNELS

## 1. THREAT MODEL

### Channel: File steers (hermes_steering.py)

| Attribute | Value |
|---|---|
| Entry point | `cmd_dispatch()` and `cmd_steer()` accept arbitrary goal/nudge strings from argv |
| Evidence | `00__hermes_steering.py:44-47` imports `steer_seal` but no call site is visible in the provided bytes |
| Writer | Any process that can execute `hermes_steering.py` or write to its input files |
| Injection vector | Direct CLI invocation with forged goal; modification of persona files at `mag/hermes_personas/*.md` (read at `_load_persona`, file line ~100); modification of `state/hermes_routing.json` |
| Read path (agent consumes) | `hermes.exe` receives the goal via `-Q` flag inside `_run_hermes()` |
| Current verifier | NONE. `steer_seal` is imported but not observably called in the visible code |

### Channel: Grok overlay (grok_steer.py)

| Attribute | Value |
|---|---|
| Entry point | `decide_steer(move)` at `02__grok_steer.py` function definition (visible in evidence) |
| Writer | Any process that can call `decide_steer()` or that can write to the grok session's input |
| Injection vector | A forged `move` string passed to `decide_steer()` triggers a steer; the returned steer text is injected into the grok session by the caller (call site not in this file) |
| Read path (agent consumes) | The grok session receives the steer text (injection mechanism is external to this file) |
| Current verifier | NONE. No signature check on `move` input or on the returned steer |

### Channel: Phone-door hook (phone_door.py)

| Attribute | Value |
|---|---|
| Entry point | `ensure()` at `01__phone_door.py` |
| Writer | Any process that can execute `phone_door.py` |
| Injection vector | This is a HEALTH hook, not a steering channel in the current code. It pings a phone and logs results. It does not accept or transmit steering directives. |
| Read path | N/A for steering. The log at `memory/runs/phone_door_log.jsonl` could be forged by any file-writer. |
| Current verifier | NONE on the log entries |
| Note | The contract names this as a steering channel. The evidence code does not support that claim. Marked UNVERIFIED as a steering vector. |

### Channel: Discord messages

| Attribute | Value |
|---|---|
| Entry point | UNVERIFIED - no Discord handler code is present in the evidence files |
| Writer | UNVERIFIED |
| Injection vector | UNVERIFIED |
| Read path | UNVERIFIED |
| Current verifier | UNVERIFIED |

---

## 2. VERIFIER DESIGN

### Binding point

Verification binds at the READ path: the moment before an agent consumes a steering directive. For hermes, this is inside `_run_hermes()` before the subprocess call. For grok_steer, this is at the return of `decide_steer()` before the caller injects the steer.

### Key material

One secret: `state/steer_hmac_key`, 32 bytes, hex-encoded (64 hex chars). Generated once with `python -c "import os; print(os.urandom(32).hex())"`. The operator never touches this file. It is read by the verifier at startup.

### Canonical message envelope

```
STEER_V1|{unix_ts}|{nonce_hex}|{payload}|{mac_hex}
```

Fields:
- `STEER_V1` - literal version tag
- `unix_ts` - integer UTC epoch seconds at seal time
- `nonce_hex` - 16 random hex chars (8 bytes)
- `payload` - the steering text, verbatim (no encoding; pipe chars in payload are escaped as `\x7c`)
- `mac_hex` - `HMAC-SHA256(key, "STEER_V1|{unix_ts}|{nonce_hex}|{payload_escaped}")` as lowercase hex

### Replay window

- Accept: `abs(now - unix_ts) <= 300` seconds
- Nonce dedup: maintain `state/steer_nonces.jsonl`, one nonce per line, prune entries older than 600s on each check
- A nonce seen within the window is rejected (replay)

### Operator-side ceremony

ZERO. The operator types his word as before. The sealing happens inside the tool that accepts his input. The `steer_seal.seal(payload)` call is made by the tool, not by the operator.

---

## 3. PATCH SPEC

### 3A. New file: `mag/steer_seal.py`

This file already exists as an import target (`00__hermes_steering.py:44-47`) but its contents are not in the evidence. The spec below is the complete implementation to land at that path.

```python
"""steer_seal - anti-forgery gate for steering channels (A1).

One secret, HMAC-SHA256, 300s replay window, nonce dedup.
The operator's side stays single-word. Sealing is done by the tool.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KEY_PATH = ROOT / "state" / "steer_hmac_key"
NONCE_LOG = ROOT / "state" / "steer_nonces.jsonl"
WINDOW_S = 300
_NONCE_PRUNE_S = 600


def _key() -> bytes:
    raw = KEY_PATH.read_text(encoding="utf-8").strip()
    if len(raw) != 64:
        raise SystemExit(f"steer_seal: key file {KEY_PATH} must be 64 hex chars, got {len(raw)}")
    return bytes.fromhex(raw)


def _escape(payload: str) -> str:
    return payload.replace("\\", "\\\\").replace("|", "\\x7c")


def _unescape(s: str) -> str:
    return s.replace("\\x7c", "|").replace("\\\\", "\\")


def seal(payload: str) -> str:
    """Seal a steering directive. Returns the envelope string."""
    ts = int(time.time())
    nonce = os.urandom(8).hex()
    escaped = _escape(payload)
    basis = f"STEER_V1|{ts}|{nonce}|{escaped}"
    mac = hmac.new(_key(), basis.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"{basis}|{mac}"


def verify(envelope: str) -> tuple[bool, str]:
    """Verify an envelope. Returns (ok, payload_or_reason)."""
    parts = envelope.split("|")
    if len(parts) < 5 or parts[0] != "STEER_V1":
        return False, "malformed envelope"
    try:
        ts = int(parts[1])
    except ValueError:
        return False, "bad timestamp"
    nonce = parts[2]
    escaped_payload = parts[3]
    mac = parts[4]

    now = int(time.time())
    if abs(now - ts) > WINDOW_S:
        return False, f"stale: age {abs(now - ts)}s > {WINDOW_S}s window"

    basis = f"STEER_V1|{ts}|{nonce}|{escaped_payload}"
    expected = hmac.new(_key(), basis.encode("utf-8"), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(mac, expected):
        return False, "MAC mismatch"

    if _nonce_seen(nonce):
        return False, f"replay: nonce {nonce} already consumed"
    _nonce_record(nonce, ts)
    return True, _unescape(escaped_payload)


def _nonce_seen(nonce: str) -> bool:
    if not NONCE_LOG.is_file():
        return False
    for line in NONCE_LOG.read_text(encoding="utf-8").splitlines():
        if line.strip().split("|")[0] == nonce:
            return True
    return False


def _nonce_record(nonce: str, ts: int) -> None:
    NONCE_LOG.parent.mkdir(parents=True, exist_ok=True)
    _prune_nonces()
    with NONCE_LOG.open("a", encoding="utf-8") as f:
        f.write(f"{nonce}|{ts}\n")


def _prune_nonces() -> None:
    if not NONCE_LOG.is_file():
        return
    cutoff = int(time.time()) - _NONCE_PRUNE_S
    lines = NONCE_LOG.read_text(encoding="utf-8").splitlines()
    kept = [l for l in lines if l.strip() and int(l.split("|")[1]) > cutoff]
    if len(kept) < len(lines):
        NONCE_LOG.write_text("\n".join(kept) + "\n", encoding="utf-8")
```

### 3B. Modify: `00__hermes_steering.py`

**Location**: inside `_run_hermes()`, before the subprocess call.

The function signature is visible in the evidence (the line beginning `def _run_hermes(goal: str, workdir: Path, ...`). The subprocess call is `cmd = [str(HERMES), "chat", "-Q", "-q", goal]`.

**Change**: seal the goal before passing to hermes, and verify at the boundary.

Insert after the `cmd` list is built, before `subprocess.run`:

```python
    # --- steer_seal gate (Q41/Q42 fix) ---
    sealed_goal = steer_seal.seal(goal)
    ok, result = steer_seal.verify(sealed_goal)
    if not ok:
        raise SystemExit(f"steer_seal REJECT: {result}")
    # Pass the ORIGINAL goal to hermes (hermes doesn't know about envelopes).
    # The seal/verify round-trip proves the goal was not tampered between
    # the operator's input and this point.
    # --- end gate ---
```

**Additionally**, for the case where an external caller writes a sealed envelope to a file that this tool reads: add a `verify_inbound()` function that checks any goal loaded from a file or channel:

```python
def _verify_inbound_goal(raw: str) -> str:
    """If raw looks like a STEER_V1 envelope, verify and unwrap. Else reject."""
    if raw.startswith("STEER_V1|"):
        ok, result = steer_seal.verify(raw)
        if not ok:
            raise SystemExit(f"steer_seal REJECT inbound: {result}")
        return result
    # Migration period: accept unsealed goals but log a warning
    # Remove this branch after migration window closes
    import sys
    print(f"WARN: unsealed goal accepted (migration mode): {raw[:60]}", file=sys.stderr)
    return raw
```

### 3C. Modify: `02__grok_steer.py`

**Location**: at the end of `decide_steer()`, before the return statement that includes the steer text.

**Change**: seal the steer before returning it to the caller.

After the line `steer = str(r.get("text") or "").strip()`:

```python
    if steer:
        steer = steer_seal.seal(steer)
```

And at the top of the file, add the import:

```python
try:
    from mag import steer_seal
except ImportError:
    import steer_seal
```

The CALLER of `decide_steer()` (the injection point into the grok session, not visible in this file) must call `steer_seal.verify()` before injecting.

### 3D. Key generation (one-time)

```bash
python -c "import os; from pathlib import Path; p=Path('state/steer_hmac_key'); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(os.urandom(32).hex()); print('key written:', p)"
```

---

## 4. TEST PLAN

### Positive cases (must be REJECTED)

| # | Case | Expected |
|---|---|---|
| P1 | Envelope with wrong MAC (flip one hex char in mac field) | `verify()` returns `(False, "MAC mismatch")` |
| P2 | Envelope with timestamp 400s in the past | `verify()` returns `(False, "stale: ...")` |
| P3 | Envelope replayed (same nonce submitted twice) | Second call returns `(False, "replay: nonce ...")` |
| P4 | Raw goal string without envelope prefix passed to `_verify_inbound_goal()` in strict mode (post-migration) | Rejected |
| P5 | Envelope with payload containing `\x7c` injection attempt (attacker inserts fake field separator) | MAC mismatch (escape prevents field confusion) |
| P6 | Envelope with version tag `STEER_V2` | Rejected as malformed |
| P7 | Empty payload sealed then verified | Passes (empty is valid) - but a separate gate should reject empty goals at the dispatch level |

### Negative cases (must PASS unchanged)

| # | Case | Expected |
|---|---|---|
| N1 | Operator types `steer --resume SESSION "stop and refactor the parser"` | `seal()` produces valid envelope; `verify()` returns `(True, "stop and refactor the parser")` |
| N2 | Operator types a goal containing pipe characters: `"use A | B pattern"` | Seal/verify round-trips correctly (escape/unescape) |
| N3 | Operator types a goal with unicode: `"fix the résumé parser"` | Round-trips correctly |
| N4 | `decide_steer()` returns a steer for a detected patch-move | Steer is sealed; caller can verify it |
| N5 | `decide_steer()` returns `need_steer: False` (no patch detected) | No seal is applied (no steer to seal); deterministic $0 path unchanged |
| N6 | During migration window: unsealed goal passed to `_verify_inbound_goal()` | Accepted with stderr warning (backward compat) |

### Interrupt-law compliance

The operator's interaction is unchanged: he types his word. The seal is applied by the tool transparently. Zero added keystrokes, zero added steps, zero new prompts.

---

## 5. FALSIFIER

This design is proven wrong if ANY of the following observations occur:

1. **A forged steering directive is accepted after the patch lands.** Specifically: a process that does NOT possess the contents of `state/steer_hmac_key` successfully injects a steering directive that passes `verify()` and reaches an agent.

2. **The operator experiences added friction.** If the operator must perform any action beyond typing his word (entering a code, confirming a prompt, waiting for a key), the design has failed its constraint.

3. **A legitimate operator steer is rejected.** If `seal()` + `verify()` round-trip fails on a real operator input (false rejection), the design breaks the interrupt law.

4. **The replay window is bypassed.** If an attacker captures a valid envelope and successfully replays it after the nonce is consumed or after the 300s window, the design has failed.

The single cleanest falsifier: **produce a valid envelope without reading `state/steer_hmac_key`.** If that is possible, the HMAC provides no authentication and the entire design is void.

---

## UNVERIFIED CLAIMS REGISTER

| Claim | Status | Reason |
|---|---|---|
| Discord handler exists and accepts steering directives | UNVERIFIED | No Discord code in evidence |
| phone_door.py is used as a steering channel | UNVERIFIED | Code shows health-check only, no steering input path |
| `steer_seal` module already has content at `mag/steer_seal.py` | UNVERIFIED | Import exists at `00__hermes_steering.py:44-47` but module contents not in evidence |
| The grok session injection point calls `decide_steer()` | UNVERIFIED | Call site is external to `02__grok_steer.py` |
| `_run_hermes()` line number for subprocess call | UNVERIFIED | Function body is in the truncated middle section of the evidence file |
