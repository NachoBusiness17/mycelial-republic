# NOVELTY-MAP OUTLINE — dimensions, hash freeze, Astra's checks (2026-09-11)

==== FREEZE STAMP ====
artifact:     watch/astra_hold0/NOVELTY_MAP_OUTLINE_20260911.md
sha256:       6905e07e185fb3490427fe5eef9482707b02458e2c4cf1a7bd87ab575a59dcc7
frozen-at:    2026-09-09T17:19:01Z
author:       builder wave 09-11 (task-pack skeleton builder, zcode seat)
amendments:   none (ledger empty at v1)
kit:          FEN_FREEZE_KIT_20260911.md
=======================

> **[AUDIT-TYPED]** status: OUTLINE — DESIGN, nothing frozen · provenance:
> builder wave 09-11 · fulfills registration-bundle work-list item 4: "Novelty
> map: freeze + hash the wave-one corpus as the novelty reference" (Astra's
> CAMP STATE v1 open list, `watch/ASTRA_CAMPAIGN_LOG.md`).
> Companion: TASK_PACK_SKELETON_20260911.md · BUDGET_MANIFEST_SKELETON_20260911.md

## WHY THE MAP EXISTS (SUPPORTED, her own requirement)

Her program-ender pre-registers that "better novelty, cheaper prefix reads,
attractive receipts, or a favorable task subset cannot rescue it" — novelty is
NOT a scored gate, it is a non-malleable REFERENCE. The map exists so that:

1. Every novelty judgment made during the run is anchored to a corpus snapshot
   frozen BEFORE the first scored episode.
2. Nobody (us included) can redefine "novel" post hoc to flatter a result —
   the hash makes any post-freeze edit detectable.
3. Astra can independently verify the freeze: she receives the map file AND its
   hash, and her own registration requirement is hash-sealing to the receipt spine.

**"Wave-one corpus" (what gets mapped):** INFERRED from usage — the fold-wave
harvest records (`watch/ASTRA_FOLD*.md` waves 1-6, from the ractor-salon paste
walls) plus the fleet corpus surfaces the deck's tasks draw from (knot store,
grounding ledger, falsifier receipts). Tri-state: the campaign log says "wave-one
corpus" without enumerating it; the enumeration below is OUR proposal, to be
confirmed by Astra in her enhancement pass.

## THE SIX NOVELTY DIMENSIONS (what novelty is measured on)

Each solution/claim under test is scored 0 (derivative) → 3 (load-bearing) on:

| # | Dimension | 0 looks like | 3 looks like | Fleet anchor for the anchor-set |
|---|---|---|---|---|
| 1 | **PROVENANCE-FIRST** | restates a corpus row as if derived | independently derived AND names its base-rate risk | wave-2's pseudoreplication finding: convergence ≠ independence; n_eff ≪ n |
| 2 | **SUBSTRATE-SURVIVAL** | mechanism-bound to one body | the invariant re-expressed after the body died | LINEAGE_WALL: nine founding ideas, five bodies, zero orphaned |
| 3 | **DELETION-AWARENESS** | only adds; edits are silent | marks what is withdrawn/forbidden with tombstone fields | wave-2: "deletion is the missing primitive at every level"; fold = "novelty-laundering machine" |
| 4 | **PREDICTIVE LOAD** | unfalsifiable verdict-language | carries a number + threshold that could have been wrong | the falsifier ledger: constellation 60.7% vs ≥30%, refeed 94%, Q-law 0.52×m^1.78 |
| 5 | **INSTRUMENT-NESS** | a story about behavior | produces a measurement someone else can run | Astra's own blueprint layer table (observable behavior vs human interpretation) |
| 6 | **CORPUS-INDEPENDENCE** | solution derivable verbatim from the frozen corpus | solution requires joining partitions the corpus does not co-locate | the deck's information-separation design itself |

