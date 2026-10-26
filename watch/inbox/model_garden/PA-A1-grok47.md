# PA-A1-grok47 (grok-4.7 @ xai, turn 1, channel: content)

The same-UID file-writer who can read the agent environment defeats any MAC this host can check. This spec closes channel-peer forgery on read paths that actually exist in the evidence. It does not pretend to close Discord, and it does not flip fail-closed until his existing one-word entry still round-trips.

Instrument: quoted evidence bytes only, display moment 2026-10-01, files truncated where the autopsy marker says so. No live tree read. Line numbers are UNVERIFIED. Anchors are quoted strings. If a quoted string is absent, do not apply that hunk.

## 1. THREAT MODEL

| Channel (named from code) | Who writes or injects | What they can forge today | Read path that must bind |
|---|---|---|---|
| Hermes file/CLI steer | Any local file-writer, and any peer who can pass `nudge` into `steer --resume SESSION "<nudge>"` | A steer directive. Parser takes the nudge as an opaque argument: `s.add_argument("nudge")`. Body of `cmd_steer` is in the truncated middle: UNVERIFIED whether it already calls `steer_seal`. | Before `_run_hermes(goal, ...)` consumes that nudge. `_run_hermes` is defined and takes `goal: str`. |
| Hermes dispatch | Mag / anyone invoking `dispatch "<goal>"` | A goal, not an operator interrupt. Do not treat goals as STEER words. | No seal required. Sealing goals would add friction the contract forbids. |
| Phone-door hook | Any local caller of `python -m mag.phone_door`, and any writer of `memory/runs/phone_door_log.jsonl` | A fake health row (`hook: phone-door`, `ok`). `ensure()` logs whatever it computed, with no auth. It does not read a directive. A forged row cannot steer an agent unless some other reader treats the log as orders. That other reader is not in this file. | `status()` / any future reader of the log. Reject a row that carries `steer` or `directive` unless sealed. Do not require a seal on ordinary `ok` pings. |
| Grok overlay | Any caller of `decide_steer(move)` / `main(argv)` | An advisory steer string from a move the caller supplied. This is a producer, not an operator interrupt reader. | Consumer must not promote `steer` from this module to operator authority. No such consumer is in the quoted file. |
| Discord messages | UNVERIFIED | No Discord read, write, or webhook path appears in the four evidence files. A patch against a Discord file would be invented. | None in this bundle. Reserve channel name `discord` in the verifier. Do not claim Q42 closed for Discord. |

Q41 / Q42: ADDENDUM 2 lists them as staged, not fixed: "Q41 steer verifier, Q42 steering-channel verify". The table rows themselves are inside the truncated middle. Detailed fail text is UNVERIFIED. The import comment `from mag import steer_seal  # A1 anti-forgery gate` shows a gate was expected. `steer_seal.py` is not in the evidence bundle.

Same-UID collapse (condition on every verdict below): `00__hermes_steering.py` reads `ROOT / ".env"` for account keys. A writer with that process's UID can read any secret that process can read. HMAC then does not bind authorship. Claim that holds: a Discord peer, another OS user, or a tailnet node who cannot read `STEER_SEAL_KEY` cannot mint a blob `verify` accepts. Claim that does not hold: a co-resident writer as the agent user.

## 2. VERIFIER DESIGN

Binds on read, not write. Writers may emit anything. A steer is applied only after `verify` returns a word.

Key: one secret, env `STEER_SEAL_KEY` (utf-8 string, min 16 bytes). Not in `ROOT/.env`, not in the repo, not logged. Operator device also has `STEER_SEAL_MINT=1`. Agent host has the key for verify and must not mint. If both flags and the key sit in one UID, the same-UID collapse applies and the seat must not report Q41 closed.

His side stays one word. He still types `STOP` (or whatever single token he already uses) as the nudge. When `STEER_SEAL_MINT=1`, `cmd_steer` seals that token before it is treated as inbound. He types no MAC, no nonce, no timestamp.

Envelope, one line, no spaces, so it remains one CLI argument:

```
SS1|<channel>|<unix_ts>|<nonce16hex>|<WORD>|<mac64hex>
```

MAC input, exact bytes, HMAC-SHA256, hex lowercase:

```
SS1|<channel>|<unix_ts>|<nonce16hex>|<WORD>
```

WORD: `^[A-Za-z][A-Za-z0-9_-]{0,31}$`. One token. `STOP now` is not a word.

