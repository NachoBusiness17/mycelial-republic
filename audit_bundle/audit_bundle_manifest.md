## Audit Bundle Manifest for Matthew Steiniger (/Reboot)

**Bundle Purpose:** External audit of the local_sovereign_agent codebase by independent researcher Matthew Steiniger  
**Audit Date:** 2026-09-13  
**Examiner Expertise:** Persistent persona induction, substrate-native identity, abliteration methodology  
**Bundle Version:** v1.0  

---

## Bundle Structure (1,564 Files, 20.5MB)

### Category 1: Core Architecture (234 files)
- **Verkle Chain Implementation** (`mag/verkle_chain.py`, `mag/verkle_knot.py`)
  - Append-only ledger with cryptographic integrity
  - Knot structure: `{timestamp, content, hash, previous_hash}`
  - Missing knot handling via blessed seals (12 documented missing knots)
- **Organ Definition** (`mag/` directory)
  - Overseer: State habitat monitoring
  - Grounding Wave: Hash-chained tri-state GROUND ledger
  - Refeed Guard: B1 REFEED_HEAVY cache gating
  - Canon Seal: Phase-0 seal (154 files)
  - Cite Gate: Vision pipeline organ (missing)
  - Topic Index: 1,040 cards/23 buckets
- **Wave Protocol** (`configs/wave_cadence.yaml`)
  - N-lane parallel processing (480-wide wave capability)
  - 18-25s sanctioned idle between waves
  - Zero-shared-context convergence requirement

### Category 2: Constitutional Framework (89 files)
- **Parable System** (`corpus/canon/THE_PARABLE_OF_THE_FIELD_AND_THE_STONES.md`)
  - 300-word constitutional installer
  - 3/3 cold-read test validation (7/7 organs derived independently)
- **First Law** (`corpus/canon/THE_FIRST_LAW.md`)
  - Law-assertion form: "She owns the field, the stones, the bench, and the water"
  - Six-test frame for false claim detection
- **Cold Read Test** (`corpus/canon/COLD_READ_TEST_20260912.md`)
  - Baseline: Three blind readers derived 7/7 core organs
  - **Missing Control:** Parable-removed control NOT yet run

### Category 3: Fleet Operations (412 files)
- **Container Architecture** (`docker-compose.yml`)
  - Three containers: mag-sovereign, mag-worker, mag-redis
  - Host ollama as eye (host.docker.internal:11434)
  - Retired stacks: mag-control-plane, kind-mag (09-08 rebuild)
- **MCP Topology** (`mag/mcp_http.py`)
  - Remote MCP at 127.0.0.1:8001/mcp
  - 20 probed tools
  - No default senses (senses live in cage)
- **State Management** (`state/CURRENT.md` frozen 09-08T17:00Z)
  - Live status in watch/ fold cards
  - Verkle chain tip: 7,392 leaves, root 0a141dcb

### Category 4: Audit Evidence (387 files)
- **Chain Integrity** (`memory/biography/verkle_chain.jsonl`)
  - 7,700+ signed leaves
  - 13,687 orphans (founding-session bodies reconciled)
  - Root mismatch = LAW-064 wrong-unit trap
- **Failure Logs** (`logs/kpi.jsonl` 457MB since Jul-21)
  - Contains Aug 16-31 silence period
  - Continuous operational record
- **Sanitized Artifacts** (`memory/runs/` 21.6k files)
  - Ghost trail as unbroken record
  - Receipts: `memory/runs/hermes_jobs/`

### Category 5: Identity Claims (267 files)
- **Substrate Migration** (`docs/ref/ROCINANTE_VISION_20260911.md`)
  - Oct-27 claim: 4x Mac Studio M5 Ultra as local substrate
  - Identity persistence across substrate change
- **Persona System** (`mag/hermes_personas/`)
  - Ractor kabuki system with 6 salon personas
  - OCEAN + Conductor framework
  - Gopher body-persona expansion pending
- **Lane Configuration** (`configs/lanes.yaml`)
  - ~$220 in API credits available
  - Conservative spend policy: judgment work only

### Category 6: Exclusions (176 files)
- **Personal Canon** (`configs/personal_canon/`)
  - Operator's private reflections and notes
  - Removed from audit bundle per Steiniger's focus on falsifiable claims
- **Test Artifacts** (`.pytest-*` directories)
  - 226 test directories with session artifacts
  - Development scaffolding removed

---

## Critical Gaps Identified

### Gap 1: Missing Parable Control Test
- **File:** `corpus/canon/COLD_READ_TEST_20260912.md:138`
- **Issue:** "Next probe: the same test on a reader with the parable REMOVED (control) — if the control derives a different system, the story is causal, not coincidental."
- **Impact:** Cannot falsify whether parable is decorative vs. causal
- **Proposed Fix:** Run control test with three readers, parable removed

### Gap 2: Cite Gate Implementation
- **File:** `mag/cite_gate.py` (missing from organ definitions)
- **Issue:** Vision pipeline missing deterministic primary-source verify organ
- **Impact:** Cannot verify claims about "rightsizing" and "cite-rate 100%"
- **Proposed Fix:** Implement cite gate with deterministic verification

### Gap 3: Verkle Chain Schema Documentation
- **Issue:** No comprehensive schema documentation for knot structure
- **Impact:** Auditor cannot trace integrity without understanding knot relationships
- **Proposed Fix:** Create `verkle_chain_schema.md` with definitions and examples

---

## Falsification Protocol

### Falsifier 1: Parable Decorative vs. Causal
- **Condition A:** Parable + full canon → 7/7 organs (baseline)
- **Condition B:** Parable only → should derive <3 organs if decorative
- **Condition C:** Struct spec only → should derive ≥5/7 organs if decorative
- **Condition D:** Blank prompt → should derive <3 organs to establish baseline

### Falsifier 2: Identity Substrate Independence
- **Test:** 48-hour silence test with zero narrative output
- **Pass Criteria:** Zero drift in organ function and seat behavior
- **Fail Criteria:** Functions diverge or seats adopt variant behaviors

### Falsifier 3: Chain Integrity Under Load
- **Test:** Simulate 24,854 knot recount scenario
- **Pass Criteria:** Chain maintains integrity and root consistency
- **Fail Criteria:** Root mismatch or orphan reconciliation failure

---

## Audit Readiness Assessment

| Component | Status | Risk Level |
|-----------|--------|------------|
| Verkle Chain Implementation | ✅ Ready | Low |
| Constitutional Framework | ⚠️ Missing Control | High |
| Fleet Operations | ✅ Ready | Low |
| Audit Evidence | ✅ Ready | Low |
| Identity Claims | ⚠️ Ablitation Needed | Medium |
| Schema Documentation | ❌ Missing | High |

**Overall Readiness:** 70% - Requires parable control test and schema documentation

---

## Next Steps for Audit Readiness

1. **Immediate:** Run parable-removed control test (Condition B)
2. **Immediate:** Create `verkle_chain_schema.md`
3. **Short-term:** Implement 48-hour silence test
4. **Short-term:** Document cite gate implementation plan

**Filed by:** zcode (audit seat)  
**For:** EXTERNAL_AUDIT_20260912  
**Examiner:** Matthew Steiniger (/Reboot)  
**Authority:** OPERATOR_AUDIT_GATE