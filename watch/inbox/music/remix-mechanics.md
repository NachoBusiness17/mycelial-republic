# remix-mechanics: what a remix DOES (gala music-ractor, division B)

Lane: remix-mechanics · 2026-10-01 · corpus `C:/Users/foste/Desktop/music-ai` (110 mp3s, spotdown.org rips, ID3-tagged; the same folder sibling lanes audio-dna and taxonomy mined).

The ask: pair every original with its remix(es) in the folder and compute what the remix DOES (duration delta, energy delta, BPM drift), then name the transform grammar. The lens question: what does it mean to replicate art that is itself transformation.

Raw run output: `watch/inbox/gala_20260925/music-ractor/lanes/remix-mechanics.check.txt` (exit 0). Raw numbers JSON: `watch/inbox/music/remix_mechanics.json`. Consistency verification: `lanes/remix-mechanics.verify.txt` (exit 0, 5 checks). Scan script: `lanes/remix_scan.py`.

## Method

Same ffmpeg+numpy recipe as sibling `lanes/audio_dna_scan.py`: ffmpeg decode to 8000 Hz mono s16le piped to numpy (ffmpeg 8.1.2-full_build, repo venv, numpy 2.4.6). Metrics: rms_dbfs, peak_dbfs, crest_db, zcr_hz, welch band ratios (low 20-150 Hz, lowmid 150-500, mid 500-2k, high 2k-4k, over 20-4k), dyn_range_db (p90-p10 of 250 ms frame RMS), onset_rate (strong upward onsets per second, the chop proxy), BPM via rms onset envelope (5 ms hop) autocorrelation 60-180 with parabolic interpolation and acf-peak/lag0 confidence. Delta vs sibling: pairs are decoded FULL LENGTH (audio-dna sampled the first 90 s) because the pairs are the gold.

Pairing: filenames + the taxonomy lane's tag table give 10 pairs over 19 unique files (Phantom Pt. II's original is shared by two remixes), plus 9 orphan remixes (no in-folder original) measured for grammar breadth. 28 files, all decoded, zero measurement errors.

## The pairs (remix minus original; positive = remix higher)

| pair (remixer) | class | dur % | rms dB | crest dB | dyn dB | zcr % | low % | mid % | high % | bpm raw/folded | onset % |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Aerodynamic / Daft Punk Remix (Daft Club tag) | SELF-TAGGED | +74.5 | +1.54 | -1.54 | -4.13 | +10.3 | -13.4 | +10.4 | +20.1 | 1.000 / 1.000 | +4.5 |
| Animal / Mark Ronson | CROSS-ARTIST | +20.4 | +12.80 | -1.62 | +0.41 | +41.3 | -19.5 | +37.4 | +187.1 | 0.663 / 1.326 | -25.0 |
| D.A.N.C.E. / MSTRKRFT | CROSS-ARTIST | +15.6 | +1.43 | -1.43 | -0.98 | +8.4 | +73.8 | -57.0 | +49.6 | 0.557 / 1.113 | -16.0 |
| NY Excuse / Justice | CROSS-ARTIST | +2.6 | +0.96 | -0.96 | -3.53 | +54.0 | -38.1 | +18.0 | +70.1 | 1.004 / 1.004 | +13.1 |
| Phantom Pt. II / Soulwax | CROSS-ARTIST | +121.5 | +1.11 | -1.11 | +13.68 | +19.2 | -11.8 | +1.7 | +17.2 | 0.543 / 1.085 | -13.1 |
| Phantom Pt. II / Boys Noize | CROSS-ARTIST | +61.7 | +1.34 | -1.34 | -0.46 | +17.1 | -24.6 | +65.7 | +33.9 | 0.534 / 1.068 | -42.1 |
| Flat Beat / Radio Edit | SELF-VERSION | -2.5 | +0.13 | -0.15 | -4.67 | -2.2 | +0.03 | -1.2 | 0.0 | 1.000 / 1.000 | +0.6 |
| Rez / Remastered | SELF-VERSION | -0.25 | +0.30 | -0.52 | -0.83 | -2.5 | +4.6 | -7.0 | -10.0 | 1.000 / 1.000 | +3.5 |
| Psychic City Radio Edit / Classixx | CROSS-ARTIST | -17.5 | -2.48 | +2.48 | +8.20 | +57.7 | +12.1 | +82.9 | +24.1 | 1.047 / 1.047 | -41.6 |
| Time To Dance Extended / Sebastian | CROSS-ARTIST | -50.2 | +3.02 | -3.02 | -12.09 | -7.6 | +25.0 | -28.8 | +28.8 | 0.847 / 0.847 | +49.9 |

CROSS-ARTIST medians (n=7): dur +15.6% (range -50.2 to +121.5), rms +1.34 dB, crest -1.34 dB, dyn -0.46 dB (range -12.09 to +13.68), zcr +19.2%, low -11.8%, mid +18.0%, high +33.9% (range +17.2 to +187.1), folded bpm 1.07 (0.85-1.33), onset -16.0%.

## The transform grammar (named rules, numeric)

