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
