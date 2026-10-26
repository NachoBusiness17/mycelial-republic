# accuracy.md - da Vinci lens ractor, accuracy lane (2026-10-07 refire, topic args present)

Lens: accuracy (falsifier-hunter). The operator order re-fired 2026-10-07 with full
args after the settings-only-amend args-loss bug; the prior fire's args loss is
receipted in-tree at watch/inbox/ractor_engine/ractor-topic/accuracy.md:3-4
("Topic arg arrived undefined"). This lane rides the topic's own accuracy law the
way the operator modeled it: tri-state every claim (DOCUMENTED / INTERPRETIVE /
ELABORATED) and byte-check the doors the source kit manifest will pin, before the
fold crowns anything. Everything below was run this sitting; nothing is copied
from the operator order's own verification pass without an independent re-run.

## Instruments run this sitting

1. Door census, curl, moment 2026-10-06 ~23:30Z local:
   - `curl -s -o /dev/null -w "%{http_code}" -L https://www.gutenberg.org/ebooks/5000` -> 200
   - `curl -s -o /dev/null -w "%{http_code}" -L https://www.gutenberg.org/cache/epub/5000/pg5000.txt` -> 200
   - `curl -s -o /dev/null -w "%{http_code}" -L https://archive.org/details/literaryworksofl01leon` -> 503
   - `curl -s -o /dev/null -w "%{http_code}" -L https://archive.org/details/literaryworksofl0000leon` -> 000 then 503 on retry; the metadata API `https://archive.org/metadata/literaryworksofl01leon` returned the body "Internet Archive: Temporarily Offline"
   - `curl -s https://x.com/TheVaultMother/status/2062263185814499652` -> 200, body is a React app shell (`data-app-env="prod"`), zero thread text in the returned bytes
2. Primary text fetch: `curl -sL -o _checks/pg5000.txt https://www.gutenberg.org/cache/epub/5000/pg5000.txt`, sha256sum reads 83e79e107270ea7cbbc4b478913978738ae3d763081e54bc173a663d08ca5b10 and ls reads 1433832 bytes (command outputs, this sitting). All pg5000 line anchors below are pinned to that hash; Richter line numbers shift across editions, so the anchors are stable only for this file.
3. Greps over `_checks/pg5000.txt` (patterns, hit counts, and line numbers cited inline).
4. Web checks: Codex Leicester sale terms; the royal itinerary of 2 May 1519; the 1476 denunciation record; the Fiesole/Ceceri flight legend (sources named inline in the findings).
5. Citation lint on this file at close: `.venv/Scripts/python.exe tools/citation_lint.py check --files watch/inbox/ractor_engine/2026-10-07-davinci-lens/accuracy.md`, result recorded in the close section.

## Findings

### F1: the DOCUMENTED tier holds in the free door for 4 anchors and fails in it for 3

Byte-verified in _checks/pg5000.txt this sitting: the Salai household entry reads
"Giacomo came to live with me on St.-Mary Magdalen's day, 1490, aged 10 years" and
ends the theft list with "Thief, liar, obstinate, glutton" (pg5000.txt:30303-30312);
the mind-as-mirror passage reads "is like a mirror which copies every thing placed
in front of" (pg5000.txt:942); "Experience never errs; it is only your judgments
that err" appears twice (pg5000.txt:23817 and pg5000.txt:23821); the great-bird
prophecy "The great bird will take its first flight" is at pg5000.txt:29769-29772
with Richter's own footnote calling it "a speculation about the flying machine".
But the same door does NOT carry three anchors the kit would need from it: the 1476
denunciation has zero hits for the grep `grep -n -i "Saltarelli\|sodomy" pg5000.txt`
(patterns over the full 32784-line file), and a naive `grep -n -i tamburo` returns
pg5000.txt:16853 which is a cupola drum, an architecture false-anchor, not the
Palazzo letter-box; the "mathematical law" flight phrasing has zero hits for
`grep -n -i "instrument working\|bird is an instrument"`; and the insufficient-human-
strength admission has no matching hit for `grep -n -i "human strength\|his strength"`
(the nearest, pg5000.txt:7198, is a machine-weight passage, not the confession).
Falsifier: re-run the four greps against the same hash; hits appearing where I read
zero kills this finding. Move (~30 min): in the kit manifest, re-route the 1476
anchor to a door that actually carries it (Wikipedia's Jacopo Saltarelli row or the
Richter Literary Works intro once archive.org returns) and the mathematical-law and
strength anchors to the Flight-of-Birds door, marking each row's probe stamp; the
claim tiers stay DOCUMENTED, the doors were wrong.

