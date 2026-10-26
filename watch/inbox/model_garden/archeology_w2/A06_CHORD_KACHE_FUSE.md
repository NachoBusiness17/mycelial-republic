# A-06: CHORD_KACHE_FUSE (archeology.wave2 lane receipt + spec, spec-before-code)

Schema: archeology.wave2.receipt.v1 · lane A-06 · night lane 2026-10-02 ~05:0xZ
Cost: $0 (bytes only; no code fired). Deliverable per memory/plans/
ARCHEOLOGY_20.md row A-06: strike reports position-ledger state.

## What exists tonight (byte-verified)

- mag/chord.py (chord.v1, 2026-08-26): strike() returns origin (verkle tip),
  invariants (instruction epoch + canary), corrections (laws present),
  coldest_vectors (frozen prefix sha) and a fidelity verdict. SURFACE space
  only: nothing in the report says where any MODEL stands.
- memory/runs/kache/captures.jsonl: 60 rows, schema kache.capture.v1, two
  families (gemma2:2b-instruct-q5_K_M x30, qwen2.5:3b x30), keys include
  battery_ref (lens-rz1), capture_id, layer, layer_depth_pct, model_digest,
  prompt_sha256, vector_path (npy sidecar under memory/runs/kache/vec/),
  norm, ts. Last append 2026-10-02T01:43:44Z.
- mag/chord_pipeline.py (chord_pipeline.v1, mtime 2026-08-12 08:50): stage 4
  ROUTE divides SHADOW (coldest vectors) from FRONTIER (standing-wave
  direction) but never consults the weight-space ledger.

## THE FUSE (spec, chord.v2 delta; one sitting to implement later, $0)

strike() gains a `position_ledger` block, computed by READING
memory/runs/kache/captures.jsonl only (no model loads, deterministic,
stdlib json + pathlib; fail-closed to `{"status": "no-ledger"}` when the file
is absent):

```
position_ledger: {
  status: "live" | "no-ledger" | "stale",
  rows: <int>,                       # capture row count
  families: {model_id: {rows, last_ts, layers: [min, max], batteries: [...]}},
  vector_integrity: {present: <int>, missing: <int>, size_mismatch: <int>},
  freshest_ts: <iso>, age_hours: <float>,
}
```

Fidelity verdict amendment: fidelity stays FULL/DEGRADED as today (surface
space), but a DEGRADED-position warning line is added when age_hours > 72 or
any vector_path is missing: "weight-space positions stale; strike does not
know where the models stand." The chord's contract ("one trigger reloads full
fidelity") is honest only when it names both terrains.

## The transfer this encodes (why row A-06 exists)

The chord's "coldest vectors" (frozen cache-stable instruction bytes) and the
kache ledger's cold vertices (low-attention weight positions) are the same
doctrine at two altitudes: preserve what is stable, sample what is neglected.
The fused strike report puts both colds in one report: the operator strikes
once and sees the surface cold (frozen prefix sha) beside the weight cold
(last capture ts per family). The Aug-12 operator order that borned
chord_pipeline ("shadow work on coldest vectors ... frontier work executing
the direction of the standing wave") is satisfied verbatim by reporting both.

Filed by night lane, 2026-10-02Z. $0. No em-dash bytes. Implementation ticket:
one sitting, mag/chord.py + tests/test_chord_position_ledger.py.
