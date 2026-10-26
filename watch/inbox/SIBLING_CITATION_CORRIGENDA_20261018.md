# SIBLING CITATION CORRIGENDA - 8 CITATION DEFECTS IN THE FOUR SIBLING 10-18 DOCS (2026-10-18)

class: RECEIPT
writer: genetic burn G1b lane i13 (i13-sibling-corrigenda <- g23, per G0/GENOME.md assignment)
moment: 2026-10-18T12:58:19Z (all byte checks and this write in the same window)
gene: `memory/runs/genetic_burn/20261018/G0/lanes/g23-sibling-synthesis.md` (section 6 defects, section 5 conflicts) + `memory/runs/genetic_burn/20261018/G0/GENOME.md` (i13 assignment)
lane record: `memory/runs/genetic_burn/20261018/G1/lanes/i13-sibling-corrigenda.md`
scope: RECORD ONLY. The four sibling docs are untouched - their lanes own them.

## 0. Method and verification weight

Docs covered (read fully this window): `watch/inbox/THE_BACKUP_BRAIN_MANIFESTO_20261018.md` (101 lines), `watch/inbox/CONTINUITY_ENGINE_SYNTHESIS_20261018.md` (75), `watch/inbox/EULER_PHASOR_STANDING_WAVE_20261018.md` (134), `watch/inbox/TWEET_RELIC_ONTOLOGY_20261018.md` (106).

- i13 re-verified ALL EIGHT defects against the named files this window (instruments: ls, git ls-files, grep, plus direct reads of `memory/biography_v2/checkpoints_v2.jsonl` and `mag/knot_at_close.py`), exceeding the 3-defect spot-check minimum. Confirmed on bob: 8 of 8, with one refinement vs g23 recorded at defect 1.
- Caveat kept from g23, unchanged: absence on bob is proof of an unverifiable carrier, not proof of absence from the mesh (t90 and desktop are not readable from this seat). Every suggested fix is therefore a CLAIM ROW with a named verifier, never a silent edit of the sibling docs.

## 1. The 8 defects

### Defect 1 - phantom primary-law file (Euler doc)

- doc: `watch/inbox/EULER_PHASOR_STANDING_WAVE_20261018.md:76-77`
- claimed: "In `STANDING_WAVE_README.md`, the estate's primary law states: 'The estate is not a process that must stay awake. It is a standing wave: a pattern that persists because every part of it is re-minted from stored bytes.'"
- byte-truth: no `STANDING_WAVE_README.md` on bob - zero hits in `git ls-files`, absent at repo root. The tracked `mag/standing_wave.py` is a DIFFERENT standing wave: its docstring says SEED / PROPAGATE / ECHO (idea propagation), not the persistence ontology. i13 REFINEMENT vs g23: the quoted sentence's distinctive substring "pattern that persists" has NO carrier anywhere under `memory/runs/lineage_audit/` (grep returned zero hits); g23's named carriers carry standing-wave doctrine language (`memory/runs/lineage_audit/grok_era_mining.md` holds "boot = standing wave; how-to-run-again" and "cold boot from standing wave" rows) but not this sentence. The quote's true carrier is UNLOCATED on this seat.
- suggested fix: register a claim row (owner g01) whose claim_regex anchors the quoted sentence, with a named verifier running a mesh-node carrier search (t90/desktop attestation); until a carrier is located, no lane treats the sentence as law text - cite it as doctrine paraphrase with no file attribution, or correct to the located carrier.

### Defect 2 - cold-boot smoke path missing (manifesto)

- doc: `watch/inbox/THE_BACKUP_BRAIN_MANIFESTO_20261018.md:89`
- claimed: cold-boot row cites `public_seed/mag/smoke.py` with "22/22 Supported organs (`COLD BOOT: Supported`) passing from zero memory".
- byte-truth: `public_seed/` on bob contains only `evidence/` - no `mag/` subtree, no smoke script under it; `git ls-files` surfaces no smoke path under `public_seed/` (tracked smoke hits are unrelated: `configs/selftest/multi_smoke_fixture.txt` and dist_audit copies).
- suggested fix: locate the real cold-boot smoke carrier (operator or t90/desktop attestation) and register the corrected path as the claim; if no carrier exists, the 22/22 claim dies as phantom and the row is struck or re-scoped to an existing smoke instrument.

### Defect 3 - Tesuji ledger path and staleness (manifesto)

