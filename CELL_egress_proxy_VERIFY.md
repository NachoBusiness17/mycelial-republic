# Egress Proxy Audit Prep Cell
## Finding — what your cell yields
The egress_proxy organ is **not explicitly defined** in the organ registry (organ_map.v1). The closest load-bearing components handling egress are:
- **api_gateway** (mag/api_gateway.py): HTTP route registry with constant-time X-API-Key gate
- **api_server** (mag/api_server.py): FastAPI wrapper exposing the gateway on 127.0.0.1:8001 with CORS from anywhere
- **switchboard** (mag/switchboard.py): Routing mesh between seats and external systems with tier-based access control
- **browser_env** (mag/browser_env.py): Allowlisted web surfaces only (computer-use seat)
- **openclaw** (deploy/openclaw/): External gateway parked behind compose profile `retired-openclaw`

The **softest assumption** is that **credential injection into external egress channels happens solely via the X-API-Key gate and allowlist enforcement**, with no explicit credential management organ visible in the core registry.

## Evidence — what in the repo supports it (file/shape, no invention)

### 1. API Gateway Security Gate (api_gateway.py:60-94)
```python
API_KEY_HEADER = "X-API-Key"
_ENV_KEY = "MAG_API_KEY"

def check_api_key(headers: dict, query: Optional[dict] = None) -> bool:
    expected = api_key()
    presented = headers.get(API_KEY_HEADER) or headers.get(API_KEY_HEADER.lower())
    if presented is None and query:
        presented = str(query.get("key") or "") or None
    if presented is None:
        return False
    return _const_eq(presented.strip(), expected)
```
- Constant-time comparison (XOR-accumulate, no early exit)
- Accepts key via header OR query parameter (`?key=`)
- Line 86: "the key may also ride ?key= (the operator's board page; loopback-bound service)"

### 2. API Server Loopback Binding (api_server.py:35-54)
```python
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8001

# 2026-08-29: the operator's board page (file:// on the desktop) fetches this
# loopback-bound service — allow cross-origin from anywhere; the port never
# leaves the machine and every route still requires the key.
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"],
                   allow_headers=["*"])
```
- Explicitly bound to 127.0.0.1:8001
- CORS allows any origin (desktop board page)
- Every route still requires X-API-Key header

### 3. Switchboard Tier-Based Routing (switchboard.py:29-40, 515-555)
```python
TIER_ORDER = ("T0", "T1", "T2", "T3")
TIER_RECEIVE = {
    "T0": frozenset({"T0"}),
    "T1": frozenset({"T0", "T1"}),
    "T2": frozenset({"T2"}),  # T2 cannot receive T0/T1
    "T3": frozenset(TIER_ORDER),
}

def tier_allows(*, holder_tier_max: str, payload_tier: str) -> bool:
    holder = (holder_tier_max or "T2").upper()
    payload = (payload_tier or "T2").upper()
    return payload in TIER_RECEIVE.get(holder, TIER_RECEIVE["T2"])
```
- T2 is the remote/public boundary
- T2 cannot inherit access to T0/T1 (more sensitive classes)
- Tier-based access control for cross-seat context drops

### 4. Browser/Computer-Use Seat Allowlist (browser_env.py:23-50, 85-96)
```python
def is_host_allowed(url_or_host: str, cfg: dict[str, Any] | None = None) -> bool:
    cfg = cfg or load_config()
    if not cfg.get("enabled"):
        return False
    host = host_from_url(url_or_host) or (url_or_host or "").lower().strip()
    if not host:
        return False
    allowed = [str(h).lower().strip() for h in (cfg.get("hosts") or []) if h]
    for a in allowed:
        if host == a or host.endswith("." + a):
            return True
    return False
```
- Only allowlisted hosts can be accessed
- Default allowlist includes: chat.openai.com, claude.ai, grok.x.ai, x.com, github.com, localhost, 127.0.0.1
- Requires explicit enable flag

