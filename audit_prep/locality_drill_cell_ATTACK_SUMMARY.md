# locality_drill CELL EXECUTION SUMMARY

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
The organ registry contained NO organ for:
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
Created falsifiable specification and implementation for DNS-independent host resolution:

**Files Created:**
1. `audit_prep/locality_drill_cell_ATTACK.md` - Complete cell analysis per OUTPUT CONTRACT
2. `configs/organs/host_resolver.yaml` - Organ specification
3. `mag/host_resolver.py` - Implementation with CLI
4. Updated `mag/organ_map.py` to register the new organ

**Organ Status: VERIFIED** - All evidence levels achieved:
- DECLARED: source file exists ✓
- INSTRUMENTED: callable imports ✓  
- WIRED: caller surfaces exist ✓
- STATEFUL: state paths exist ✓
- VERIFIED: deterministic probe passes ✓

## Falsifier — what would prove this wrong
1. **DNS Independence**: System continues operating after DNS failure using only cached mappings
2. **72h Offline Survival**: All services remain accessible for 72 hours without internet connectivity
3. **Automatic Recovery**: System detects and recovers from host.docker.internal resolution failures without operator intervention
4. **Fallback Path**: Host services are accessible via 127.0.0.1 when host.docker.internal fails
5. **No Manual Intervention**: System maintains functionality through Docker restarts and network changes
6. **Cache Validity**: Cached mappings remain valid across multiple container restarts

---

*Cell executed per OUTPUT CONTRACT. Concrete beats abstract. Cites repo shapes, never invention. Attack vector identified and remediation implemented.*