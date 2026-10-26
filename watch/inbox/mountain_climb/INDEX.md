# MOUNTAIN CLIMB INDEX - the brief's cover page

Date: 2026-09-30 · Owner: ZCode seat (INDEX lane) · Parent plan: `watch/inbox/THE_MOUNTAIN_CLIMB_PLAN.md` · No commit.
This directory holds the Phase 0 dossiers (lanes MC1-MC6) that feed the Opus-lensing brief. The brief is assembled by pasting these into the skeleton's slots (§1 of `OPUS_BRIEF_SKELETON.md`); the evidence pack is regenerated from bytes at assembly time, never from these files. Em-dash count: 0 (house law).

## 1. Inventory (all hashes and sizes byte-read this session)

| File | Bytes | sha256-8 | One-line purpose | Status |
|---|---|---|---|---|
| `SHERPA_DOSSIER.md` | 19,189 | 40acc9fe | MC1. The carrier architecture: seats, mates, stealth fleet, improve cycle, memory organs, meters, discipline organs, compute laws; every organ PROVEN / PARTIAL / DORMANT with its receipt | **landed** (2026-09-30) |
| `GOALS_DOSSIER.md` | 17,384 | 04e98f37 | MC2. Where we want to be: the summit statement in the operator's words, the five-layer goal stack, canon quotes with paths, non-goals | **landed** (2026-09-30) |
| `GAP_ANALYSIS.md` | 4,478 | 86831f0c | MC3. Where we are: eight system rows (status, maturity, missing piece, source) plus the brutal one-paragraph truth: everything passes its own tests, nothing has met a stranger | **landed** (2026-09-29) |
| `ROUTE_V0.md` | 27,945 | 1fef52ee | MC5. The climb from where we stand to the summit: eight pitches (P1-P8), each with WHAT / WHY NOW / HOW / a falsifier VERIFICATION / lane-day ESTIMATE / named ATTACK SURFACE; written to be attacked | **landed** (2026-09-30, 14:49 local; the "incoming" named in the order is in) |
| `BIBLIOGRAPHY.md` | 15,030 | df6926b6 | MC4. Curated per-domain design sources (netcode, MMO servers, procgen, anti-cheat, GWAP/verifiable play, engine failure, distribution), each with verification mark [V]/[T]/[K], what it teaches, why it earns the slot | **landed** (2026-09-29) |
| `OPUS_BRIEF_SKELETON.md` | 14,831 | 1ec18b0b | MC6. The spec for the paid ask: seven sections with byte budgets (37,000 target / 40,960 ceiling), the seven-instrument evidence pack rules, the ask questions; the ROUTE slot stays v1-empty until Phase 1 hardening | **landed** (2026-09-30; it is the SPEC, not the brief) |

Known drift, named: ROUTE_V0 byte-checked the-mountain at HEAD `7d5dbe2`, past the `cf2ec7d` the gap analysis cites; gap rows were verified one session earlier (09-29). ROUTE_V0 is the fresher read where they differ.

## 2. Reading order for a frontier model reading cold

1. **SHERPA_DOSSIER** - learn the carrier first: what machinery exists, what is proven vs dormant, and the reading laws (trust bytes, not reports) every other dossier obeys.
2. **GOALS_DOSSIER** - the destination: the summit statement and goal stack the route serves.
3. **GAP_ANALYSIS** - the current position: system-by-system truth, and the missing mile (SRP6 port + one real build + one external player).
4. **ROUTE_V0** - the path between the two: pitches, orderings, falsifiers, attack surfaces. Read it adversarially; it was written to be attacked.
5. **BIBLIOGRAPHY** - the external map: which primary sources back each design decision the route cites by `bib §N.N`.
6. **OPUS_BRIEF_SKELETON** - how all of the above gets compressed into the 40 KiB paid ask; the output contract and ask questions live here.

## 3. Cross-reference: the operator's order → the dossier that answers it

Order (verbatim): "sherpa our goals where we are where we want to be and the systems within as well as their sources"

| Phrase of the order | Answered by | Where exactly |
|---|---|---|
| "sherpa" (the carrier) | `SHERPA_DOSSIER.md` | All sections: seats (§1), mates (§2), stealth fleet (§3), organs 4-8, the one-paragraph carrier truth |
| "our goals" | `GOALS_DOSSIER.md` | §1 summit statement (operator's words), §2 goal stack, §3 canon, §5 non-goals |
| "where we are" | `GAP_ANALYSIS.md` | §table rows 1-8 (system, status, maturity, missing piece) + the brutal one-paragraph truth |
| "where we want to be" | `GOALS_DOSSIER.md` (the summit) + `ROUTE_V0.md` (the path to it) | Goals §1-2; Route §1 thesis, §2 pitches |
| "the systems within" | `SHERPA_DOSSIER.md` (estate organs) + `GAP_ANALYSIS.md` (game-stack systems) | Sherpa organs 1-8; Gap rows 1-8 |
| "as well as their sources" | Every dossier's per-claim path cites + `BIBLIOGRAPHY.md` | Receipt paths inline in each; external design sources in Bib §1-§7 |
| (how it reaches Opus) | `OPUS_BRIEF_SKELETON.md` | §1 slot map: which MC dossier pastes into which brief section |

## 4. Status board

- **Landed (6/6 files):** everything in §1. All six MC lanes of the plan's Phase 0 have bytes on disk; each file carries its own filing note and em-dash-zero claim.
- **Building:** nothing in this directory. Phase 1 (adversarial read of the route by the estate's own fleet, per plan) is the next transform: it turns ROUTE_V0 into v1.
- **Slot-reserved (no bytes yet, expected in this dir's flow):**
  - ROUTE v1: the hardened route after Phase 1 attacks; the skeleton's section 4 slot stays empty until it exists.
  - The assembled OPUS brief itself: built by `tools/lensing_ask.py` from the skeleton slots + evidence pack regenerated from bytes at assembly time; fires ONLY on operator GO (AA1 law). Not a hand-edit file.

**Filing:** this INDEX is a receipt; registered as the cover page for the brief assembly. Owner: this seat. No commit.
