# locality_drill CELL EXECUTION — 72h OFFLINE TEST ATTACK

## Finding — what your cell yields
The system's weakest offline assumption is **host.docker.internal as a stable localhost resolver**. This assumption breaks when Docker Desktop restarts, host networking changes, or the Windows host loses internet connectivity. The attack reveals: 1) containers lose access to host services (ollama, APIs) when DNS resolution fails, 2) the system lacks DNS-independent fallback paths, 3) operator intervention becomes required for basic functionality despite claims of local autonomy.

## Evidence — what in the repo supports it (file/shape, no invention)
### 1. Host Dependency in docker-compose.yml (lines 25-31, 61, 270, 293)
```yaml
# The eye is HOST ollama (127.0.0.1:11434) since 2026-09-07 — Docker Desktop
# proxies host.docker.internal to host loopback (same proven path as Bionic).
# OLLAMA_HOST: "http://host.docker.internal:11434/v1"
extra_hosts:
  - "host.docker.internal:host-gateway"
```

### 2. API Gateway Loopback Binding (api_server.py:35)
```python
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8001
```

### 3. Browser Environment CDP (browser_env.yaml:7)
```yaml
cdp: "ws://127.0.0.1:9222"   # containerized Playwright/Chromium CDP over localhost
```

### 4. Organ Registry Blindness (organ_map.py:46-409)
The organ registry contains NO organ for:
- Host service discovery
- DNS-independent host resolution
- Network state monitoring
- Service health fallbacks

## Risk if wrong — what the audit breaks on if this is missed
1. **Local Autonomy Claim Failure**: If the system cannot operate without internet or stable host networking, the "sovereign local substrate" claim is falsified
2. **Container Isolation Breach**: Host.docker.internal resolution failures break container isolation guarantees
3. **Service Availability Crisis**: Ollama, API gateway, and browser seat become unreachable simultaneously
4. **Operator Dependency**: System requires manual DNS/network intervention instead of self-healing
5. **Offline Capability Claim**: The 72h offline test fails at the first Docker restart or network change

## The act — the concrete prep step (file/spec/number)
Create a falsifiable specification for DNS-independent host resolution:

**File**: `configs/organs/host_resolver.yaml`
```yaml
# host_resolver organ specification v1
schema: organ.v1
id: host_resolver
label: DNS-Independent Host Resolver
module: mag.host_resolver
callable: resolve_host
source: mag/host_resolver.py
design:
  dns_fallback: /etc/hosts + environment variable override
  service_discovery: ollama, api_gateway, browser_cdp on 127.0.0.1
  network_monitor: detect connectivity loss and trigger fallback
  health_probe: verify service availability before use
  offline_mode: maintain cached service mappings when disconnected

wired_by:
  - docker-compose.yml
  - mag/api_server.py
  - mag/browser_env.py
  - mag/swarm_worker.py

state_paths:
  - memory/runs/host_resolver/mappings.jsonl
  - memory/runs/host_resolver/network_state.json

receipt_paths:
  - memory/runs/host_resolver/receipts.jsonl

security_invariants:
  - "Must resolve host.docker.internal without DNS"
  - "Fallback to 127.0.0.1 when DNS fails"
  - "Cache mappings survive 72h offline"
  - "No external dependencies for host resolution"
```

**Implementation**: Create `mag/host_resolver.py` implementing:
- DNS-independent host resolution using /etc/hosts and environment overrides
- Network state monitoring with automatic fallback to loopback
- Service health discovery for ollama (11434), api_gateway (8001), browser_cdp (9222)
- Offline capability maintaining cached mappings
- Integration with organ registry for status reporting

## Falsifier — what would prove this wrong
1. **DNS Independence**: System continues operating after DNS failure using only cached mappings
2. **72h Offline Survival**: All services remain accessible for 72 hours without internet connectivity
3. **Automatic Recovery**: System detects and recovers from host.docker.internal resolution failures without operator intervention
4. **Fallback Path**: Host services are accessible via 127.0.0.1 when host.docker.internal fails
5. **No Manual Intervention**: System maintains functionality through Docker restarts and network changes
6. **Cache Validity**: Cached mappings remain valid across multiple container restarts

---

*Cell executed per OUTPUT CONTRACT. Concrete beats abstract. Cites repo shapes, never invention.*