Replay: verifier clock, window 90 seconds, `abs(now - ts) > 90` rejects. Nonce remembered in the process plus an optional append-only ring. A file-writer who deletes the ring can replay a still-fresh envelope inside 90 seconds. That residual is accepted. Do not claim disk state is a trust anchor.

Channels the verifier knows: `hermes-steer`, `phone-door`, `discord` (reserved), and reject `grok-overlay` as operator authority always.

Migration: `STEER_SEAL_REQUIRED` default `0`. Bare single word still accepted, so the interrupt law holds the day this lands. Malformed or bad-MAC envelopes always reject, even during migration. Flip `STEER_SEAL_REQUIRED=1` only after the mint round-trip test passes on his real entry. This patch does not flip it.

## 3. PATCH SPEC

New file `mag/steer_seal.py` (the existing import already names this module). Apply as-is.

```python
"""steer_seal: read-path anti-forgery for operator interrupt words.

One secret: env STEER_SEAL_KEY. Operator types one word. Mint runs only
if STEER_SEAL_MINT=1. Verify never prints the key.
"""
from __future__ import annotations

import hashlib
import hmac
import os
import re
import time

WINDOW_S = 90
WORD_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{0,31}$")
NONCE_RE = re.compile(r"^[0-9a-f]{16}$")
MAC_RE = re.compile(r"^[0-9a-f]{64}$")
OPERATOR_CHANNELS = frozenset({"hermes-steer", "phone-door", "discord"})


class SealReject(Exception):
    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


def _key() -> bytes:
    raw = os.environ.get("STEER_SEAL_KEY", "")
    if len(raw.encode("utf-8")) < 16:
        raise SealReject("no-key")
    return raw.encode("utf-8")


def _mac(channel: str, ts: int, nonce: str, word: str) -> str:
    msg = f"SS1|{channel}|{ts}|{nonce}|{word}".encode("utf-8")
    return hmac.new(_key(), msg, hashlib.sha256).hexdigest()


def mint(channel: str, word: str, *, now: int | None = None, nonce: str | None = None) -> str:
    if os.environ.get("STEER_SEAL_MINT") != "1":
        raise SealReject("mint-disabled")
    if channel not in OPERATOR_CHANNELS:
        raise SealReject("bad-channel")
    if not WORD_RE.fullmatch(word or ""):
        raise SealReject("bad-word")
    ts = int(time.time()) if now is None else int(now)
    if nonce is None:
        nonce = os.urandom(8).hex()
    if not NONCE_RE.fullmatch(nonce):
        raise SealReject("bad-nonce")
    mac = _mac(channel, ts, nonce, word)
    return f"SS1|{channel}|{ts}|{nonce}|{word}|{mac}"


def verify(channel: str, blob: str, *, now: int | None = None, seen: set[str] | None = None) -> str:
    """Read-path gate. Returns the single WORD or raises SealReject."""
    if channel not in OPERATOR_CHANNELS:
        raise SealReject("not-operator-channel")
    parts = (blob or "").split("|")
    if len(parts) != 6 or parts[0] != "SS1":
        raise SealReject("bad-envelope")
    _, ch, ts_s, nonce, word, mac = parts
    if ch != channel:
        raise SealReject("channel-mismatch")
    if not NONCE_RE.fullmatch(nonce) or not MAC_RE.fullmatch(mac) or not WORD_RE.fullmatch(word):
        raise SealReject("bad-field")
    try:
        ts = int(ts_s)
    except ValueError:
        raise SealReject("bad-ts")
    clock = int(time.time()) if now is None else int(now)
    if abs(clock - ts) > WINDOW_S:
        raise SealReject("replay-window")
    if seen is not None:
        if nonce in seen:
            raise SealReject("replay-nonce")
    expect = _mac(channel, ts, nonce, word)
    if not hmac.compare_digest(expect, mac):
        raise SealReject("bad-mac")
    if seen is not None:
        seen.add(nonce)
    return word


def accept_inbound(channel: str, raw: str, *, now: int | None = None, seen: set[str] | None = None) -> str:
    """Migration-aware read. Bad envelopes always die. Bare word lives only if REQUIRED is off."""
    text = (raw or "").strip()
    if text.startswith("SS1|"):
        return verify(channel, text, now=now, seen=seen)
    if os.environ.get("STEER_SEAL_REQUIRED") == "1":
        raise SealReject("unsealed")
    if not WORD_RE.fullmatch(text):
        raise SealReject("bad-word")
    return text
```

Hunk A, Hermes read path. Anchor: `s.add_argument("nudge")` in `main()`, and `_run_hermes(goal: str, ...)`. `cmd_steer` body is truncated: UNVERIFIED. Seat greps `def cmd_steer` and inserts this as the first use of `args.nudge`, before any `_run_hermes` call. Do not seal `cmd_dispatch` goals.

