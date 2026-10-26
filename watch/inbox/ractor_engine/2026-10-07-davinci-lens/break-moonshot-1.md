# BREAK-MOONSHOT-1 - hostile second pass on moonshot-1.md (2026-10-07)

Seat: break-moonshot-1. Target: moonshot-1.md (the Five-Hundred-Year Soil lens,
third fire). Every claim below was re-run by me this sitting unless marked
not-run. Instruments: sha256sum, grep -c/-i/-n/-a over banked bytes, sed line
pulls, cmp, ls mtimes, Read of moonshot-1.md, THREAD_POSTS_v0.md, lineage.md
:95-110, moonshot-2.md :28-78. No new network fetches (my pass is over the
estate's banked bytes; the ask's probes are moment-scoped and labeled as such).
No em-dashes. Anything I could not run is stated as not run.

## 0. BYTE-CHECK SUMMARY (what reproduced, what did not)

Reproduced exactly this sitting:

- sha256 of sources/pg5000_richter_notebooks.txt =
  83e79e107270ea7cbbc4b478913978738ae3d763081e54bc173a663d08ca5b10 (full 64 hex
  matches the lens's prefix), byte-identical to _checks/pg5000.txt, size
  1,433,832 bytes (find -printf %s and ls agree).
- Every cited line resolves verbatim: :942 mirror ("reason, is like a mirror
  which copies every thing placed in front of"), :23817 experience ("Experience
  never errs; it is only your judgments that err by"), :30302-30303 ("Giacomo
  came to live with me on St.-Mary Magdalen's day, 1490, aged 10 years."),
  :30310 ("of the fact.--Thief, liar, obstinate, glutton."), :16853 ("The drum
  (tamburo) of these cupolas is generally octagonal"), :20863 ("and of Fiesole,
  and of", hydrography), :31570 ("Giovanni da Fiesole, of Bartolommeo della
  Gatta" = Fra Angelico), :23389-23397 (sect. 1123 bat-wings), :28492 (Salai
  letter: "now send Salai to explain to your Lordship"), :28595 (letter range
  end still Salai: "I am sending thither Salai"), :29160-29166 (Richter
  factotum gloss, runs exactly 29160-29163 with tail through 29166).
- Counts over the full file, untruncated: saltarelli 0, "codex leicester" 0,
  tamburo 1, fiesole 2, "bird is an instrument" 0, instrument-lines also naming
  bird 0, "never errs" 1, mirror 104, Salai 35 ("Salaì" 0, "Salaino" 0 in
  pg5000: Richter spells Salai only).
- Both short quotes byte-present in BOTH banked X fetches: "500 years of soil"
  5 hits each, "Santa Croce is where they buried me" 2 hits each.
- lineage.md:101-102 carries the founding premise text ("X blocks anonymous /
  fetch, so the operator's clipboard is the lawful door"); the lens's cite
  :100-102 covers it.
- Amenti cite verified: watch/inbox/AMENTI_TRANSLATION_20261005.md:53 reads "No
  endorsement of unmeasured claims (frequencies, tension figures) - the reply
  says so explicitly in her own courtesy", exactly as moonshot-1.md:52-54 leans
  on it. ROLL_SHAPE_TURING_CASTLE_20261007.md exists in watch/inbox/.

Not re-run by me (reported as not run, not passed): the F4 live curl probes
(/items/ 404 vs /details/ 200 vs metadata 200 vs download HEAD 302). I verified
their BANKED artifacts instead: _checks/lw1_metadata.json (101,810 bytes) and
_checks/lw2_metadata.json (16,448 bytes) list the exact file names F4 claims
(lw2: literaryworksofl0000leon.lcpdf, .pdf, _djvu.txt, _djvu.xml,
_encrypted.pdf; lw1: .epub, .pdf, _djvu.txt, _djvu.xml), so the per-file
downloadability claim is anchored to banked metadata even though the HTTP codes
are the lens's own moment.

## 1. VERDICTS

### F1 (thread anonymously fetchable; founding premise half-wrong): CONFIRMED, strengthened

Byte checks above all pass. The falsifier ("a repeat fetch from a different
session hitting a login wall") has ALREADY BEEN TESTED by a sibling lane and did
not fire: _checks/x_thread_fetch_break.html (244,552 bytes, sha c0fccef4..., mtime
2026-10-07 00:08:58, a second anonymous fetch ~14 minutes after the first,
_checks/x_thread_fetch_20261007.html 244,553 bytes sha 461f1777... 23:54:57)
carries both quotes at identical counts, zero "sign in" hits, zero "something
went wrong" hits, and cmp shows the two files differ in exactly 3 bytes
(offsets 157-159, the page nonce). Two distinct sessions, no wall, opening post
and reply text served to a logged-out client both times. The lens did not know
its own falsifier had already been run and survived. Defect found in the lens's
own bank: THREAD_POSTS_v0.md:4 records the fetch moment as "2026-10-07 ~03:45-04:00
ET" but the file mtime is 2026-10-06 23:55:30-0400, so the stated moment is UTC
mislabeled as ET (the lens's own protocol rule 6 is confession-header hygiene;
fix the label). Stronger still, see Addition A1: the "OWED verbatim reply
bodies, still clipboard-gated" tail of F1 is dead, the bodies are in the banked
HTML.

### F2 (Santa Croce demonstration on her own words): CONFIRMED

The quote is byte-verified in both fetches and in THREAD_POSTS_v0.md:31. The
ELABORATED half rides the ask's operator pass (material the ask gave), honestly
carried, and its falsifier (documented evidence placing the body at Santa
Croce) has not fired against anything in the banked corpora. Two sharpenings the
lens missed: (a) the DOCUMENTED half (Chapel of Saint-Hubert, Amboise) is still
carried-not-anchored: grep over the banked Vasari vol4 returns "Santa Croce" 0,
"Saint-Hubert" 0, "Amboise" 0, so the banked second door does not yet anchor
either half of the burial row; (b) the banked Vasari DOES anchor the adjacent
death legend the same GIVE will need: the death-in-Francis-arms scene at
sources/pg28420_vasari_lives_vol4.txt:3593-3597 ("the King having risen and
having taken his head... his spirit, which was divine... expired in the arms of
the King, in the seventy-fifth year of his age"), verified by my own sed pull
this sitting (note the passage's own "seventy-fifth year" chronology is Vasari's
claim, part of the legend text, tri-state accordingly).

### F3 (anchors byte-verified; flight quote hangs on a missing door): WEAKENED

The measurement half stands: every pg5000 anchor resolves verbatim, the flight
quote is absent from pg5000 under every phrasing I tried (zero
instrument-lines naming bird; "mathematical" 10 hits, none adjacent to
bird/instrument; closest cousin :23844 "Mechanics are the Paradise of
mathematical science"). The door narrative half is FALSE at the report's own
write moment: moonshot-1.md:150-151 says "the flight-facsimile door, which is
not yet fetched" and blind spot 2 says "still an unfetched door", but
sources/codex_flight_of_birds_1893_djvu.txt (297,057 bytes, sha
1e13c03c804a9a942f7263d1b24f88092213c5801152fb3f0a7b931f99e053d0, identical to
_checks/volo_djvu.txt) has file mtime 2026-10-06 23:53:48, about 3.5 minutes
BEFORE moonshot-1.md (mtime 23:57:07), fetched by the sibling moonshot-2 seat
into the same sources/ directory the lens pins its sha256s against (receipt:
moonshot-2.md:52-53, the exact archive.org/download/IManoscrittiDiLeonardoDaVinci
URL F3's own move proposed). The manifest row is stale the same way: Vasari
28420 marked "FETCHABLE TONIGHT" (moonshot-1.md:67) while
sources/pg28420_vasari_lives_vol4.txt landed 23:52:43. The row's classification
does NOT flip though: I re-ran the flight-quote greps myself and they corroborate
moonshot-2.md:59-61: in the banked 1893 OCR "istrumento" 0, "strumento" 9 (all
flying-machine apparatus or editor preface, none the famous line), "matematica"
0, "mathematique" 0 (accent form), "math" only 4 hits (:220, :1032, :1666,
:1725, all editor preface/bibliography), "operante"/"opérant" 0, "leggi" 4 (all
editorial/orthographic). So the row stays DOCUMENTED-elsewhere / OWED-
translation, but for the true reason (door fetched, OCR carries no greppable
line), not the lens's reason (door unfetched). The conclusion survives, the
evidence story is dead: weakened.

### F4 (a bare 200 is not a door status): CONFIRMED

The kit law is minted in moonshot-1.md section 3 as claimed and the banked
metadata JSONs carry the exact per-file evidence the finding describes (file
lists quoted in section 0 above). I did not re-run the live probes; the claim
is self-scoped to the lens's sitting and the falsifier (a stably-200 /items/
form across sessions) remains untested. Nothing contradicts it in the banked
bytes, and the finding's instrument discipline (record URL form, UA, code,
moment, file names per row) is the same law this pass applied to itself.

### F5 (corpus boundary measured, maps her episodes): WEAKENED

The counts reproduce exactly (section 0). Two defects:

(a) Killed overreach: moonshot-1.md:180-181 says "the 1476 charge, the
Leicester pages, and the Fiesole injury DO NOT EXIST in it at all." The
Leicester clause is FALSE against the lens's own banked fetch: bare "leicester"
= 3 hits, all in the lens's own instrument range: :251 (Richter preface, "the
Earl of Leicester" among manuscript owners), :263 ("the Revd A. Napier,
Librarian to the Earl of Leicester at Holkham Hall"), :30810 (footnote: "The
note referring to this author thus suggests a solution of the problem of the
date of the Leicester Manuscript"). The compound-phrase grep ("codex
leicester") was too narrow an instrument for the existence sentence built on it,
which is the exact quantifier-law failure class the register carries. The
episode-CONTENT absence (Leicester water-studies text) still stands; the row
must be re-scoped to "the manuscript is named only in editorial apparatus
(:251, :263, :30810); zero water-studies content." The falsifier as written
("an OCR sweep of the IA Richter djvu.txt volumes") was aimed at the wrong
corpus: the counterexample lived in pg5000 itself.

(b) The episode mapping's Vasari leg is backwards: moonshot-1.md:82-84 and :189
say "Vasari 28420 grounds the Fiesole legend text and the death-in-France
legend." The banked Vasari grounds the death legend (F2 sharpening above) but
NOT the Fiesole legend: my scoped re-census over the Leonardo chapter range
(:2975-3700, sed then grep -c -i "fiesole\|ceceri") returns 0, and all 10
whole-book "fiesole" hits are Fra Angelico's life, S. Domenico da Fiesole, or
index entries (:1717, :2594, :4452, :5163, :6269, :9510, :9781, :9800, :9815,
:9926). moonshot-2.md:42-44 measured the same zero. The Fiesole legend's second
door remains unbought; moonshot-1's manifest row asserts a grounding that the
banked bytes refute. Weakened, not killed: the counts, the NEED-SECOND-DOOR
classification for 1476 and Leicester-content, and the executable estate
mapping all stand.

## 2. ADDITIONS (what the lens missed)

### A1. The verbatim thread bank already exists in _checks; the clipboard-gated OWED is dead

The two banked X HTMLs carry full verbatim post text in the relay payload and
the og: meta, greppable with grep -a. Verified this sitting by my own
extractions: opening post verbatim via og:description ("...He came to me at 10
years old as an apprentice. He was a thief. He stole from me constantly. He
lied. He ate enough for 4 men. I called him \u201cil Salaino\u201d :: little
devil. I wrote i\u2026"); Botticelli reply verbatim ("He was not my nemesis. He
was my weather. Some days sunny. Some days a storm I wanted nothing to do with.
He painted like it was candy. Sweet/bright/immediate. I painted like it was
surgery. Precise/slow/sometimes the pat..."); cowardice reply verbatim
("cowardice &amp; called it strategy. Sometimes the strategy WAS cowardice &amp;
I could not tell the difference until years later. That is the burden of a mind
that sees 10 moves ahead..."); flight reply verbatim ("...That failure taught me
more than any success... Some seeds need 500 years of soil. The helicopter I
drew :: it flew. Just not while I was breathing. Vlad. Men like him were not
rare..."); and the two "cut" replies terminate in payload at authorial
cliffhanger links, not truncation: the 1476 reply's text field ends "The truth
is more complicated than https://t.co/A5QjSzN9zl" and the travel reply ends
"...It is the GEOMETRY. https://t.co/06JZoNDiVi". The "Show more" truncation the
WebFetch pipeline reported is a RENDER artifact; the data is served. Falsifier:
an authenticated fetch showing a reply whose payload text field is itself
truncated mid-sentence with no link terminator. Move: parse the two HTMLs'
text fields into THREAD_POSTS_v1.md, unescape \n and &amp;, strike the
clipboard-gated OWED rows in moonshot-1.md section 3 and THREAD_POSTS_v0.md
(:54-58); 30 to 45 minutes, zero new fetches.

### A2. "Morning Coffee with Leonardo" is a pipeline artifact, not her title

grep -a "Morning Coffee" over the banked break HTML returns 0 hits; the og:
title/og:description carry the Salaino text instead. THREAD_POSTS_v0.md:13
heads the table with "Morning Coffee with Leonardo" as if it were her framing;
it is the render pipeline's label. Mark it as artifact in v1 (the lens's own
blind spot 4 warned of this class; the v0 bank nonetheless carries it as a
header).

### A3. The lens-card HOME row is factually wrong: the code organ exists

moonshot-1.md:33-35: "lineage.md's shelf finding checked: there is no mag/
ractor* code organ; the skill shelf is the library." False: ls mag/ractor*
returns 4 files (mag/ractor_corpus.py, mag/ractor_ocean_bridge.py,
mag/ractor_selfsteal_seeds.py, mag/ractor_vessels.py), re-run by me this
sitting from repo root. moonshot-2.md:66-67 already measured the same four.
The sharper true finding sits one grep deeper and moonshot-1 missed it:
grep -c -i "leonardo\|vinci" over mag/ractor_corpus.py returns 0 rows, so the
estate's own corpus harvester has no Leonardo shelf. The HOME row should read: skill shelf
AND ractor_corpus.py both exist; the missing organ is a Leonardo shelf row in
the harvester, which is exactly where the kit's four free fetches should be
registered. Falsifier: a mag/ractor_corpus.py SHELVES dict containing a
leonardo row would convert this to "registered, needs update." Move: add the
Leonardo shelf row (or an explicit OWED row in the kit manifest), 15 minutes,
operator-gated as a code change.

### A4. The Vasari legends are locally anchorable tonight; the lens's blind spot 3 was curable by one grep

Blind spot 3 says the Vasari legend texts were "carried from the ask and the
sibling seat, not independently verified by me this sitting." The file had been
banked in the same sources/ directory 4 minutes before the report was written
(mtime 23:52:43). My independent pulls this sitting: death-in-Francis-arms
legend at pg28420:3593-3597 (full text quoted under F2), Salai row at
:3399-3402 ("In Milan he took for his assistant the Milanese Salai, who was
most comely in grace and beauty, having fine locks, curling in ringlets, in
which Leonardo greatly delighted"), Monna Lisa/Francis-at-Fontainebleau row at
:3437. The burial row is the one thing the banked Vasari does NOT settle (Santa
Croce / Saint-Hubert / Amboise all 0): that stays carried-by-ask, honestly
labeled. Move: add the two path:line anchors to the rebuild manifest's
NEED-SECOND-DOOR list, 10 minutes.

### A5. Fetch-moment mislabel in the banked capture (confession-grammar defect)

THREAD_POSTS_v0.md:4 states the fetch moment as "2026-10-07 ~03:45-04:00 ET";
the file mtime is 2026-10-06 23:55:30-0400, which is 03:55 UTC. The moment is
UTC mislabeled as ET, and on the mislabel the capture would postdate its own
bank by hours. The lens's protocol rule 6 (confession grammar: corpus tip,
fetch moment, sha, frozen true or false) is the right law; the v0 bank breaks
it on its own header line. Move: correct the line to UTC or local with offset,
2 minutes.

### A6. F1's falsifier was already run and survived; record it as evidence, not risk

Per F1: the sibling lane's second anonymous fetch (00:08:58) is the repeat
session F1's falsifier asked for, and it passed. The finding's evidence column
should cite both fetch shas and the 3-byte cmp delta, upgrading the claim from
"my claim names the pipeline and moment" to "two sessions, both served, one
nonce apart." Zero minutes (record already banked; cite it).

## 3. PASS INSTRUMENTS (exact commands this sitting)

sha256sum over the seven banked files (section 0, hashes quoted); find -printf
size listing of the folder; sed -n line pulls at pg5000 :246-266, :942, :16853,
:20863, :23389-23397, :23623, :23817, :28492, :28595-28596, :29160-29166,
:30302-30312, :30795-30825, :31570; grep -c -i counts over pg5000 for
saltarelli, "codex leicester", leicester, tamburo, tamburi, fiesole, "bird is
an instrument", mathematical, "never errs", mirror, plus Salai/Salaì/Salaino;
grep -n context pulls for leicester, tamburi, mathematical, instrument+bird;
grep -n "X blocks anonymous fetch" scope check via sed on lineage.md :95-110;
grep -a counts and -o extractions over both X HTMLs for the two quotes, "sign
in", "something went wrong", "Show more", nemesis/weather, cowardice, Salaino,
"500 years of soil", GEOMETRY, "complicated than", full_text; cmp -l over the
two HTMLs (3 bytes, offsets 157-159); ls mtimes for every file in the folder;
sed on moonshot-2.md :28-78; sed on vasari :3395-3460 and :3585-3600; scoped
census sed -n '2975,3700p' | grep -c -i "fiesole\|ceceri" (= 0) and whole-book
fiesole (= 10); grep -o '"name":"..."' over lw1/lw2 metadata JSONs; grep -o
identifier over flight metadata JSON (= IManoscrittiDiLeonardoDaVinci);
flight-text counts for istrumento, istrumenti, mattematica, matematica,
mathematique, instrument, volatile, uccello, math, strumento, leggi, oiseau,
operante, opérant, volare/voler; sed :53 on watch/inbox/AMENTI_TRANSLATION_
20261005.md; ls of ROLL_SHAPE_TURING_CASTLE_20261007.md; ls mag/ractor* from
repo root plus grep -c -i leonardo/vinci over mag/ractor_corpus.py (= 0).
NOT run: live HTTP probes of any door (F4's codes are the lens's moment, its
banked metadata JSONs re-read by me), any new X fetch, any test suite (none
exists for prose lens reports; the ask named none).
