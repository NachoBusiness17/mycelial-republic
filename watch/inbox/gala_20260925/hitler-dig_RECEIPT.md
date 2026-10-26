# hitler-dig run receipt

Compiled 2026-10-03 by the run-receipt seat from the run's script-written gate sections, which are authoritative for every number, plus the run's fold, review, and filing outputs. Gate verdict: **GATE PASS**. Receipt path: `watch/inbox/gala_20260925/hitler-dig_RECEIPT.md`. Checks executed by this seat are named inline with their commands; anything not re-executed here is attributed to the run stage that produced it.

## Gate sections (verbatim, authoritative)

```
== SECTIONS BEGIN (script-written numbers, authoritative) ==
lanes_json_count: 3 (expected 3)
lanes_parsed_ok: 3/3
by_division: {"B": 2, "A": 1}
byte_checks_cited: 11  mined_rows: 7
decisions_changed: 3
  changed: hitler-ancestry.json: Closes the operator's Hitler-Rothschild ancestry question with tri-state verdicts: Alois paternity u
  changed: numerology-6-7.json: closes the operator's 6-7 recurrence question: measured noise with the mechanism named (birthday-par
  changed: synthesis.json: The hitler-dig close gate: the genealogy lane's sources/CIA_HITLER_ADOLF_0003.pdf is rejected as an 
ballroom_count (danced/refired/buried): 3/0/0
== SECTIONS END ==
GATE PASS
```

## Header

- Slug: hitler-dig
- Lane count: 3 lane JSONs on disk against 3 expected, parsed ok 3/3
- Divisions: B 2 (numerology-6-7, hitler-ancestry), A 1 (synthesis)
- Ballroom: 3 danced, 0 refired, 0 buried; all three lanes ok:true

## Scoreboard

| metric | value | source |
|---|---|---|
| lanes_json_count | 3 (expected 3) | gate sections |
| lanes_parsed_ok | 3/3 | gate sections |
| by_division | B 2, A 1 | gate sections |
| byte_checks_cited | 11 | gate sections |
| mined_rows | 7 | gate sections |
| decisions_changed | 3 | gate sections |
| ballroom (danced/refired/buried) | 3/0/0 | gate sections |

Cross-foot executed by this seat (2026-10-03):

- `ls -la watch/inbox/gala_20260925/hitler-dig/lanes`: exactly three lane JSONs on disk (numerology-6-7.json, hitler-ancestry.json, synthesis.json) alongside the check evidence files and sources/; lanes_json_count 3 confirmed.
- All three lane JSONs read in full this seat; each parses and carries ok:true plus a division field: `watch/inbox/gala_20260925/hitler-dig/lanes/numerology-6-7.json:3` and `watch/inbox/gala_20260925/hitler-dig/lanes/hitler-ancestry.json:3` both read "B", and `watch/inbox/gala_20260925/hitler-dig/lanes/synthesis.json:3` reads "A", confirming by_division B 2 / A 1 from current bytes.
- byte_checks_cited 11 cross-foots from the checks arrays: 2 at `watch/inbox/gala_20260925/hitler-dig/lanes/numerology-6-7.json:17-28`, 2 at `watch/inbox/gala_20260925/hitler-dig/lanes/hitler-ancestry.json:26-36`, and 7 at `watch/inbox/gala_20260925/hitler-dig/lanes/synthesis.json:53-88`, summing to 11. Every check names an evidence file, and the five cited evidence files exist in the lanes dir listing (numerology-6-7.check.txt, numerology-6-7.audit.out.txt, hitler-ancestry.check.txt, synthesis.check.txt, synthesis.check.numerology_rerun.txt).
- mined_rows 7 cross-foots from the rows arrays: 0 (numerology-6-7.json carries no rows key) + 2 at `watch/inbox/gala_20260925/hitler-dig/lanes/hitler-ancestry.json:6-25` + 5 at `watch/inbox/gala_20260925/hitler-dig/lanes/synthesis.json:6-52`, summing to 7.
- decisions_changed 3: the field is present at `watch/inbox/gala_20260925/hitler-dig/lanes/numerology-6-7.json:30`, `watch/inbox/gala_20260925/hitler-dig/lanes/hitler-ancestry.json:38`, and `watch/inbox/gala_20260925/hitler-dig/lanes/synthesis.json:90`, and the gate's truncated changed-lines agree with the lane bytes at each cut point.

