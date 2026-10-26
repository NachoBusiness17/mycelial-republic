== STYLE_SPEC.md ==
# STYLE_SPEC: the music-ai canon, in three languages

Folder: `C:/Users/foste/Desktop/music-ai` (110 mp3 files, 44.1 kHz on 105/110, ~240 kbps median).
This is the style DNA the cutters cut from. Every measured number below comes from this lane's own
shared-recipe run over all 110 files (receipt: `watch/inbox/gala_20260925/music-ractor/lanes/style-synthesis.profile.json`),
cross-checked against two prior independent runs (`watch/inbox/music/audio-dna.md` 30-track sample;
`state/fuel/music_bpm.json` 52-track full-length decode). No artist names appear anywhere in this spec,
including the Suno strings: Suno blocks artist names, so the style must be describable without them.

Recipe (shared, reproduce with):
`ffprobe` for stream meta + `ffmpeg -t 90 -ac 1 -ar 8000 -f s16le` decode piped to numpy:
RMS dBFS, onset envelope autocorrelation 60-200 BPM (1x+2x harmonic sum, parabolic refine),
zero-crossing rate, sub-160 Hz spectral power share, spectral centroid.
Profiler: `watch/inbox/gala_20260925/music-ractor/lanes/style-synthesis.profile.py`. 110/110 profiled, 0 failures.

## Language 1: plain language (what this canon IS)

This is a club-era canon built on a permanent four-on-the-floor kick. It lives on a tension between two
poles. One pole is **filter disco**: a chopped-up 1970s disco loop, guitar and string stabs looping under a
resonant low-pass filter that opens and closes over 16 or 32 bars, warm and dusty, built from sampler
culture, where the whole track is one groove slowly revealed by the filter. The other pole is **electro
punch**: saturated, overdriven synth bass growling in syncopated riffs, snappy compressed snare, gated
noise, punk energy played by machines, the blog-house decade's answer to rock: louder, dirtier, harder.

Between the two poles sits the glue: **sidechain pumping**. On almost every track the bass and pads duck
on every kick, so the groove breathes like a lung. And a third face surfaces often: **vocoder and talk-box
vocal hooks**, machine voices singing wordless melodies over disco-funk chords, the pop front of the same
club machinery.

The deepest tension is disco-funk vs electro: sampled warmth (real drummer breaks, real strings, wah
guitar, handclaps) against synthesized aggression (distorted bass, digital stabs, clipping masters). The
best cuts here ride both at once: a disco loop you can hum and a bass you can feel in the chest. Song
forms are DJ forms: long intros and outros, builds, filter drops, 16-bar loop logic, 3:30 to 5:30
runtimes. Mood: confident, physical, night-city, never ambient, never EDM-supersaw-bright.

## Language 2: numeric (the target zone, measured 110/110)

| target | value | measured evidence (this census, n=110) |
|---|---|---|
| tempo center | **124-125 BPM** | folded median 124.0; strong-confidence subset (45 rows) 125.0; prior 30-track sample folded median 125.0; prior 52-track full-decode run agrees within ±2 BPM or an octave on 46 of 52 overlap rows |
| tempo band | **115-130 BPM** | folded p25/p75 = 115.5/129.75; 89 of 110 tracks fold into [100,140), mode bin 125-130 (26 tracks) |
| tempo law | fold raw autocorrelation into [90,180) before comparing | 30 of 110 raw detections are half-time (60-79); raw median 110.5 is octave-torn, not a real center |
| loudness (RMS) | **-13.9 to -11.1 dBFS** over the first 90 s | median -12.35, p25 -13.95, p75 -11.13 |
| mastering ceiling | **peak pinned at 0 dBFS** | 97 of 110 peaks within 0.5 dB of full scale; loudness-war club master, crest ~12 dB |
| brightness | **deliberately warm/dark** | ZCR median 1272/s (p25 961, p75 1528); spectral centroid median 1070 Hz (p25 902, p75 1187). Modern EDM would sit far higher; keep cuts low-passed and warm |
| low-end | **kick-dominant** | sub-160 Hz power share median 0.47 (p25 0.21, p75 0.63): up to half of total spectral energy below the kick's ceiling on the heavy rows |
| runtime | **232-328 s** (cut 3:30-5:30) | median 264.6 s, p25 231.6, p75 328.1 |
| production signature (from the numbers, not assumed) | steady 4/4 + strong low band + ducked bass = sidechain pumping; looped samples + dark centroid = filter-disco texture; 0 dBFS ceiling + 12 dB crest = punch master | this census + `audio-dna.md` peak-pinning and welch low-ratio (0.62 median) agree |

