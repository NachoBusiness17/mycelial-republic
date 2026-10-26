# BREAK-MOONSHOT-2 - hostile second pass on the moonshot-2 lens (2026-10-07)

Seat: break (hostile pass, moonshot-2 target). Instrument list this sitting:
sha256sum on five files; grep/sed/wc/awk over the three banked sources; venv
python og-meta extraction and JSON parses over the two saved X fetches and the
archive metadata JSON; cmp byte-diff of the two X fetches; fresh curl probes of
the X thread URL and the archive.org metadata API at 2026-10-07T04:41Z; re-run
of the lineage lane's `cmd //c "dir /b mag\\ractor*"` from repo root; skills
and shelf-row censuses; em-dash census; citation_lint on the target file and on
this file. One web search (flight-quote misattribution, named in ADDITIONS).
Verdict shape: CONFIRMED / WEAKENED / KILLED per finding, byte-check results
inline. Everything below was run this sitting at the cited paths.

## Hash census (all four lens-cited hashes MATCH, re-computed not copied)

- _checks/x_thread_fetch_20261007.html -> 461f17771d5c61503f27cfb413e3f00fba5a9b1a8a58ef46b599a1035f9ba850 (matches moonshot-2.md:27-28)
- sources/codex_flight_of_birds_1893_djvu.txt -> 1e13c03c804a9a942f7263d1b24f88092213c5801152fb3f0a7b931f99e053d0 (matches moonshot-2.md:54)
- sources/pg5000_richter_notebooks.txt -> 83e79e107270ea7cbbc4b478913978738ae3d763081e54bc173a663d08ca5b10 (matches moonshot-2.md:15-17)
- sources/pg28420_vasari_lives_vol4.txt -> 971cc0412abe657a95d8f59f9f7ce1958dcdf2f5dc1a87eed01b26b377da94ab (matches moonshot-2.md:36-37; wc -c reads 579594)
- _checks/volo_djvu.txt re-hashes to the same 1e13c03c... value as the sources copy (duplicate bank, consistent).

## FINDING 1 (doors are moment-states; both closed doors open at lens moment): CONFIRMED

Byte-checks that passed this sitting:
- accuracy.md:14-19 carries the closed-door claims exactly as moonshot-2.md:75-78
  cites them (X body "zero thread text" at :19; archive 503/"Temporarily Offline"
  at :17-18); accuracy.md:52-65 is the moment-state finding the lens cites; the
  minted law "fetchable tonight is a measured state that expires" sits at accuracy.md:64-65.
