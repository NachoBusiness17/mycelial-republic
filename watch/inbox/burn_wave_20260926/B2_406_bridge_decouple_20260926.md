# B2-406 receipt: bridge symbol family re-link at the corrected drop number (2026-09-26)

## Verdict

LANDED as the EXPLICIT DECOUPLING arm. Re-checked on bytes: the bridge-symbol family in the visual register does NOT track drop #1104 (or any single historic drop). It is recurring channel art whose count scales with triage volume across the whole register: 8 in B1's top-40 viewed, 193 in B5's 840, 237 in B6's 1,040, plus 16 and 19 in the B7/B8 waves. The register is Telegram-era channel imagery while drop #1104 (Think Bridge) is a 2018-04-09 8ch post, and no caption- or message-level tie between any bridge-tagged image and drop #1104 was ever established anywhere in the export. VISION_READING_B1.json now carries the dated decoupling field linkage_erratum_20260926_b2_406 superseding the number-only erratum; the original findings line and the symbol census stand unchanged (history preserved, correction chained). Downstream sweep: no VISION_READING_B2+ file cites drop 874, so no downstream claim needs amending.

## Evidence file:line quotes

- watch/inbox/mrpool_export/VISION_READING_B1.json findings:26: "bridge x8 in images: drop 874 (Think Bridge) symbol family is live in the visual register" (the stale linkage, left in place as history).
- VISION_READING_B1.json erratum_20260926: "...repeats the STEGO_PASS1.json numbering error: canonical drop #874 is the Snowden HK post (8ch post 580331, 2018-03-07); the Think Bridge post is drop #1104 (2018-04-09); the bridge x8 symbol census itself stands unchanged, only the drop number is corrected..." (number-only fix; the linkage question this brief files).
- VISION_READING_B1.json linkage_erratum_20260926_b2_406 (new, this lane): "...the findings line ... is retracted in its linkage claim, not just its number ... The bridge family is CHANNEL ART independent of any single historic drop; the symbol census itself stands."
- Scaling census: VISION_READING_B5.json symbols bridge=193 (triaged 840), VISION_READING_B6.json bridge=237 (triaged 1040), VISION_READING_B7.json bridge=16, VISION_READING_B8.json bridge=19, VISION_READING_B1.json bridge=8 (triaged 40).
- Downstream sweep (grep this export dir): "drop 874" appears only in VISION_READING_B1.json (stale findings + errata) and STEGO_PASS1.json (its own erratum_20260926: "CORRECTION to also_filed: canonical drop #874 is the Snowden HK post ..."), i.e. no live downstream vision claim carries the bad linkage.

## Work done

1. Traced the erratum chain: B2_93_stego_erratum_20260926.md fixed the number in STEGO_PASS1.json and B1's erratum prose, but B1's findings line kept the stale linkage text and neither file addressed whether the imagery actually tracks drop #1104 (the brief's core question).
2. Answered the question on export bytes: pull the bridge counts across every vision batch (B1/B5/B6/B7/B8) and showed monotone scaling with triage volume (a corpus-wide motif), with no per-image caption/message tie to drop #1104 recorded anywhere in the export (no bridge-tagged image record carries a drop reference; the only 874/1104 mentions are the errata themselves).
3. Filed the decoupling: wrote the dated linkage_erratum_20260926_b2_406 field into VISION_READING_B1.json (valid JSON verified, original findings line intact, supersession stated explicitly).
4. Swept downstream files for live citations needing the same correction: none found; named that in the field.

## Falsifier

The brief's falsifier: "any downstream vision claim cites bridge x8 with drop 874 after 2026-09-26 and no erratum anchor." State after this lane: the only uncorrected citation is B1's original findings line, which now sits directly under TWO dated errata anchors in the same JSON (number-only + decoupling), so the falsifier is closed: every citation post-dating 2026-09-26 either carries the anchor or is a new violation naming its file. The decoupling itself dies if: (a) a per-image record surfaces tying a bridge-tagged Telegram image caption to drop #1104 text (that would convert the decoupling into a corrected linkage and this field must be retracted by the finder), or (b) the bridge census stops scaling with triage volume in a future batch while concentrating on a single post (a concentrated family would reopen the linkage question).

## Bibliography closed

All read this lane: watch/inbox/mrpool_export/VISION_READING_B1.json (full, pre + post edit), VISION_READING_B2/B5/B6/B7/B8.json (censuses), STEGO_PASS1.json (also_filed + erratum_20260926), SOUND_READING_FULL.json (bridge 0, audio arm negative), watch/inbox/burn_wave_20260926/B2_93_stego_erratum_20260926.md (pointer), grep sweep of the export dir for 874, QUEUE.md B2-406 row.