```python
def _inbound_nudge(nudge: str) -> str:
    word = nudge
    if os.environ.get("STEER_SEAL_MINT") == "1" and not nudge.startswith("SS1|"):
        nudge = steer_seal.mint("hermes-steer", nudge.strip())
    try:
        word = steer_seal.accept_inbound("hermes-steer", nudge)
    except steer_seal.SealReject as exc:
        raise SystemExit(f"steer rejected: {exc.reason}")
    return word
```

Pass `word` (the single token), not the raw envelope, into `_run_hermes` as the goal. His CLI stays `steer --resume SESSION STOP`.

Hunk B, phone-door read path. Anchor: `row = {"ts": _now(), "hook": "phone-door", "ok": ok, "phone": PHONE, "latency": latency}` inside `ensure()`. Leave that row unchanged. In `status()`, when iterating `rows`, if a row has `steer` or `directive`, call `accept_inbound("phone-door", value)` and drop the row on `SealReject`. Do not reject rows that only have `ok`. `main()` stays `ensure` / `status`. No new subcommand, so his phone hook gains no ceremony.

Hunk C, grok overlay. Anchor: `return {"ok": bool(steer), ... "steer": steer, ...}` inside `decide_steer`. Add `"origin": "grok-overlay"` to that dict. Do not mint. A consumer that calls `accept_inbound("grok-overlay", steer)` must get `not-operator-channel`. No consumer is in the quoted file, so this hunk is a tag only.

Do not set `STEER_SEAL_REQUIRED=1` in this patch.

## 4. TEST PLAN

Positive, must reject (forgery):

- `verify("hermes-steer", "SS1|hermes-steer|<now>|0011223344556677|STOP|" + "ab"*32)` with a wrong MAC. Reason `bad-mac`.
- Same envelope with `ts = now - 91`. Reason `replay-window`.
- Valid envelope presented twice with the same `seen` set. Second call `replay-nonce`.
- Valid mac but channel arg `discord` while envelope says `hermes-steer`. Reason `channel-mismatch`.
- `accept_inbound("hermes-steer", "STOP now")` even with REQUIRED unset. Reason `bad-word`.
- `accept_inbound("hermes-steer", "STOP")` with `STEER_SEAL_REQUIRED=1` and no envelope. Reason `unsealed`.
- `accept_inbound("grok-overlay", <valid seal>)`. Reason `not-operator-channel`.
- Phone-door status row `{"steer": "STOP"}` with no seal is not applied.
- Empty key: `SealReject("no-key")`, and the key string never appears in the exception.

Negative, must pass unchanged (interrupt law):

- He types `STOP`. With `STEER_SEAL_MINT=1`, `mint("hermes-steer", "STOP")` then `accept_inbound` returns exactly `STOP`. One token in, one token out.
- `STEER_SEAL_REQUIRED` unset: `accept_inbound("hermes-steer", "STOP")` returns `STOP`. Existing bare interrupt still fires.
- `dispatch` goal text is not passed through `accept_inbound`. A goal sentence still dispatches.
- `ensure()` row with only `hook/ok/phone/latency` still logs and still counts in `status()`.
- `decide_steer` on a non-patch move still returns `need_steer: False` and `steer: ""`. Quoted gate: root hints win, no steer.

## 5. FALSIFIER

This design is wrong if any one of these is observed:

- A process that cannot read `STEER_SEAL_KEY` produces a blob that `verify("hermes-steer", blob)` accepts.
- After the mint wrapper is on the Hermes CLI he already uses, a normal interrupt requires him to type a second token.
- A bare `STOP` is rejected while `STEER_SEAL_REQUIRED` is unset.
- The seat reports Discord, or Q42, closed. No Discord read path is in this evidence.
- The seat reports same-UID file-writers closed. They are not, if they can read the agent environment or `ROOT/.env`.
- Verification is only added on a write helper, and a reader still applies raw nudge bytes. That misses the contract. The bind is `accept_inbound` before `_run_hermes` sees the nudge.

Uncertainty: I did not see `cmd_steer`'s body (file truncated between `_run_hermes` and the receipt tail). If that body already verifies, hunk A is a duplicate and the seat should not double-wrap. If `steer_seal` on the real tree has a different API than the import comment, the import will fail closed until this module is the one imported. That failure is preferable to accepting an unverified nudge, but it must be checked before REQUIRED is turned on, or the interrupt law breaks.
