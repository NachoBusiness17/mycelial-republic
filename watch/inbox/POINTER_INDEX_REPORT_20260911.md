# POINTER INDEX VALIDATION — by-session_*.json (2026-09-11)

**Scope:** all 7,786 `by-session_*.json` stubs in `memory/biography/knots/` — the candidate
join table for a retro-knotter folding orphan records back into the verkle chain.
**Method:** pure Python, zero LLM calls, read-only except this file. Chain set recomputed
from `memory/biography/verkle_chain.jsonl` (7,377 rows, 7,377 distinct filenames).
Verification was run on the **full population**, not just the requested sample
(200 random, seed 20260911, + all July / Aug 16–31 targets) — the full pass was cheap, so the
sample numbers below are superseded by census numbers.

## Headline rates (census, n=7,786)

| Metric | Rate | Numbers |
|---|---|---|
| Target resolution (file exists on disk) | **100%** | 7,786 / 7,786, zero missing, zero unreadable |
| leaf_hash match (pointer hash == target file's own hash) | **99.99%** | 7,785 / 7,786 |
| Pointer target already IN the chain | **97.2%** | 7,570 / 7,786 |
| True orphans (target NOT in chain) | **2.8%** | **216 pointers** |
| Pointer hash == chain leaf_hash (same filename) | **100%** | 7,570 / 7,570, zero mismatches |
| Chained knots with NO pointer (index coverage gap) | 0.4% | 31 / 7,377 |

## PREMISE CORRECTION (important for the retro-knotter)

The index is **not** a pure orphan list. Only **216** of the 7,786 pointers point at
unchained files; the other 7,570 point at knots already folded into the chain — and for
every one of those, the pointer's leaf_hash agrees exactly with the chain's leaf_hash
(0 disagreements). So this is best understood as a **mirror + pending-tail**: a redundant
side index of the chain plus a 216-row orphan tail. The mirror is harmless (and a free
integrity cross-check); the retro-knotter's actual work queue is the 216.

## The index is THREE families, not one naming scheme

| Family | n | Pointer-name derivation | Name→session_id join verified |
|---|---|---|---|
| `v2_<32hex>` | 7,347 (94.4%) | **sha256(session_id)[:32]** | 7,347/7,347 exact (md5: 0/7,347) |
| `<8hex>-<3-4hex>` (uuid slice) | 153 | **first 12 chars of session_id** | 153/153 (100%) |
| semantic truncation (`law-LAW-3-00`, `memlang-*`, `rib_bus_*`, `work-seat-*`…) | 286 | 12-char prefix of session_id | 249 literal + 34 with `:`/`_`→`-` normalization = 283/286; 3 degenerate (`unknown`, `usage_digest` — empty session_id; `q-knot-q-888` — not a prefix) |

**Direct answer to the naming question:** `by-session_<uuid>` being the uuid-SLICE of the
target's session_id is TRUE — but only for the 153 uuid-format pointers (100% of them,
tested as literal prefix against the target file's `session_id` field). The majority
family (v2, 94.4%) keys on sha256(session_id) instead. A retro-knotter must implement all
three derivations (plus the 34 normalized semantic joins) to walk the full index.

## Orphan tail (the 216) — composition and quality

- Families: 104 uuid-slice, 111 semantic, 1 v2.
- Target dates: **all ≤ 2026-08-31** (July: 24, August: 192). Every September target is
  already chained. The orphan window CLOSED at the Aug/Sep boundary.
- Hash integrity: 215/216 = 99.5%. Single failure: `by-session_q-knot-q-888.json` →
  `2026-08-08_1838_holographic-q_q-knot-q_9ca926a3.knot.json` holds stale hash
  `70e7d7cd…` vs the file's actual `9a8a3c15…` (file was re-knotted after the pointer
  was written). Rule for the knotter: **trust the file, not the pointer**, on hash conflict.
- Peak orphan dates: 08-09 (43), 08-17 (20), 08-10 (19), 08-11 (16), 08-12 (13) — the
  mid-August knot-minting burst left the residue.

## Duplicate targets

225 targets carry 2 pointers each (450 pointers); max multiplicity 2, none higher.
224/225 duplicate pairs agree exactly on leaf_hash; the one disagreement is the same
stale q-knot pointer above. Duplicates are a cosmetic redundancy, not a data risk.

## Target date distribution (all 7,786)

2026-07: 24 · 2026-08: 6,530 · 2026-09: 1,232. The index is an August artifact with a
September continuation; nothing predates July.

## VERDICT: **SUPPORTED** (as join table), with two corrections

The index is **trustworthy as the join table for retro-knotting**:

- Resolution 100% (7,786/7,786 targets exist).
- Hash integrity 99.99% (7,785/7,786; the 1 stale pointer is identified by name).
- Pointer-vs-chain agreement 100% where both exist — no silent drift.
- Join keys are deterministic per family and verified at 100% / 100% / 99.0%
  (uuid-slice / v2-sha256 / semantic-normalized).

Two corrections to carry into any knotter build:

1. **It is not an orphan list** — 97.2% of it is already in the chain. The working set
   is the 216-row tail, all dated July–August 2026. Re-derive the orphan set at runtime
   (filename-join against the chain), never from the pointer population.
2. **31/7,377 chained knots (0.42%) have no pointer at all** — the index is incomplete
   in the other direction. If the knotter treats pointer absence as orphanhood, it will
   miss those 31; join on the chain side too.

Tri-state: SUPPORTED with numbers above. The one DISPUTED element is the framing of the
index as 7,786 orphans; the UNPROVEN residue is nil — every pointer in the population was
physically opened and checked.

— zcode seat, fleet research worker, 2026-09-11
