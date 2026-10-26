# TRAVEL KIT 2026-09-19 — the fleet in one file

**What:** `memory/portable_bags/travel_kit_20260919T220156Z.zip` (134.9 MB zip, 252.9 MB unpacked, 15,517 files), built by `scripts/build_travel_kit.py`, self-verified 15,517/15,517 sha256 ok. Manifest (every file hash + every pointer) committed as the receipt: `memory/portable_bags/travel_kit_20260919T220156Z.manifest.json`.

**Composition:** code (mag 1,033 files / scripts / tools / configs incl. gitignored runtime `providers.yaml` and `.env`), live ledgers (queue lanes + trails, memory small dirs incl. briefs/rib/rib_bus/packs/law/portable_bags/research_packs), docs, tests, watch top-level (INDEX + contracts + recent receipts), all root docs. Per-file cap 8 MB.

**Pointers (14 over-cap files stay archived here, listed in manifest with sha256 up to 64 MB):** the three runaway dashboard files (largest 2.14 GB), `training/events.jsonl` (204.5 MB), engine + churn logs, dashboard media (suno mp3s, ractor full dump), `matthew_export.tar.gz`. Rule: ask the archive, verify the hash.

**Boot on a cold machine:** unzip, `ensure_venv.ps1`, `mag.cmd doctor`, `mag.cmd lab` (:8765). README inside the zip carries the same steps.

**Honest deltas vs the filed tier-1 estimate:** 15,517 files / 253 MB, not ~4,000 files / <0.1 GB. The estimate undercounted small-but-live state: watch inbox receipts (56.5 MB), handoff (28.2 MB), docs (21.2 MB), and 9,142 small memory ledger files (50.1 MB). Still a one-file transport: Drive, USB, or any git release asset. The zip itself is gitignored (regenerable); only the manifest is tracked.

**Regenerate anytime:** `.venv/Scripts/python.exe scripts/build_travel_kit.py` (builds + verifies). `--verify` re-checks the newest kit. Laptop law from TWO_MACHINE_SYNC_20260919.md still applies: one machine live at a time.
