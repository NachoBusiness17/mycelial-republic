# PA-D2-grok47 (grok-4.7 @ xai, turn 1, channel: content)

# Adjudication: Doctrine Roast, Movement 2

## Conditions of this read

- Instrument. This session's pasted evidence only: `00__MOVEMENT2_CHEAP_ANSWERS.md` (movement 2 answers plus the movement 3 report in the same file), `01__D1_doctrine_roast_movement1.md` (truncated), `02__workflow_gate.py` (truncated), `03__REGISTRY.jsonl` (truncated). No commands run. No files opened on disk.
- Moment. Single pass, this session. Cheap-arm moments are the ones those reports name, not this pass.
- Context assumption. Quoted spans below are the bytes in the paste. Truncation markers mean the middle was not shown. A line number I did not count through an intact file is UNVERIFIED.
- What I will not do. I will not treat a cheap-arm sentence as a file citation. Reports are leads. Claims about code need a quoted span or the mark UNVERIFIED.

---

## (1) EXIT SEMANTICS: L1 amends. The hard-block reading dies.

D1's L1, as its own falsifier states it, was a contradiction claim: that `logic.md` and the gate disagree on which exit blocks, and that exit 1 might be the hard block. The falsifier said L1 drops to wording if the file documents exit 1 as warn and exit 2 as the undecidable-with-evidence block.

What the paste actually shows:

- Docstring, counted from the shebang in `02__workflow_gate.py:10`: "exit 2 is the only hard block; every submission registers a row". That sentence is byte-true. The cheap-arm quote matches this line.
- Same file, tail of `main`, line number UNVERIFIED (truncation): `return 1` after `GATE ERROR: cannot read script`. Then `if args.no_register: return 2 if failed else 0`. Then `if failed: ... return 2` and `return 0`. Then `sys.exit(main())`.
- Literal `sys.exit(1)` : not in the visible bytes. The cheap-arm's "zero `sys.exit(1)` sites" is consistent with what is shown. It does not mean exit status 1 is unreachable. `sys.exit(main())` propagates `return 1`.

Verdict. The claim "exit 1 is a hard block on a push" dies. The claim "exit 2 is the only hard block" survives at `workflow_gate.py:10` and at the visible `return 2` on `failed`. L1 does not fully die, because the docstring in the visible lines never names exit 1 as "warn" or "undecidable". The only visible `return 1` is a read error, not a check warn. Movement 3's pin "returns 1 (soft, lines 216/298), 2 (block, 269/313), 0 (pass, 271)" is UNVERIFIED here: those lines sit in the truncated middle.

- Positive (holds). A FAIL check path in the visible tail returns 2, matching the docstring's only hard block.
- Negative (does not hold). "Exit 1 never occurs" is false on the visible `return 1`. "Exit 1 is documented as warn" is not in the visible docstring, so D1's falsifier condition for a clean death is not met.

Amended L1. Exit 2 is the only check-failure block in the bytes shown. Exit 1 is a real status (read error at minimum) and is unnamed in the visible contract prose. That is a wording gap, not a second hard block.

---

## (2) REGISTRY ORDER: A4/O7 holds as moment-indexed census arithmetic. Row pins UNVERIFIED in this paste.

D1 A4 said accuracy.md's "45 rows" and operations.md's "40 rows" cannot both be true of one append-only file at one moment, and that 45-then-40 is impossible.

Cheap-arm report (not a file quote): 45 rows total; row 40 `ts` `2026-09-30T01:18:10Z` (frontier-olm-mine); rows 41-45 all `2026-10-01`. I cannot see row 40 or a 45-row count in `03__REGISTRY.jsonl`. The paste is head plus tail. Those two timestamps and the integer 45 are UNVERIFIED against this paste.

What the paste does show: the file is JSONL with `ts` fields, earliest visible `2026-09-25T18:52:02Z`, and the tail contains `2026-10-02T01:52:01Z` and `2026-10-02T01:52:29Z` (`ractor-engine.dwf.ts`). Those October 2 rows are later than the cheap-arm's "rows 41-45 are all 2026-10-01". So if this paste is the same append-only file at a later moment, "45" was already stale when this evidence block was cut. That does not break append-only arithmetic. It is another moment.

Verdict. The reconciliation holds as census-law arithmetic under these conditions: the file is append-only; "40" and "45" are counts at two different read moments; neither chapter stated its moment. It does not hold as a claim that the file still has 45 rows. This paste's tail is evidence the count moved again, to at least the October 2 rows, exact N UNVERIFIED.

