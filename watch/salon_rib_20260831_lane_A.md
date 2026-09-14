# SALON LANE A — RIB inventory + RenderMan map (Mag). 2026-08-31.

> **[AUDIT-TYPED 2026-09-08]** status: PROSE · claims: the fleet already implements deterministic hash-chained record patterns (party_subchain, verkle chain, riddler archives) while openclaw_traj has no deref pointers — SUPPORTED (file paths + line/byte counts + key schemas cited at audit time) · falsifier: cited files missing or their schemas diverge from the described keys

## Q1 — Patterns ALREADY implemented (file → pattern → evidence)
1. **party_subchain** = ObjectInstance spine. `/mag/memory/runs/party_subchain/chain.jsonl`
   (167 L, 134509b)+head.json. Per line: kind, seat, ok, move(prose), prev_hash, parent_leaf_hash,
   parent_root, n, hash. Define-once-cite-many, hash-chained to verkle leaf. Invariant:
   `/mag/memory/rib_bus/party_subchain.json`.
2. **verkle chain** = hash-bound spine (read_archive(span) pointers).
   `/mag/memory/biography/verkle_chain.jsonl` (4914 L, 3410857b)+`verkle_tip.json`+18080 knots.
   Per line: leaf_hash, session_id, parent_verkle_root→verkle_root, n_leaves. Knots provide
   tension_index, dossier_commit, theme_vector → deterministic per-session bounds.
3. **riddler private/public** = DelayedReadArchive exact (private=archive, public=baked bound).
   `.../riddler/riddler-2026-08-30T161205-6740f34e4c6b339a.private.json` (keys: scratch_id, role_map,
   constraint_map, private_map_ref, fingerprint_seed, domain) + `.public.json` (keys: schema, scratch_id,
   public_story, public_question, allowed_story_actions, shape_hash, loss_report, tier, expires_at).
   .public={shape_hash,loss_report,tier}=deterministic metadata. Pvt=archive; `.decoded.json`=deref.
4. **OpenClaw compaction ledger** = token-bound only, NO pointer. `/board/openclaw_traj.jsonl`
   (13 L, 2139b): ts, session, tokensBefore, tokensAfter, compactedCount. No spans→no deref.

## Q2 — deterministic vs prose-only
- Deterministic: verkle_chain, party_subchain, riddler public(shape_hash, loss_report) + private
  (fingerprint_seed, private_map_ref), knot leaf.
- Prose-only: party `move`, riddler `public_story`, openclaw_traj counts (no span/hash).

## Q3 — atomic pairs / scope stack?
- Atomic unit = one hash-chained line (kind+ok). No tool-call/tool-result pair structure or grammar-rule
  scope stack found. OpenClaw keeps full `.trajectory.jsonl` + compacted `.jsonl` in
  `/root/.openclaw/agents/main/sessions/`. `.decoded.json` = deref artifact.

## Q4 — compacts vs grows forever
- Compacts: openclaw_traj (13 events, e.g. 107202→24561); surface shrinks, trace kept.
- Grows forever (append-only): verkle_chain, 18080 knots, party_subchain, grok_feed,
  session_digest, room, summarized_sessions.json, biography_backup_* (full retessellate).

## Dig notes
- No python3 host; used node. NO read_archive harness — pattern present, no deref.
