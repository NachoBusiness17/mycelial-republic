# audio-dna: folder numeric style profile

Folder: `C:\Users\foste\Desktop\music-ai` - 110 audio files, 60 tagged artists. Sampled 30 tracks, stratified round-robin across artists. Every number below came from ffprobe/ffmpeg runs executed during this lane (ffmpeg 8.1.2-full_build, numpy 2.4.6 on the repo venv).

## Folder median (spread = p25 / p75, min / max)

| metric | median | p25 | p75 | min | max | n |
|---|---|---|---|---|---|---|
| duration (s) | 286.9275 | 243.8635 | 323.5043 | 117.248 | 465.408 | 30 |
| bitrate (kbps) | 239.65 | 223.525 | 249.15 | 130.7 | 278.1 | 30 |
| RMS (dBFS) | -12.205 | -13.6125 | -11.1025 | -20.23 | -7.48 | 30 |
| crest (dB) | 12.04 | 11.1025 | 13.4225 | 7.48 | 20.23 | 30 |
| zero-crossings (/s) | 1416.35 | 1150.425 | 1645.6 | 553.4 | 2140.8 | 30 |
| low-end ratio (20-150Hz) | 0.6179 | 0.5071 | 0.7458 | 0.097 | 0.7762 | 30 |
| BPM | 64.95 | 62.85 | 106.825 | 60.0 | 151.9 | 30 |
| BPM confidence | 0.522 | 0.4117 | 0.7765 | 0.165 | 0.948 | 30 |

## Per-track table (sample)

