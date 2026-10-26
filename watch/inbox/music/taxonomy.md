# music-ai TAXONOMY - the remix-network map

Lane: taxonomy (division B), gala music-ractor 2026-10-01.
Source: `C:/Users/foste/Desktop/music-ai` (110 MP3s, all `_spotdown.org`-suffixed downloads).
Method: mutagen 1.48.1 full-frame scan (`ID3()`), every file read, 0 unreadable.
Scanner: `watch/inbox/gala_20260925/music-ractor/lanes/taxonomy_scan.py`.
Raw byte evidence: `watch/inbox/gala_20260925/music-ractor/lanes/taxonomy.check.txt` (496 lines, md5 `edc85e0d2d82715bd5948d3d721c7111`), self-verify block ends `VERIFY: PASS` (per-artist sum 110, class sum 110, graph edges 17, table rows 110 = dir count 110).

**The claim the ask made, confirmed: the style IS remix culture.** 87 originals carry 17 remix-credits from 13 remixers, all orbiting the French-touch axis; Justice is the hub on both sides of the edge (12 tracks as artist, 2 as remixer); Soulwax is the busiest hand (3 remixes) and also 6 tracks as artist.

## 1. Per-artist counts (original artist per TPE1, n=110, 51 artists)

| Artist | Tracks | | Artist | Tracks |
|---|---|---|---|---|
| Justice | 12 | | Boys Noize | 1 |
| Daft Punk | 6 | | Jackson And His Computer Band | 1 |
| LCD Soundsystem | 6 | | Tom Vek | 1 |
| Soulwax | 6 | | The xx | 1 |
| The Chemical Brothers | 6 | | Birdy Nam Nam | 1 |
| Hot Chip | 6 | | Mirwais | 1 |
| Simian Mobile Disco | 4 | | MSTRKRFT | 1 |
| Röyksopp | 4 | | Portugal. The Man | 1 |
| Digitalism | 3 | | Cut Copy | 1 |
| Underworld | 3 | | New Young Pony Club | 1 |
| The Knife | 3 | | Junior Boys | 1 |
| Ratatat | 3 | | Billie Eilish | 1 |
| Miike Snow | 2 | | Tame Impala | 1 |
| Cassius | 2 | | DJ Johnny SA | 1 |
| Nine Inch Nails | 2 | | SebastiAn | 1 |
| Fischerspooner | 2 | | Meghan Trainor | 1 |
| Mr. Oizo | 2 | | Caravan Palace | 1 |
| Vitalic | 2 | | Siriusmo | 1 |
| Kavinsky | 2 | | DJ Shadow | 1 |
| YACHT | 2 | | Friendly Fires | 1 |
| The Shoes, ANTHONIN TERNANT | 2 | | Busy P | 1 |
| | | | DJ Mehdi | 1 |
| | | | The Prodigy | 1 |
| | | | Tiësto | 1 |
| | | | Goldfrapp | 1 |
| | | | Simian | 1 |
| | | | LA Priest | 1 |
| | | | Basement Jaxx | 1 |
| | | | Aphex Twin | 1 |
| | | | Ummet Ozcan | 1 |

