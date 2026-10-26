# assemble-A1 - ASSEMBLED by cheap seat from the premium reasoning channel (descent law leg 6)

# 1. THREAT MODEL

| Threat | Vector | Consequence | Mitigation |
|---|---|---|---|
| Forged steering directive | Attacker writes a directive file into the inbox without authorization | Agent executes attacker-controlled steering | HMAC envelope over directive bytes; verify before admit |
| Tampered directive | Attacker modifies an already-sealed directive in transit or at rest | Agent executes altered steering | HMAC covers full payload; any byte change fails verify |
| Replay | Attacker re-submits a previously valid sealed directive | Stale or duplicated steering applied | Envelope carries nonce and timestamp; verifier rejects reused nonce and expired timestamp |
| Key compromise via loose permissions | Keyfile readable by other local users or processes | Attacker can mint valid seals | Keyfile contract: mode 0600, owned by the agent user, path outside the inbox |
| Downgrade / bypass | Caller skips verify and admits raw directive | All envelope guarantees void | Single admit path; admit calls verify; no direct read path into the steering consumer |
| Fail-open on verifier error | Verifier raises or returns ambiguous result and caller proceeds | Unverified directive admitted | Safe-fail rule: restrictive-honored-on-verify-fail; any non-affirmative verify result means reject |

# 2. VERIFIER DESIGN

The verifier is the only gate between the inbox and the steering consumer.

Envelope fields: version, key_id, nonce, timestamp, payload, mac.

MAC is HMAC over the canonical serialization of version, key_id, nonce, timestamp, and payload. Canonical serialization is fixed field order, no whitespace variance, UTF-8.

Keyfile contract:
- Path is configured, not derived from the directive.
- Mode 0600.
- Owned by the agent user.
- Loaded once at startup, held in memory, never logged.
- key_id in the envelope selects the key; unknown key_id fails verify.

Verify procedure:
1. Parse envelope. Parse failure is a verify failure.
2. Check version is supported. Unsupported version is a verify failure.
3. Look up key by key_id. Unknown key_id is a verify failure.
4. Recompute MAC over canonical serialization. Mismatch is a verify failure.
5. Check nonce against the seen-nonce store. Reuse is a verify failure.
6. Check timestamp against the freshness window. Outside window is a verify failure.
7. Only if all checks pass, return affirmative.

Safe-fail rule: restrictive-honored-on-verify-fail. Any exception, timeout, missing key, unreadable keyfile, or ambiguous result is treated as verify failure. On verify failure the directive is rejected and the restrictive default is honored. The verifier never returns "unknown" that a caller could read as "proceed."

Admit procedure:
- admit(path) reads bytes, parses envelope, calls verify, and only on affirmative passes payload to the steering consumer.
- On verify failure, admit rejects and records the rejection. It does not fall back to raw payload.
- There is no alternate admit path.

# 3. PATCH SPEC

Module sketch, paste-able as `mag/steer_seal.py`:

```python
# mag/steer_seal.py
import hmac, hashlib, json, os, time

VERSION = 1
FRESHNESS_SECONDS = 300

class VerifyError(Exception):
    pass

class KeyStore:
    def __init__(self, path):
        self.path = path
        self.keys = {}
        self._load()

    def _load(self):
        st = os.stat(self.path)
        if st.st_mode & 0o077:
            raise VerifyError("keyfile permissions too open")
        with open(self.path, "rb") as f:
            raw = json.load(f)
        self.keys = {k: bytes.fromhex(v) for k, v in raw.items()}

    def get(self, key_id):
        key = self.keys.get(key_id)
        if key is None:
            raise VerifyError("unknown key_id")
        return key

class NonceStore:
    def __init__(self):
        self.seen = {}

    def check_and_record(self, nonce, ts):
        if nonce in self.seen:
            raise VerifyError("nonce reuse")
        self.seen[nonce] = ts
        self._evict(ts)

    def _evict(self, now):
        cutoff = now - FRESHNESS_SECONDS
        self.seen = {n: t for n, t in self.seen.items() if t >= cutoff}

def canonical(env):
    return json.dumps(
        {
            "version": env["version"],
            "key_id": env["key_id"],
            "nonce": env["nonce"],
            "timestamp": env["timestamp"],
            "payload": env["payload"],
        },
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")

def compute_mac(key, env):
    return hmac.new(key, canonical(env), hashlib.sha256).hexdigest()

def seal(key_id, key, payload):
    env = {
        "version": VERSION,
        "key_id": key_id,
        "nonce": os.urandom(16).hex(),
        "timestamp": int(time.time()),
        "payload": payload,
    }
    env["mac"] = compute_mac(key, env)
    return env

def verify(env, keystore, noncestore, now=None):
    try:
        if env.get("version") != VERSION:
            raise VerifyError("unsupported version")
        key = keystore.get(env["key_id"])
        expected = compute_mac(key, env)
        if not hmac.compare_digest(expected, env.get("mac", "")):
            raise VerifyError("mac mismatch")
        ts = env["timestamp"]
        now = now if now is not None else int(time.time())
        if abs(now - ts) > FRESHNESS_SECONDS:
            raise VerifyError("stale timestamp")
        noncestore.check_and_record(env["nonce"], ts)
        return True
    except VerifyError:
        return False
    except Exception:
        return False

def admit(path, keystore, noncestore):
    with open(path, "rb") as f:
        env = json.load(f)
    if not verify(env, keystore, noncestore):
        raise VerifyError("directive rejected")
    return env["payload"]
```

Wiring points:
- Construct KeyStore once at startup from the configured keyfile path.
- Construct NonceStore once at startup, process-lifetime.
- The steering consumer calls admit() and nothing else. It never reads inbox files directly.
- On 