- Positive. 40 at an earlier moment, 45 at a later moment, then more rows on 2026-10-02, is the only order consistent with append-only.
- Negative. Reading both chapters as a census of one instant is still a defect (D1 A4's moment-law point). The cheap arm settled the contradiction, not the missing timestamps in the chapters.

Uncertainty. If row 40's real `ts` is after the rows the cheap arm called 41-45, this verdict flips. I have not seen those lines.

---

## (3) UF-124: objection 1 stays OPEN. Movement 3's "CONFIRMED" does not close it, and inverts D1's falsifier.

Movement 2: premise paths not found; zero UF-124 hits in the sweep it ran; objection 1 OPEN. That is the state this contract asked me to adjudicate, and it is the state this paste supports.

Movement 3, same evidence file, reports the files exist at `watch/inbox/burn_wave_20260926/` and `watch/inbox/union_fullsend_20260917/`, and reports the answer carried `openreview.net/forum?id=XYZ` plus "Constitutional AI - OpenAI". Those strings are not in any premise-file paste here. UNVERIFIED. A report that files exist is not the bytes.

Logic check, independent of that report. D1's own falsifier: if the cited id resolves to real fetched bytes, objection 1 is confirmed (an id-only gate would pass a misattributed real paper). If the id does not resolve, objection 1 weakens to a hypothetical. A literal `id=XYZ` would fail an existence check. Movement 3's sentence "OBJECTION 1 CONFIRMED: the gate would have caught it" is the weakening branch, not the confirmation branch. I do not adopt it.

What closes objection 1 (all three, from the files, not from a report):

1. Quoted line from `DAY_PACK.md` (whatever path `grep -n` resolves) showing the UF-124 answer's citation span: the id or URL, verbatim.
2. Quoted line from `B2_16_uf_sweep_20260926.md` showing the misattribution span (who it names versus who the paper is).
3. A same-session fetch receipt: either the id returns real bytes (author and effect-size span quoted), or the fetch fails / the id is a placeholder. Resolve means confirm. Non-resolve means the in-chapter instance of objection 1 dies, and the objection survives only as a hypothetical about a different, real-id misattribution.

Until those three quotes are in the paste, objection 1 is OPEN, not confirmed, not refuted.

---

## (4) ONE landable amendment (due from movement 1)

Chapter: `accuracy.md`. Replace the first sentence of §Incident 1 "Instrument upgrade", and align the "(2)" clause of §Decision ledger so it cannot say the contract already changed.

Paste-able sentence:

> A row carrying an external citation or a tool-behavior claim lands LANDED only when the same session's receipt quotes, from fetched bytes or captured command output, the span carrying the specific claimed value (author attribution, effect size, default behavior); an id that resolves without that span lands UNVERIFIED, and until a resolver enforcing this exists in tracked code this rule is PROPOSED, not a changed contract.

Why this one, not a logic.md exit patch. Exit semantics amended in place as a verdict (section 1). The accuracy landing-contract sentence is the movement 1 amendment that is still owed, and UF-124 did not retire it. It stays PROPOSED until tracked code enforces it. That last clause is what stops the chapter from banking a 13th "ok:true-equals-landed" on itself.

- Passes. Receipt quotes the span that carries the claimed author or the claimed default, next to the claim.
- Fails, lands UNVERIFIED. An id fetches a real page, and no quoted span shows the claimed authors or the claimed effect size.

---

## (5) Next 3 dig tickets

Commands only. Zero opinion in the ticket.

1. Exit sites, exact. `grep -n "sys.exit\|return 0\|return 1\|return 2" tools/workflow_gate.py`. Question: which line numbers return 1, and is each a read-error, a soft warn, or a check FAIL? Settles the UNVERIFIED movement 3 pins (216/298/269/313/271) against section 1.
2. Census at one named moment. `wc -l memory/workflows/REGISTRY.jsonl` then `sed -n '40p;45p;$p' memory/workflows/REGISTRY.jsonl` and print only `ts` and `name`. Question: what are row 40, row 45, and the last row at the moment of the command? Settles whether "45" and the 2026-10-02 tail are the same file at different moments.
3. UF-124 bytes. `grep -n "UF-124\|openreview\|Constitutional" watch/inbox/union_fullsend_20260917/DAY_PACK.md watch/inbox/burn_wave_20260926/B2_16_uf_sweep_20260926.md`. Question: what is the verbatim citation id, and what author string does the sweep line use? If either path errors, `rg -l "UF-124" watch/inbox` and quote the matching line. This is the close condition in section 3.

---

## Falsifier for this deliverable

This adjudication is wrong if any of the following is shown from the files, not from a report:

- Exit. `grep -n` shows a check-FAIL path returning 1, or the docstring at line 10 does not contain "exit 2 is the only hard block". Then amended L1 dies and the hard-block objection returns.
- Census. Row 40's `ts` is later than the rows counted as 41-45 in the same file with no rewrite. Then append-only reconciliation fails.
- UF-124. The quoted answer cites a resolving id, and the fetched bytes do not contain the claimed author or effect size. Then objection 1 confirms, and movement 2's OPEN status was only a missed path.
- Amendment. A tracked resolver already enforces the paste-able sentence. Then labeling it PROPOSED is false.