### F2: the door census is a moment-state, not a constant: one of the kit's verified doors is dark tonight

The operator order pins archive.org/items/literaryworksofl01leon and
literaryworksofl0000leon as "probed 200 on 2026-10-06"; tonight both read 503 with
"Internet Archive: Temporarily Offline" (instrument output in section 1). Both
claims are true at their moments; the difference is the moment, the same lesson the
ractor50 retro files as moment-verdict decay (watch/inbox/ractor50/accuracy.md,
incident 3 and the B2-216 denominator law). Gutenberg alone carried the entire
DOCUMENTED verification tonight and is free. Falsifier: an archive.org probe
reading 200 again would make the outage moment-scoped and the doors fine; the law
this finding mints (per-door probe command + timestamp + status column in the
manifest) is needed either way. Move (~15 min): add the probe-stamp column and a
fallback chain to the kit manifest, and make "fetchable tonight" a measured state
that expires, never an asserted property of a URL.

### F3: the trigger artifact is unverifiable from the seat; a 200 on x.com is not thread evidence

The curl probe of the thread URL returns HTTP 200 but the body is the logged-out
React shell with no post text in the bytes (section 1). Counting that 200 as
"thread verified" is exactly the ok:true-equals-landed class that filed fabricated
citations as landed in the ractor50 retro (watch/inbox/ractor50/accuracy.md,
incident 1). Consequence for the fold: the register mapping (frequencies, seeds,
bindings) rests on the operator's briefing of what the thread says, not on her
sentences; the lens card's voice protocol must be built from the briefing and
marked as such. Falsifier: an unauthenticated curl returning the thread's text in
the response body. Move (~5 min): the rebuild manifest marks the thread itself as
operator-supplied source (paste-able by her, unverifiable by the seat), and no
deliverable quotes her post text as fetched bytes.

### F4: the two legend verdicts CONVERGE with external sources, and my in-corpus absence claim names its instrument