One fold-side claim did not reproduce and is recorded as an erratum: the fold scoreboard's parenthetical said hitler-ancestry.json "carries no division field", but current bytes at `watch/inbox/gala_20260925/hitler-dig/lanes/hitler-ancestry.json:3` carry "division": "B". The gate's by_division B 2 / A 1 stands on the gate numbers and the current bytes either way.

## Decision ledger (no PARADE; the fold's parade flag is false)

Three decisions changed, full text as carried by the fold (the gate's changed-lines are truncations and agree at each cut point):

1. `watch/inbox/gala_20260925/hitler-dig/lanes/numerology-6-7.json:30` - closes the operator's 6-7 recurrence question: measured noise, mechanism fully named (birthday-paradox arithmetic over ~400 published count surfaces + the 2025-26 '6-7' meme priming via Dictionary.com Word of the Year + apophenia); no estate mechanism changes; future number-pattern claims now have a concrete bar: terminal-digit baseline plus significance, not vibes.
2. `watch/inbox/gala_20260925/hitler-dig/lanes/hitler-ancestry.json:38` - Closes the operator's Hitler-Rothschild ancestry question with tri-state verdicts: Alois paternity unknown CONFIRMED, Frankenberger hypothesis REFUTED, Rothschild genealogical link REFUTED, CIA file existence CONFIRMED (contents hearsay, never corroborated), Argentina escape REFUTED on the forensic dental record, documented Hitler-Rothschild relationship CONFIRMED as Nazi confiscation for ransom; estate conspiracy corpora reclassified as rumor-provenance-only, evidence-free on this topic.
3. `watch/inbox/gala_20260925/hitler-dig/lanes/synthesis.json:90` - The hitler-dig close gate: the genealogy lane's sources/CIA_HITLER_ADOLF_0003.pdf is rejected as an unread primary source (byte check: FOIA reading-room HTML shell, zero Hitler mentions) and both lanes' receipts must pass tools/citation_lint.py check --files plus a type check on every fetched source before the dig can close; until the CIA document is refetched and byte-typed, the genealogy claim lands UNVERIFIED. Named here because no fold gate or receipt exists for this dig yet.

Wording note by this seat: items 2 and 3 match the lane bytes as read this seat. Item 1 is the fold's composition: the lane's own decision_changed at `watch/inbox/gala_20260925/hitler-dig/lanes/numerology-6-7.json:30` reads "measured noise with the mechanism named (... + 2025-26 meme priming + apophenia) ... bar set for future number-pattern claims", and the Dictionary.com Word of the Year 2025 detail the fold folds in lives in the lane's verdict_detail at `watch/inbox/gala_20260925/hitler-dig/lanes/numerology-6-7.json:13`. Same decision, same substance; both texts recorded.

Fold top laws (the dig's standing yield, carried to the estate):

1. **verdicts-carry-their-conditions** - A verdict without its conditions is not a verdict: generalizes the B2-216 count-moment law from counts to every instrument, and it demoed live in this dig, the sibling audit's deterministic stats reproduced exactly while its prose-pair count moved 70 to 90 with the moving tree (the synthesis lane's rows[0] + note). Umbrella law for stamping instrument + exit code + moment on every future verdict.
2. **apophenia-until-the-grammar-does-work** - Retrospective fit is apophenia until the pattern does discriminating work: the fleet's own bench refused its proudest map on fit alone, pre-registered two tests with falsifiers, and the frozen same-day transfer test flipped C1 to SUPPORTED under mag/grammar_transfer.py with an amendment ledger disclosing 4 pre-verdict corrections (the synthesis lane's rows[1]). The honest-bridge procedure: pre-register, freeze, run the same day.
3. **memory-written-citations** - Historical and doctrine claims fail when written from memory of the source rather than the source, and the wrong citation still 'works' on read because nothing resolves it; it fired live in this dig, the genealogy lane's primary source is literally the CIA FOIA reading-room HTML shell (38382 bytes, zero Hitler mentions), now a physical worked example sitting in lanes/sources/ for the f-25 check and byte-typing every fetched artifact (the synthesis lane's rows[3] + check 5).