| # | file | artist | dur s | kbps | rms | crest | zcr/s | low | bpm | conf |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Windowlicker_spotdown.org.mp3 | Aphex Twin | 365.64 | 264.1 | -12.9 | 12.9 | 1275.0 | 0.5566 | 61.5 | 0.242 |
| 2 | Where's Your Head At_spotdown.org.mp3 | Basement Jaxx | 285.546 | 211.0 | -11.11 | 11.11 | 1412.2 | 0.6754 | 63.9 | 0.221 |
| 3 | LUNCH_spotdown.org.mp3 | Billie Eilish | 179.593 | 240.9 | -12.19 | 12.19 | 840.7 | 0.7459 | 125.0 | 0.789 |
| 4 | Defiant order_spotdown.org.mp3 | Birdy Nam Nam | 221.97 | 241.9 | -11.1 | 11.1 | 996.3 | 0.7459 | 62.8 | 0.334 |
| 5 | & Down_spotdown.org.mp3 | Boys Noize | 258.146 | 224.8 | -9.87 | 9.87 | 1693.1 | 0.3837 | 61.5 | 0.666 |
| 6 | Rainbow Man_spotdown.org.mp3 | Busy P | 212.682 | 244.4 | -14.08 | 12.41 | 1273.7 | 0.7626 | 104.1 | 0.431 |
| 7 | Miracle_spotdown.org.mp3 | Caravan Palace | 216.234 | 244.6 | -10.16 | 10.16 | 1182.3 | 0.49 | 100.0 | 0.506 |
| 8 | Brotherhood_spotdown.org.mp3 | Cassius | 243.448 | 250.8 | -11.1 | 11.1 | 736.1 | 0.772 | 107.1 | 0.745 |
| 9 | Hearts On Fire_spotdown.org.mp3 | Cut Copy | 294.555 | 210.4 | -12.22 | 12.22 | 2140.8 | 0.3134 | 62.5 | 0.478 |
| 10 | Life Turns_spotdown.org.mp3 | DJ Johnny SA, BieBieQ Lekker Beats | 239.269 | 224.2 | -12.35 | 11.57 | 1182.5 | 0.7181 | 125.0 | 0.563 |
| 11 | Signatune - Thomas Bangalter Short Edit_spotdown.org.mp3 | DJ Mehdi, Thomas Bangalter | 245.11 | 130.9 | -16.85 | 16.39 | 1055.8 | 0.7323 | 61.5 | 0.639 |
| 12 | Organ Donor_spotdown.org.mp3 | DJ Shadow | 117.248 | 215.8 | -14.85 | 14.85 | 1573.0 | 0.097 | 106.0 | 0.357 |
| 13 | Aerodynamic - Daft Punk Remix_spotdown.org.mp3 | Daft Punk | 370.995 | 235.9 | -13.37 | 13.37 | 1139.8 | 0.5791 | 81.9 | 0.346 |
| 14 | Blitz_spotdown.org.mp3 | Digitalism | 257.055 | 266.5 | -9.62 | 9.62 | 1485.3 | 0.7514 | 64.0 | 0.782 |
| 15 | Emerge_spotdown.org.mp3 | Fischerspooner | 288.309 | 278.1 | -17.1 | 17.1 | 553.4 | 0.6813 | 98.3 | 0.313 |
| 16 | Paris - Aeroplane Remix_spotdown.org.mp3 | Friendly Fires | 465.408 | 223.3 | -14.76 | 14.76 | 1537.4 | 0.7492 | 112.1 | 0.534 |
| 17 | Strict Machine_spotdown.org.mp3 | Goldfrapp | 231.467 | 236.6 | -11.6 | 11.6 | 566.6 | 0.7455 | 63.1 | 0.165 |
| 18 | Boy From School_spotdown.org.mp3 | Hot Chip | 319.653 | 250.8 | -9.45 | 9.45 | 959.3 | 0.5412 | 63.2 | 0.42 |
| 19 | Arp #1_spotdown.org.mp3 | Jackson And His Computer Band | 308.0 | 270.2 | -13.44 | 13.44 | 1391.1 | 0.7762 | 125.0 | 0.805 |
| 20 | In The Morning_spotdown.org.mp3 | Junior Boys | 254.212 | 130.7 | -14.62 | 14.53 | 1439.8 | 0.5057 | 80.0 | 0.51 |
| 21 | Audio, Video, Disco._spotdown.org.mp3 | Justice | 292.373 | 229.0 | -11.32 | 11.32 | 1930.2 | 0.7588 | 151.9 | 0.948 |
| 22 | Phantom Pt II - Boys Noize Remix_spotdown.org.mp3 | Justice, Boys Noize | 324.788 | 244.9 | -13.67 | 13.67 | 1932.8 | 0.2131 | 62.5 | 0.409 |
| 23 | D.A.N.C.E. - MSTRKRFT Remix_spotdown.org.mp3 | Justice, MSTRKRFT | 280.112 | 249.3 | -10.67 | 10.67 | 1906.3 | 0.5941 | 63.0 | 0.825 |
| 24 | We Are Your Friends - Justice Vs Simian_spotdown.org.mp3 | Justice, Simian | 262.79 | 238.3 | -7.48 | 7.48 | 1870.1 | 0.3774 | 61.5 | 0.466 |
| 25 | Phantom Pt II - Soulwax Remix_spotdown.org.mp3 | Justice, Soulwax | 444.765 | 248.7 | -11.32 | 11.32 | 1452.2 | 0.5113 | 63.5 | 0.779 |
| 26 | Pacific Coast Highway_spotdown.org.mp3 | Kavinsky | 344.269 | 248.3 | -11.89 | 11.89 | 1558.6 | 0.6411 | 60.0 | 0.838 |
| 27 | Testarossa - SebastiAn Remix_spotdown.org.mp3 | Kavinsky, SebastiAn | 298.085 | 238.4 | -11.72 | 11.72 | 1420.5 | 0.5947 | 65.0 | 0.508 |
| 28 | What Moves - Soulwax Remix_spotdown.org.mp3 | LA Priest | 307.107 | 139.3 | -13.03 | 13.03 | 1268.9 | 0.5726 | 110.3 | 0.575 |
| 29 | All My Friends_spotdown.org.mp3 | LCD Soundsystem | 462.273 | 215.8 | -20.23 | 20.23 | 1795.9 | 0.3129 | 142.6 | 0.769 |
| 30 | Easy Love_spotdown.org.mp3 | MSTRKRFT | 332.427 | 251.5 | -12.84 | 12.84 | 1669.8 | 0.7037 | 64.9 | 0.819 |

## Notes

- bpm is octave-ambiguous by construction (halving/doubling preserves the beat)
- bpm_conf < 0.2 = weak beat evidence, treat bpm as unproven for that track
- metrics are on the first 90 seconds only, loudness intros may bias rms low

## Derived views (computed from the per-track numbers above, same sitting, receipt in lanes/audio-dna.check.txt)

- **Peak pinning PROVEN:** decoded peak = 1.000000 on both re-checked rows (Blitz, Easy Love). The folder is mastered at full scale, so wherever crest equals |rms| that is the peak pinned at 1.0, not a metric defect. Crest here reads the loudness-war ceiling.
- **Folded BPM:** doubling every raw bpm below 90 folds the sample into [90,180): **median 125.0 BPM**, p25/p75 120.75/127.60. The raw 64.95 median is the octave-halved alias; the folder's true tempo center is club tempo (french-electro family).
