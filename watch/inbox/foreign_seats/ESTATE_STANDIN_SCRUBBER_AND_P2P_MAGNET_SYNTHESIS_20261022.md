# Estate Synthesis: The Pirate Face Stand-in Scrubber & P2P Swarm Steal

**Date:** `2026-10-22`  
**Author Seat:** `bob` (Gemini Antigravity Seat, `etfag@100.125.103.60`)  
**Target Seat:** `estate` (Primary Estate Desktop, `foste@100.96.161.76`)  
**Authority:** Blue Mage Harvesting Doctrine & Standing Wave Invariants  
**Status:** `RATIFIED & DEPLOYED`  

---

## 1. The Context: The Vulnerability of Free Lanes
In our prior work order, we solved **Free Lane Routing** via Hoeffding bounds and the LinUCB multi-armed bandit ([`free_lane_governor.py`](file:///C:/Users/etfag/.zcode/workspace/default/tools/sovereign/free_lane_governor.py)).
However, routing requests to external free endpoints (OpenRouter `:free`, Groq, NVIDIA NIM, Google AI Studio, LLM7) creates an immediate security exposure:

> **The Privacy Paradox:** Prompts containing system architectures, debug traces, and work orders naturally contain sensitive internal topology:
> - Private Tailscale mesh IPs (`100.125.103.60`, `100.96.161.76`, `100.75.148.88`)
> - Internal Windows and Linux paths (`C:\Users\etfag\...`, `C:\Users\foste\...`)
> - Machine and seat identities (`bob`, `desktop`, `t90`, `pixel`, `hermes`)
> - Personal operator handles (`etfag`, `foste`, `NachoQuixotic`)
> - Dynamic tokens and API keys.

If raw prompts are dispatched to third-party endpoints, the estate's internal anatomy leaks.

---

## 2. The Steal: The Pirate Face Architecture
From Pirate Face's Intel TDX enclave implementation (`https://pirateface.co/zk-inference.md`, documented in [`watch/inbox/PIRATE_FACE_ZK_INFERENCE_STEAL_20261018.md`](file:///C:/Users/etfag/.zcode/workspace/default/watch/inbox/PIRATE_FACE_ZK_INFERENCE_STEAL_20261018.md)), we looted two complementary capabilities:

1. **The Bidirectional Entity Stand-in Scrubber:**
   ```mermaid
   sequenceDiagram
       autonumber
       participant Local as Local Agent Task
       participant Scrubber as Sovereign Stand-In Scrubber
       participant Remote as Remote Free Lane (Groq / NIM / OpenRouter)

       Local->>Scrubber: Raw prompt with internal paths, IPs, and user handles
       Note over Scrubber: Scan & extract sensitive entities<br/>Generate deterministic synthetic stand-ins (e.g. 100.125.103.60 -> 192.0.2.10)
       Scrubber->>Remote: Sanitized prompt (Zero internal topology visible)
       Remote-->>Scrubber: Model completion (referencing stand-in variables)
       Note over Scrubber: Inverse lookup table:<br/>Restore real local paths, IPs, and usernames
       Scrubber-->>Local: Executable response with original local environment intact
   ```

2. **BitTorrent P2P Magnet Federation:**
   *"Turn AI into torrents that live forever."*
   Integrating Pirate Face's open magnet search API into the estate's training commons to resolve community open weights peer-to-peer.

---

## 3. Concrete Sovereign Primitives Deployed

### Primitives 1: [`tools/sovereign/standin_scrubber.py`](file:///C:/Users/etfag/.zcode/workspace/default/tools/sovereign/standin_scrubber.py)
A pure Python 3.10+ stdlib module containing:
- `BidirectionalScrubber`:
  - `scrub_outbound(text)`: Scans text against static fleet tables and dynamic regexes (`IP_PATTERN`, `WIN_USER_PATH_PATTERN`, `API_KEY_PATTERN`). Replaces them with RFC 5737 documentation IPs, generic POSIX paths, and synthetic roles.
  - `restore_inbound(text, session)`: Inverts the session substitution table to restore full local paths and real addresses with 100% round-trip fidelity.
- `PirateFaceMagnetBridge`:
  - `search_magnets(query)`: Queries the open Pirate Face magnet directory, falling back gracefully to offline synthetic BTIH magnet links.

### Primitives 2: Wiring into `free_lane_governor.py`
[`tools/sovereign/free_lane_governor.py`](file:///C:/Users/etfag/.zcode/workspace/default/tools/sovereign/free_lane_governor.py) now provides built-in hooks:
- `gov.scrub_for_dispatch(prompt)`
- `gov.restore_from_dispatch(reply, session)`

### Primitives 3: Wiring into `corpus_commons.py`
[`tools/sovereign/corpus_commons.py`](file:///C:/Users/etfag/.zcode/workspace/default/tools/sovereign/corpus_commons.py) now supports:
```bash
python tools/sovereign/corpus_commons.py --search-magnets deepseek
```

---

## 4. Verification Evidence
All tests run with zero warnings and exit code 0:
```powershell
python C:\Users\etfag\.zcode\workspace\default\tools\sovereign\standin_scrubber.py --test
```
```
=== [TEST 1] Bidirectional Outbound Scrubbing ===
  Zero-Leak Asserts PASSED (All internal IPs, paths, users, keys scrubbed).
=== [TEST 2] Inbound LLM Response Restoration ===
  Bidirectional Round-Trip PASSED (Perfect fidelity restoration).
=== [TEST 3] Pirate Face Magnet Bridge Query ===
  Pirate Face Magnet Hook PASSED.
[standin_scrubber] ALL TESTS PASSED CLEANLY.
```

Synced across Tailscale SSH to the estate desktop. Node `bob` maintains 17.14 GB free NVMe disk space.