### 5. OpenClaw External Gateway Status (organ_map.py:182-191)
```python
{
    "id": "openclaw",
    "label": "OpenClaw runtime policy",
    "module": "",
    "callable": "",
    "source": "deploy/openclaw/openclaw.container.json",
    "wired_by": ["docker-compose.yml", "deploy/openclaw/entrypoint.sh"],
    "state_paths": [r"C:\Users\foste\.openclaw\openclaw.json"],
    "receipt_paths": [],
    "proof": "openclaw_config",
}
```
- External gateway system
- Parked behind compose profile `retired-openclaw` (watch/OPENCLAW_RETIRED_20260909.md)
- Zero traffic 09-02→09-09

## Risk if wrong — what the audit breaks on if this is missed

1. **Credential Injection Flaw**: If external egress accepts credentials through channels other than the X-API-Key gate, abliteration would reveal unprotected credential injection points.

2. **Tier Boundary Violation**: If T2 seats can receive T0/T1 payloads, the tier system is compromised, breaking the documented security model.

3. **Allowlist Bypass**: If browser_env allows non-allowlisted hosts, the computer-use seat becomes an unrestricted egress vector.

4. **Loopback Exposure**: If the API server binds to 0.0.0.0 instead of 127.0.0.1, the authenticated gateway becomes network-reachable.

5. **Query Parameter Key Leak**: If ?key= parameter is logged or exposed in CORS responses, API keys could leak to unintended origins despite CORS restrictions.

## The act — the concrete prep step (file/spec/number)

Create a falsifiable specification file that defines the egress_proxy organ and its security invariants:

**File**: `configs/organs/egress_proxy.yaml`
```yaml
# egress_proxy organ specification v1
schema: organ.v1
id: egress_proxy
label: Iron Egress Proxy
module: mag.egress_proxy
callable: proxy_request
source: mag/egress_proxy.py
design:
  security_gate: X-API-Key constant-time comparison
  allowlist_mode: hosts + window titles only
  tier_boundary: T2 (remote/public) cannot receive T0/T1
  loopback_only: 127.0.0.1:8001 binding
  credential_injection: only via X-API-Key header
  external_gateway: openclaw (retired profile)
  computer_use_seat: browser_env.yaml allowlist

wired_by:
  - mag/api_gateway.py
  - mag/api_server.py
  - mag/switchboard.py
  - mag/browser_env.py

state_paths:
  - memory/runs/egress_proxy/audit.jsonl

receipt_paths:
  - memory/runs/egress_proxy/receipts.jsonl

security_invariants:
  - "X-API-Key gate must use constant-time comparison"
  - "No credential injection except via X-API-Key"
  - "Tier T2 cannot receive T0/T1 payloads"
  - "Host allowlist enforced for computer-use seat"
  - "API server bound to 127.0.0.1 only"
  - "Query parameter ?key= must not be used in production"
```

**Implementation**: Create `mag/egress_proxy.py` implementing the organ with these features:
- stdin/stdout Python organ (single-file)
- Constant-time API key gate
- Host allowlist enforcement
- Tier-based routing
- Credential injection surface only via X-API-Key

## Falsifier — what would prove this wrong

1. **Constant-time bypass**: A timing attack reveals API key comparison is not constant-time.

2. **Credential injection via other channels**: Secrets or tokens injected through URL parameters, headers, or body fields bypass the X-API-Key gate.

3. **Tier boundary violation**: A T2 seat successfully receives and processes a T0/T1 payload.

4. **Allowlist bypass**: The browser_env seat accesses a non-allowlisted host (e.g., external API without explicit entry in browser_env.yaml hosts).

5. **Loopback exposure**: The API server binds to 0.0.0.0 or any non-loopback address.

6. **Query parameter key leak**: The ?key= parameter appears in CORS responses, browser history, or server logs.

7. **External gateway activation**: The `retired-openclaw` profile is unparked and begins receiving traffic without explicit operator GO.

---
*Cell executed per OUTPUT CONTRACT. Concrete beats abstract. Cites repo shapes, never invention.*