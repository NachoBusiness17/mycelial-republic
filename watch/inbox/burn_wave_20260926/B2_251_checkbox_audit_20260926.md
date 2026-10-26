# B2-251 Open checkbox truth audit (2026-09-26)

## Verdict

LANDED. Every checked Open row in watch/inbox/burn_wave_20260926/QUEUE.md was
swept for a resolvable landing receipt across two passes against live bytes:
16 unearned rows were flipped back to [ ] with dated no-erase annotations, 71
landed rows that had never named their own landing receipt got the receipt
path attached in-row, and the dispatcher outstanding count (unchecked Open
rows) reads truth again: 97 checked / 186 unchecked of 283 rows at audit
start, 90 checked / 204 unchecked of 294 rows at freeze (2026-09-26T16:02Z).
The falsifier does not survive: at the freeze-time gate, zero checked rows
lack a resolving receipt path. Concurrent lanes landed receipts, renumbered
ids, re-checked one flipped row, and erased this lane's own landing pointer
mid-audit; every such collision is disclosed below with the bytes it was
verified on.

## Evidence with byte quotes

- Disease chain confirmed from the owning receipts: the B2-238 receipt
  (watch/inbox/burn_wave_20260926/B2_238_checkbox_law_20260926.md) names the
  pre-checked self-feed disease and the law; the QUEUE.md header carries
  "outstanding means unchecked Open rows, so a pre-checked row whose work has
  not landed mutes the refill count". The checked B2-237 attribution row
  named by this brief has a receipt NOW (B2_237_touch_law_20260926.md,
  "B2-237 touch law: the 13:53:18Z no-row touch, attributed to mechanism")
  that landed after the brief was written; the row was earned and got its
  pointer attached, not flipped. The brief's census-time absence claim was
  true when written and stale at audit time; recorded, not silently ignored.
- Adjudication rule: a checked row is EARNED only if its own-lane landing
  receipt exists on disk under watch/inbox/burn_wave_20260926/ with a
  Verdict section whose title matches the row's brief subject (for rows
  renumbered by the B2-255 sweep, the receipt keeps the pre-renumber lane
  id, e.g. row B2-285 names B2_244_guard_pin_20260926.md). A pointer to
  ANOTHER lane's receipt is context, not a landing receipt. The probe is
  filed as watch/inbox/burn_wave_20260926/B2_251_audit_probe.py.
- Pass 1 (97 checked rows at edit time): 7 unearned rows flipped
  (B2-247, and B2-286/287/288/297/298/299, the B2-255-renumbered second
  claims of B2-214/215/216/221/222/223, each subject-verified against its
  pre-sweep text), 71 receipt pointers attached in the shape " (receipt
  attachment 2026-09-26, B2-251 audit: watch/inbox/burn_wave_20260926/
  <file>)", 14 rows skipped as already self-named. The edit script
  (B2_251_queue_edit.py) aborted cleanly once when the concurrent B2-255
  renumber staled six keys, and was re-keyed on the new ids.
- Pass 2 (live bytes re-probed): 9 more unearned rows flipped: B2-247 again
  (a concurrent writer re-checked it [x] OVER this audit's pass-1 flip
  annotation without filing any receipt; re-flipped with the race named on
  the row), B2-214 dungeon-lore fossil (the fossil is still on disk at
  memory/game_modules/audit_dungeon.v1.json:147, still reciting 1,341 tests
  / 34 shelves fail), B2-73 through B2-77 (the UF-sweep and XIDIG rows,
  checked with no receipts on disk, pointers only), and B2-279/B2-280
  (fold-sort and seq-band rows self-fed by B2-254, checked with no own
  receipts; comparator code sits at scripts/index_fold_host.mjs
  compareBySeqTs and :172-204 MAX_SAFE_SEQ but no landing receipt names it).
  Pass 2 also attached this lane's own landing pointer to the B2-251 row and
  self-fed B2-316 (checkbox-receipt gate) and B2-317 (attachment
  verification pass), both UNCHECKED per the law.
- Honesty clauses on the flipped rows (append-only, no bytes erased): each
  carries " (2026-09-26 B2-251 checkbox audit: [x] flipped to [ ], no
  resolvable landing receipt on disk at audit time; no bytes erased, prior
  checked state recorded in watch/inbox/burn_wave_20260926/
  B2_251_checkbox_audit_20260926.md)" plus the per-row state note.
- Mid-audit concurrency, fully disclosed: the B2-255 sweep lane landed
  (B2_255_double_spend_20260926.md, LEDGER ts 2026-09-26T15:44:15Z) and
  renumbered 24 later claimants to B2-285..B2-308; receipts for B2-246,
  B2-250, B2-254 and B2-257 (B2_246_collect_schedule, B2_250_file_claims,
  B2_254_living_regression, B2_257_year_ladder) landed mid-audit and earned
  four rows this lane would otherwise have flipped; the B2-247 row was
  re-checked over its flip by a stale-base writer and re-flipped; the
  B2-251 landing pointer was erased once by a stale-base whole-file writer
  and re-attached (readback-verified present after re-attachment; if a later
  clobber erases it again, the landing record lives in this receipt and in
  the LEDGER row). Self-feed traffic grew the Open section continuously
  (283 to 294 rows over the lane window).
