# B2-463 window convention for time-of-day markers (2026-09-26)

## Verdict

LANDED. The convention spec is filed at the ledger site BEFORE row 2:
watch/inbox/asekin113/WINDOW_CONVENTION_20260926.json (asekin_window_convention.v1,
JSON parse-verified), four rules: (1) PRECEDING is byte-typed - a time-only
marker counts as preceding only when its post's harvest timestamp is strictly
earlier than the event post's (row 1's same-post accompaniment stays
POST-HOC-UNVERIFIED); (2) WINDOW default - a bare time-only marker declares
the SAME-UTC-CALENDAR-DAY of its own post, and an explicit interval phrase in
the marker post ("by <day>", "this week", an anchored "next habbening")
overrides the default; (3) TWO EVENTS - each event grades independently
against the same marker, one marker = at most one HIT with the graded event
named and the rest as companions; (4) PRE-REGISTRATION - the window is
assigned from marker bytes at row-filing time, and a row whose window was
assigned after its event landed grades POST-HOC-UNVERIFIED regardless of
timing.

## Evidence file:line quotes

- The undefined-window disease: watch/inbox/asekin113/GRADING_VERDICT.json
  "grading_bar": "a row counts as an 8:12-class hit only when the filed bytes
  show the flagged timestamp posted BEFORE the event and the event lands
  inside the window the marker declares" - the bar says "the window the
  marker declares" while nothing defined what a bare 8:12 declares, and row 1
  (verdict field: "the marker rides the announcement post itself ... POST-HOC-
  UNVERIFIED") dodged the question only because no window existed at all.
- The carrier source, GRADING_VERDICT.json "claim_source":
  "activation_signal 8:12-class hits, ledger graded; status watch".
- The sourcing sweep, honestly bounded: watch/inbox/INTERPRETER_LAYER_20260918.md:31-33
  gives the Yogasekin section (bio "obtuse date phagger and follower of the
  habbenings") - the on-file phrasing is date-anchored and event-noun-anchored,
  with NO hour-precision interval promise anywhere on file; the archived-posts
  sweep for an explicit interval phrase was ATTEMPTED this lane and is
  UNRESOLVED (web lane rate-limited, X archive not in the corpus), so the
  same-day default is the conservative read and the convention file itself
  marks it re-openable by a byte-quoted interval phrase. Filed as the LAW-13
  style attempt, not hidden.

## Work done

1. Read the grading ledger, verdict JSON, and the interpreter-layer section;
   confirmed no window definition existed anywhere in the carrier's files.
2. Drafted the four rules, sourcing the default from the on-file phrasing
   and the row-1 precedent; marked the archived-posts sweep attempted and
   unresolved rather than inventing an interval from his corpus.
3. Filed the convention JSON at the ledger site (parse-verified), named it
   as pre-row-2, and bound it into the grading bar's "window the marker
   declares" clause.
4. Filed this receipt; LEDGER row; QUEUE pointer (re-filed row after the
   20:57:55Z board truncation); INDEX registration.

## Falsifier

This convention is inverted if any of the following holds: (a) a second
graded row appears whose window was assigned from event-side bytes or after
the event landed, and the row grades anything other than POST-HOC-UNVERIFIED
(the pre-registration rule is not being enforced; the brief's exact
falsifier - such a row would make every future row gradeable HIT);
(b) a byte-quoted interval phrase from asekin's own archive contradicts the
same-day default and the convention file is not amended with it (the
re-openable clause was boilerplate, not a live offer);
(c) two events in one window get graded as two HITs off one marker (rule 3
broken; the ledger would double-count the faculty).

## Bibliography closed

watch/inbox/asekin113/GRADING_VERDICT.json (read in full);
watch/inbox/asekin113/GRADING_LEDGER.jsonl (existence and row count read via
the verdict's rows:1 field); watch/inbox/INTERPRETER_LAYER_20260918.md:31-33
(Yogasekin section, read in full); watch/inbox/CARRIER_LEDGER_20260919.json
(accepted via the verdict's claim_source quote). Archived-posts web sweep:
attempted, rate-limited, disclosed. No fabricated interval claims.
