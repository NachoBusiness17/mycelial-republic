ENTRY FILE
packs/p320_matthew_ds_20260913.json (see ids smoke_harness__mapa / smoke_harness__mapb)

OUTSIDER READING GUIDE
- Entry file: packs/p320_matthew_ds_20260913.json — the pack carries the smoke_harness context and IDs the wave uses.
- Three things to check:
  1) Smoke runner: run the multi-smoke command invoked by phase1_verify.cmd ("main.py multi-smoke" → %TEMP%/mag_smoke.json). Verify mag_smoke.json contains "\"ok\": true" and the expected "dual_local" marker.
  2) Pack IDs and topics: confirm the pack includes smoke_harness__mapa/mapb by grepping packs/p320_matthew_ds_20260913.json and packs/p160_matthew_20260913.json; correlate with dashboard/static/topic_index.json topics built timestamp.
  3) Seat contracts: inspect jobs/first-4h-chain/SPEC.md and jobs/first-4h-chain/seat_contract.json for explicit smoke directives (model ids, GET /v1/models requirement) to ensure the harness' threat model is declared.
- The one trap: implicit assumption that "multi-smoke" passes equals fidelity. The harness tests connectivity and a lightweight chat, not visual/measureText/gradient fidelity; the examiner will expect explicit headless-render fidelity tests.

SUMMARY:
Wrote this one-page guide pointing the examiner to the pack entry, three concrete checks, and the single trap.

DELIVERABLE:
C:/Users/foste/Documents/projects/local_sovereign_agent/packs/smoke_harness__map_README.md
