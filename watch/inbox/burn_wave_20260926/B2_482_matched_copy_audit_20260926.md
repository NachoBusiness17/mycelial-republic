# B2-482 matched-copy identity audit 2026-09-26

## Verdict

Landed. The 32 dual-copy msg_ids audited from bytes: ZERO of the 32 matched copies are byte-identical to their media_full siblings (32/32 differ) while ALL 32 pairs agree in byte length, so the B2-12 builder and the B2-89 fill's "media_matched as canonical copy" treatment is now a MEASURED decision, not just register faith. Winning-copy decision registered: media_matched is canonical for every dual-copy msg_id (its register sha256 rows verify against disk bytes 32/32), the media_full siblings are provenance-only for these ids, and a full-side sha backfill for the 32 is filed as owed to the B2-89 owner (their addendum rows for these msg_ids carry no sha field at all). The dedup decision is registered as an append-only dedup_decision.v1 row at the media_register.jsonl tail; zero existing register rows were edited. The brief's falsifier has no live instance: no dual-copy msg_id has TWO register shas that differ (only the matched side carries a sha), and this receipt now names the winning copy, so the record-keeping gap is closed before it could fire.

## Evidence file:line quotes

- watch/inbox/mrpool_export/media_register.jsonl row 1 shape: {"msg_id": 2002, "file": "media_matched/msg_2002.jpg", "sha256": "6d769f12...", "bytes": 209456, ...} (matched rows carry sha256); B2-89 addendum rows (tail, lane B2-89, computed_at 2026-09-26T17:58:32Z) carry computed_at but the 32 dual-pair full rows carry NO sha256 field.
- Byte measurement (this lane, sha256 over full file bytes): msg 368 matched 45076B sha b084e6c7e2a9f80f... vs full 45076B sha a82e76c715ef331f... (equal bytes FALSE); msg 477 19417B 1c626abe vs f7ee88b0; msg 911 67636B 405425277e343773 vs 34c8e98543ff65a9. Full table: watch/inbox/burn_wave_20260926/B2_482_audit_results.json (32 rows, byte_identical false x32, bytes_equal true x32, matched_register_sha_verified_on_disk true x32).
- Decision row appended (register tail): {"schema":"dedup_decision.v1","ts":"2026-09-26T22:40:00Z","lane":"B2-482","decision":"media_matched is the canonical copy ...","audit_results":"watch/inbox/burn_wave_20260926/B2_482_audit_results.json"}.

## Work done

1. Built the 32-pair crosswalk: main register rows 1..32 region (media_matched) against addendum media_full rows by msg_id; 32/32 msg_ids present on both sides.
2. Hashed all 64 files from disk; compared pair-wise for byte identity (0/32) and byte-length equality (32/32); verified the matched-side register sha against disk (32/32 match, so the matched register rows are byte-true).
3. Checked the full-side sha coverage: none of the 32 addendum rows for these ids carries a sha256 field, so the brief's premise "B2-89 addendum gives every media_full file a sha256" holds for its own range but not for these 32; filed the full-side backfill as owed rather than fabricating a comparison.
4. Registered the dedup decision as an append-only dedup_decision.v1 register row (never editing landed rows, per the register law) and wrote the structured audit results JSON.

## Falsifier

Dies if: (a) any future full-side sha backfill shows a dual pair byte-identical while this receipt says 32/32 differ (rerun the audit JSON regeneration); (b) a consumer keeps treating media_full as canonical for these msg_ids contrary to the registered decision row; (c) the decision row is edited or deleted instead of superseded by a new dated row.

## Bibliography closed

Read whole: watch/inbox/mrpool_export/media_register.jsonl (main rows + addendum tail), watch/inbox/burn_wave_20260926/B2_89_hash_backfill_20260926.md pointer from the brief. Bytes: 64 files hashed live, register rows parsed, decision row appended. Nothing synthesized; the full-side sha gap named as owed, not guessed.
