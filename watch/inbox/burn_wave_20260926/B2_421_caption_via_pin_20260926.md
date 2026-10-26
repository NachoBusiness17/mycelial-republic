# B2-421 caption_via invariant pin (2026-09-26)

## Verdict

LANDED. The invariant is now enforced two failure classes deep: (1) any
present caption_via whose carrier is not grouped=True / non-empty text / same
calendar date, and (2) any PINNED carrier that a rebuild loses, blanks, or
moves. The pin froze the 111 landed (msg_id -> caption_via) pairs from
watch/inbox/CAPTION_LEDGER_20260926.jsonl (102 B2-12 + 9 B2-90 v2) into
B2_421_caption_via_pin.json, and the B2-12 builder now runs the verifier as a
hard post-write gate, so the exact regression the brief names (a plain rebuild
regressing the 9 v2 rows to empty with every current gate green) exits
nonzero naming the 9 rows instead of passing.

## Evidence file:line quotes

- Pin on the landed ledger (this lane):
  "CAPTION_VIA ok 111/111 (rows with caption_via: 111, pinned: 111,
  violations: 0)", exit 0.
- Falsifier run (this lane): a regressed COPY with the 9 v2 rows
  (4618 4600 4599 3610 2981 1785 1784 1783 1393) blanked feeds the pin and
  returns exit 1 with exactly nine "CAPTION_VIA FAIL msg <id>: pinned carrier
  lost" lines, e.g. "CAPTION_VIA FAIL msg 4618: pinned carrier lost (pin says
  '@MrPool_Q#4622', ledger row is empty)" ... final line
  "CAPTION_VIA FAIL 93/102 (rows with caption_via: 102, pinned: 111,
  violations: 9)". Copy removed after the run; landed bytes untouched.
- Mid-lane correction, stated because it is load-bearing: the first pin draft
  checked only present carriers, and on the regressed copy it printed
  "CAPTION_VIA ok 102/102" exit 0, which IS the brief's disease reproduced
  (blanked rows silently drop out of the checked set). The pinned-floor arm
  exists because of that measured failure.
- watch/inbox/burn_wave_20260926/B2_12_caption_ledger_build.py (post-edit)
  tail: post-write gate subprocess-calls B2_421_caption_via_verify.py with
  the cause-and-evidence comment and propagates a nonzero rc; builder parse
  verified (ast.parse) after the edit; builder logic untouched otherwise.
- watch/inbox/burn_wave_20260926/B2_90_album_captions_v2.py:6-10: targets
  "4618 4600 4599 3610 2981 1785 1784 1783 1393 (empty text, grouped=True, no
  same-date grouped sibling with text within +/-3, per B2-12 search order)",
  the widened-window carriers the pin freezes.

## Work done

1. Census of the landed ledger: 2,726 rows, 111 with caption_via.
2. Wrote B2_421_caption_via_verify.py (carrier-validity check + pinned-floor
   check + pinned-row-presence check, --ledger/--full/--pin overridable).
3. Froze the pin fixture from landed bytes: 111 pairs, sorted, with the 9 v2
   carriers inside.
4. Ran the first-draft pin against a regressed copy, watched it pass green
   (102/102), named that as the measured disease, and added the pinned-floor
   arm; reran: real ledger 111/111 exit 0, regressed copy exit 1 naming
   exactly the 9 v2 rows.
5. Wired the gate into B2_12_caption_ledger_build.py after the OUT write
   (hard gate, rc propagated), validated the file parses, removed the
   regressed copy.
6. Filed this receipt, LEDGER row, QUEUE pointer, INDEX registration.

## Falsifier

This pin is inverted if any of the following holds: (a) the regressed-copy
experiment stops firing (rerun: blank the 9 v2 rows on a copy, run the pin;
exit must be 1 naming 9 rows, otherwise the pin regressed);
(b) the landed ledger drifts (a carrier moves or a rebuild lands) without the
pin firing at build time and without a receipt updating
B2_421_caption_via_pin.json (the pin is being bypassed, e.g. the builder gate
deleted or --ledger pointed at a doctored path in the wiring);
(c) the pin fixture itself names a carrier that violates the invariant
(rerun the pin on the real ledger: any carrier-validity FAIL means the frozen
expectation contains a bad carrier).

## Bibliography closed

watch/inbox/CAPTION_LEDGER_20260926.jsonl (census + pin freeze source bytes);
watch/inbox/burn_wave_20260926/B2_12_caption_ledger_build.py (read: docstring
schema, SIBLING_ORDER constant, main tail; edited: gate block only);
watch/inbox/burn_wave_20260926/B2_90_album_captions_v2.py (targets + v2 rule
read); the B2-409 landing row in QUEUE.md (line 261, the pin-in-results-JSON
shape this receipt mirrors). No network calls.