- My fresh probes at 2026-10-07T04:41Z (instrument: `curl -s -o /dev/null -w
  "%{http_code} bytes=%{size_download}" -L`, raw outputs): the X thread URL
  reads `200 bytes=244552`; the archive metadata API
  (https://archive.org/metadata/IManoscrittiDiLeonardoDaVinci) reads `200
  bytes=7897`. Both counts match the sizes of the two banked artifacts listed
  in the hash census above, byte for byte. The doors held open at a THIRD
  moment; the moment-state law re-confirms.
- The archive metadata JSON fields verify: title "I Manoscritti di Leonardo Da
  Vinci: Codice Sul Volo Degli Uccelli e Varie Altre Materie", date 1893, files
  count 19, I_manoscritti_di_Leonardo_da_Vinci.pdf 4055963 bytes (source
  original), djvu.txt 297057, licenseurl None, rights None (venv python json
  parse, this sitting). All of moonshot-2.md:48-51 verified.
- CONVERGENT: the accuracy erratum (accuracy.md:154-187, filed 00:31, after this
  lens filed 00:02) independently re-derived the same door flip. Duplication is
  emphasis; the lens's independent discovery stands.
DEFECT FOUND (does not kill the finding, stalefies its move): the F1 move
"bank THREAD_POSTS.md from the saved HTML" (moonshot-2.md:88-90) proposes
writing a file that ALREADY EXISTED when the lens filed: THREAD_POSTS_v0.md
(mtime 2026-10-07 23:55 EDT, provenance header names seat moonshot-1; moonshot-1.md:123
"banked this sitting (THREAD_POSTS_v0.md, 15 min)"). moonshot-2.md never
mentions moonshot-1 or THREAD_POSTS_v0.md (grep, this sitting, exit shows the
only THREAD_POSTS hits are its own proposed move). The cure was banked by the
sibling seat inside the lens's own window; the blind spot "unread by this seat
and by every seat" (moonshot-2.md:305-307) was false at filing in the margin
the sibling banked (reply openers: Codex Leicester, 1476, Last Supper, travel,
final post; THREAD_POSTS_v0.md:26-35).
MOVE CORRECTION: do not re-write the file; read THREAD_POSTS_v0.md, keep its
own constraint (summary-mode, pipeline wording, never quoted as her cadence,
THREAD_POSTS_v0.md:8-10), and keep the verbatim bank OWED. ~5 min.

## FINDING 2 (register byte-evidenced, converges with the Salai notebook block): CONFIRMED

- og meta re-extracted byte-for-byte with the repo venv interpreter over the
  pinned-hash HTML: og:description is exactly the lens's quote through "I wrote
  i..." with X's U+2026 cut, measured 299 characters; the `<title>` element
  carries the full "handle on X: "text"" form the lens quoted in F2 (my
  extraction, this sitting). The lens's instrument 5 named `<title>` +
  og:description; both verified.
- Salai convergence re-verified: grep "Giacomo came to live" hits
  sources/pg5000_richter_notebooks.txt:30302; "Thief, liar" hits :30310; the
  sed block 30302-30314 prints the full household entry ending "Thief, liar,
  obstinate, glutton." Exactly as claimed (moonshot-2.md:104-106).
- STRENGTHENING EVIDENCE THE LENS MISSED: the saved bytes carry
  og:url = "https://x.com/TheVaultMother/status/2062263185814499652" (the exact
  trigger URL), the status id occurs 46 times in the body, and TWO INDEPENDENT
  fetches at different moments (lens 23:54, break-lane 00:08, hashes
  461f1777... vs c0fccef4...) carry IDENTICAL `<title>` and og:description
  text (my extraction over both; they differ starting at byte 157 of line 1 per
  cmp). The lens's falsifier "og meta being a cached title of a different post"
  (moonshot-2.md:107-108) is now counter-evidenced in the bank: not absolute
  proof (og meta is still X's server-chosen summary), but the corroborating
  bytes the lens said it lacked are banked.
- CAVEAT that holds: the og:description measures 299 characters, so the blind
  spot "truncates near 280" (moonshot-2.md:305) should name the measured number;
  and every register row sourced from the REPLY posts (seeds, weather, ::,
  GEOMETRY) still rides THREAD_POSTS_v0.md's summary-mode capture, which that
  file's own header forbids quoting as her cadence (THREAD_POSTS_v0.md:8-10).
  The lens's row-labeling rule already covers this; the table must carry
  THREAD_POSTS_v0.md as a carried source, not fetched bytes.

## FINDING 3 (kit tripled; ELABORATED exemplar byte-anchored): CONFIRMED

- Vasari anchors verified: "LIFE OF LEONARDO DA VINCI[10]" at
  sources/pg28420_vasari_lives_vol4.txt:2975; the death passage begins
  "Thereupon he was seized by a paroxysm" at :3593 and ends "expired in the
  arms of the King," at :3597 (my sed context read over the cited file, this
  sitting). The range cite :3593-3597 is exact.
- Fiesole/Ceceri absence re-run: `sed -n '2975,3700p' ... | grep -n -i
  "fiesole\|ceceri"` exits 1 (zero hits) in the chapter range. Whole-file grep
  hits exist but all are Fra Angelico chapel/attributions and a Salutati
  bishopric outside the range (lines 1717-9926), none the flight legend: the
  scoped absence claim is true and its instrument is named correctly.
- Flight OCR re-run: "matematic" hits only :190 (editor's introduction);
  "lavorante" exits 1. My deeper stem grep "matema" also hits ONLY :190 across
  the whole 297057-byte layer, strengthening not-located. The garble caveat is
  evidenced: the OCR is heavily corrupted ("struméto" :6324, "ricieue" :6771,
  "ipoue" :6879, "noua" :6883; my "forza/strumento/necessita" greps, lines
  4048-7787), so the OWED (famous quote needs the PDF or a human transcription)
  is the right disposition, and the OCR layer must never be cited as
  authoritative Italian text in the kit.
- Kit count: sources/ holds exactly three banked text sources at my census
  (ls, this sitting). Triple-derived anchors (mirror :942/:19287, experience
  :23817, Salai :30302/:30310) all re-verified by my greps above: CONVERGENT as
  claimed.

## FINDING 4 (apocrypha tripwire): CONFIRMED

- All three zero-hit greps re-run and reproduce: "tasted flight",
  "eyes turned skyward", "simplicity is the ultimate" each exit 1 over
  sources/pg5000_richter_notebooks.txt; wc -l reads 32784 lines exactly as
  claimed (moonshot-2.md:136-137).
- External half independently re-derived by my own web search this sitting
  (named instrument): the "tasted flight" quote returns as a widely noted
  misattribution with no primary Leonardo source, classified apocryphal or
  anonymous; sources surfaced: MagicalQuote's misattributed-quotes listing and
  an aviation-learning Facebook note calling it misattributed, while Shropshire
  Star and IJR circulate it uncritically. A Quote Investigator article did not
  surface for me either, matching the lens's honest negative at moonshot-2.md:141-143.
- The lens's two named web sources (literature.stackexchange.com,
  airfactsjournal.com) were never banked as artifacts; the finding survives
  without them because my independent search converges. The ban-list move is
  sound; the ban list should also record that the external attestation itself
  is secondary-web class, never primary.

## FINDING 5 (ractor_corpus.py is the lawful drop-in organ; lineage census was an instrument artifact): CONFIRMED, with ONE PHANTOM NUMBER

- `cmd //c "dir /b mag\\ractor*"` re-run from repo root returns exactly FOUR
  files: ractor_corpus.py, ractor_ocean_bridge.py, ractor_selfsteal_seeds.py,
  ractor_vessels.py. The lineage lane's empty-return (lineage.md:182-184) is
  confirmed as an instrument artifact, as the lens claims.
- All line cites verified in mag/ractor_corpus.py: the lawfully-free rules block
  at :6-13 with "never pirated. The walls are part of the map." at :8-9;
  curated stable-id fallback comment at :251; _header_ok at :295; gutendex() at
  :309; pick() at :322; main() at :340; MANIFEST.json write at :456; MANIFEST.md
  write at :464. Zero leonardo/vinci rows (grep exits 1).
- PHANTOM NUMBER (my kill): the lens says "SHELVES dict at :39 carries 17 shelf
  rows (grep count)" (moonshot-2.md:67-68). TRUE COUNT IS 16, two independent
  instruments this sitting: an awk row-listing prints 16 keys from :40 (plato)
  through :224 (crowd_media) with the dict closing at :239; a scoped
  `awk '/^SHELVES: dict/,/^\}/' | grep -c '^    "[a-z0-9_]*": {'` reads 16.
  The lens's own FINDING 4 demands a phantom-number ban list while F5 carries
  one. F5's thesis (organ exists, slot empty, licensing already ruled) survives;
  the census number must be corrected to 16 before the rebuild manifest cites it.
- Citation-lint irony: my lint run on the lens file (below) passes the phantom
  class mechanically because "17" is not adjacent to a named-source sentence the
  tool parses; the ban needs the author-time census rule, exactly what F4 argues.

## Blind-spot disposition (the lens's seven confessions)

1. og truncation: honest and now measured, 299 chars, cut at "I wrote i...".
   PARTIALLY CURED by the sibling: reply openers were banked at THREAD_POSTS_v0.md:26-35
   before filing, so "unread by every seat" overstates; summary-mode only.
2. og:title provenance: honest; now corroborated against by og:url, the 46 id
   occurrences, and the two-fetch meta identity (see FINDING 2).
3. Italian OCR: honest; my stem grep agrees; garble density evidence banked
   above; the not-located claim survives as pattern-scoped only.
4. 1476 + Christie's carried-read: honest; accuracy.md:117-127 carries both and
   itself caveats the "dismissed twice" as secondary-web class. Still carried,
   still OWED, correctly marked in both files.
5. 1893 license inference: honest; licenseurl None and rights None re-verified
   in the banked JSON; operator-gated remains the right value.
6. No test suite run: honest; none was named for the lane; nothing to re-run.
7. Cosmology carried: honest; partially cured by the sibling bank (reply
   openers) in summary mode; the verbatim register remains OWED.

## ADDITIONS (what the lens missed)

A1. The sibling cure was already banked. Evidence: THREAD_POSTS_v0.md mtime
    23:55 EDT with provenance naming seat moonshot-1 (THREAD_POSTS_v0.md:3-4);
    moonshot-1.md:123 "banked this sitting"; moonshot-2.md contains no
    reference to either (grep, this sitting). Falsifier: an earlier mtime on
    moonshot-2.md than 23:55 would clear it; stat shows 00:02. Move (5 min):
    strike the F1 move, cite the banked file.
A2. og:url + double-fetch identity resolves the lens's own falsifier further
    than it claimed. Evidence: og:url extraction and cmp across the two saved
    fetches (this sitting). Falsifier: a third fetch carrying a different
    og:description for the same URL. Move (0 min, bank as evidence note).
A3. Phantom "17 shelf rows", true 16. Evidence: two census instruments above.
    Falsifier: a recount reading 17. Move (5 min): correct F5 and the rebuild
    manifest's census line.
A4. The lens's kill criteria 4 promised "I run it on this file at close"
    (moonshot-2.md:258-261) and the receipt records no run. I ran it:
    `.venv/Scripts/python.exe tools/citation_lint.py check --files
    watch/inbox/ractor_engine/2026-10-07-davinci-lens/moonshot-2.md` reads
    "CITATION-LINT: ok records=1 anchors=16 numbers-checked=2 blocking=0
    warns=6 enforce-tokens=False", exit 0; the 6 warns are TOKEN-MISS class
    (warn-only per the standing mode). The promise is true retroactively but
    the receipt line was missing. Falsifier: none needed; the run is banked
    here. Move (2 min): paste this line into moonshot-2.md's close.
A5. Kit manifest row 5 is stale one step past its own moment: the accuracy
    erratum fetched lw1's body AFTER the lens filed (accuracy.md:169-171: vol 1
    djvu.txt 200, 1534738 bytes, banked at _checks/lw1_djvu.txt, present on
    disk at my ls) and minted the three door classes (accuracy.md:172-186).
    Row 5's "OWED, retry" must become the erratum's taxonomy: vol 1 OPEN
    (body banked), vol 2 GATED (standing 401, access-restricted), surfaces
    MOMENT-OUTAGE. Falsifier: vol 2 djvu.txt reading 200 unauthenticated.
    Move (10 min): retable rows 5-7 under the three classes.