1. **The floor law (version vs transformation).** Self-versions move only length and loudness: Flat Beat radio edit -2.5% dur, +0.13 dB, spectral identity (high band 0.0% rel); Rez remaster -0.25% dur, +0.30 dB, all bands within 10%. Below this floor a "remix" claim is a reissue or a re-rip. The `dup_suspect` triple (|dur| <= 1.5 s AND |rms| <= 0.7 dB AND zcr <= 3%) fired on zero rows: every pairing in the folder is a genuine transformation.
2. **The form operator.** Cross-artist remixes rewrite song form: median +15.6% duration, extremes are deliberate - Soulwax doubles Phantom Pt. II (+121.5%, 200.8 s to 444.8 s: a built intro and build section), Sebastian halves Time To Dance (-50.2%, 411.5 s to 204.9 s: the chop). Duration delta is the cheapest remix-vs-remaster discriminator there is.
3. **The energy operator, and its confound.** Remix RMS median +1.34 dB with crest -1.34 dB (louder, less headroom). But the Animal pair's +12.8 dB is NOT arrangement energy: the original rip peaks at -11.17 dBFS (a quiet master/rip), so the delta is mastering. Deltas under roughly 4 dB are the only ones this instrument can attribute.
4. **Two schools of dynamics.** The median (-0.46 dB) hides a bimodal split. Wall school compresses: Sebastian -12.09 dB, Aerodynamic -4.13, Justice -3.53, MSTRKRFT -0.98, Boys Noize -0.46. Shape school restores: Soulwax +13.68 dB (dyn 7.4 to 21.08: the DJ tool needs somewhere to go), Classixx +8.20 (un-crushes the radio edit, 4.64 to 12.84). The proof is same-source: Phantom Pt. II remixed by Soulwax (+13.68 dB) and by Boys Noize (-0.46 dB) - a 14.14 dB gap on one original. "Remix" is not one operation; the remixer's fingerprint IS the dynamics choice.
5. **The brightness ratchet.** High-band ratio rises in 8 of 8 transformation pairs (median +33.9%, min +17.2%); nobody goes darker. Both self-versions sit at 0.0% and -10.0%, so the ratchet itself separates transformation from reissue. ZCR rises in 7 of 8 (exception Sebastian -7.6%).
6. **Named spectral operators.** Electro-ification (MSTRKRFT on D.A.N.C.E.): low +73.8%, mid -57.0%, high +49.6% - remove the original's mid band, pay in sub and sizzle. Distortion swap (Justice on NY Excuse): structure untouched (dur +2.6%, folded bpm 1.004) but zcr +54.0%, high +70.1%, low -38.1%, dyn -3.53 dB - fuzz harmonics replace bass, the form is a wall.
7. **The tempo anchor.** Folded bpm ratio stays inside 0.847-1.326 across all 10 pairs (cross-artist median 1.07). Raw half-time reads (0.534-0.557 on Phantom/D.A.N.C.E.) are octave artifacts of the estimator: the folded side carries the higher confidence in every such case (Boys Noize 0.745 vs original 0.388; MSTRKRFT 0.792 vs 0.381). True re-tempos exist but are rare and flagged: Sebastian 0.847 (conf 0.676) and Ronson raw 0.663, a two-thirds slowdown (conf 0.255, weak evidence).
8. **The chop operator.** Onset density moves both ways: Sebastian +49.9% (nearly doubles trigger rate - the chop), wall school smooths (Boys Noize -42.1%, Classixx -41.6%), median -16%. Chop is a signature, not a rule.

## The replication answer

In this canon the only invariant a remix keeps is folded tempo near unity; form, energy, dynamics, spectrum and onset density are all operator-controlled. The same source under two remixers agrees on the anchor and disagrees on every operator (rule 4's 14.14 dB gap). So a faithful replica of art that is itself transformation is typed by its DELTA OPERATOR, not by similarity to the source: replicate the transform grammar, never the output bytes. Two replicas that "sound the same as the original" have failed; one that reproduces the operator list (this long, this loud, this compressed, this chopped, this tempo) has succeeded. That is the estate's own citation-resolution-at-landing law in another key: verify the operation against the source bytes, not the claim's surface.

## Honest gaps

- RMS is a loudness proxy, not LUFS; mastering variance rides on every energy delta (rule 3's confound is measured, not assumed).
- BPM is octave-ambiguous by construction; raw and folded ratios plus confidence are both banked. Three pair-sides carry conf < 0.4 (Aerodynamic 0.324/0.355, Animal remix 0.255, Phantom Pt. II original 0.388): those bpm numbers are weak-evidence rows.
- Two of the ten pairs are version-vs-remix bases (Psychic City Radio Edit, Time To Dance Extended Version), not true originals; the plain originals are not in the folder.
- n=7 cross-artist pairs: medians over 7. This is a canon sample, not a population claim.
- The "Aerodynamic - Daft Punk Remix" is tagged SELF-REMIX (album Daft Club); secondary sources commonly attribute the actual production to Soulwax. This lane reports tags and numbers, not lore; the numbers do not depend on who made it.
- First verify attempt exit 1: my own filter bug (the brightness-ratchet check wrongly included SELF-VERSION pairs, which sit at 0.0%/-10.0% by design). Filter fixed to transformation pairs, all 5 checks pass; both facts banked here.
- The 9 orphan remixes (Soulwax x3, DFA, Aeroplane, Glass Animals, Photek, Justice-vs-Simian, Bangalter edit) are measured in the JSON but not paired; their band-swap fingerprints are the ready-made next sit.

## Checks run this lane

- `".venv/Scripts/python.exe" remix_scan.py > remix-mechanics.check.txt 2>&1` - exit 0, 28 files decoded full length, 10 pair diffs, 0 measurement errors.
- Consistency verify (5 checks: pair/file counts, brightness ratchet on 8 transformation pairs, same-source 14.14 dB gap, tempo anchor bounds 0.847-1.326, floor-law bounds, check.txt cross-read) - exit 0, output `lanes/remix-mechanics.verify.txt`.
- Violation ratchet: not run - no code under `mag/` or `tools/` touched (this lane wrote only under `watch/inbox/`).
