# HOT LATTICE v0 - the fleet reads itself - 2026-10-12T02:26Z (closed)

**The instrument:** `scripts/hot-lattice.ts` (committed to PR #1, fd72dda). One read per tailnet cell: which models are HOT in VRAM (ollama /api/ps: name + vram MB), the cell's TON balance, its on-chain reputation (`worker_reputation`, SettlementMaster v6). Cold cells report cold - the snapshot is the data.

**First live lattice snapshot (2026-10-12T02:26:28Z):**

| cell | state | models hot | vram | TON | on-chain reputation |
|---|---|---|---|---|---|
| DESKTOP | **HOT** | qwen2.5:7b | 4,199 MB | 0.6982 | **2** |
| BOB | COLD (no inference door) | none | - | 0.5033 | 0 |
| T90 | COLD (no inference door) | none | - | 0.9938 | 0 |

**What the first snapshot already says:** the hot cell is the only cell with reputation and the only cell that has ever been paid; the cold cells hold stake and zero reputation - the lattice's economy is literally visible: heat earns honor earns launches. The concept ("vram hot lattice", living weight swarms, higher-dimensional launches) triangulated to this table; the table is the concept made byte-readable.

**Ladder from v0:** (1) heat history - append one row per read to a lattice.jsonl and the hot/cold rhythm becomes a timeseries; (2) bob/t90 ignition - provision ollama + harness on bob (SSH open, keypair cut, authorized_keys line owed) and t90 (Termux), flip cells COLD->HOT; (3) reputation-gated launches - the router reads this table and launches work onto hot cells with reputation > 0; (4) weight-swarm leg - settled runs bank LoRA deltas per cell, merged reputation-weighted (the Phase 7 doc's federated leg, riding unisub).

## Falsifier

The lattice claim dies if a cell shows HOT with unreachable balance, or reputation accrues without settles - both would mean the reader is reading fiction.