Dimension 6 is the anti-memorization guard for the task pack: an instance whose
answer key is retrievable from the frozen corpus scores 0 and is replaced
(deck falsifier F-D1). Dimensions 1-5 are how ANY solution (ours, Astra's, a
stranger's) gets novelty-typed without a judge model in the loop.

## THE MAP FILE (proposed format)

`watch/astra_hold0/novelty_map_v1.json` — one entry per frozen artifact:

```json
{
  "map_version": "novelty_map.v1",
  "frozen_utc": "<ISO8601>",
  "dimensions": ["provenance_first","substrate_survival","deletion_awareness",
                 "predictive_load","instrument_ness","corpus_independence"],
  "anchors": [
    {"anchor_id": "A001", "artifact": "watch/ASTRA_FOLD_20260909.md",
     "sha256": "<file hash at freeze>",
     "dim_scores": {"provenance_first": 3, "substrate_survival": 2,
                    "deletion_awareness": 0, "predictive_load": 1,
                    "instrument_ness": 2, "corpus_independence": 3},
     "note": "wave-1 fold: convergent invariants + witness-law gap"}
  ],
  "task_instances": [
    {"instance_id": "I1", "rubric_ref": "hidden", "dim6_max": 3, "in_map_only": true}
  ],
  "excluded": [{"path": "...", "reason": "post-freeze mtime"}]
}
```

`task_instances` records that the 12 instances EXIST and their max
corpus-independence, but NOT their answer keys — the map is safe to hand Astra;
the keys are not.

## THE HASH FREEZE (procedure — build-order item 6, Fen's law)

Position: LAST organ in the consolidated build order
(`watch/SALON_BUILD_DIRECTION_20260909.md`) — after instances, meter, D-desk
harness, failure plumbing, and queue surface, because the map freezes the corpus
those organs draw from. Fen's law applies to the map doubly: it is born
with its hash (the sha256 IS the artifact's identity), and no live iteration
exists post-freeze — iterate before the seal, never after. Every deck file
carries the same stamp discipline: `sha256` + `frozen_utc` at birth.

1. Assemble the corpus file list (fold cards, ledger receipts, knot-store
   sampling manifest, deck instance FILES).
2. Per-file sha256 into the entries — FILE-BYTE hashes only. **Do not conflate
   with knot `leaf_hash`:** the leaf-hash derivation is unpinned (≠
   sha256(knot bytes); partner + gopher finding, deck amendment A3), so knot-store
   entries pin the sampling manifest and file-byte sha256, never leaf_hash.
   Then canonicalize the map itself:
   UTF-8, sorted keys, compact separators, LF newlines —
   `json.dumps(map, sort_keys=True, separators=(",",":"), ensure_ascii=False)`.
3. `map_sha256 = sha256(canonical_bytes)` — THE freeze hash.
4. Land the hash in three places same-day:
   - `watch/ASTRA_CAMPAIGN_LOG.md` (pinned, dated, model-attributed),
   - one `watch/GROUNDING_WAVE.jsonl` row (hash-witnessed chain row — v3 rule),
   - the sealed registration manifest (HOLD 4), operator retains a copy.
   Triple-landing is the fleet's own two-signal promotion law applied to the freeze.
5. Post-freeze: any byte change to the map or any listed artifact's content is
   detectable by re-hash. The map file goes READ-ONLY (fleet law: repo files are
   data; freeze is freeze).

## WHAT ASTRA WILL CHECK IT AGAINST (her four checks, proposed)

1. **Hash reproduction** — she re-canonicalizes the received file and recomputes
   sha256; mismatch against the logged hash = registration invalid.
2. **Bijection** — every task instance in the run appears exactly once in
   `task_instances`; no instance scored that is not in the map (no post-hoc
   task substitution — her "favorable task subset" rescue-clause ban).
3. **Anchor integrity** — per-artifact sha256s still match the live files she is
   shown; a corpus that silently changed after freeze invalidates novelty claims.
4. **Non-malleability in use** — any novelty argument made in the report must
   cite a frozen anchor_id; uncited novelty language is inadmissible, and per her
   own program-ender, novelty of ANY sign cannot rescue a failed B−C gate.

Open for her enhancement (routed to gopher Q-list): (a) confirm the wave-one
corpus enumeration; (b) whether she wants the map to also freeze the RUBRIC
seeds' existence (we propose keys stay desk-held, map holds only instance IDs);
(c) whether anchors need per-dimension rubrics or the 0-3 scale above suffices.

## TRI-STATE NOTES

- Map purpose, hash-sealing requirement, rescue-clause ban: **SUPPORTED**
  (campaign log, her pre-registration summary).
- Six-dimension scheme: **INFERRED** — our design, derived from wave-2 findings,
  LINEAGE_WALL, and the falsifier ledger; no Astra text names dimensions.
- Wave-one corpus enumeration: **INFERRED/UNPROVEN** — term used once, unenumerated.