- doc: `watch/inbox/THE_BACKUP_BRAIN_MANIFESTO_20261018.md:56`
- claimed: "persistent corpus (`TESUJI_MAP.jsonl`, `watch/inbox/TESUJI_*`)" - the bare name reads as a repo-root file.
- byte-truth: no `TESUJI_MAP.jsonl` at repo root; the ledger is `watch/TESUJI_MAP.jsonl` (210,571 B on disk, mtime 2026-09-13, untracked in git; tracked siblings are `watch/TESUJI_MAP.md` and `watch/TESUJI_MAP_5_3FLASH_20260906.md`, rendered by `mag/tesuji_map.py`). The ledger is 5 weeks cold as of 2026-10-18.
- suggested fix: cite `watch/TESUJI_MAP.jsonl` by full path; add the corpus-freshness claim row (g23 B4) so staleness becomes a patrol finding instead of silent carrier rot.

### Defect 4 - offline_queue.py misattributed to mag/ (manifesto)

- doc: `watch/inbox/THE_BACKUP_BRAIN_MANIFESTO_20261018.md:27` (diagram node: offline task queue) and `:84` (estate table row)
- claimed: "Offline Task Queue (mag/wal_queue.py / offline_queue.py)" and the row "`mag/wal_queue.py` & `offline_queue.py`" - both read as `offline_queue.py` living beside `mag/wal_queue.py`.
- byte-truth: no `mag/offline_queue.py`; the real carriers are `reference/gstdcoin/A2A/src/gstd_a2a/offline_queue.py` and `state/gstd_full/A2A/src/gstd_a2a/offline_queue.py` (both on disk, both untracked). `mag/wal_queue.py` itself is real (i13 ls hit this window).
- suggested fix: cite the two gstd_a2a paths, or attribute the queue concept to `mag/wal_queue.py` alone; g04 owns the adoption call (g23 B2, Organ 4).

### Defect 5 - law-file carriers wrong (continuity doc)

- doc: `watch/inbox/CONTINUITY_ENGINE_SYNTHESIS_20261018.md:62`
- claimed: crosswalk row cites "`LAWS.md`, `BEHAVIOR_POLICY.md` (R1-R6 harms refused)".
- byte-truth: no `LAWS.md` at repo root - the on-disk carrier is `kit/LAWS.md`; `BEHAVIOR_POLICY.md` is untracked anywhere (zero `git ls-files` hits) and absent at root.
- suggested fix: cite `kit/LAWS.md`; register `BEHAVIOR_POLICY.md` as an unverifiable-carrier claim row (may live on another node) or strike the name from the row.

### Defect 6 - .gstdmesh/ribs/ does not exist on this seat (continuity doc)

- doc: `watch/inbox/CONTINUITY_ENGINE_SYNTHESIS_20261018.md:48`
- claimed: "immutable ribs in `.gstdmesh/ribs/`".
- byte-truth: no `.gstdmesh` directory on bob; ribs live in `memory/rib/` (populated - e.g. `memory/rib/DOCTRINE_MEMWEAVE_20260810.md`).
- suggested fix: correct the doc line to `memory/rib/`; if `.gstdmesh/ribs/` is a t90-side convention, the claim row needs a t90-side verifier, not a bob edit.

### Defect 7 - relic 7-tools table dead citations (relic doc)

- doc: `watch/inbox/TWEET_RELIC_ONTOLOGY_20261018.md:71-77`
- claimed: the estate-implementation column maps `wave_flywheel.py` (row 1), `mag/observer_lens.py` + `pocket_mcp.js` (row 3), `stagger_probe.py` (row 4), bare `verify_tails.py` (row 6), and `tails.jsonl` (row 7).
- byte-truth: all five names are dead on bob - zero `git ls-files` hits, absent at repo root and at their implied subpaths (`tools/verify_tails.py` and `mag/observer_lens.py` both missing); no `tails.jsonl` ledger on disk (nearest name `watch/steer_field/TAILS.md` is a different object). Same-table verified-true rows sampled by i13 this window: `mag/lane_runner.py`, `mag/inference_budget.py`, `memory/biography_v2/` all exist - the table mixes live organs with dead names.
- suggested fix: per g23 R1 the substance dedups into existing organs under other names; register per-tool corrected carriers as claim rows (owner g01) and mark the table NOT consumable as a build map until every row carries a live path.

### Defect 8 - checkpoint claim same-day rot (continuity doc)

