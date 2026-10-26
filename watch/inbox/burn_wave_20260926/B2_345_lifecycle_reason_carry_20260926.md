# B2-345 Lifecycle reason into the training event and improve candidate, 2026-09-26

## Verdict

LANDED. The lifecycle carry (B2-80's should/should_reason/signals on the gap row) now flows into BOTH downstream sinks inside track_loop_gap: the training event's join gains bounded should / should_reason / signals fields, and the improve candidate's claim string gains a "[should=<verdict> reason=<truncated reason>]" suffix, so the training token and the candidate are attributable whenever the row is, and stay untouched when it is not (no-lifecycle callers keep join={"gap": name} and the bare claim, byte-compatible). Sandbox-proven this lane with both sinks monkeypatched: carry call -> emit join {"gap": "lifecycle_gap:ollama", "should": "True", "should_reason": "janitor tier host", "signals": {"probe": "200"}} and claim containing "[should=True reason=janitor tier host]"; no-carry call -> join keys exactly ["gap"], claim without the should bracket. py_compile clean, added lines em-dash 0. The row remains the full-fidelity source; the sinks now name the verdict instead of only the piece id.

## Evidence file:line quotes

- mag/temperature_stack.py track_loop_gap (post-edit), training block: comment "B2-345 (2026-09-26): carry the lifecycle verdict into the training join so the token is attributable whenever the gap row is (B2-80 made the row carry should/should_reason/signals; the emit and the improve candidate still named only the piece id). Bounded fields, no schema change to the event shape."; code join["should"] = str(lifecycle.get("should") or "")[:8]; join["should_reason"] = ...[:200]; join["signals"] = {str(k)[:40]: str(v)[:80] for ... items()[:8]}.
- Same file, candidate block: comment "B2-345 (2026-09-26): the candidate claim carries the lifecycle verdict too, same attribution law as the training join above."; code claim = "%s [should=%s reason=%s]" % (claim, str(lifecycle.get("should") or "")[:8], str(lifecycle.get("reason") or "")[:160]).
- Pre-edit bytes: emit(..., join={"gap": name[:80]}, ...) and "claim": f"[loop gap] {name}: {detail or where or kind}" — the brief's named defect, verbatim.
- Sandbox probe (this lane, sinks monkeypatched to a tmp dir): "emit {"gap": "lifecycle_gap:ollama", "should": "True", "should_reason": "janitor tier host", "signals": {"probe": "200"}}"; candidate id gap-<key> with claim "[loop gap] lifecycle_gap:ollama: off [writer pid=...] [should=True reason=janitor tier host]"; no-carry run: "no-carry join keys: ['gap']" and "no-carry claim has should bracket: False".
- B2-80 basis (same file, row block): row["should"] = str(lifecycle.get("should") or "")[:8]; row["should_reason"] = ...[:400]; row["signals"] = dict(...) with the B2-80 fix comment citing B2_20_loop_gaps_20260926.md.
- Claim law: CLAIM SW-00 mag/temperature_stack.py filed before the edit (file is working-tree-modified by concurrent lanes); retired at landing; the landed bytes are a rebase on the tree as of claim time (B2-394's writer-identity detail block was already present and is untouched).

## Work done

- Read track_loop_gap whole (row build, B2-80 carry, gaps-log append, emit block, candidate block, pointer block) plus the two callers passing lifecycle= (track_lifecycle_into_improve gaps and waste loops).
- Spec-first in the dated comments inside both sink blocks; implemented the bounded carry into join and claim; no signature or schema changes; callers untouched.
- Proved both directions in a sandbox (production gaps log, training events, and candidates never touched): carry call attributes, no-carry call byte-compatible.
- py_compile clean; em-dash 0 in added lines; ratchet scope check: mag/temperature_stack.py already working-tree-modified by concurrent lanes, this lane's added lines introduce no new debt class (no except-pass added, file length unchanged class).
- Filed this receipt, the LEDGER row, and the QUEUE row pointer.

## Falsifier

- A lifecycle gap row landing with a full should_reason while its training join or candidate claim names only the piece id kills the landing (rerun the sandbox probe shape against current bytes; production occurrence detectable by diffing the next gaps-log row against the next training event row for the same name).
- A signals payload with more than 8 entries or a reason over 200/160 chars is silently truncated in the sinks by design; the row keeps the full fields, so truncation is disclosed by comparing row to sinks, never silent data loss in the row itself.
- If B2-80's row fields are renamed again, the sink mappings here must follow or they empty-string silently; the bounded str() coercions make absence invisible by intent (honest empty, matching the row's variable-field law).
- Any except-branch added around the carry code that swallows a bad lifecycle dict into a plain claim would be fallback-branch creep: the carry is keyed on `if lifecycle:` truthiness exactly as the row block does.

## Bibliography closed

mag/temperature_stack.py (track_loop_gap pre/post-edit; track_lifecycle_into_improve callers; _lifecycle_carry); watch/inbox/burn_wave_20260926/B2_80_reason_carry_20260926.md (referenced via the B2-80 comment block in code); watch/inbox/burn_wave_20260926/B2_20_loop_gaps_20260926.md (census cited in the B2-80 comment); sandbox probe transcripts quoted above. No web sources. Em-dash count 0.
