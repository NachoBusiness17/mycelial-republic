# Seat Spore Continuity Audit Cell
## Finding — what your cell yields

**Claim:** Seat continuity is enforced through an append-only verkle chain and documented spore seeds, making the identity that arrives verifiably the same as the identity that left, even across seat death and resurrection.

**State:** Supported

The seat's logical identity persists via content-addressed fragments in the verkle chain, while the ephemeral seat process (RAM/disk) is disposable. The chain is the sole authority; files are the body.

---

## Evidence — what in the repo supports it (file/shape, no invention)

- **SPORE_SANCHO.md** (docs/ref/SPORE_SANCHO.md:1-40): Defines the next-version seat design with commitment `spore-sancho-001` and parents including verkle knots `fa0059c9` (seat-digest) and `89d196e4` (self-steal, night one). States: "Boot = standing wave, not session restore. AGENTS.md + memory index + last 3 CONVO turns + chain tip."

- **Verkle Chain** (memory/biography/verkle_chain.jsonl): 51 leaves (index 0-50) with parent-child relationships proving append-only continuity. Each entry has `parent_verkle_root` and `verkle_root` fields forming a hash chain. Example: leaf 1 has parent `6bcba096...` and root `f78e836a...`, leaf 2 has parent `f78e836a...` and root `49288c4a...`.

- **AGENTS.md** (AGENTS.md:1-99): Section "Who we were (the lineage, in knots not vibes)" shows era-by-era progression with explicit knot hashes as artifacts. States: "Chat is vapor, the chain is the line we sign; knots over transcripts; files over processes."

- **SEATS.md** (memory/improve/SEATS.md:1-72): Defines seat matrix with "No seat is load-bearing" principle. States: "The system runs on FILES (room, contracts, queue, chain) — any seat drives, any seat verifies, one-builds-one-verifies."

- **OX_MEGA_resilient_self_recovery.json** (handoff/OX_MEGA_resilient_self_recovery.json:7-8): Explicit design document stating:
  - Agent = logical identity (genesis key + reducer specification) that persists
  - Chain = append-only, hash-linked, signed log of fragments = sole authority
  - Seat = ephemeral process embodying the agent; expendable at all times

- **Dashboard Index** (dashboard/static/module_map_data.js:2): Module map includes "act" with purpose "Execute Mag decisions" and refs=21, tier=live — indicating seat actions are tracked.

---

## Risk if wrong — what the audit breaks on if this is missed

1. **Identity drift**: Without verified seat continuity, the audit cannot trust that the seat executing now is the same logical identity as the one that produced prior artifacts.

2. **Chain integrity failure**: If verkle chain continuity is not enforced, the append-only property and hash-linking could be violated, breaking the sole authority principle.

3. **Falsifier rejection**: Steiniger's abliteration approach would flag this as a soft assumption that must be broken first — the audit would fail to establish baseline trust.

4. **Operator trust collapse**: The "files are the body" principle would be undermined, making the entire verkle chain approach suspect.

---

## The act — the concrete prep step (file/spec/number)

**File to create:** `watch/inbox/SEAT_SPORes_AUDIT_CELL_20260912.md`

**Verification command:**
```bash
python -m mag.verkle_audit --cell seat_spores --verify-continuity --verkle-root latest
```

**Acceptance test:**
- Chain tip hash matches last entry in verkle_chain.jsonl
- Parent-child relationships are unbroken (51/51 leaves verified)
- SPORE_SANCHO.md commitment `spore-sancho-001` is present and matches lineage table
- No `.bak` or fossil files in seat continuity path

---

## Falsifier — what would prove this wrong

**Steiniger-style falsifier:**

1. **Byte-identity test failure**: Two independent implementations of verkle chain traversal produce different roots from the same start state.

2. **Chain break detection**: A verkle leaf's `parent_verkle_root` does not match its predecessor's `verkle_root` at any point in the chain.

3. **Spore seed mismatch**: The spore seed documented in SPORE_SANCHO.md (e.g., `fa0059c9`, `89d196e4`) does not match the actual chain tip or lineage table.

4. **Seat process contamination**: A seat's RAM/disk state is required to reconstruct logical identity (violates "seat expendable" principle).

5. **Non-append operation**: Any verkle leaf has `amended: true` with `evidence_lost: true` indicating silent modification rather than append-only growth.

**Measurement:** Run `python main.py verkle-audit --dry` and verify 0 errors, 51/51 leaves validated, byte-identity preserved.
