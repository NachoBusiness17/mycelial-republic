# SALON DOSSIER: MAKING THE ARC SEED DEFAULT — recovery without breakage
**Commissioned:** Operator, 09-07 ~00:4xZ — "now how can we make this default without
breaking everything... so we can always have a recovery and feed them through our
existing surfaces... consult all vertexes. fan out."

## THE MECHANISM (already built, dogfooded)
`mag/arc_seed.py` parses a session rollout (model-io-sess_*.jsonl) and emits:
1. **CACHE ANATOMY** — per-call hit curve (this session: cold 9.03% → warm 99.98%;
   88.4% of all input tokens were re-fed cache reads; stable prefix 287,934 tok).
2. **ARC CHAIN** — verkle-style hash chain over per-turn envelopes, arc root committed
   (this session: eacb5b32e9ad5b9a).
3. **ARC SEED** — a single-prompt skeleton in three layers: L0 immutable system
   prefix / L1 the operator's orders verbatim (the branch points) / L2 the
   committed-state delta (files, cards, knots — durable memory outside the context).
Falsifier (untested yet): a fresh session given the seed should state the arc's next
move blind; 2-of-3 match = the seed carries the load-bearing state.
Isomorphism already in production: the boot prompt (AGENTS.md + memory index + CONVO
tail) IS an arc seed for the Sancho seat; SPORE_SANCHO.md is its distilled form.

## THE QUESTION BEFORE THE BENCH
Make arc-seeding DEFAULT for every session — crash recovery always available —
WITHOUT breaking anything. Answer four things, each with a checkable falsifier:
1. **WHERE to hook**: at what moment does a session's arc seed get compiled?
   (candidates: the knot-at-close ritual `mag/knot_at_close.py`; the night-shift
   sweeps 23:00/02:00/05:00 as a batch pass; per-N-turns live; on-demand only).
   The night shift + knot-at-close both EXIST — extending existing organs beats
   birthing new ones (fifth-need-is-a-row law).
2. **WHAT BREAKS**: enumerate the failure modes of defaulting this (rollout files
   rotate/prune — one session's rollout held only 9 calls; secrets in operator
   forks; store growth; chain-write risk if arc roots enter the biography chain;
   cost if the replay falsifier runs per session; duplicate-work if two windows
   seed the same session — the duplicate-order class).
3. **RECOVERY PROTOCOL**: a seat dies mid-lane. Who reads the seed, what proves
   the resume is faithful (the falsifier as gate?), what does the fresh seat read
   FIRST, and how is the recovery itself recorded?
4. **SURFACES**: the seeds must flow through surfaces that already exist. Known
   surfaces: watch/arc_seeds/ (files), CONVO.md rows (mesh wire), room.jsonl
   (live feed), dashboard/static Fleet Console + visual deck (UI), the biography
   verkle chain (tip 7,369+, append-only, sacred). Which carry the seed, which
   carry only the pointer, and which must NOT be touched?

## CONSTRAINTS (law, not preference)
- $0 default path (local parse only; model calls only for the replay falsifier,
  gated, flash).
- Read-only on sources; silent-fail; a missing rollout never blocks a close.
- Secrets never in seeds (operator forks may embed keys — redaction pass required).
- No new scheduled task if an existing organ can carry the pass (fleet services
  law: existing cadences only).
- Versioned schema (arc_seed.v1); old seeds must stay parseable.
- Backup-first only if any existing file is modified (target: modify none — all
  hooks are additive calls inside existing rituals).

## CHAIR OUTPUT FORMAT
Each chair: (a) WHERE hook, (b) top-3 break risks with mitigations, (c) the
recovery protocol in 5 lines, (d) verdict SUPPORTED/DISPUTED/UNPROVEN + one
falsifier. Max 300 words. Disagree with the dossier where the evidence does.
