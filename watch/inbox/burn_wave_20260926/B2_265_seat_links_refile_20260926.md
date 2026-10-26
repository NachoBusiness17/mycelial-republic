# B2-265 Re-file the seat LINKS row through the add gate

## Verdict

LANDED. The hand-appended zcode-seat-20260926 row (watch/inbox/LINKS.jsonl:335, seq 1790430176111) is repaired with the B2-26 field-only backfill pattern: the off-schema "op": "register" field is DROPPED (a link row's schema is seq/ts/canonical/url/canonical_sha256/title/duplicate_of/writer/note) and canonical_sha256 = 910C79621487C8B8... (full 64-hex, mag/link_library.canonical_sha256 of the canonical) is ADDED. Exactly one line's bytes changed; row count stays 345; the falsifier's failure arm does NOT fire: link_library check_url on the url now returns known=true with this row as first_entry (before the fix the row was invisible to the known-canonicals map because it lacked the key). The living prefix was re-sealed per LIVING_HASH_LAW section 5 because bytes changed: this lane appended a --living re-seal (seq 1790455566985931012, sha E1327F9763026F49... over the same 220,613-byte prefix); a concurrent lane's later register superseded it in the fold with a LONGER seal (230,164 bytes, sha 454E4868D4239B8B...) that also covers the repaired row, and the fold verify counts LINKS.jsonl living-ok with no mismatch line: the current seal state is consistent and includes the fix.

## Evidence file:line quotes

- watch/inbox/LINKS.jsonl:335 (pre-fix): `{"seq": 1790430176111, "ts": "2026-09-26T13:42:56.111090+00:00", "op": "register", "canonical": "https://x.com/Dr_Singularity/status/2103595521688449418", "url": "...?s=20", "title": ..., "duplicate_of": "", "writer": "zcode-seat-20260926", "note": ...}` - op present, canonical_sha256 absent, exactly as the brief describes.
- mag/link_library.py:16 (the row schema the brief cites): `{"seq", "ts", "canonical", "url", "canonical_sha256", "title", "duplicate_of", "writer", "note"}`; :129-130 canonical_sha256 = sha256(canonical.encode('utf-8')).hexdigest().upper().
- check_url after the fix: `{"canonical": "https://x.com/Dr_Singularity/status/2103595521688449418", "known": true, "first_entry": {"seq": 1790430176111, ...}}`.
- Byte proof: line-level diff shows exactly 1 of 345 lines changed; file bytes 230,432; prefix-seal sha over the first 220,613 bytes moved 40DEF30EB200 (pre) to E1327F976302 (post), matching the seal the INDEX previously carried (the B2-254 re-pin at sha 40DEF30E over 220,613 bytes).
- Fold state at filing: `add: appended seq 1790455566985931012 for LINKS.jsonl`; current INDEX item `living: True, size: 230164, sha: 454E4868D4239B8B` (concurrent supersession, longer seal, covers the repair); `verify: ... living-ok ...` with NO LINKS.jsonl failure line.

## Work done

1. Located the offending row (line 335, single match in 345) and confirmed all three defects on bytes (hand-append per the brief's steps.jsonl provenance, op field, missing canonical_sha256).
2. Applied the field-only backfill in a single anchored line rewrite: dropped op, added canonical_sha256 via the library's own function, preserved every other field and the schema key order; asserted the row count and the one-line-only diff before writing.
3. Executed the falsifier arm: check_url(url) returns known=true with first_entry = the repaired row (the negative arm "canonical unknown after the fix" does not fire).
4. Re-sealed per LIVING_HASH_LAW section 5: appended a --living register sealing 220,613 bytes over the repaired prefix; recorded the concurrent supersession (longer seal, same file, no failure in fold verify) rather than fighting last-register-wins.
5. Filed this receipt, LEDGER row, QUEUE row.

## Falsifier

Brief's falsifier: "link_library check_url reports the canonical unknown after the fix, or the row count or any other byte moves." Executed inverted: check_url reports the canonical KNOWN (first_entry = the repaired row), row count is unchanged at 345, and the line-level diff is exactly the one repaired line. Reproduction: `python -c "from mag.link_library import check_url; print(check_url('https://x.com/Dr_Singularity/status/2103595521688449418?s=20'))"` must print known=true; `wc -l watch/inbox/LINKS.jsonl` must print 345; a line-count change or any second changed line inverts the receipt (appends by later lanes after this filing are expected and are not this lane's bytes).

## Bibliography closed

- watch/inbox/LINKS.jsonl (the repaired row; 345 lines)
- mag/link_library.py (schema :16, canonical_sha256 :129, check_url :163)
- watch/inbox/burn_wave_20260926/B2_26_links_sha_backfill_20260926.md (the backfill pattern)
- watch/inbox/burn_wave_20260926/B2_221_prefix_editor_20260926.md Evidence last clause (the brief's pointer; the prefix-seal context)
- watch/inbox/LIVING_HASH_LAW_20260926.md section 5 (re-seal rule)
- scripts/index_fold_host.mjs add --living + verify (the re-seal and its verification)
- Nothing owed.
