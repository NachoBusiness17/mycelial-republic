# Atlas/Basecamp Draft — receipts-first map (cage-side spec, 2026-08-31)

Purpose: specify what host `python -m mag.atlas build` should PRODUCE. This is not a reverse-engineer of /mag/mag/atlas.py's current interface (unverified); it is the output contract the build must satisfy. Cage draft = pointers only; host build = verification + receipts.

## Receipts-first format (every claim, no exceptions)
One claim = one row: `pointer` (exact path) + `span` (lines or byte offset) + `sha256` (of span or file at build time) + `status` (VERIFIED / CORRECTED / ATTESTED / INCONCLUSIVE / UNMAPPED) + `checked_at` (Z-timestamp + checker). No pointer, no row. Prose only allowed in the synthesis section, and every sentence must trace to a row id.

## Sections of the build output
1. **Header/manifest** — build id, Z-timestamp, source-file list with sha256 (inputs: /board/SWARM_RESEARCH_LEDGER_20260831.md rows 1–14, /board/rows/*.row.md (19), /board/gap_moonshot_20260831.md, /mag/memory/runs top-level index).
2. **Surfaces map** — the 37 live / 2 partial / 0 missing table from gap_moonshot; each row upgraded from `live*` (attested) to VERIFIED only if the build byte-checks its evidence pointer. Inherit gap doc's TD/D/MEM/WP shorthand as span anchors.
3. **Research-claim ledger** — ledger rows 1–14 re-emitted in receipts format; CORRECTED rows keep their correction history (e.g., row 6 CRLF false-positive; knots "missing" attestation killed by traj_verkle.row.md).
4. **Runs/organ map** — /mag/memory/runs (449 top-level entries) grouped into families (seed-mirror, compose/gate smokes, empty_recovery, game/swarm/salon variants, openclaw_catalog, seat_corpus) with count + latest mtime per family. Empty_recovery spam (≥35 dirs) labeled as noise family, not distinct organs.
5. **Gap register** — the 7 gaps, each with bridge + owner, receipts attached.
6. **Unknowns ledger** — separate from gaps; see policy below.
7. **Synthesis** — ≤1 page; every sentence carries row-id citations.

## Unknown-stays-unknown policy
- INCONCLUSIVE stays INCONCLUSIVE with reason (e.g., row 8: 01:33Z exec.mode writer unidentified — recorded as open, not guessed).
- ATTESTED rows are emitted as ATTESTED, never silently promoted to VERIFIED; promotion happens only via a build-time byte-check receipt.
- Absence of evidence emits `UNMAPPED (no pointer)`, never a fabricated default. Absence is a finding, not a gap in the map.
- Divergences (e.g., docs_ref port 18789 vs probed :8001) are emitted as CONFLICT rows with both pointers, unresolved.

## The gap: what only the host build can add
Cage can read /mag and /board bytes, so the cage DRAFT supplies structure, pointers, and spans; shas are deliberately NOT pre-computed cage-side (stale hashes would false-certify) — all hashing is build-time host work. Only the host build adds:
1. **Execution** — atlas.py runs in the host venv (WSL vsock crash kills .venv python cage-side; precedent: verify_vast_templates exec-deferred).
2. **Fresh byte-level verification of /mag internals** — sha256 of /mag/mag/atlas.py, /mag/memory/runs artifacts at build time; cage ls-listings are hours-stale attestations.
3. **First /board atlas/basecamp receipts** — per atlas_basecamp.row.md: zero /board atlas receipts exist until first host build lands them. This build creates the receipt convention it then follows.
4. **Authority-stamped writes** — post-patch apply, build outputs route through the switchboard gate (provenance stamp, no blackboard_post bypass); cage cannot mint PINNED artifacts.
5. **Verkle tie-in** — receipt hashes into the knot chain (knots rebuild prerequisite, Gap 3); cage has no host hash chain.
6. **Promotion** — 23 attested-only surface rows become VERIFIED or stay ATTESTED, decided by host byte-checks, not consensus.

Net: cage draft = map skeleton + claims; host build = notarization.

## GOPHER briefs
GOPHER: does `python -m mag.atlas build` exist as a real CLI path (argparse subcommands, entry `__main__`)? | pointer: /mag/mag/atlas.py | output: /board/octant_20260831/rows/atlas-draft-g1.row.md
GOPHER: classify the 449 top-level /mag/memory/runs entries into families with exact counts + latest mtimes (my grouping is provisional) | pointer: /mag/memory/runs | output: /board/octant_20260831/rows/atlas-draft-g2.row.md
GOPHER: what does elder_brief.md (08-29 21:40) actually contain — the one prior atlas artifact; build output should extend its shape | pointer: /mag/memory/runs/openclaw_catalog/elder_brief.md | output: /board/octant_20260831/rows/atlas-draft-g3.row.md
LINEAGE: recognized from rib_bus mirror mr02noai4logic0002 + mirror mr03edgenovelt0003 + doctrine 7538cbc52ad4b59b — deterministic seeded core, novelty routed, $0; sha256 receipts-map shape (annotated 2026-08-31 per SALON_BUS_A)