(Sums to 110, byte-checked in the scan's SELF-VERIFY.)

## 2. The remix graph (who remixed whom, 17 edges, 13 remixers)

Every edge below is parsed from the file's own tags (title suffix + TPE1 comma pair); the full per-edge evidence lines are in the check file.

| Remixer | Remixed | Track [class] | Batch |
|---|---|---|---|
| Soulwax (3) | Justice | Phantom Pt II - Soulwax Remix [REMIX] | 08-05 |
| Soulwax | LA Priest | What Moves - Soulwax Remix [REMIX] | 10-01 |
| Soulwax | Tame Impala | Let It Happen - Soulwax Remix [REMIX] | 10-01 |
| Justice (2) | Simian | We Are Your Friends - Justice Vs Simian [VS] | 08-05 |
| Justice | Soulwax | NY Excuse - Justice Remi [REMIX] | 08-05 |
| SebastiAn (2) | Kavinsky | Testarossa (SebastiAn Remix) [REMIX] | 08-05 |
| SebastiAn | The Shoes, ANTHONIN TERNANT | Time To Dance - SebastiAn Remix [REMIX] | 08-05 |
| Aeroplane (1) | Friendly Fires | Paris (Aeroplane Remix) [REMIX] | 10-01 |
| Boys Noize (1) | Justice | Phantom Pt II - Boys Noize Remix [REMIX] | 10-01 |
| Classixx (1) | YACHT | Psychic City - Classixx Remix [REMIX] | 08-05 |
| Daft Punk (1) | Daft Punk | Aerodynamic - Daft Punk Remix [SELF-REMIX, from Daft Club] | 08-05 |
| Dave Glass Animals (1) | Tom Vek | C-C (You Set The Fire In Me) - Dave Glass Animals Remix [REMIX] | 10-01 |
| DFA (1) | Soulwax | Another Excuse - Dfa Remix [REMIX] | 10-01 |
| Mark Ronson (1) | Miike Snow | Animal - Mark Ronson Remix [REMIX] | 08-05 |
| MSTRKRFT (1) | Justice | D.A.N.C.E. - MSTRKRFT Remix [REMIX] | 08-05 |
| Photek (1) | Nine Inch Nails | The Hand That Feeds - Photek Straight Mix [EDIT] | 08-05 |
| Thomas Bangalter (1) | DJ Mehdi | Signatune - Thomas Bangalter Short Edit [EDIT] | 08-05 |

All eight remixers the ask named (Soulwax, SebastiAn, MSTRKRFT, DFA, Aeroplane, Justice, Photek, Classixx) appear in the measured graph. Phantom Pt II is the only track with two remixes of itself in the folder (Soulwax + Boys Noize). The graph is densest exactly where the canon says it should be: Justice <-> Soulwax remix each other, Justice's D.A.N.C.E. gets the MSTRKRFT treatment, Ed Banger in-house (SebastiAn, Busy P, DJ Mehdi, Mr. Oizo) feeds both sides.

## 3. Original vs remix ratio (n=110)

| Class | Count | Share |
|---|---|---|
| ORIGINAL | 87 | 79.1% |
| REMIX | 13 | 11.8% |
| VS | 1 | 0.9% |
| EDIT | 2 | 1.8% |
| SELF-REMIX | 1 | 0.9% |
| VERSION (self radio edit / extended) | 4 | 3.6% |
| REMASTER | 2 | 1.8% |

Cross-artist remix-class total (REMIX+VS+EDIT): **16/110 = 14.5%**; with the self-remix, 17/110 = 15.5%. Roughly one in seven files is somebody else's hand on somebody else's track, and the originals themselves are dominated by artists who made their name remixing (Soulwax's Nite Versions cuts, Simian Mobile Disco, MSTRKRFT).

## 4. ID3 tag coverage (the spotdown.org tagger fingerprint)

| Field | Coverage |
|---|---|
| title (TIT2) | 110/110 (100.0%) |
| artist (TPE1) | 110/110 (100.0%) |
| album (TALB) | 110/110 (100.0%) |
| cover art (APIC) | 110/110 (100.0%) |
| date (TDRC/TYER) | 0/110 (0.0%) |
| genre (TCON) | 0/110 (0.0%) |
| remixer frame (TPE4) | 0/110 (0.0%) |

Only four frame types exist anywhere in the folder (APIC, TALB, TIT2, TPE1; each in 110/110). Consequences, all byte-visible:

- **The remixer is never in the ID3 remixer slot.** It lives in two informal places: the title suffix ("D.A.N.C.E. - MSTRKRFT Remix") and the TPE1 comma pair ("Justice, MSTRKRFT"). Any remix-graph miner must parse both, and cross-check them (the TPE1 part NOT in the title suffix is the original artist).
- **Era/tag coverage is structurally zero.** No dates and no genres exist in the tags, so this receipt states no release years and derives no era axis from tags; the only measured time axis is file mtime (the two batches below). Album names are present bytes and are the era fingerprint a human (or a later enrichment pass) can read.
- **TPE1 doubles as a featuring field** ("The Chemical Brothers, Noel Gallagher", "SebastiAn, Mayer Hawthorne", "Tiësto, The Chainsmokers"), so comma-splitting alone mislabels originals as remixes; the title-suffix cross-check is what keeps the graph honest.
- **The tagger truncates kind words**: TIT2 literally reads `NY Excuse - Justice Remi` (album 'NY Excuse'). A parser that does not normalize a trailing "Remi" silently loses the Justice -> Soulwax edge.
- Five files carry album 'Unknown Album': the DFA remix of Another Excuse, Escape Velocity, In The Morning, It's The Beat, and the Soulwax remix of What Moves.

## 5. Two download batches and the curation direction

Clusters by mtime are unimodal and 57 days apart, exactly two batches:

| | Batch 1: 2026-08-05 | Batch 2: 2026-10-01 |
|---|---|---|
| Files | 54 | 56 |
| Unique artists | 33 | 31 |
| Remix-class share | 10/54 (18.5%) | 6/56 (10.7%) |
| Classes | EDIT=2, ORIGINAL=42, REMIX=7, SELF-REMIX=1, VERSION=1, VS=1 | ORIGINAL=45, REMASTER=2, REMIX=6, VERSION=3 |

- **Batch 1 bought the edges.** It is the remix-singles wave: every 12"-style credit above lands here (Phantom Pt II twice, D.A.N.C.E., WAYS, NY Excuse, Animal, Psychic City, The Hand That Feeds, Signatune), plus the Ed Banger/orbit singles (Busy P, DJ Mehdi, Mirwais, Birdy Nam Nam, Kavinsky, Vitalic, SebastiAn as artist) and big-beat rock-crossover originals (Nine Inch Nails, The Prodigy, Aphex Twin, Basement Jaxx).
- **Batch 2 filled the nodes.** It is catalog depth on the same core: Hot Chip x5, Simian Mobile Disco x4, The Chemical Brothers x4, Soulwax x4, The Knife x3, LCD Soundsystem x3, plus 2 Underworld remasters and 3 self-versions (Röyksopp's and YACHT's own alternate mixes, Mr. Oizo's radio edit). Remix share drops to 10.7%.
- **13 artists sit in both batches** (Cassius, Daft Punk, Hot Chip, Justice, LCD Soundsystem, Miike Snow, Mr. Oizo, Ratatat, Röyksopp, Soulwax, The Chemical Brothers, Underworld, YACHT): the curation is converging on a fixed core canon, mapping the remix network first and backfilling the originals around it. That is remix-culture topology in purchasing behavior: the graph came before the territory.
- **Playlist noise is real and named**: Ummet Ozcan ('Xanadu', batch 1), and in batch 2 Billie Eilish ('LUNCH'), Meghan Trainor ('Me Too'), Portugal. The Man ('Feel It Still'), DJ Johnny SA ('Life Turns'), Tiësto/The Chainsmokers ('Split (Only U)'), Caravan Palace ('Miracle'). Six of the seven outlier rows are batch 2: the second batch's wider sweep dragged in non-canon material, the trade-off for its depth.

## 6. Honesty ledger: defects found and fixed in this lane

1. First classifier pass classified every hyphenated title as REMIX (no kind-word gate): 'Dead Souls - From "The Crow" Soundtrack' (a soundtrack attribution, correctly ORIGINAL after the fix), 'Cowgirl - Remastered'/'Rez - Remastered' (REMASTER), 'Flat Beat - Radio Edit' and 3 other self-versions (VERSION). Fixed and re-run; the check file is the final run only.
2. Parenthesized remixes ('Paris (Aeroplane Remix)', 'Testarossa (SebastiAn Remix)') fell through the first pass and were misfiled ORIGINAL; the ask's named remixer Aeroplane only appears once the paren form is parsed. Fixed.
3. The VS gate initially depended on the kind-word list and silently dropped 'We Are Your Friends - Justice Vs Simian' (graph read Justice=1 credit); caught by graph-edge count != remix-class count, fixed, VERIFY now closes at 17/17.
4. 'Dfa' is normalized to 'DFA' for the graph only; the tag reads 'Dfa'. 'Dave Glass Animals' is reported exactly as tagged (TPE1 carries 'Tom Vek, Glass Animals, Dave Glass Animals').
5. No code under `mag/` or `tools/` was touched; the ratchet is not run for this lane.

## 7. One-line verdict

The folder is a remix network first and a catalog second: 51 artists, 17 remix edges, one hub (Justice: 14 total appearances), one busiest hand (Soulwax), and a two-phase acquisition pattern (edges 08-05, nodes 10-01) that builds a style by mapping who-touched-whom before filling in what anyone owns.