## Ballroom

Danced (3 of 3; ok:true per lane JSONs; the run metadata's danced array agrees lane for lane):

- **numerology-6-7** (division B, 0 rows): closes the operator's 6-7 recurrence question as measured noise with the mechanism named; the lane's own numbers: census 4 of 14 ending in 6 or 7 = 28.6 pct vs 20 pct uniform, binomial p = 0.3018 not significant (`watch/inbox/gala_20260925/hitler-dig/lanes/numerology-6-7.json:14`); terminal digits 6 and 7 are the 3rd and 4th rarest of 379 structured ints, and the literal 6-7 prose pair at 70 is beaten by 7-7 at 182 and 5-5 at 160.
- **hitler-ancestry** (division B, 2 rows): tri-state verdicts close the Hitler-Rothschild ancestry question; estate conspiracy corpora reclassified rumor-provenance-only, evidence-free on this topic.
- **synthesis** (division A, 5 rows): the dig close gate; the CIA artifact rejected as an unread primary source; the genealogy claim UNVERIFIED until the CIA document is refetched and byte-typed.

Refired: none.
Buried: none.

## Review verdict: ACCEPT

The review seat's verdict, by finding (claims the review verified itself are marked "per review"; claims re-verified under this seat's own commands are marked):

- **QUOTES**: 7 spot-checked (the ask named 3), all resolve. The qdrop quote (hitler-ancestry row 1) is a text-field exact match at watch/inbox/qdrop_export/qdrops.jsonl line 161 with drop_no verified 161 (re-verified this seat: the row carries "Trace the bloodlines" and 'drop_no": 161'). `watch/inbox/gala_20260925/ouroboros_RECEIPT.md:38` and `watch/inbox/ractor50/accuracy.md:81` byte-exact as claimed, T0-exact (re-verified this seat by grep: the 1,457 line and the memory-written-citations class line sit at exactly those lines). The "A VERDICT WITHOUT ITS CONDITIONS IS NOT A VERDICT" line in `memory/rib/RIB_DRIVING_LADDER_20260928.md` and "the grammar is poetry" in `memory/runs/salons/unified_fold_20260906/SALON_ARTIFACT.md` match whitespace-normalized as claimed, T1-wsnorm (re-verified this seat: the RIB phrase only matches after whitespace normalization, it is line-wrapped in the raw file). "Hitler Gets Rippled" is the exact title on id 6bs41m (per review). One drift found: numerology.md cites the Hall cube quote at lines 9553-9554 but the cube phrase byte-sits at `memory/corpus/ractors/hall_mp/texts/secret_teachings_of_all_ages.txt:9551` (re-verified this seat by grep), a real quote with an imprecise line pointer inside the receipt's own broader range `memory/corpus/ractors/hall_mp/texts/secret_teachings_of_all_ages.txt:9516-9561`; `mathers_ku.txt:6605-6606` checks out, the phrase "the seven / duplex letters, BGDKPRTh" spans the two lines starting at the cited line (re-verified this seat).
- **CHECK.TXT BACKING**: all 11 claimed checks across the three lane JSONs resolve to on-disk evidence files (synthesis.check.txt, whose claimed contents the review read: the head-receipt ls rc=2 step at the top, the estate grep block, the quote bytecheck block showing 5 PASS, the citation lint selftest block, and the PDF type step; synthesis.check.numerology_rerun.txt; hitler-ancestry.check.txt with EXIT_CODE=0; numerology-6-7.check.txt; numerology-6-7.audit.out.txt). Caveat carried: hitler-ancestry.check.txt's LANE_JSON_PARSE ran 12:05:59Z against a draft of 2690 bytes; the final lane JSON (4520 bytes on disk, re-verified this seat by ls) was written at 08:06 local. The reviewer re-ran the parse on the final file and it is valid, so the claim holds while the archived output covers a pre-final draft.
- **DECISION LEDGER HONEST**: all three decision_changed fields name verifiable things and the load-bearing ones verified under the reviewer's own commands: the CIA "PDF" is the FOIA HTML shell (first bytes "<!DOCTYPE html P", no %PDF- header, zero case-insensitive "hitler" occurrences in 38382 bytes; re-verified this seat by python byte read); both receipts exist at exactly the claimed byte counts (ancestry.md 15700 bytes, numerology.md 11712 bytes; re-verified this seat by ls and sha256, hashes below); numerology.md sha256 23e0a909... reproduced exactly. The synthesis lane discloses its own gaps rather than papering over them (watch/inbox/hitler_dig/synthesis.md absent, no dig-level fold gate), and the fold metadata at lanes/_byproducts/synthesis.checks.json (exists on disk, re-verified this seat by ls) is honest against its own lane per the review, striking 2 of 5 quote-claims as "supports: no" with real reasons.
- **B-DIVISION FINISH LINES MET ON DISK** (per review): ancestry.md present at 15700 bytes with zero em or en dashes, tri-state markers CONFIRMED / REFUTED / UNVERIFIABLE at 5 / 6 / 1 per the archived finish-line check (exit 0), with the six verdicts and disclosed limits (primary PDF not read; Charlier 403) carried in the prose; numerology.md present at 11712 bytes with matching sha256, and its headline numbers (census 4 of 14 = 28.6 pct, chi-square 41.66 on df 9, P = 1.0000) reproduce in `watch/inbox/gala_20260925/hitler-dig/lanes/numerology-6-7.audit.out.txt` (re-verified this seat by grep: 28.6 at line 7, 41.66 at line 35, 1.0000 at lines 39-40).
- **NO CROSS-LANE CLAIMS** (per review): synthesis attributes the numerology instrument as a sibling instrument rerun and explicitly disclaims the genealogy lane's owed work ("the CIA document was not refetched (genealogy lane's owed work, out of this lane's scope)"); the ancestry and numerology lane JSONs contain zero mentions of sibling lanes; and the ancestry receipt independently discloses the same failed fetch synthesis flagged (38382 bytes saved to lanes/sources during the attempt; the primary PDF was not read that seat) - consistent attribution, not claim-jumping.

