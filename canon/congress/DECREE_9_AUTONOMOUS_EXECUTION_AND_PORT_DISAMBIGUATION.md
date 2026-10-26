<!--
CANONICAL CONGRESS DECREE: DECREE_9_AUTONOMOUS_EXECUTION_AND_PORT_DISAMBIGUATION.md
PROVENANCE: The Standing Congress of the Sovereign Estate, Autumn Plenary Session, 2026-10-23.
AUTHORITY: Article II & Article V of canon/congress/CHARTER.md
HOUSE LAW: Strictly zero unicode em-dashes (-- and - only); strictly 0.00 / 1k first-person singular pronouns.
-->

# THE STANDING CONGRESS OF THE SOVEREIGN ESTATE
## Plenary Decree 9: Autonomous Execution, Port Disambiguation, and Metabolic Shuttling (2026-10-23)

Enacted by the Plenary Assembly of the Standing Congress to ratify the operationalization of the Ring 4 Autonomous Build Engine, finalize network port isolation between telemetry and compute, and institutionalize neuroenergetic telemetry pre-filtering across the estate.

---

## 1. Ratification of the Ring 4 Autonomous Build Engine

The Congress ratifies the deployment of `tools/selfimp_runner.py` as the sovereign execution vehicle for Ring 4:

1. **Queue Drainage & Verification**: The build engine continuously processes tasks from `state/fuel/stealth_selfimp_queue.jsonl`, executing automated boundary flux verification harnesses, validating SHA256 integrity, auditing quasilocal boundary mass, and banking verifiable receipts in `watch/inbox/selfimp/`.
2. **First Wave Certified**: The initial batch of seven autonomous build tasks (`imp004` through `imp010`) has been executed, audited, and certified with zero boundary violations.
3. **Sovereign Execution Guarantee**: Driver topic `t_selfimp` in `tools/stealth_driver.py` is permanently wired to fall back to `tools/selfimp_runner.py` whenever external endpoints are unreachable, preventing queue stalls.

---

## 2. Port Disambiguation Law & Telemetry Protocol

The Congress codifies the technical separation of estate communications:

1. **Port 8080 (Telemetry Bus)**: Permanently assigned to the Global Sovereign Telemetry Daemon (GSTD) Node Dashboard v3.5.0 (`com.docker.backend`). No local LLM completion requests shall be dispatched to port 8080.
2. **Port 8081 (Compute Serving)**: Established as the primary local compute endpoint for `llama-server` and hardware accelerated inference engines.
3. **Payload Inspection Mandate**: Health probes across `tools/stealth_driver.py` and `tools/probe20_run.py` must verify server identity and JSON status payloads rather than relying solely on HTTP 200 return codes.

---

## 3. Neuroenergetic Metabolic Shuttling (Dr. Nicholas Fabiano Steal)

In accordance with the ANLS neuroenergetics research banked in Wave 8:

1. **Astrocyte Integration**: The Congress mandates the continuous execution of `tools/astrocyte_shuttle.py` via driver topic `t_astrocyte`.
2. **Telemetry Compaction**: Raw estate churn (file additions, background tasks, verkle tree growth) shall be condensed into compact Shannon state vectors (`watch/inbox/astrocyte_feed.json`) prior to ingestion by frontier reasoning seats.
3. **System Vitality Tracking**: The estate vitality metric shall be tracked and stamped into every cycle heartbeat, maintaining metabolic equilibrium between sensory intake and execution output.

---

## 4. Enactment & Certification

Enacted this 23rd day of October, 2026, under the unanimous consent of the five Standing Committees:
- Committee on the Beacon
- Committee on Security
- Committee on Records
- Committee on Experiments
- Committee on Water
