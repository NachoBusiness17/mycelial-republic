# W6 — SEED REGISTRY + LOAD-TIME SELF-SCAN (the provenance symbiote v1) — 2026-09-07

**Lane:** W6, ladder from watch/WORLDLINE_SEED_20260907.md §3 door 2. **Cost: $0-local**
(files only, no docker, no config, no secrets, no network). **Builder:** zcode seat.
**Organ:** `mag/seed_registry.py` (~450 lines) + registry ledger
`memory/worldline/REGISTRY.jsonl` + falsifier battery `memory/runs/seed_registry/`.

## 1. Design

SkillSpector (NVIDIA) scans third-party agent skills for injection/theft/supply-chain
risk pre-install. The lawful mirror: point the same shape of paranoia at OUR OWN body —
scan OUR worldline seeds for provenance breaks and foreign-pointer risks BEFORE anything
reconstitutes from them. The worldline seed IS what such a scanner sees: a
self-propagating context payload. Our answer is the provenance-chained symbiote: hash
lineage end to end, forged lineage refuses at the door, replication stays operator-gated.

Two commands:

- **`register [SEED_PATH...]`** (default glob `memory/worldline/*/SEED.json`): full scan
  per seed, then appends one hash-chained registry row — `{ts, seed_path, session_id,
  seed_hash, chain_tip, verdict, flags, reasons, slab_shas, lens, prev_reg_hash,
  reg_hash}` — to `memory/worldline/REGISTRY.jsonl` (grounding_wave-style chain:
  genesis `0000000000000000`, reg_hash = sha256 over the canonical row minus reg_hash,
  first 16 hex). REFUSE verdicts are RECORDED too (append-only provenance history) but
  set exit 2. `verify` recomputes the registry's own chain.
- **`scan <SEED_PATH>`** — the pre-load self-scan, four lenses, verdict
  PASS / PASS-WITH-FLAGS / REFUSE, exit 0 / 2 (W1 convention):
  - **PROVENANCE** — runs `mag.worldline_seed._verify_impl` (the W1 contract, read-only
    import) when importable; else an independent MIRROR checker (same shas, marked
    MIRROR). Second belt: W6 recomputes seed_hash itself. **INTEGRITY vs DRIFT split
    (v1.1, earned during dogfood):** manifest edits (seed_hash mismatch, missing
    slab/file, truncated tape/chain) = REFUSE; *living-file drift* (manifest intact,
    seed_hash recomputes, but a snapshot sha no longer matches disk because the body
    moved on after the death-rite emit) = REVIEW flag — staleness, not forgery. W1/W2
    load-time law still refuses to reconstitute from a stale snapshot until re-mint;
    the scan is never silent about it.
  - **LINEAGE** — `position.chain_tip.leaf_hash` must EXIST in
    `memory/biography/verkle_chain.jsonl` (or in a prior registry row). A tip that
    exists nowhere = forged lineage = REFUSE.
  - **FOREIGN** — every path-keyed value and every absolute-path-looking string must be
    INSIDE the body: workspace root `C:/Users/foste/Documents/projects` or the memory
    dir worldline_seed indexes. Anything else = FOREIGN flag = REFUSE. The symbiote
    only points at its own body.
  - **HYGIENE** — the seed must be hashes/pointers/metadata only. Any string field
    >200 chars = REVIEW flag (location, length, head/tail snippet, never silent).
    Allowlisted verbatim blocks inside SEED.json: none in v1. The AGENTS.md verbatim
    embed is lawful in the W2 RESURRECTION_BUNDLE (that bundle IS the genome being
    reconstituted, sha-checked at load), NOT in the seed manifest.

