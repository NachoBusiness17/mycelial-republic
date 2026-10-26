# BREAK-ACCURACY: hostile second pass on the accuracy lens report, Track 5 gauntlet

- Seat: break-accuracy (the lens-breaker). Moment: 2026-10-07, one sitting,
  after the accuracy lens banked watch/inbox/ractor_engine/2026-10-07-track5-rewrite/accuracy.md.
- Job: byte-check every evidence cite in the accuracy lens report against
  the estate and the live web, verdict each finding, bank what the lens
  missed. I never edit files; this receipt is my only write.
- Target file: the lens report as carried in the ask JSON and banked at
  watch/inbox/ractor_engine/2026-10-07-track5-rewrite/accuracy.md (122
  lines). NOTE: the ask JSON arrived TRUNCATED (finding 5's falsifier cut
  mid-word and its move field absent); verdicts below were completed
  against the banked accuracy.md:77-83, which carries both in full.

## WHAT I RAN THIS SITTING (instrument + moment, per the quantifier law)

1. Exact re-run of the lens's sweep: `rg -l -i --no-ignore --hidden
   --glob "!.git" "half a step sharp|what the file keeps|island keeps its
   names|shadow with a tongue" .` from the repo root. Output: NINE
   fragment-bearing files, not the lens's two: the lens's two
   (watch/inbox/LENS_READING_TRACK5_20261007.md,
   memory/trajectory/steps.jsonl) PLUS all seven sibling banks in
   watch/inbox/ractor_engine/2026-10-07-track5-rewrite/ (accuracy.md,
   communication.md, economics.md, lineage.md, logic.md, moonshot-1.md,
   moonshot-2.md). The same run logged 4,632 error lines (rg access
   denials and device-name failures), see ADD-2.
2. Fragment census: `rg -o -i` over the nine files, sorted: 23 hits total;
   accuracy.md itself carries "half a step sharp", "what the file keeps",
   "island keeps its names" once each; no file carries a full v1/v2
   lyric. LENS_READING:73-74 wraps "the island / keeps its names" across
   two lines, which is why single-line rg only sees the second half.
3. Bank directory census: `ls -la watch/inbox/ractor_engine/2026-10-07-track5-rewrite/`
   shows seven lens banks, NO v1/v2 lyric file; the lens's finding-1 move
   (bank v1 and v2 verbatim) is UNEXECUTED as of this check.
4. Skipped-surface probe: the 4,632 rg error lines name a wider skipped
   surface than the lens disclosed: 20 `.pytest-*` root dirs, `./nul`
   (os error 1), a dozen-plus `agents/pytest-*` dirs (os error 5),
   `.mimosa/hook-state/*.baseline` paths (os error 3), and
   `corpus/library/ai-engineering-from-scratch/nul` (os error 1). Probe
   results: `./nul` read clean: 3,420 bytes of ping 127.0.0.1 output,
   zero fragment hits (grep count 0). The `.pytest-*` dirs deny reads to
   me too (`ls -R .pytest-arrival-repaired` = Permission denied; `find
   .pytest-* -type f | wc -l` = 0 readable). Blind surface persists.
5. Git history probe: `git log --all --oneline -S "half a step sharp" --
   watch/ memory/ state/ queue/ docs/` returned exactly one commit
   (75c3b7369, the LENS_READING bank itself) then ABORTED: `E:
   unsupported filetype .../CIA_HITLER_ADOLF_0003.pdf / fatal: unable to
   read files to diff`. The PDF is tracked at
   watch/inbox/gala_20260925/hitler-dig/lanes/sources/CIA_HITLER_ADOLF_0003.pdf
   (git ls-files hit), inside the pathspec. History absence is therefore
   UNPROVEN, not proven-absent: the pickaxe dies mid-traversal on this
   tree.