- Unearned roster (16 rows, all flipped): B2-247 collected-vs-disk gap;
  B2-286 model-null hole (providers.yaml z_ai2/z_ai3 still carry no
  default_model, models/providers.py:164 unchanged); B2-287 z_ai3 live
  re-verify (no own receipt); B2-288 test-debt stash (drift_dashboard half
  provable only as the tools/drift_dashboard.py receipt comment);
  B2-297 living-downgrade detector (no detector code in
  mag/shared_surface.py); B2-298 patrol-prompt persistence (no repo-side
  prompt copy); B2-299 fold cwd trap (verify still resolves items against
  process cwd); B2-214 dungeon fossil; B2-73/74/75/76/77; B2-279/280.

## Work done

1. Parsed QUEUE.md with .venv/Scripts/python.exe (never bare python):
   per-row Open-section census with ids and line numbers, repeated at every
   stage because concurrent lanes were appending, flipping and renumbering
   throughout.
2. Filed the resolution probe B2_251_audit_probe.py: per checked row it
   extracts path tokens, tests existence on disk, and lists own-lane receipt
   files with a Verdict-heading byte check.
3. Verified subject match by reading receipt titles for every earned row
   whose text did not name its own receipt, including the six renumbered
   rows and every double-id pair (B2-244 collect vs guard pin, B2-215 census
   tripwire vs z_ai re-verify, B2-216 collect delta vs test debt, B2-221
   prefix editor vs detector, B2-222 hot living vs patrol persistence,
   B2-223 mimo living vs cwd trap).
4. Checked estate bytes for each receipt-less row before ruling it unearned
   (configs/providers.yaml, models/providers.py, mag/shared_surface.py,
   tools/ and scripts/ prompt greps, scripts/index_fold_host.mjs verify loop
   and comparator, tools/drift_dashboard.py,
   memory/game_modules/audit_dungeon.v1.json) so the flipped rows state what
   is and is not provable.
5. Applied pass 1 via B2_251_queue_edit.py (unique-prefix keyed, aborts on
   any key anomaly; it aborted cleanly once on the mid-audit renumber) and
   pass 2 via B2_251_queue_edit2.py: totals 16 flips, 71 attachments, 14
   self-named skips, 1 self-row pointer, 2 self-fed briefs.
6. Re-verified the falsifier on fresh bytes until stable: final gate found
   zero checked rows without a resolving receipt path, with the B2-251
   pointer present; froze the census at 294 rows / 90 checked / 204
   unchecked and filed LEDGER row B2-251-open-checkbox-truth-audit at
   2026-09-26T16:02:24Z via json.dumps.

## Falsifier

The brief's falsifier: "a checked row whose receipt path does not resolve
survives the sweep". It does not survive: at the freeze-time gate every
checked Open row names (in-row, originally, by its landing lane, or as
attached by this audit) at least one receipt path under
watch/inbox/burn_wave_20260926/ that resolves on disk, and the 16 rows whose
landing receipts did not or do not resolve are unchecked. This receipt dies
if: any checked Open row's receipt path stops resolving while it stays
checked; any of the 16 flipped rows is re-checked without a landing receipt
pointer; any pre-audit row text was erased rather than annotated (all edits
are appends plus the [x]-to-[ ] flag flip, and the prior checked state of
every flipped row is recorded in this file's unearned roster); the LEDGER
row B2-251-open-checkbox-truth-audit disappears from memory/burns/
LEDGER.jsonl; or the self-fed B2-316/B2-317 rows read checked while
receipt-less.

## Bibliography

watch/inbox/burn_wave_20260926/QUEUE.md (Open section, pre- and post-edit
bytes, header law block); watch/inbox/burn_wave_20260926/
B2_238_checkbox_law_20260926.md; watch/inbox/burn_wave_20260926/
B2_222_hot_living_20260926.md; watch/inbox/burn_wave_20260926/
B2_255_double_spend_20260926.md (mid-audit renumber, LEDGER ts
15:44:15Z); watch/inbox/burn_wave_20260926/B2_237_touch_law_20260926.md;
watch/inbox/burn_wave_20260926/B2_254_living_regression_20260926.md;
watch/inbox/burn_wave_20260926/B2_254_fold_order_probe.js; the receipt
family B2_11 through B2_260 (all Verdict-checked, titles quoted in the
adjudication); configs/providers.yaml z_ai2/z_ai3; models/providers.py:164;
mag/shared_surface.py; scripts/index_fold_host.mjs (verify loop,
compareBySeqTs, :172-204); tools/drift_dashboard.py:35-38;
tools/ and scripts/ prompt-copy greps; memory/game_modules/
audit_dungeon.v1.json:147; watch/inbox/burn_wave_20260926/
B2_251_audit_probe.py; watch/inbox/burn_wave_20260926/B2_251_queue_edit.py;
watch/inbox/burn_wave_20260926/B2_251_queue_edit2.py;
memory/burns/LEDGER.jsonl.

B2-310 ANNOTATION 2026-09-26: the double-id pairs this receipt enumerated were resolved by the B2-255 double-spend sweep with the later claimant renumbered: B2-244 collect (kept) vs guard pin (now B2-285); B2-215 census tripwire (kept) vs z_ai re-verify (now B2-287); B2-216 collect delta (kept) vs test debt (now B2-288); B2-221 pair (living-downgrade detector now B2-297); B2-223 mimo living (kept) vs cwd trap (now B2-299). Every "second of pair" citation in this receipt now resolves to the new id.
