ROW
pointer: http://mag-sovereign:8765/api/v1/fleet/hypervisor
claim: Mag dashboard fleet/hypervisor endpoint live — serves fleet data (200)
type: probe
confidence: H
status: VERIFIED
arbitration: initial lane verdict DECAYED tested 127.0.0.1 from inside the cage — wrong namespace; dashboard listens on the mag-sovereign container/host, not cage loopback. Sancho re-probe via docker net: mag-sovereign:8765 -> 200 (2026-08-31 04:59Z). Host-loopback :8765 remains the operator's Windows surface.
evidence: HTTP 200 from mag-sovereign:8765/api/v1/fleet/hypervisor; ECONNREFUSED only for in-cage 127.0.0.1
