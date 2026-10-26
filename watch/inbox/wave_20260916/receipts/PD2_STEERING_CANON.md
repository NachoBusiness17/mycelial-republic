# PD2 — STEERING CANON receipt

- **Wave:** wave_20260916 · **Lane:** PD2 · **Date:** 2026-09-16
- **Started:** 2026-09-16T23:53:15Z
- **Law:** receipt FIRST, append as you go · no git · public-domain fetches via Project Gutenberg / Standard Ebooks / CCEL only
- **Durable write root:** `memory/corpus/steering_canon/` (this receipt = wave-side pointer)

## Mission

Fetch the steering canon — the contemplative primary documents whose form the fleet's parable register inherits — into `memory/corpus/steering_canon/` with a manifest. Targets (all public domain): Meditations (Long), Enchiridion (Carter), Pensées (Trotter), The Cloud of Unknowing, The Practice of the Presence of God (Brother Lawrence), The Imitation of Christ (Book I), The Rule of St. Benedict, The Way of a Pilgrim, Ecclesiastes (KJV).

## Plan

1. Dirs created: `memory/corpus/steering_canon/` + this receipts dir.
2. Resolve legal source IDs (PG search pages / CCEL), fetch byte-identical UTF-8 text, sha256 each.
3. Extracts where the legal source bundles more than the target: Imitation of Christ → Book I only; Enchiridion → extract if source is the complete works.
4. `MANIFEST.md` + `MANIFEST.json` in `memory/corpus/steering_canon/`; receipt ends with fetched table + fleet-mechanism mapping.

## Log (appended as I go)

- 23:53Z — dirs created; receipt filed first per wave-lane law. INDEX.json untouched (concurrent wave writers; left to wave coordinator to fold).