Genre priors used for triangulation (stated as priors, not measurements): french touch/filter house
clusters 120-125 BPM with heavy filtering and sidechain; blog-house/electro clusters 125-132 BPM with
saturated bass; both share the four-on-the-floor spine and loudness-war mastering. All three measured
sources (this census, the 30-track sample, the 52-track full-decode run) land on the french-touch side of
the seam at 124-125 folded center, with the electro punch showing up in the loudness and low-end numbers
rather than the tempo.

## Language 3: Suno style strings (three triangulated facets, no artist names)

Each string is a standalone Suno style prompt. Cut toward ONE facet per generation; do not merge facets.

### Facet A: filter-disco

```
Filter disco house, 124 BPM, four on the floor kick, chopped 70s disco loop as the main instrument, looped wah guitar and string stabs rising through a resonant low-pass filter sweep, filter opens into a full-band disco drop, pumping sidechain compression ducking the bass on every kick, warm saturated vintage sampler texture, bright disco violins, handclaps on 2 and 4, tight shuffle hats, filtered spoken vocal snippets used as percussion, long DJ style filter builds and releases, 16 bar loop arrangements with small variations, dusty 1970s disco warmth heard through a late 1990s club sound system, confident hypnotic groove, no drop aggression, let the loop do the work
```

### Facet B: electro-punch

```
Blog house electro, 127 BPM, four on the floor stomper, heavily saturated sawtooth bass growling in syncopated riffs locked to the kick, aggressive sidechain pumping, crunchy overdriven electro bass answering a chopped disco vocal stab, gated noise sweeps, snap tight compressed snare on 2 and 4, dirty distorted drop after a rising filter build, gritty low bitrate synth character, hard clipped loud master pushing the red, vocoder shout accents on the hook, punk energy played by machines, electro rock attitude, relentless dancefloor punch, big minor key riff, rave stabs, white noise risers, keep the kick huge and the bass nastier
```

### Facet C: vocoder-pop

```
Electro pop with vocoder lead, 122 BPM, soft four on the floor club kick, warm disco funk bassline, silky seventh chord synth pads, talk box and vocoder hooks singing wordless melodies, layered over a clear human pop vocal, sparkling filtered disco guitar loops, gentle sidechain breathing, bright disco strings lifting the chorus, crisp tight snare, handclaps and tambourine, hopeful bittersweet mood, French house warmth with real pop song structure, verse, pre chorus, chorus, filter drop into the final chorus, romantic smooth city at night feeling, warm analog master, radio sheen over club bones
```

## Verification notes for cutters

- Generate at the facet's stated BPM; check the result's folded BPM lands in 115-130 (recipe above).
- Loudness: aim RMS near -12 dBFS with the peak touching full scale; if the cut sounds thin, raise the
  sub-160 Hz share toward 0.4-0.5, do not brighten (centroid target 900-1200 Hz).
- Runtime target 3:30-5:00 for cuts meant for the canon shelf.
- A cut that passes tempo but sounds bright/thin is off-canon: the canon's signature is warm, dark,
  loud, and pumping, not crisp.


== remix-mechanics.md ==
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
8. **The cho