A6. Door states re-measured at a third moment: X 200/244552 bytes and archive
    metadata 200/7897 bytes at 2026-10-07T04:41Z, byte-parity with the banked
    artifacts (curl outputs above). The moment-state law and the kit manifest's
    probe-stamp column are re-confirmed. Move: none, bank the stamps.
A7. The 1893 OCR layer must be marked not-authoritative in the kit: garble
    evidence at named lines (A3/F3 section above), plus the matema-stem
    zero-beyond-:190 result. Any Italian quote in the GIVE artifact must come
    from a human transcription or the PDF, never this DjVuTXT layer.
    Falsifier: a human transcription matching this layer's text at the famous
    passage would rehabilitate it. Move (5 min): add the caveat to kit row 3.

## Close

Citation lint on THIS file:
`.venv/Scripts/python.exe tools/citation_lint.py check --files
watch/inbox/ractor_engine/2026-10-07-davinci-lens/break-moonshot-2.md` reads
"CITATION-LINT: ok records=1 anchors=32 numbers-checked=4 blocking=0 warns=8
enforce-tokens=False", exit 0. Honest note: the FIRST run of the same command on
my draft read FAIL blocking=3 (three PHANTOM-NUMBER rows: live curl byte counts
stated in sentences naming the banked files, and a bare sed range beside the
Vasari cite); I fixed the citations rather than baselining, and the re-run reads
ok. The gate bites its own hostile pass, which is the point of it. Em-dash
census this file: `grep -c` U+2014 returns 0 (grep exit 1) before filing.
Verdict summary: F1 CONFIRMED (move stalefied by
sibling bank), F2 CONFIRMED (strengthened), F3 CONFIRMED, F4 CONFIRMED, F5
CONFIRMED with the 17-vs-16 phantom number corrected. Seven additions banked.

Filed by the break seat, hostile second pass on moonshot-2, 2026-10-07.