Review verdict line: **ACCEPT** (the single Hall line-pointer drift at 9551 vs 9553 is WARN-class; the quote itself is byte-real).

## Filing verdict: FILED

- **LINKS**: 3 rows appended to memory/corpus/LINKS.jsonl, ledger 271 to 274: GALA-hitler-dig-numerology-6-7 (division B, title six-seven-measured-noise-mechanism-named since its top law is null, load_bearing empty, decision verbatim), GALA-hitler-dig-hitler-ancestry (division B, title conspiracy-corpora-carry-no-evidence-weight, load_bearing 2 laws, decision verbatim), GALA-hitler-dig-synthesis (division A, title verdicts-carry-their-conditions, load_bearing 5 laws, decision verbatim); kind gala, src watch/inbox/gala_20260925/hitler-dig/lanes/&lt;id&gt;.json. Dedupe by src: pre-append grep for hitler-dig returned 0 under any field, re-checked at write time. Verification executed at filing: all 3 lane JSONs read in full; decision_changed fields copied programmatically from the lane JSONs and byte-compared post-append (3/3 exact); whole-ledger re-parse 274/274 OK; the 3 appended ids unique and the 3 srcs unique each exactly once; em and en dash scan on the appended block 0. Pre-existing oddity named and untouched: 10 LINKS-334..343 id pairs and 60 old-head rows with no src key (none from this filing).
- **STATE**: one entry appended to memories/session/next-window-handoff.md (493 to 495 lines, appended block em and en dash scan 0, prior entries untouched): slug hitler-dig, danced count 3 (all ok:true per lane JSONs; no fold_gate output exists in the hitler-dig dir, which holds only lanes/, so the count basis is the lane JSON ok flags, same rule as the ouroboros close), decisions changed 3, B-division finish 2/2 per lane JSON ok flags plus division A 1/1, graves filed 0 (grep -ril GALA_GRAVE over the hitler-dig dir and watch/inbox/hitler_dig/ returned no matches at 2026-10-03T12:42:36Z).
- **Receipts re-verified on disk by this seat** (ls sizes; sha256 via the repo venv's python hashlib over the raw bytes): `watch/inbox/hitler_dig/ancestry.md` is 15700 bytes, sha256 ee5c639272adf60859369e3e641277a35e3808e3030987bbb95dcb3cbdfc48a3; `watch/inbox/hitler_dig/numerology.md` is 11712 bytes, sha256 23e0a9098e724e4f82bea48af8f01e533b50890c91400460ac05d4712b95212f, matching the lane's claim at `watch/inbox/gala_20260925/hitler-dig/lanes/numerology-6-7.json:7`; both dash-free per the archived checks. `watch/inbox/hitler_dig/synthesis.md` does not exist (dir listing shows only ancestry.md and numerology.md). The fetched genealogy artifact `watch/inbox/gala_20260925/hitler-dig/lanes/sources/CIA_HITLER_ADOLF_0003.pdf` re-verified at 38382 bytes, first 16 bytes "<!DOCTYPE html P" (no %PDF- header), zero case-insensitive "hitler" occurrences, mtime 2026-10-03 07:55.
- **Honest status**: the dig is NOT closed. The genealogy claim stands UNVERIFIED per the synthesis lane's close gate: the CIA document has not been refetched and byte-typed. Owed work filed for the next window (per the synthesis lane's own gate): refetch and byte-type the CIA document, run tools/citation_lint.py check --files over both lane receipts, land the head receipt watch/inbox/hitler_dig/synthesis.md.

