# break-accuracy.md - hostile second pass on the da Vinci lens accuracy lane (2026-10-07)

Pass: byte-check every evidence cite in accuracy.md, re-run each check this sitting,
verdict each finding confirmed / weakened / killed, add what the lens missed.
Everything below was run this sitting; instruments and outputs named inline.
All new artifacts banked at `_checks/` (hashes pinned below). No em-dashes.

## Moment and fresh-fetch provenance

- Fresh upstream fetch: `curl -s -o pg5000_fresh.txt https://www.gutenberg.org/cache/epub/5000/pg5000.txt`
  reads 1433832 bytes, sha256 83e79e107270ea7cbbc4b478913978738ae3d763081e54bc173a663d08ca5b10,
  byte-identical to the lens's banked `_checks/pg5000.txt` (same size, same hash, verified
  with wc/sha256sum). The lens's pinned door provenance is real end to end.
- Gutenberg door tonight: `curl -sI https://www.gutenberg.org/cache/epub/5000/pg5000.txt`
  reads HTTP 200 (last-modified Fri, 02 Oct 2026 18:50:46 GMT); `/ebooks/5000` also 200.

## Verdicts

### F1 (DOCUMENTED tier holds for 4 anchors, 3 missing from the pinned door; door mapping needs repair): CONFIRMED, move weakened

Every byte claim reproduced against `_checks/pg5000.txt` (32784 lines, 1433832 bytes,
sha256 83e79e...5b10):
- Salai 1490 age-10 entry with "Giacomo came to live with me on St.-Mary Magdalen's
  day, 1490, aged 10 years" and "Thief, liar, obstinate, glutton" at :30310, inside
  the claimed :30303-30312 span (_checks/pg5000.txt:30300-30315, printed in full).
