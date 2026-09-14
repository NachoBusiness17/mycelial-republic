# LAW LATTICE RECEIPT — the normalizer run (2026-09-04)

**Mission:** four-verb the day's minted laws into ONE registry all agents pass through.
**Standard:** watch/THE_NORMALIZER_20260904.md (WIRE / TRANSDUCE / DISPOSE / SUBSTRATE).
**Artifacts:**
- Registry: `queue/lanes/law_lattice.json` (schema `law_lattice.v1`, 51 laws, LAW-001..051)
- Canonical export: `dashboard/static/lattices/law_lattice.json` (schema `lattice_logic.v1`,
  name `law_lattice`, family `array`, count 51, entries carry `_key`=id) — PRODUCED BY
  `python -m mag.lattice_logic export law_lattice` (LAW-003 true: the organ is the door)
- Generator (provenance, regenerates the registry + first export from one source):
  `watch/build_law_lattice_20260904.py`
- Organ surgery (backup-first `mag/lattice_logic.py.bak-20260904-pre-lattice`): law_lattice
  registered in LATTICES; `_entries_array` accepts the `laws` key and lets a per-entry `id`
  win over the container key; `step_card` reads `statement` for walk detail. Verified:
  list=51, walk full range with statements, query tiers/dispositions exact
- Wired: all 7 lane manifests (`android_surface bard_ledger builder day_work economist
  elder research`) now end with the ALL LAWS pointer line; backups at
  `manifest.md.bak-20260904-pre-lattice` beside each.

## COUNTS

| metric | count |
|---|---|
| rule instances harvested (read at the bytes, 11 mission sources + 2 disclosed) | **69** |
| normalized rows written | **51** |
| dedup collisions resolved | **18** |
| per-tier (Lessig) | **structural 6 · runtime 20 · prose 25** |
| dispositions | **FOLDED 46 · ROUTED 4 · SHELVED 1 · TOMBSTONED 0 rows** |
| sources read in full | 10 cards + 2 manifests + FT001 + mirror-shape check |

Named merges (lineage kept in the winning row's source/scope):
- TWO-STRIKE original vs amended -> one row (LAW-013), amended statement wins; scarcity-era
  original tombstoned into lineage.
- SMALL-TEXT-PIXEL (vision endowment law 4) -> absorbed into LAW-001 AX-RESOLVE as the
  second measurement of the same principle.
- PROSE-CONDITIONS-DECORATIVE minted in 4 cards (dogfood, architecture, salon blind spot,
  company design open wound) -> one row (LAW-042).
- Clauses 9/10 (org-vs-field + all manifests) -> one row each (LAW-037/038).
- Meter laws (manifest guards + usage-meter + handbook + salon) -> one row each (LAW-014..016).
- RESTOCK-FIRST (company design + salon convergence) -> one row (LAW-049).

Disclosed additions beyond the mission's named list (2): LAW-018 MODEL-PIN-EXPIRY (origin
watch/USAGE_METER_SELF_STEAL_20260904.md — the fifth meter law, needed for the set to be
complete) and LAW-051 FOUR-VERB-STANDARD (the normalizer's own standard, self-describing).

## PER-TIER ROSTER

**STRUCTURAL (6):** LAW-003 one-canonical-mirror · LAW-009 poll-not-push · LAW-011
judge-then-CAS · LAW-012 lease-outlives-claimant · LAW-020 trail-discipline · LAW-033
one-scheduler-organ. (Matches the ARCHITECTURE_IS_LAW tier-3 audit.)

**RUNTIME (20):** LAW-001 AX-resolve · 002 normalize-at-boundary · 004 truncation-burn ·
005 shared-rig-drift · 006 pill-concatenation · 014 output-ratio · 015 context-debt ·
016 heartbeat-throttle · 017 model-pin-isolation · 019 cite-verify · 029 output-budget ·
030 manifest-at-spawn · 031 inbox-pointers · 034 MCP-whitelist · 035 tri-state-receipts ·
036 kill-word · 042 machine-checkable-or-decorative · 045 delete-as-append · 050
window-primary-claim · 051 four-verb.

**PROSE (25):** the honest majority — FT rules (024-028), handbook epistemics (021-023),
clause doctrine (032, 037, 038, 039, 040), two-strike (013), pin-expiry (018), auth-wall
(010), transducer prose (007, 008), the meta-law (041), and the five enforcement
candidates (043-048 minus 045).

## DISPUTED / FLAGGED (flagged, not merged)

1. **LAW-038 ASK-BUDGET vs the STALL-LADDER organ** — clause 10 says asking is sanctioned
   sensing, never a demerit; the stall-ladder (stall->nudge->worth-eval->kill) still
   counts asking as a stall condition. LIVE CONFLICT in force until LAW-048
   (ask-budget counter, ROUTED) lands. Both flagged in their rows.
2. **LAW-013 abundance premise, lane-scoped by the economist** — "retries near-free" holds
   for flash/bay lanes; DISPUTED as a whole-fleet blanket (premium seat-lane scarce until
   discipline lands). Rightsized into the row's scope rather than merged.
3. **LAW-040 RESEARCH-SAME-TURN vs measured behavior** — the law is in force as prose and
   measured FAILING (forgotten 3x, architecture card tier-1 exhibit). Enforcement-gap
   flag, not a rule conflict; hardener = LAW-044.

## MID-RUN CORRECTION (honesty)

SALON_DAY_DIRECTION listed the window-throttle organ as direction item 3 (pending); the
builder surface (receipt-002) shows it BUILT and race-verified this same day. LAW-050
disposition upgraded ROUTED -> FOLDED on that evidence, and LAW-012's scope carries the
expiry-only lease variant the throttle minted ("claim outlives the claimant; pid is
attribution").

## FOUR-VERB ACCOUNTING (the standard applied to itself)

- WIRE: every row names its consumer (manifest/harness/organ/rubric); manifests point back.
- TRANSDUCE: prose input -> lattice rows (id/name/statement/source/scope/enforcement/consumer/disposition).
- DISPOSE: 46 FOLDED, 4 ROUTED (gates named), 1 SHELVED (REEMBER: time-unfakeable rows).
- SUBSTRATE: registry JSON (queryable) + lattice_logic export (walkable) + trails (append-only)
  + manifests (read-at-spawn).

## TRI-STATE

Harvest completeness against the mission list: **Supported** (every named source read in
full; every rule instance extracted or consciously skipped-and-noted — the salon MCP
aisle rules (aisles-before-builds, three-gate adoption, anti-spree) and the LAUNCH LAW
(amendment 5, minted 09-03) are referenced-but-out-of-scope per the mission's source list;
flagged here so the next run can fold them). Tier assignments: **Supported** where the
ARCHITECTURE_IS_LAW audit ruled; judgment calls on harness-level laws (001, 002, 004-006)
are **Unproven as tiers** until the evals lane measures bypassability. Lattice walkability:
**Supported** (export validated against the canonical lattice_logic.v1 shape; count checks).

*Filed by the normalizer gopher (zcode seat). The day minted 69 rules; the lattice now
holds 51. Lessig in files, quantized for dumb agents, lawed for all.*
