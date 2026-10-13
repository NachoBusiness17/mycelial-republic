# CORPUS FOLD: music (music-ai canon + remix mechanics)

Folded 2026-10-01 by the fill-corpus-fold lane (gala fillball-1001, division B) from the program's own measured receipts. House format per state/fuel/corpus_fold_prompt.md. The DeepSeek corpus-fold draft for this program was seat-verified and REJECTED (fabricated subject and citations, zero grounded paths); this entry is folded directly from the source digests.

## music-ai canon and remix transform grammar (the canon is measured, not vibes: 110/110 profiled target zones plus a numeric remix-vs-reissue grammar)

## Top mechanisms

1. **Shared-recipe audio profiling as the objective style organ.** One ffmpeg+numpy recipe (8000 Hz mono s16le decode; RMS dBFS, onset-envelope autocorrelation 60-200 BPM with 1x+2x harmonic sum and parabolic refine, zero-crossing rate, sub-160 Hz spectral power share, spectral centroid) profiled 110/110 corpus files with 0 failures, and every canon number below is its output, cross-checked against two prior independent runs (30-track sample, 52-track full decode). Feeds the cutter/generation organ: any cut is checked with the same recipe it was cut from.
2. **The fold-to-octave tempo law.** 30 of 110 raw BPM detections are half-time (60-79) and the raw median 110.5 is octave-torn; folding raw autocorrelation into [90,180) before comparing is what makes the corpus center real: folded median 124.0, strong-confidence subset (45 rows) 125.0, and the two prior runs agree within plus-or-minus 2 BPM or an octave on 46 of 52 overlap rows. Feeds any organ that stores or compares BPM (state/fuel/music_bpm.json consumers, cutter acceptance checks).
3. **The numeric canon target zone.** 124-125 BPM center, 115-130 band (folded p25/p75 115.5/129.75), RMS -13.9 to -11.1 dBFS over the first 90 s (median -12.35), peak pinned at 0 dBFS on 97 of 110 files, deliberately warm/dark spectrum (centroid median 1070 Hz, ZCR median 1272/s), kick-dominant low end (sub-160 Hz share median 0.47), runtimes 232-328 s. Feeds generation acceptance: a cut that passes tempo but sounds bright or thin is off-canon.
4. **The remix floor law (version vs transformation).** Self-versions move only length and loudness (Flat Beat radio edit -2.5 percent duration, +0.13 dB, high band 0.0 percent; Rez remaster -0.25 percent, +0.30 dB, all bands within 10 percent); below that floor a remix claim is a reissue or a re-rip, and the dup_suspect triple (duration within 1.5 s AND RMS within 0.7 dB AND ZCR within 3 percent) fired on zero rows, so every pairing in the folder is a genuine transformation. Feeds duplicate detection and library triage.
5. **The cross-artist transform grammar.** Cross-artist remix medians (n=7): duration +15.6 percent (extremes deliberate: Soulwax doubles Phantom Pt. II at +121.5 percent, Sebastian halves Time To Dance at -50.2 percent), RMS +1.34 dB, high-band ratio +33.9 percent rising in 8 of 8 pairs (the brightness ratchet nobody goes darker on), folded BPM ratio 0.847-1.326; dynamics split into a wall school (Sebastian -12.09 dB) and a shape school (Soulwax +13.68 dB, a 14.14 dB gap between two remixes of one original), and energy deltas under roughly 4 dB are the only ones this instrument can attribute (Animal's +12.8 dB is mastering: the original rip peaks at -11.17 dBFS). Feeds the taxonomy organ and the lens question of what replication-of-transformation means.

## Falsifiable probes

1. Re-run the shared recipe on any 10 canon tracks and check the folded medians land inside the published zone (BPM 115-130, centroid 900-1200 Hz, peak within 0.5 dB of full scale); a miss falsifies the profiler-reproducibility claim.
2. Generate one cut from Facet A (filter-disco, 124 BPM), measure it with the same recipe, and check folded BPM lands in 115-130 with centroid under 1200 Hz; a bright/thin pass-tempo cut falsifies the facet-to-output discipline.

## Sources

- watch/inbox/gala_20260925/music-ractor/lanes/style-synthesis.json + style-synthesis.check.txt + style-synthesis.profile.py (110/110 profile run; note: STYLE_SPEC names it style-synthesis.profile.json, the on-disk receipt is style-synthesis.json)
- watch/inbox/music/audio-dna.md (30-track sample) and watch/inbox/music/remix_mechanics.json (raw pair numbers)
- state/fuel/music_bpm.json (52-track full-length decode)
- watch/inbox/gala_20260925/music-ractor/lanes/remix-mechanics.check.txt (exit 0), remix-mechanics.verify.txt (exit 0, 5 checks), remix_scan.py
- watch/inbox/gala_20260925/music-ractor/lanes/cutter-disco.check.txt and cutter-electro.check.txt (cutter pack gates: artist-name-free style strings, DNA triangulation)
