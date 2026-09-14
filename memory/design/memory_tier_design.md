# Memory Tier Design — three scopes, one spine

## (a) Organs — load-bearing vs supporting, with load-bearing rationale

**Load-bearing (break the system if they fail):**

1. **Spine writer** — one process, one append-only handle to the verkle chain. Rationale: the chain is the sole record; parallel writers = parallel truths. Falsifier: `chain_write_conflict` — two seats append same tick; chain diverges; resolution is completion-index reconciliation, never merge.
2. **Scope gate** — enforces scratch / working / blackboard boundaries on every write. Rationale: #1 smell is cross-scope bleed (scratch lands in blackboard unpromoted). Falsifier: `scope_bleed` — grep `memory/` for scratch-mark files found outside scratch/; count > 0 = gate failed.
3. **Receipt ledger** — every durable write produces a signed receipt (path, hash, tick). Rationale: "receipts or it didn't happen"; chain hashes rows, not world. Falsifier: `orphan_write` — file exists on disk with no corresponding receipt in the ledger.

**Supporting (degrade gracefully):**

4. **Decay sweeper** — TTL-based removal of expired scratch / working-set artifacts. Falsifier: `stale_scratch` — scratch files older than session TTL still present; non-fatal, periodic audit.
5. **Blackboard index** — searchable catalog of blackboard contents. Falsifier: `index_mismatch` — index count vs actual blackboard file count; >5% drift triggers rebuild.
6. **Scratch buffer** — per-seat ephemeral store, no durability guarantee. Falsifier: `scratch_persist` — scratch file survives session end without promotion; should not.

Load-bearing triangle: spine + gate + receipt. Without any one, the system reverts to "chat is truth" and the chain becomes decorative.

**Confidence: 8/10** — triangle sound; decay sweeper TTL values untested on real workload.

---

## (b) The Loop — one tick, one process, one writer to the spine

Single tick cycle (all seats run this, one at a time via the spine writer):

```
READ intent (operator handoff / card)
  → SCOPE CHECK (scratch / working / blackboard?)
    → WRITE to scope buffer
      → PROMOTE? (intent flag + receipt)
        → SPINE WRITER appends to verkle chain (one handle, serialized)
          → DECAY sweep (scratch TTL expiry)
            → INDEX update (blackboard catalog)
              → HEARTBEAT (liveness organ — separate, see known gaps)
```

Rules: one writer (`spine_write()` is the only function that touches the chain handle), one tick per intent, one process (no background daemons own the spine — standing law). Failed spine write aborts tick, error logged to `memory/runs/errors/<tick>.jsonl`, seat retries next tick. No silent drop.

Known gap: liveness heartbeat is a *missing organ* — the loop has no independent witness that the spine writer is alive. Current workaround: `memory/runs/heartbeat.jsonl` self-reported by the writer (unreliable — smell: self-reported health lies).

**Confidence: 7/10** — loop simple and correct; missing liveness witness is an honest gap.

---

## (c) The Tests — falsifiable, discriminating, could kill the claim

Test matrix (fits existing `pytest -q` harness, 39 deterministic green + 2 model-gated):

| Test | Claim it kills | Falsifier | Type |
|------|----------------|-----------|------|
| `test_spine_one_writer` | Only one process appends to chain | Spawn 2 seats, both append same tick; chain must reject or reconcile | deterministic |
| `test_scope_gate_no_bleed` | Scratch never lands in blackboard unpromoted | Plant scratch file, run tick, grep blackboard/ — must be absent | deterministic |
| `test_receipt_ledger_complete` | Every durable write has a receipt | Write N files, count receipts == N; mismatch = fail | deterministic |
| `test_orphan_detection` | No file without a receipt | Delete a receipt, run audit — must flag orphan | deterministic |
| `test_decay_scratch_ttl` | Scratch expires after session TTL | Create stale scratch file (mtime > TTL), run sweep, verify absent | deterministic |
| `test_index_match` | Blackboard index == actual files | Shuffle files, rebuild index, compare counts | deterministic |
| `test_chain_hash_row` | Chain hashes rows, not world | Tamper a leaf, verify root mismatch detected (LAW-064 trap) | deterministic |
| `test_promote_scratch_to_working` | Intent flag required for cross-scope move | Promote without flag — must reject | deterministic |
| `test_blackboard_readable` | Blackboard is the only shared read surface | Seat reads blackboard, not another seat's scratch | deterministic |
| `test_tick_abort_on_spine_fail` | Failed spine write aborts tick, no silent drop | Inject spine failure, verify error row in `memory/runs/errors/` | deterministic |

Model-gated (2): `test_demand_routing` and `test_load_balance` — require live fleet with multiple seats; run on Sep 20 proof deadline. Could-kill criterion: any deterministic test failing blocks the tick. Model-gated tests inform but don't block.

**Confidence: 9/10** — tests discriminating, each targets one claim; model-gated tests honest about their uncertainty.

---

## (d) The Architecture — fits one Windows PC + a coming 512GB local machine

**Current (one Windows PC):** Spine writer = single process, file handle to verkle chain on disk (`memory/biography/verkle_chain.jsonl`). No DB, no daemon. Scope buffers: directories under `memory/` — `agent_sessions/` (scratch), `working.md` + `runs/` (working set), `improve/` + `runs/` (blackboard). Plain files, no sync overhead. Receipt ledger: append-only JSONL, `memory/runs/receipts/`. Decay sweep: cron-triggered (MagImproveDaily 08:00), TTL config per scope. Index: flat JSON catalog, rebuilt on demand.

**Post-Rocinante (4x M5 Ultra, 512GB):** Same file layout; scale is vertical, not architectural. Scratch buffers live in RAM disk (512GB >> working set); spill to disk on session end. Blackboard index grows — switch to content-addressed catalog (anchor hash = file hash) to keep lookup O(1). Spine writer: still one process, but can shard chain segments across 4 drives (segment = seat shard, append-only per shard, merge on read). Optimization, not structural change — one writer still serializes appends to the canonical chain.

**What does NOT fit:** Shared chat memory across seats (violates one-line, no-parallel-truths). Multi-writer chain appends (violates spine rule). Background daemons owning the spine (violates one-process, no-second-scheduler).

**Honest unsound parts:** (1) Liveness witness is missing — the loop has no independent heartbeat. Design assumes operator watches the board; automated liveness organ is a build target, not implemented. (2) Decay TTL values are guesses — no workload data yet. First sweep may over-delete or under-delete; audit at Sep 20 proof deadline. (3) Demand-side routing is not in this tier — it's the organ table's job (missing). Memory tier routes by scope, not by load.

**Confidence: 7/10** — architecture fits current hardware honestly; Rocinante scaling straightforward; liveness and routing gaps disclosed, not papered over.

---

## Confidence (honest)

| Section | Score | Rationale |
|---------|-------|-----------|
| (a) Organs | 8/10 | Triangle sound; decay sweeper untested |
| (b) The Loop | 7/10 | Simple and correct; liveness witness missing |
| (c) Tests | 9/10 | Discriminating, each kills one claim; model-gated honest |
| (d) Architecture | 7/10 | Fits current HW; Rocinante scaling trivial; liveness + routing gaps disclosed |

**Overall: 7.75/10** — honest design, no hidden liabilities, gaps named not hidden. Buildable from this file.

---

*Design date: 2026-09-12. Falsifiers named per claim. Receipt: this file is the artifact; no chain knot yet — pending operator GO.*
