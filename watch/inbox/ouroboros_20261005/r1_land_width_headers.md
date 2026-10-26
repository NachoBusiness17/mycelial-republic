# R1 LAND: width-declaration headers + the olm-mine phantom strike (ourobolos 2026-10-05, R1 lane)

Filed by the R1-landing lane (the non-colliding half of fold row 5 + row 8 +
row 9's operator queue). Fold:
watch/inbox/ractor_engine/2026-10-05-ouroboros-r1-fleet/SYNTHESIS.md (read
first; every row number below is that table's).

## What landed

1. ROW 5, width-declaration half. A `// max_concurrency: N` declaration
   comment now sits in the header of all 19 saved workflows
   (.zcode/workflows/*.dwf.ts), immediately after the metadata block close,
   in the sanctioned `// judge-model:` / `// source-fetched:` stamp position.
   Before: zero declared literals in the fleet (the G8 width gate passed the
   entire standing fleet vacuously; the only 2 text hits were the-gala prose
   at :11/:24). After: 19/19 declared.
   - 16 files at N=3 (fan-out width law default): drop-dig, the 5 game-dig
     near-twins, game-mechanics-deep-dig, librarian-expedition, mickey17-v2,
     music-cut, olm-mine, ractor-engine, salon-mine, the-gala (its own babystep
     ladder is 1-then-3, so 3 matches its bytes), tree-doctrine-dig, wide-dig.
   - 3 files at N=10 + `// envelope-receipt:
     watch/inbox/ENVELOPE_50W_HIT_20260926.md`: fill-ball, gap-analysis,
     the-50. N=10, not 50, because the receipt's measured shape is 5 runs x
     max_concurrency 10 = 50 children (first 429 contact, width HELD); 10 is
     the per-workflow datum the receipt certifies. the-50's stamp says so
     inline (its description's fire-at-50 prose names the fleet shape).
   - Stamp spelling is `envelope-receipt:` (not the brief's `// envelope:`)
     because that is what the gate bytes match: G8_ENVELOPE_STAMP_RE at
     tools/workflow_gate.py = `(?i)\benvelope[-_ ]receipt\s*:`; a bare
     `envelope:` stamp would not count and G8 would fail the 10-wide files.
   - Edits touched the header comment region only; no script body changed.

2. ROW 8, the struck 191.8M provenance in olm-mine.dwf.ts metadata
   description. "Provenance: 191.8M-token run 2026-09-29" replaced by the
   byte-backed framing: run 2026-09-29 (32/32 miners, 21/24 confirmed kept,
   they byte-check in the DIGEST per the errata lane), the aggregate headline
   marked STRUCK per ERRATA 001 (watch/inbox/48h_synth/ERRATA.md, verified on
   disk): no binding surface exists, the DIGEST and the REGISTRY rows carry
   no aggregate token total. Cut, not rebound, per the register's own "or cut
   the number" (watch/inbox/fillball/errata.md). No double quotes introduced
   (the description is a quoted YAML scalar); ascii, no em-dashes.

3. ROW 9, operator-dawn queue only. state/NIGHT_LOOP_20261005.md now carries
   an OPERATOR DAWN QUEUE section: the retirement call (the-50,
   tree-doctrine-dig, music-cut, the 5 game-dig near-twins; merge wide-dig)
   riding the 10-02 minimum-viable-fleet verdict, plus the zombie-cert
   evidence (tree-doctrine-dig cert minted 2026-10-04T02:34:06Z, postdating
   the a53b101d4 retirement verdict). NOTHING was retired by this lane.

## Gate numbers (instrument named per B2-216)

- tools/prepush_workflow_metadata.py BEFORE: `ok - scanned 87 workflow
  file(s) (22 without a metadata block), 0 finding(s)`, exit 0.
- After the 19 Edit-tool insertions: WARN, 2 CR-IN-METADATA findings
  (game-mechanics-deep-dig: 18 CR, ractor-engine: 37 CR). Cause: the Edit
  tool's line-ending normalization rewrote those two metadata blocks to CRLF
  (they were the two files whose `*/` boundary rode CRLF; the patrol tool's
  own docstring names this exact hazard and mandates block-scoped byte
  surgery). Fix per that law: CR stripped from the two blocks only, with
  before/after byte verification (prefix/suffix byte-identical, body
  byte-identical, exactly 18 + 37 CR bytes removed).
- AFTER (final): `ok - scanned 88 workflow file(s) (22 without a metadata
  block, skipped), 0 finding(s) (0 accepted by name)`, exit 0. This is also
  the parse check over every edited workflow (the patrol parses each
  metadata block; the file count moved 87 to 88 mid-window, a sibling lane's
  draft, not this lane's edit).
- G8 simulation (the gate's own regexes run read-only over all 19 files,
  workflow_gate.py untouched): 19/19 pass. 16 declare max(widths)=3 (pass,
  no stamp needed); 3 declare 10 and pass via the envelope stamp naming an
  existing file (os.path.isfile verified true).

## OWED (named per the fence)

- Fold row 6, stop-cert clause (a retired-status script fails or skips
  re-certification) and fold row 7, FIRE_LEDGER check-time append
  ({ts, script, fired_args, max_concurrency} to
  memory/workflows/FIRE_LEDGER.jsonl): both live in tools/workflow_gate.py,
  which a live workflow (executor dwfrun-e9656e14) owns this window. They are
  held in the driver's post-executor queue; also written into the night
  loop's dawn queue for operator visibility.

## Residue / falsifiers

- game-mechanics-deep-dig (30 diggers) kept at N=3: the brief names exactly
  the-50, fill-ball, gap-analysis as envelope shapes. If the operator wants
  the envelope stamp there too (its 5x10 fleet was the envelope event's own
  shape), it is a one-line amendment.
- mickey17-v2's width arg (default 50, "machine caps concurrency lower") is
  lane count, not declared concurrency; its stamp stays 3 unless the operator
  amends.
- Falsifier for this landing: any future G8 run over these files that fails
  width-shape, or any patrol CR-IN-METADATA finding on the 19, means a later
  edit re-broke the stamps; the stamps are declarations, the firer still
  sets max_concurrency at run time.