- doc: `watch/inbox/CONTINUITY_ENGINE_SYNTHESIS_20261018.md:47`
- claimed: "Hourly consistency proofs (... Checkpoint #5, `n=12,215`, `root=0bd488ab2e2d9ebf..`)".
- byte-truth: the last row of `memory/biography_v2/checkpoints_v2.jsonl` at i13's read is n=12,621, prev_checkpoint_n=12,556, root=44e2666d573d33a183258c516c966094adcc6ea31817c10e2216899009f9d56f, ts 2026-10-18T12:04:07.223670Z, status unsigned-pending-operator. The doc's `0bd488ab` prefix survives in historical rows per g23's checkpoint-tip read, so the claim was true at mint and went stale within hours - the founding receipt that the sibling docs need Organ 1 on themselves.
- suggested fix: sibling docs must stop freezing mint-instant checkpoint numbers in prose; cite the ledger plus a newest-row-at-read-time rule instead. g06's patrol takes this as its founding recurrence test (g23's falsifier): catch a same-day-stale checkpoint claim in a fresh .md within one patrol cadence.

## 2. The 3 named conflicts - VERBATIM from g23 section 5

Source copied byte-for-byte: `memory/runs/genetic_burn/20261018/G0/lanes/g23-sibling-synthesis.md` section 5. i13 edits: ONE bracketed source insertion inside CONFLICT-2 (citation-lint number pairing); every other byte verbatim. i13 resolves nothing.

- CONFLICT-1 - CANON ARITY (DOC 1 vs DOC 2): `CONTINUITY_ENGINE_SYNTHESIS_20261018.md:25-52` codifies a TRIPARTITE canon (three movements, third = the Oct 2026 live estate). `THE_BACKUP_BRAIN_MANIFESTO_20261018.md:97-100` declares itself "the ultimate answer to The Continuity Engine ... and The Sovereign Mirror Relic" - i.e. a FOURTH movement (pocket sovereignty / blackout doctrine). Disagreement: is the canon 3 documents or 4? Lane g02 must elect the count explicitly in canon_beacon.json rows; this map does not resolve it.
- CONFLICT-2 - ROOT SEMANTICS (DOC 4 vs DOC 2/3): `TWEET_RELIC_ONTOLOGY_20261018.md:88` claims "the identical root hash (e11937d6...) persists with zero loss" and :13 calls it "the permanent lattice commitment across all generations", while DOC 2 (:47) and DOC 3 (:123) anchor the same architecture on a ROTATING hourly checkpoint root (doc cites Checkpoint #5 root=0bd488ab...; live tip is now 44e2666d..., n=12,621 [live-tip carrier: `memory/biography_v2/checkpoints_v2.jsonl`]). Face value: the root cannot be both immutable-forever and rotating. Prior estate art already splits the object (`docs/ref/strike_origin.md`: story fidelity key vs disk hash chain; `mag/knot_at_close.py:189`: framework_root) - cited here as prior art, still not a silent resolution: the sibling docs themselves never make the split, and g01's claim rows must.
- CONFLICT-3 - DIVERGENCE POLARITY (DOC 3 vs DOC 4): the Euler doc's diagram (:52-73) labels asynchronous node divergence the time-domain DISEASE ("Coupled Differential Thrashing (State drift, hallucination loops)") to be projected away into invariants. The relic doc's Phase 3 (:23, :60) says the same phenomenon - phase gradients across nodes - "induce torsion that directly feeds back into systemic coherence" and high-tension cycles are productive ("immediate local stress relief while storing torsion... The lattice strengthens and lightens with every single use"). Same physics, opposite sign: is offline divergence pathology to be collapsed (DOC 3) or the coherence-feeding dynamics itself (DOC 4)? Doctrine-only; flag to g02 canon rows; no build item follows from either reading.

OPERATOR-GATED NOTE (one line): none of the three conflicts is resolved by this receipt - electing canon arity, root semantics, or divergence polarity is an operator call, and every lane must carry both sides open until the operator rules.

## 3. Consumers and handoff

- g01: fold these 8 rows into the claim-row seed set (g23 section 7 already routed 7 seeds; defect 1's carrier search and defect 2's smoke-carrier search are the two new verifier tasks).
- g06 / i02-i03 (patrol build + tests): defect 8 is the founding recurrence test.
- i01 (ledger build): the claims.jsonl schema must carry {doc, claimed, byte-truth, verifier} per row exactly as recorded here.
- g02 / i04 (canon build): the 3 conflicts above are open doctrine rows, never silently inherited.

## Falsifier (inherited unchanged from g23)

If the g06 patrol cannot catch a recurrence of defect 8 (a same-day-stale checkpoint claim in a fresh .md) within one patrol cadence, the CLAIM-ROW-over-rewrite verdict is wrong and the sibling docs should instead be edited in place on every mint.

## NEXT TASK (self-designed)

Pair the 8 corrigenda defects into paste-ready `watch/claims.jsonl` seed rows (claim_regex + carrier_path + owner + verifier each, g01 house style) so i01's ledger and g06's patrol can enforce them on landing.