Death-in-the-king's-arms is contradicted by the documented itinerary: the Chateau
d'Amboise official page states Francois I was at Saint-Germain-en-Laye on 2 May
1519 and calls the deathbed scene "fake news" (https://www.chateau-amboise.com,
"The story of Leonardo da Vinci's death"), with the Ingres painting of 1818 named
as the popularizer and Cellini's retelling of Melzi's words as the legend's seed
(same page). The injured student at Fiesole traces to the Monte Ceceri flight-test
legend with no contemporary source (Vasari and the Anonimo Gaddiano silent; the
notebook seed is Leonardo's note about flying "from the mountain which bears the
name of the great bird"; Monte Ceceri Wikipedia row via web search this sitting).
My own instrument over the primary door: `grep -n -i "Fiesole" _checks/pg5000.txt`
returns exactly 2 hits (pg5000.txt:20863 and pg5000.txt:31570), both painter
attributions, zero about an injured student, an absence claim scoped to this one
file and hash. Both verdicts are CONVERGENT with the operator's own tri-state
(duplication is emphasis). Falsifier: any pre-1520 document placing Francois I at
Clos Luce on 2 May 1519, or any contemporary record of the Ceceri injury. Move
(~10 min): the lens card's kill criteria list both legends as
assert-only-under-ELABORATED-label, with these two sources as the standing refs.

### F5: the tri-state law and the estate's citation lint are the same instrument at two layers, and the gate is runnable

DOCUMENTED equals citation-resolves; INTERPRETIVE equals the source exists and the
claim outruns it; ELABORATED equals no resolvable source. That is
tools/citation_lint.py in prose: the PHANTOM-NUMBER class is defined at
tools/citation_lint.py:23 and the anchor resolver at tools/citation_lint.py:151;
the pre-push hook already runs it on changed prose per AGENTS.md. The lens card
therefore does not need a new gate, only a mandate: her artifact ships through the
same lint before it leaves the seat. This file is the dogfood proof; the close
section records the run. Falsifier: the lint command below returning FAIL on this
file, or a PHANTOM-NUMBER fixture passing it. Move (~5 min): one line in the
rebuild manifest, "author-time command: python tools/citation_lint.py check
--files <lens-card.md>", and the tri-state labels ride every historical claim in
the lens card.

## What checks out beyond the findings (verified this sitting)

- Codex Leicester: sold to Bill Gates at Christie's New York on 11 November 1994
  for US$30,802,500, 72 sheets, mirror script (https://en.wikipedia.org/wiki/Codex_Leicester
  via web search this sitting). Matches the operator order's figure to the cent.
- The 1476 record: anonymous denunciation dropped in the tamburo of the Palazzo
  della Signoria, jurisdiction of the Ufficiali di Notte, naming Jacopo Saltarelli,
  dismissed on the signed-accusation requirement, with the case recorded twice in
  1476 and no trial (https://en.wikipedia.org/wiki/Jacopo_Saltarelli and the
  sources it cites, via web search this sitting). Caveat: "dismissed twice" is
  verified only through secondary web sources tonight; no primary archive fetch
  was possible (F2).

## OWED (not verified this sitting, marked, never asserted)

- Salai staying ~25 years and inheriting (the Mona Lisa legacy in Melzi's will):
  not in _checks/pg5000.txt, no door probed tonight.
- The "insufficient human strength" admission and the mathematical-law flight line:
  true doors not resolved tonight (F1); the Flight-of-Birds codex door is unprobed.
- Her thread text, the Vasari public-domain translation door, and both
  archive.org items: unreachable tonight (F2, F3).
- The Richter translation edition behind ebook 5000: unverified; the line anchors
  are pinned to the sha256 above, not to "Richter" in the abstract.

## Close

`.venv/Scripts/python.exe tools/citation_lint.py check --files
watch/inbox/ractor_engine/2026-10-07-davinci-lens/accuracy.md` ran this sitting:
"CITATION-LINT: ok records=1 anchors=12 numbers-checked=2 blocking=0 warns=4",
exit 0; the 4 warns are TOKEN-MISS heuristics, WARN-only by the standing mode
(AGENTS.md: --enforce-tokens flips them), each one an auxiliary-token miss where
the quoted span itself matched. Em-dash census: zero U+2014 characters
(`grep -c $'\u2014'` on this file returned 0 before filing). Primary text and probes
preserved at watch/inbox/ractor_engine/2026-10-07-davinci-lens/_checks/ for the
rebuild manifest's byte anchors.

Filed by the accuracy lens, 2026-10-07 refire, one seat one sitting.

## ERRATUM (hostile second pass verdict: F2 WEAKENED; re-checked and corrected 2026-10-07)

The hostile pass verdict is accepted: F2's falsifier fired, so F2's factual core
("archive.org dark tonight") is withdrawn as a durable claim. Re-run this sitting
(all curl, exit codes as printed):

- `curl -s -o /dev/null -w "%{http_code} bytes_downloaded=%{size_download}" -L
  https://archive.org/details/literaryworksofl01leon` -> 200, 266235 bytes
- same for details/literaryworksofl0000leon -> 200, 217042 bytes
- metadata/literaryworksofl01leon -> 200, 101810 bytes (exactly the figure the
  hostile pass quoted; my earlier "Temporarily Offline" read was moment-scoped
  and lifted inside the same window)
- `curl -s https://archive.org/metadata/literaryworksofl0000leon` parsed with the
  repo venv python: metadata.access-restricted-item = "true", collection =
  internetarchivebooks / inlibrary / printdisabled
- `https://archive.org/download/literaryworksofl0000leon/literaryworksofl0000leon_djvu.txt`
  -> 401, 172-byte body; `literaryworksofl01leon_djvu.txt` -> 200, 1534738 bytes

CORRECTION: the kit's door classes are three, not two, and my original finding
lumped the last two together. (1) OPEN: Gutenberg pg5000 (200) and Richter vol 1
djvu.txt (200, 1534738 bytes) fetch directly. (2) MOMENT-OUTAGE: archive.org
details/metadata surfaces flapped 503 to 200 inside one window; a 503 is a retry,
never a door verdict. (3) GATED: vol 2 renders a 200 details shell while its text
download returns a standing 401 under the access-restricted lending gate; a
details-page 200 is transport success, not text access, which is exactly the
ok:true-equals-landed class. Tightened falsifier: vol 2's djvu.txt reading 200
unauthenticated collapses the gate class; vol 1's djvu.txt going 401 makes the
whole shelf gated; details 503 while downloads read 200 confirms the two surfaces
flap independently and probes must hit the download URL, not the page. Move
(~20 min): the kit manifest encodes the three classes with three probe commands
(OPEN probes the djvu.txt directly; MOMENT-OUTAGE retries with backoff; GATED
routes vol 2 to operator-gated rather than fetchable-tonight). The erratum edits
no finding above F2; F1, F3, F4, F5 stand as filed. Gate re-run after this edit:
CITATION-LINT ok, blocking=0 (result recorded below), zero U+2014 characters.