6. Citation lint on the lens's own records:
   `.venv/Scripts/python.exe tools/citation_lint.py check --files
   accuracy.md LENS_READING NACHO` = `ok records=3 anchors=1
   numbers-checked=0 blocking=0 warns=1`, the one warn being
   accuracy.md:61 TOKEN-MISS (word "carries" appears in none of cited
   NACHO :112's lines; the line says "came forward"). The lens's
   "kept lint-clean by hand" claim (accuracy.md:117-121) holds at the
   blocking level.
7. Web re-anchor via the web-reader lane (the lane the lens itself used;
   my four direct WebFetch attempts to Wikipedia and justice.gov all
   timed out at 60s, reproducing the lens's failure mode; the guessed
   DOJ URL
   https://www.justice.gov/usao-sdny/pr/ghislaine-maxwell-convicted-sex-trafficking-crimes
   returns Page not found, the page noting prior-administration releases
   moved to an Archive section):
   - https://en.wikipedia.org/wiki/Ghislaine_Maxwell fetched live,
     byte-matches the lens verbatim: convicted 2021-12-29 on "five sex
     trafficking-related counts" = "one of sex trafficking of a minor
     (maximum: 40 years), one of transporting a minor with the intent to
     engage in criminal sexual activity (10 years) and three of
     conspiracy to commit choate felonies (15 years total)", "acquitted
     on the charge of enticing a minor to travel"; sentencing quote "by
     and with Jeffrey Epstein" verbatim; habeas section: December 2025
     petition, "four unindicted co-conspirators" and "secret settlements
     with twenty-five men", unsealed June 2026, BBC denial ref dated 25
     August 2026, SCOTUS declined cert 6 October 2025.
   - https://en.wikipedia.org/wiki/Jean-Luc_Brunel fetched live,
     byte-matches: Guardian ref (Lucy Osborne, 28 May 2022, "six women
     on being abused by fashion agent Jean-Luc Brunel"); Le Monde 12
     March 2026, "eleven women had accused Brunel of sexual assault",
     ten rape per the prosecutors' interviews; died 19 February 2022,
     La Sante prison, suicide concluded March 2023.
   - https://en.wikipedia.org/wiki/Robert_Maxwell fetched live:
     infobox "Died 5 November 1991, Atlantic Ocean near the Canary
     Islands"; inquest December 1991, "death by a heart attack combined
     with accidental drowning, although three pathologists had been
     unable to agree"; the title "Gideon's Spies" appears NOWHERE on the
     page; the Gordon Thomas citations are ref 68 = Thomas, Gordon
     (2003), Robert Maxwell, Israel's Superspy (Hachette), bibliography
     = Thomas;Dillon 2002 (Carroll and Graf) AND Thomas;Dillon 2003
     (Robson, "The Assassination of Robert Maxwell, Israel's Superspy"),
     PLUS an unresolved short cite "Thomas (1999), p. 210" (ref 79) that
     the lens did not mention.
8. Estate prior-art sweep:
   `rg -l -i --no-ignore --hidden --glob "!.git" "gideon.{0,2}s spies|israel.s superspy|gordon thomas" watch corpus docs memory state`
   hits ONLY the five sibling gauntlet banks (moonshot-2, logic,
   economics, communication, accuracy). No pre-existing estate receipt
   carries any Gordon Thomas address; the ask's spine row is the only
   in-estate carrier.

## VERDICTS

- finding-1 (v1/v2 lyrics not byte-present on the estate): CONFIRMED.
  The falsifier (a full lyric file surfacing) has not fired: my re-run
  of the exact instrument returns nine fragment-quoting files, none a
  v1/v2 lyric, and the bank dir holds no lyric file, so the move (bank
  v1/v2 verbatim, operator paste) is still owed before the argue round
  hardens. Three corrections ride along: (a) the evidence's "output:
  LENS_READING and steps.jsonl only" is stale within the gauntlet's own
  window, the seven sibling banks now carry the fragments too, so any
  receipt must stamp its census moment; (b) the ":44" line cite in the
  evidence is wrong, :44 carries the deer-mask line, the four fragments
  sit at LENS_READING :20, :29, :34, :73-74 (wrapped), :76; (c) the
  absence claim is working-tree-scoped only, see ADD-2 for the
  un-sweepable history.

- finding-2 ("five trafficking counts" fails precision): CONFIRMED, and
  now independently re-anchored by my own live fetch, not just the
  lens's: the composition (five of six, one the trafficking count
  itself, three conspiracy, one transportation, acquitted on
  enticement) byte-matches the live Ghislaine Maxwell page. The brief's
  spine row is byte-present in the ask text I received ("convicted
  December 2021 on five trafficking counts"). One correction to the
  move: the in-flight asks cannot be amended, so the composition
  phrasing lands in the merge-round receipt and the accuracy floor row
  (accuracy.md:26, :87), not in the dispatched asks.

- finding-3 ("six models" is a floor, not a total): CONFIRMED,
  re-anchored. NACHO_VEIN_ARCHAEOLOGY_20261007.md:112 carries the
  six-models row byte-exact ("six models came forward against Epstein
  associate Jean-Luc Brunel"). My own live Brunel fetch byte-matches
  the instrument pair: Guardian 2022-05-28 six women (Lucy Osborne),
  Paris case eleven sexual-assault accusers (Le Monde 2026-03-12), ten
  rape per prosecutors, death 2022-02-19, suicide concluded 2023-03.
  Both falsifiers (case file below six; Guardian retraction) unfired.

- finding-4 ("the trial named no clients" needs its scope welded):
  CONFIRMED, re-anchored. My live Ghislaine fetch byte-matches every
  element: counts charged trafficking of minors to Epstein; sentencing
  wording "by and with Jeffrey Epstein" quoted verbatim; the December
  2025 habeas petition (public June 2026) alleging four unindicted
  co-conspirators and secret settlements with twenty-five men; denial
  ref dated 2026-08-25 (BBC); SCOTUS cert declined 2025-10-06. The
  scoped line "the verdict named no one but Epstein" is safe to stand
  on; "no clients existed" is not. The lens's two-clause weld into the
  merge receipt is the right move.

- finding-5 (Gordon Thomas citation real but mis-addressed): CONFIRMED
  as flagged, WITH a completeness correction. My live Robert Maxwell
  fetch confirms the title "Gideon's Spies" appears nowhere and the
  main spy-allegation cite is Israel's Superspy; the lens correctly
  reported the book-contents check as NOT RUN and it is still not run
  by me (OWED). The correction: the lens said "the article's Gordon
  Thomas citation is Israel's Superspy (2003), no Gideon's Spies
  mention" and missed that the article carries (a) a SECOND Thomas-Dillon
  edition (2003 Robson, "The Assassination of Robert Maxwell, Israel's
  Superspy") alongside the 2002 Carroll and Graf printing, and (b) an
  unresolved short cite "Thomas (1999), p. 210" at ref 79, the only
  plausible hook for the brief's Gideons-Spies address since Gideon's
  Spies is Thomas's 1999 book. The citation-address question is more
  recoverable than the lens's account implies. See ADD-3.

- blindspot-1 (spine stands on Wikipedia, primaries unfetched):
  CONFIRMED, and reproduced: my four WebFetch attempts timed out
  exactly as the lens's did, and my DOJ guess URL 404s (archive moved).
  Partial cure this sitting: the web-reader lane re-anchored all three
  Wikipedia pages independently; the DOJ primary and the Guardian/Le
  Monde originals remain unfetched (NOT RUN, still OWED before the
  liner receipt publishes).

- blindspot-2 (Gideon's Spies contents not verified): CONFIRMED.
  Accurately scoped as not run by the lens; still not run by me. My
  estate sweep (WHAT I RAN item 8) found no prior estate receipt to
  borrow an address from.

- blindspot-3 (v1/v2 lyrics never read): CONFIRMED. Still true; the
  bank move is unexecuted (WHAT I RAN item 3).

- blindspot-4 (rg skipped dirs on access errors): WEAKENED as stated,
  meaning the admission is real but materially UNDERSTATES its own
  scope: the lens named ".pytest-* and nul-protected directories"; my
  identical rerun logged 4,632 error lines also covering
  agents/pytest-*, .mimosa hook-state baselines, and a second nul
  inside corpus/library/ai-engineering-from-scratch/. I probed what was
  readable: ./nul is a ping-output capture with zero fragment hits; the
  .pytest-* dirs deny reads to me as well. The blind surface persists
  and is wider than disclosed; the absence claim should carry the wider
  scope note.

- blindspot-5 (habeas docket is live, rulings are snapshots): CONFIRMED.
  Properly hedged. My fetch is itself a later snapshot, taken the same
  day, and matches the lens's on every dated element, so no motion was
  observed between the two snapshots.

## ADDITIONS (what the lens missed)

- ADD-1: The lens's own two-file hit list went stale inside the
  gauntlet's own window: at my rerun the four fragments live in nine
  files, the seven sibling banks included, accuracy.md itself quoting
  three. The v1/v2 absence survives, but "lines no one can re-read" is
  shrinking: the fragments are now multi-banked in the track5 dir.
  Falsifier: a receipt that restates "two hits only" without a moment
  stamp. Move: every receipt from this gauntlet stamps its census
  moment; 2 min.
- ADD-2: Git-history absence is unprovable with the pickaxe on this
  tree: scoped `git log --all -S` runs abort on
  watch/inbox/gala_20260925/hitler-dig/lanes/sources/CIA_HITLER_ADOLF_0003.pdf
  ("unsupported filetype", "unable to read files to diff"), so "not
  byte-present anywhere on the estate" is proven for the working tree
  only, never for history. Falsifier: a history sweep with the PDF's
  directory excluded that surfaces a lyric bank. Move: rerun the
  pickaxe with :(exclude)gala_20260925/hitler-dig or per-dir pathspecs;
  10 min.
- ADD-3: The Robert Maxwell article's unresolved "Thomas (1999), p. 210"
  cite (ref 79) plus the second 2003 Robson edition are the missing
  half of the citation-address finding: the brief's Gideons-Spies
  address maps plausibly onto the 1999 cite, so "dual-cite or swap"
  should read dual-cite Israel's Superspy (2002/2003) AND resolve
  Thomas-1999, not swap. Falsifier: Thomas (1999) resolves to a
  different title than Gideon's Spies. Move: one fetch resolving the
  ref-79 short cite, then weld the full citation set into the liner
  receipt; 10 min.
- ADD-4: The operator's own source file already tri-states the exact
  rows findings 3 and 4 amend: NACHO_VEIN_ARCHAEOLOGY_20261007.md:111
  marks the cult/Mystery-Babylon thesis ELABORATED-performed and
  Bretton Woods DOCUMENTED-datable, and :112 marks "Brunel accusations
  = on-record; the wider tie-in = INTERPRETIVE" with "the DOCUMENTED
  spine available to the Tiller voice". The merge round can cite these
  as the in-estate label anchors; the scoping is not lens-imposed, it
  is the operator's own grammar. Falsifier: a merge receipt that
  treats the labels as foreign additions. Move: weld NACHO :111-112
  into the receipt next to the two scoping clauses; 5 min.
- ADD-5: Citation lint run on the lens's own three records: blocking=0,
  warns=1 (accuracy.md:61 TOKEN-MISS, "carries" vs the cited line's
  "came forward"). The "kept lint-clean by hand" claim holds at the
  blocking level. Move: none, warn-only; 0 min.
- ADD-6: The ask's "14 rows" figure for the NACHO file is a derived
  count, not byte-present: the file header says "12 posts"
  (NACHO:1), the doctrine table body holds 11 rows (NACHO:14-24), and
  two appended rows self-label "vein row 13" and "vein row 14"
  (NACHO:111-112). Receipts citing "the 14-row table" should say "12
  posts, rows numbered to 14". Falsifier: a byte-present "14" in the
  file. Move: one-line wording fix in the receipt; 2 min.

## STANDING OWED (unchanged by this pass)

- Primary-document re-anchor (DOJ release or SDNY verdict sheet,
  Guardian 2022-05-28, Le Monde 2026-03-12): NOT RUN this sitting by
  either seat; WebFetch times out and the DOJ guessed URL 404s. The
  web-reader lane reaches Wikipedia but was not tried against the
  primaries' own URLs here beyond the DOJ 404.
- Gideon's Spies contents check: NOT RUN by either seat.
- v1/v2 verbatim bank: NOT EXECUTED; directory shows no lyric file.
- .pytest-* unreadable dirs: NOT READABLE from this seat (permission
  denied); the absence claim stays scoped to the readable tree.
