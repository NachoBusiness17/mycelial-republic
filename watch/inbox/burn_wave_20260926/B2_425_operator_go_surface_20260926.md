# B2-425 canonical operator-GO surface (2026-09-26)

## Verdict

LANDED. The convention exists and the three prose-gated cards are migrated:
watch/inbox/OPERATOR_GO.jsonl (schema operator_go.v1: ts, gate, order,
source_transcript, transcribed_by) is the single surface, appended only by
lanes transcribing a real operator order with its source named; the reader
helper tools/operator_go.py gives every lane a machine check (exit 0 = GO on
file with the row printed, exit 1 = NO-GO-on-file). The surface is seeded
with exactly one byte-sourced row (the burn-wave order, transcribed from the
board's own header) and the three gates read NO-GO-on-file - which is the
honest state: no transcript of a width-15, seed-flip, or grok-packet GO
exists on any file, which is precisely the disease this brief names.

## Evidence file:line quotes

- The three gates' GO-less state, from their own bytes:
  B2_97_width15_probe_20260926.md:5 "No explicit operator GO for width 15
  exists on QUEUE.md or any 2026-09-26 receipt"; B2_23_seed_flip_card_20260926.md:5
  "No link exists yet; operator GO required"; B2_53_grok_fire_card_20260926.md:5
  "FIRE, with three amendments before GO" (GO still pending).
- The seeded row (watch/inbox/OPERATOR_GO.jsonl line 1): gate
  "burn-wave-20260926", order transcribed from watch/inbox/burn_wave_20260926/QUEUE.md:3-5
  ("Operator order: burn remaining quota into estate work before reset...
  until 23:55 local or quota death"), source_transcript naming those bytes -
  a real order already on file, not a new claim.
- Reader behavior (this lane): `operator_go.py burn-wave-20260926` exits 0
  and prints the row; `operator_go.py width-15`, `seed-flip`,
  `grok-lane-packet` each print "NO-GO-on-file: <gate>" and exit 1.
- The migrations (appended dated sections, no card bytes rewritten):
  B2_97 card now names "This card fires only on exit 0" of
  `tools/operator_go.py width-15` and retires its Evidence prose-grep for
  future checks; B2-23 names `seed-flip`; B2-53 names `grok-lane-packet`
  with the three amendments attached regardless.

## Work done

1. Read the three gate cards; confirmed all three sit NO-GO-on-file and that
   each documented GO-verification as prose grepping with self-named scope
   limits.
2. Wrote tools/operator_go.py (load_rows, has_go(gate) newest-row semantics,
   CLI with exit-code contract) and the JSONL surface.
3. Seeded the surface with the one order that has on-file bytes (QUEUE
   header); refused to invent rows for the three gated cards.
4. Appended GATE SURFACE MIGRATION sections to all three cards (append-only)
   binding each gate to its gate-id and the exit-code contract.
5. Filed this receipt; LEDGER row; QUEUE pointer; INDEX registration.

## Falsifier

The convention is inverted if any of the following holds: (a) a lane fires a
gated card while `tools/operator_go.py <gate>` exits 1 (the migration is
being ignored; the card's own pointer names the check that was skipped);
(b) a row appears in OPERATOR_GO.jsonl whose source_transcript does not
resolve to bytes (a fabricated order; the no-fabrication law makes that a
kill, not a warning); (c) a real operator order exists in chat, a lane acts
on it, and no row lands within the acting lane's own receipt (the
transcription duty is being dodged exactly as the B2-97 receipt's sweep-scope
limits demonstrated).

## Bibliography closed

watch/inbox/burn_wave_20260926/B2_97_width15_probe_20260926.md,
B2_23_seed_flip_card_20260926.md, B2_53_grok_fire_card_20260926.md (all read;
all three migrated); watch/inbox/burn_wave_20260926/QUEUE.md:3-5 (the seeded
order's source bytes); tools/operator_go.py and watch/inbox/OPERATOR_GO.jsonl
(created this lane, behavior verified by direct invocation). No network calls.