- Mirror passage "like a mirror which copies every thing placed in front of" at :942.
- "Experience never errs" at :23817 and "Experience does not err" at :23821, both hits.
- Great bird at :29769 ("The great bird will take its first flight;--") through :29772.
- Zero-greps reproduced exactly: `grep -n -i "Saltarelli\|sodomy"` exit 1; "instrument
  working" exit 1; "human strength" exit 1. Near-miss check: `grep -n -i "his strength"`
  nearest hit :7198 is a machine-weight passage ("raise as much more than his weight as
  his strength may be more"), exactly as the lens characterized it.
- Tamburo false anchor: :16853 "The drum (tamburo) of these cupolas is generally
  octagonal", a cupola drum, not the Palazzo letter-box. Confirmed.
- Absence nuance I added: "mathematical science" DOES appear at :23844 and :24350
  ("Mechanics are the Paradise of mathematical science"), so a manifest row must quote
  the true flight-codex phrasing, not a paraphrase, or a near-miss row will bait.

Move defect found: both re-route destinations the move names FAIL their own fetch test
tonight. (a) Richter Literary Works vol 1 (archive.org 1883, unrestricted): fetched
`https://archive.org/download/literaryworksofl01leon/literaryworksofl01leon_djvu.txt`
HTTP 200, 1534738 bytes, sha256 6d465ee0...c58c; greps over it: saltarelli|sodomy zero,
salain zero, accus only at :769 (unrelated) and :31751 (Italian variant text),
"instrument working\|mathematical law" zero, "1476" hits only a regency line at :40289.
(b) Flight-of-Birds codex door (archive.org item IManoscrittiDiLeonardoDaVinci, the
1893 NYPL "Codice Sul Volo Degli Uccelli" scan, metadata JSON banked at
`_checks/flight_of_birds_archive_metadata.json`, title+date verified by parse): fetched
its DjVu text HTTP 200, 297057 bytes, sha256 1e13c03c...53d0; "operante" zero,
"matematic" only in the editor's introduction at :190, OCR badly word-joined
("laforza", "siipoue"), so absence here is OCR-limited (instrument named: grep over the
2014 IA OCR of the 1893 scan). Verdict: the finding's claims stand, but its move routes
anchors to doors that were never verified to carry them; as measured tonight the three
re-routed anchors (1476, mathematical law, strength) have NO fetchable primary home in
any door probed this sitting.

### F2 (door census is a moment-state; archive.org dark tonight): WEAKENED, lesson reinforced

The lens's own falsifier fired: `curl -sI https://archive.org/details/literaryworksofl01leon`
reads HTTP 200 (nginx/1.31.3, 04:08:19 GMT), `.../literaryworksofl0000leon` HTTP 200,
and `curl -s https://archive.org/metadata/literaryworksofl01leon` returns valid item
JSON (101810 bytes), not "Temporarily Offline". The 503 was moment-scoped and lifted
inside the same window. The stamp-law move stands and is proven by the flip itself.
The deeper miss: the lens treated BOTH Richter doors as the same moment-state class,
but vol 2 (`literaryworksofl0000leon`) is a STANDING access gate, not a moment-state:
its metadata reads `access-restricted-item: true`, collections
internetarchivebooks/inlibrary/printdisabled, and
`curl -sL https://archive.org/download/literaryworksofl0000leon/literaryworksofl0000leon_djvu.txt`
returns HTTP 401 with a 172-byte error body (banked as `_checks/lw2_djvu.txt`), while
vol 1 downloads freely. A probe-stamp column alone would mark both "200 tonight" and
hide the difference; the manifest needs an access-class column too.

### F3 (trigger unverifiable; zero post text in the 200 body): KILLED

The lens's falsifier ("an unauthenticated curl returning the thread's actual text in
the response body") fired twice. (1) My fresh probe:
`curl -s -A "Mozilla/5.0..." "https://x.com/TheVaultMother/status/2062263185814499652"`
returns HTTP 200, 244552 bytes (sha256 c0fccef4...3433, banked
`_checks/x_thread_fetch_break.html`), whose `<title>` reads verbatim: "I loved someone
named Salai. Andrea Salaino. He came to me at 10 years old as an apprentice. He was a
thief. He stole from me constantly. He lied. He ate enough for 4 men. I called him
'il Salaino' :: litt..." and whose meta description reads "...Everyone else approached
me with reverence or agenda. Salai approached me with his hand in my coin purse..."
(extracted with `grep -a -o ".{60}salai.{60}"`; the file needs `grep -a`, it carries
binary bytes). (2) The lens's OWN banked artifact
`_checks/x_thread_fetch_20261007.html` (244553 bytes, mtime 2026-10-06 23:54:57)
contains the same post text ("coin purse" x5, same title text): the report's "zero
thread text in the returned bytes" (accuracy.md:19, written 23:39:27) contradicts the
evidence file banked under its own directory. X serves the logged-out shell WITH the
opening post's text in title and meta tags. Residue that survives: only the FIRST post
is in the shell; the thread's subsequent posts and replies still require the operator
or an authed fetch, so "paste-able by her" remains right for posts 2..n. The first-post
text confirms the briefing's register (thief, ate for 4 men, coin-purse vs reverence)
at zero cost; the register blind spot is partially cured tonight.

### F4 (legend verdicts converge; absence claim names its instrument): CONFIRMED, one cite defect

- Fiesole absence reproduced exactly: `grep -n -i "Fiesole" _checks/pg5000.txt` returns
  exactly 2 hits (:20863 "of Fiesole, and of", :31570 "Giovanni da Fiesole, of
  Bartolommeo della Gatta"), both painter attributions. Also new: "Ceceri" has zero
  hits in the same file (grep exit 1), so the primary door carries no Ceceri seed.
- chateau-amboise.com re-fetched this sitting (French page
  /le-recit-de-la-mort-de-leonard-de-vinci/): it does place Francois I at
  Saint-Germain-en-Laye on 2 May 1519 ("Il s'est rendu a Saint-Germain-en-Laye pour la
  naissance de son second fils"), frames the deathbed scene as fake news
  ("une fake news avant l'heure", "Cette scene fictive", "historiquement inexact"),
  and names the Ingres 1818 painting (Petit Palais). All three confirmed.
- Cite defect: the lens's "Cellini retelling of Melzi the seed (same page)" is NOT on
  the page I fetched; the page's only discussed source is Vasari. The Cellini/Melzi
  attribution needs its own source row (Cellini's memoir), not that page. My English
  URL guess 404'd, so I could not check whether an English variant carries it; the
  sub-claim is unverified as attributed.
- The Vasari/Anonimo-Gaddiano silence and the Monte Ceceri Wikipedia row were cited
  "via web search this sitting"; I could not re-run the lens's search, only the primary
  absence above, which is consistent.

### F5 (tri-state law and citation lint are the same instrument; gate runnable): CONFIRMED

- tools/citation_lint.py:23 is the PHANTOM-NUMBER definition line ("PHANTOM-NUMBER
  a notable quantity appears in NONE of its sentence's"); tools/citation_lint.py:151 is
  `def check_anchor(...)` (sed 20-26 and 148-154).
- The lint run reproduced byte-for-byte:
  `.venv/Scripts/python.exe tools/citation_lint.py check --files
  watch/inbox/ractor_engine/2026-10-07-davinci-lens/accuracy.md` reads "CITATION-LINT:
  ok records=1 anchors=12 numbers-checked=2 blocking=0 warns=4 enforce-tokens=False",
  exit 0. All 4 warns are TOKEN-MISS, WARN-only, matching the lens's close section.
- Em-dash census reproduced: `grep -c $'\u2014'` and `grep -c -P "\x{2014}"` both
  return 0 on accuracy.md.
- The prior fire's args-loss receipt is verbatim at
  watch/inbox/ractor_engine/ractor-topic/accuracy.md:3-4 ("Topic arg arrived undefined").
- Second falsifier prong fails to fire: `.venv/Scripts/python.exe -m pytest -q
  tests/test_citation_lint.py` reads "11 passed in 83.44s", so the PHANTOM-NUMBER
  founding fixture is enforced and cannot pass a broken doc silently.
- One seat-law note: my first parse attempt used bare `python` and was rejected by the
  seat-law hook; re-run with `.venv/Scripts/python.exe` (AGENTS.md env law). The lens's
  own commands all used the venv path.

## Additions the lens missed

1. Standing-gate door class (F2's blind spot): `literaryworksofl0000leon` is
   access-restricted (metadata `access-restricted-item: true`; text download HTTP 401,
   172-byte body) while `literaryworksofl01leon` is unrestricted (HTTP 200, 1534738
   bytes). The kit manifest needs an access-class column (free / lending / login) next
   to the moment-stamp column, or every refire rediscovers the 401.
2. Both F1 re-route destinations fail their own fetch-and-grep test tonight (vol 1 OCR:
   zero anchors; 1893 flight codex OCR: zero greppable anchors, OCR word-joining). The
   three re-routed anchors currently have no verified fetchable primary home; until one
   is found, the kit must carry them as secondary-carried (e.g. the Wikipedia rows the
   lens already cites) rather than DOCUMENTED-via-primary.
3. The thread's opening post IS seat-fetchable in the logged-out shell (title + meta),
   so the rebuild manifest should pin the first post as fetched bytes (banked at
   `_checks/x_thread_fetch_break.html`, sha256 c0fccef4...3433) and keep only posts 2..n
   operator-supplied. The lens's F3 move over-returns bytes to the operator.
4. Report-vs-evidence drift inside one sitting: accuracy.md written 23:39:27, then the
   flight metadata JSON banked 23:52:45 and the x.com fetch 23:54:57, neither folded
   back; the OWED section still says "the Flight-of-Birds codex door is unprobed" while
   `_checks/flight_of_birds_archive_metadata.json` (banked 23:52:45) proves the probe
   happened. Amend-not-rewrite applies to lens artifacts too.
5. pg5000.txt near-miss hazard: "mathematical science" lives at :23844 and :24350 in the
   pinned door. A manifest row paraphrased as "mathematical law" would look DOCUMENTED
   on a loose grep. Quote exact phrasing per row; the quote is the probe.
6. The 1893 flight-codex door (IManoscrittiDiLeonardoDaVinci) is real, free, and
   fetchable tonight (metadata + DjVu text 200), but it is an OCR-poor 1893 scan; it is
   a facsimile-class door (image PDF) with a weak text derivative. The kit should pin
   the PDF for eyes-on and never cite its djvu.txt for absence claims.

## What this pass did not do

- Did not verify the Codex Leicester sale figures (F4-adjacent "checks out" row);
  secondary-web only, same caveat the lens filed.
- Did not locate a fetchable primary/transcription door for the 1476 denunciation, the
  mathematical-law quote, or the strength confession; three doors grepped, all zero in
  greppable form (instruments named above).
- Did not read the full thread beyond the opening post; posts 2..n remain
  operator-supplied.

## Close

This bank file was itself gated with the instrument F5 vouches for, and the gate bit
on the first draft: `.venv/Scripts/python.exe tools/citation_lint.py check --files
watch/inbox/ractor_engine/2026-10-07-davinci-lens/break-accuracy.md` first returned
"CITATION-LINT: FAIL ... blocking=1" with "PHANTOM-NUMBER 30300 number appears in none
of the sentence's named sources" (a bare sed range written as prose numbers); fixed by
re-writing the span as the resolvable anchor _checks/pg5000.txt:30300-30315, second run
reads "CITATION-LINT: ok records=1 anchors=5 numbers-checked=7 blocking=0 warns=3",
exit 0, the 3 warns being TOKEN-MISS / UNRESOLVED-SOURCE heuristics in the WARN-only
mode. Live proof, on a fresh artifact, that F5's two-layer claim holds and that the
number rule is enforced-and-fair. Em-dash census on this file: zero U+2014 (grep -c,
exit 1).

Filed by break-accuracy, hostile second pass, 2026-10-07, one seat one sitting.