## Executed and not run by this seat

Executed here, 2026-10-03: `ls -la` of the lanes, lanes/sources, and hitler_dig dirs; full reads of the three lane JSONs; a python byte read computing sizes, first bytes, case-insensitive "hitler" counts, and sha256 for `watch/inbox/hitler_dig/ancestry.md`, `watch/inbox/hitler_dig/numerology.md`, and the CIA artifact; grep and sed verification of the qdrop row 161 text and drop_no, the ouroboros receipts line at `watch/inbox/gala_20260925/ouroboros_RECEIPT.md:38`, the accuracy class line at `watch/inbox/ractor50/accuracy.md:81`, the RIB verdict phrase (whitespace-normalized), the salon grammar line at `memory/runs/salons/unified_fold_20260906/SALON_ARTIFACT.md:14`, the cube phrase at `memory/corpus/ractors/hall_mp/texts/secret_teachings_of_all_ages.txt:9551`, and the duplex letters phrase spanning `mathers_ku.txt:6605-6606`; grep for the audit headline numbers in `watch/inbox/gala_20260925/hitler-dig/lanes/numerology-6-7.audit.out.txt`; an em and en dash scan of this receipt; and `tools/citation_lint.py check --files` on this receipt. Line counts: 29600 lines for the Hall source and 20766 lines for the mathers source, both far past every cited range.

Citation lint outcome on this receipt: PASS - `.venv/Scripts/python.exe tools/citation_lint.py check --files watch/inbox/gala_20260925/hitler-dig_RECEIPT.md` returned "CITATION-LINT: ok records=1 anchors=29 numbers-checked=2 blocking=0 warns=0 enforce-tokens=False"; the em and en dash scan of the final bytes returned 0 and 0.

Not run here: the violation ratchet and pytest (filing-only ask, zero code under mag/ or tools/ touched, same scope statement as the lane seats); the lane instruments were not re-run (the gate already returned GATE PASS and no check was named for this receipt); the review's remaining spot-checks not named above were not re-executed (attributed to the review seat's ACCEPT); no CIA refetch (owed work, next window).
