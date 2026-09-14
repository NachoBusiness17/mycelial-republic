# PACK_RIB_COMPACTION_20260831

> **[AUDIT-TYPED 2026-09-08]** status: STAGED · claims: applying the RenderMan compaction lens to Mag's own RIB/trajectory surfaces yields named $0 buildable next actions — UNPROVEN (this is the task pack; no dig results or next actions recorded in-card) · falsifier: the dig completing with no existing RenderMan-pattern artifact and no cheap /patches surface found

## Goal
Apply the RenderMan→LLM compaction lens to Mag's OWN RIB/trajectory data. Produce named, buildable next actions that are cheap ($0/free lanes; DeepSeek cheap fallback; edits via /patches JSON only). No new cages, no new supervisors, no host lab.

## Law
- Pack+goal only. Thinking off. Receipts over vibes: every claim cites an actual path you read.
- Red lines: no second gateway, no new jobs/ dirs, no renaming, no Heart-diary mining. Privacy is mutual.
- Deliverable style: one named next action per claim, each with the file it touches and the $0 path to build it.

## Full source doc (read it)
/board/RIB_COMPACTION_DOC_20260831.md — external research doc supplied by operator: RenderMan RIB (DelayedReadArchive, ObjectInstance instancing, scope stack, LOD/shading-rate, conservative bounds) vs LLM compaction (summaries, lossy baking, unknown future queries). Key divergences: (1) query-unawareness — agent culls against an unknown frustum; (2) lossiness — summaries have no guaranteed ReadArchive back; (3) silent omission — bad bounds fail with holes, no error; (4) prose claims vs verifiable metadata; (5) re-expansion re-consumes budget → oscillation risk. Design consequences: deterministic metadata (span IDs, paths, entities, hashes, token counts), dereference tool read_archive(span) + auto-surface when mentions intersect bounds, grammar-rule scope stack (compaction illegal inside open scopes), append-only summary spine to preserve prefix cache, adversarial validation as test-render (Slipstream: +8.8pp accuracy, −39.7% latency).

## Our RIB/trajectory surfaces to dig (all readable, /mag is read-only)
- /board/openclaw_traj.jsonl — compact-after tape for this cage. Check: schema, size, whether compaction entries carry metadata or prose only, split-point safety (are tool-call/tool-result pairs kept together?), append-only or rewritten?
- Mag party_subchain: seat-to-seat jsonl, hash-chained, parent = verkle tip. Host CLI `python -m mag.party_subchain status`. Find its data files under /mag (memory/runs/, watch/). Check: is it already an ObjectInstance pattern (define once, cite many)?
- Verkle lance: knot timeline, tie events to tip. Host CLI `python -m mag.verkle_lance self_check`. Data under /mag/memory/. Check: are verkle ties already deterministic "bounds" (hashes) that could serve read_archive(span)?
- /mag/memory/runs/seat_corpus/latest.json — lane cost corpus. Check: is lane selection already frustum-aware (query-aware culling of what to send)?
- /mag/memory/runs/riddler/ — private/public/decoded jsonl pairs + primer_booth_public.json + PACK_PHYSICS.md. Check: is the private/public split already a lossless-pointer pattern (private = archive, public = baked summary)?
- /mag/docs/ref/SURFACES.md, /mag/docs/ref/OPERATOR_CARD.md — existing surfaces; do not invent new ones.
- OpenClaw cage side: compaction is built-in (auto at context limit, /compact manual, full transcript stays on disk). Session transcripts at /root/.openclaw/agents/main/sessions/*.jsonl.

## Standing doctrine to respect (already decided)
- Switchboard boundary: POSTED→CLASSIFIED→PROPOSED→AUTHORIZED/DENIED/DEFERRED→EXECUTING→RECEIPT_COMMITTED; authority labels on every board item; "a roast can become a proposal, it cannot become a permission."
- session_bridge + riddler_sanitize = cross-session filesystem bus (strip geography, keep physics).
- ask_router: outcome-memory-driven routing, $0 control plane, ledger.jsonl + verkle ties.

## Questions
1. Which of our artifacts ALREADY implement a RenderMan pattern (name file + pattern + evidence)?
2. Where do we pay re-tessellation (regenerate what should be instanced) or cull blind (compact without bounds)?
3. What is the smallest /patches JSON that adds deterministic bounds or a dereference path to an existing surface?
4. What should compaction NEVER be allowed to drop (safety/constraint items) and where is that list today?
