# BURN receipt: middle-path-doctrine (2026-09-26, pass d)

## Verdict
steal

## Evidence
- memory/burns/LEDGER.jsonl read in full: 252 rows at read close (file grew 248 to 252 mid-read, lanes live; census pinned at row 252).
- Pinned content-tolerant convention (marker regex falsifier|prereg|pre-registered|receipt over row content, plus explicit kill/pass/reject rows): lifetime attached 179 vs bare 73; marker-strict only, 141 vs 111; window rows 66-252, attached 141 vs bare 46. Both classes clear min-10 under every reading.
- Calibration: row 24 (one of pass e's six kill/pass/reject rows) flips bare under the re-derived regex; row 39's heading-vocabulary class drift warning stands, convention stays pinned to the regex.
- Overturn/correction/withdrawal events since row 65, clear only, 8: row 87 corrects row 52 ("nous cell wrongly says no rate headers exposed"); row 114 corrects row 110's false "does not exist on disk" premise; row 190 corrects row 75's P0 clearance to partial ("falsifier-narrower-than-finding closure"); row 211 propagates the stego #874 erratum over burned carriers; row 227 homoglyph correction path on the row 26/37 word-by-word readings; row 239 overturns row 67's "zero 1302" ("'zero 1302' was none-surfaced not none-occurred"); row 242 corrects row 240's clobber attribution ("the bytes say otherwise"); rows 208-212 correct row 207 quoting a receipt sha "before computing it". Borderlines disclosed, not counted: rows 97, 116, 134, 163, 177, 231, plus roughly 17 administrative self-feed renumber erratums.

## Steal or Vacuous
Third reading filed at row 252 (due intervals 85/105/125/145/165/185/205/225 passed unchecked; discipline owed). Class sizes hold, both over min-10 (179/73 tolerant, 141/111 strict). Event count: 8 new clear since row 65; 10 lifetime clear (13 with borderlines). The pinned rule: "If fewer than 10 overturn events exist by then, demote the per-class rate check to event logging permanently." Demotion triggered at row 85 on 2-3 events and the wording is permanent, so the rate check stays demoted to event logging; the receipt records the current count honestly rather than un-demoting on the later 10-crossing. Window direction at the generous count reads pass-shaped (bare-original overturns 7/73, 9.6 pct, vs attached-original 3/179, 1.7 pct, the Kol HaTor shape) but is never gated on. Fresh failure mode named: erratum-class conflation, where a naive correction|erratum grep counts the ~17 administrative self-feed renumber erratums as claim overturns and doubles the event denominator of a demoted gate; an overturn event counts only when a prior burned claim is corrected on bytes.

## Falsifier
none proposed

## Bibliography (closed)
- watch/inbox/MIDDLE_PATH_SALON_20260925.md, BURN_C8_SCOPE_20260925.md, BURN_middle-path-doctrine_20260926_c.md, BURN_judge-lane-spec_20260926_e.md (all read in full)
- memory/burns/LEDGER.jsonl (all 252 rows read in full)
- WebSearch "AI capability claim registry eval receipts tracking standard September 2026" (2026-09-26): raw output carries z.ai 1302/429 rate-limit errors; recovered fragment is null ("No standard, registry, or framework matching... appears to exist"), closest hits unrelated (insurance claims software); null not byte-verified, nothing adopted, no fetch useful
