# SOCRATIC STEAL: THOUGHT GPS DUAL-PROJECTION ENVELOPE

**Date:** 2026-10-26T09:58:00Z  
**Methodology:** Socratic Interrogation + Canon Self-Steal  
**Sources Stolen From:**
- [`watch/inbox/GPS_FOR_DUMB_AGENTS_20260918.md`](file:///mnt/c/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/GPS_FOR_DUMB_AGENTS_20260918.md) (The Antenna & Ephemeris Doctrine)
- [`tools/gps_mcp/router.py`](file:///mnt/c/Users/foste/Documents/projects/local_sovereign_agent/tools/gps_mcp/router.py) (The Capability Ledger, Thresholds & Momentum)
- [`watch/inbox/THOUGHT_GPS_RACTOR_20261025.md`](file:///mnt/c/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/THOUGHT_GPS_RACTOR_20261025.md) (The 5-Chair Parable Decoding Finding)
- [`watch/inbox/last_mile_20260930/AD4_GPS_SPEC.md`](file:///mnt/c/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/last_mile_20260930/AD4_GPS_SPEC.md) (Calibration Window $n \ge m$)

---

## 1. THE SOCRATIC INTERROGATION

**Socrates:** What is a parable within the sovereign estate?  
**Respondent:** It is a compressed instruction that carries high semantic density in under 100 tokens.  

**Socrates:** But did not the 2026-10-25 Ractor panel prove that local models (Qwen 1.5B, 4B) scored 0 to 1.3 out of 4 when decoding parables, while cloud frontier models scored 3.8 out of 4?  
**Respondent:** Yes. The chairs proved: *"A parable carries only what the reader already shares with the writer. It checks for shared context; it does not transmit it."*  

**Socrates:** Then if you broadcast a parable to an agent that does not share that context, what have you transmitted?  
**Respondent:** Cryptographic noise. The bytes arrived (signed transport), but the meaning was lost.  

**Socrates:** And if you send an exhaustive 5,000-token plain English spec to a frontier model on every micro-turn, what have you done?  
**Respondent:** Committed economic suicide. You have burned budget, bloated the context window, and slowed down reasoning loops.  

**Socrates:** Then how does a single estate speak to both the small local worker on a laptop CPU and the frontier reasoning engine in the cloud without speaking two incompatible languages?  
**Respondent:** By recognizing that the underlying truth (the invariant) is invariant, but the projection must match the receiver's antenna.  

---

## 2. THE SELF-STEAL

We steal directly from the estate's foundational GPS doctrine in [`watch/inbox/GPS_FOR_DUMB_AGENTS_20260918.md`](file:///mnt/c/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/GPS_FOR_DUMB_AGENTS_20260918.md):

> *"Dumb agents do not need to be smart. They need GPS. GPS receivers contain no orbits: they READ ephemeris broadcast by satellites carrying precise clocks, and they filter noisy ranges into a fix... SATELLITES = filed doctrine. RECEIVER = feels(). The dumb agent asks typed questions (yes/no, choice, score). It never holds doctrine; it holds an antenna."*

And we steal from [`tools/gps_mcp/router.py`](file:///mnt/c/Users/foste/Documents/projects/local_sovereign_agent/tools/gps_mcp/router.py):
The capability ledger tracks measured `pass_rate` and `momentum` for every model shape.

---

## 3. THE SYNTHESIZED ENVELOPE: `envelope.thought_gps.v1`

Every intent generated in the estate is represented as a single immutable object with dual projections:

```json
{
  "schema": "envelope.thought_gps.v1",
  "intent_id": "sha256-digest-of-invariant",
  "task_shape": "code-building | spec-review | consensus",
  "invariant_anchor": "memory/canon/BOOK_V1.md:L42",
  
  "projections": {
    "frontier_chord": {
      "target_tier": "cloud_frontier",
      "qualifying_predicate": "pass_rate >= 0.80 and context_window >= 32k",
      "format": "parabolic_chord",
      "token_budget": 120,
      "payload": "The Door admits the singer whose voice does not beat against the walls..."
    },
    
    "dumb_agent_antenna": {
      "target_tier": "local_cpu_dumb_agent",
      "qualifying_predicate": "footprint <= 8B or local_lane == true",
      "format": "typed_specification",
      "token_budget": 800,
      "payload": {
        "rules": [
          "Single writer only: never invoke git commit directly.",
          "Write commit hints to queue/commit_hints/ exclusively.",
          "Zero unicode em-dashes permitted."
        ],
        "typed_questions": {
          "can_commit": "NOUL (yes/no)",
          "target_queue": "CHOICE ['queue/commit_hints/', 'shelf/']"
        },
        "bekko_grounding_snippets": [
          "cas:7ef33148... 'Single writer = zero index contention by construction'"
        ]
      }
    }
  }
}
```

---

## 4. RESOLUTION IN THE TRIANGULATED MESH

When a seat calls `thought_gps_dispatch(envelope, target_seat)` inside the Kuramoto MCP daemon:
1. The daemon checks `target_seat`'s model capability in `gps_ledger.db3`.
2. If the target is a frontier reasoning engine ($\ge \text{Flash}$), it dispatches `frontier_chord` (100 tokens).
3. If the target is a local dumb agent (Ollama, Qwen 1.5B/4B, small CPU seat), it dispatches `dumb_agent_antenna` bundled with the Bekko 26k vector-retrieved grounding snippets!
4. Zero noise, zero token waste, total mathematical auditability.