**W2 INTEGRATION SEAM — deliberately UN-WIRED.** `mag/worldline_seed.py` `load` (W2
resurrection loader) should call `mag.seed_registry.scan_manifest` BEFORE reconstituting
— any REFUSE = no bundle, tamper dies at the door. W6 leaves that call site unwired and
does NOT modify `worldline_seed.py` (read-only for this lane; W1/W2's builder owns it).
The seam is one import: `from mag.seed_registry import scan_manifest` (writes nothing,
machine-readable dict, `.verdict` + `.flags`).

## 2. Falsifier battery (all three fired, receipts below)

Specimens forged from the REAL W1 seed by `memory/runs/seed_registry/make_specimens.py`,
kept OUT of `memory/worldline/` so the register default glob stays clean. The foreign
target `C:/Users/foste/Documents/attic_other/AGENTS.md` is a fiction; nothing exists there.

**(i) The real seed → PASS-WITH-FLAGS (exit 0).** `memory/worldline/
w1-dogfood-20260907/SEED.json` (seed_hash `8dbd503f64bd163c`): 0 integrity FAIL,
lineage green (tip `d0a798c2…` found at verkle chain **line 7377**), FOREIGN 0/44 path
refs outside the body, HYGIENE 0/234 string fields over 200 chars. Two REVIEW flags,
both honest living-drift: MEMORY.md + 3/40 curator files changed on disk since the
12:16Z emit (the fleet is live; the body outran the death-rite snapshot). seed_hash
recomputes OK — nothing forged. W1's own `verify` still says REJECT for those two
(living files, correct for LOAD); W6 records the distinction instead of flattening it.

**(ii) Forged seed, foreign path in a slab ref → REFUSE (exit 2) with FOREIGN flag.**
Two forgeries, both caught:
- `forge_a_naive.json` (foreign path, hash left stale) → REFUSE: seed_hash mismatch +
  FOREIGN + missing file. The amateur caught four ways.
- **`forge_b_rehashed.json` — the load-bearing one:** foreign path + seed_hash honestly
  RECOMPUTED (`8794195f40e654ed`), so provenance integrity is green and only the FOREIGN
  lens can catch it → `FLAG[FOREIGN] slabs.genome.agents_md.path: path outside the
  body` → REFUSE, exit 2. The foreign check is content-based (path vs body), not
  existence-based, so pointing at a real file outside the body dies the same way.

**(iii) Stuffed 5KB free-text field → PASS-WITH-FLAGS (exit 0), never silent.**
`forge_c_stuffed.json`: `slabs.record.curator_notes_free_text` = 5,120 chars, manifest
otherwise lawful and rehashed → `FLAG[REVIEW] … string field 5120 chars (> 200) —
head="The curator's running commentary on this worldline, stuffed far past anything a…"
tail=…` → PASS-WITH-FLAGS. A long-field stuffed payload gets named, located, and
snippered, never waved through.

## 3. Registry state

`memory/worldline/REGISTRY.jsonl` — 3 rows, chain intact (`python -m mag.seed_registry
verify` → `PASS 3 rows, tip=cb3ed78011f8090b | chain intact | verdicts: REFUSE=1,
PASS-WITH-FLAGS=2`). The three rows ARE the build's honest history, append-only:

| # | reg_hash | prev | verdict | note |
|---|---|---|---|---|
| 1 | `9d5e409c4d40e82c` | `0000…` | REFUSE | v1.0 strict: W1 FAILs taken wholesale — REFUSEd the real seed on living-file drift (over-strict, honestly recorded) |
| 2 | `24cd6d068f968ccb` | `9d5e…` | PASS-WITH-FLAGS | v1.1 integrity/drift split: real seed passes with drift named |
| 3 | `cb3ed78011f8090b` | `24cd…` | PASS-WITH-FLAGS | v1.2 final (card tally fix); verdict unchanged, lens fields clean |

The row-1 REFUSE stays in the ledger on purpose: an append-only provenance registry that
silently rewrites its own history would be exactly the thing it exists to catch.

## 4. Dogfood

Every work command wrapped through `python -m mag.bash_local`, session
`w6-seed-registry-20260907`: 10 rows (forge battery, register x3, scan real x2, scan
specimens, scan b, scan c, registry verify, tape verify), per-session chain intact.
Tape verify: `PASS 44 rows, 18 session(s), tip=4e59fa88f7a60d25 | all rows valid, chains
intact` — the W6 close-out row holds the global tip at seal time.

## 5. Handoffs / open doors

- **W2 loader** (worldline_seed owner): wire `scan_manifest` before reconstitute —
  REFUSE = no bundle. One import; the seam is documented in the module docstring.
  Un-wired by design this lane.
- **Re-mint door:** the real seed's snapshot is now stale vs the living memory body
  (drift flags). W1's owner can `emit` a fresh seed; W6's register picks it up on the
  next default-glob run. Deliberately not done here (read-only on seeds).
- **SkillSpector-shaped, v1 scope:** length-based hygiene only; injection-pattern and
  secret-pattern lenses are the natural v2 (same four-lens card, more lenses).

**Lineage:** trajectory lens (09-05) → W0 bash-local tape (09-07) → W1 death rite
(seed provenance) → F-W5 selector → **W6 the seed learns to defend itself** — forged
lineage refuses, the symbiote points only at its own body.
