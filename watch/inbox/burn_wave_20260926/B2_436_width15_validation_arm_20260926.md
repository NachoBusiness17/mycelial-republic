# B2-436 gate the width-15 fire on the provider-error counter 2026-09-26

## Verdict

LANDED. Checked whether the B2-98 counter landed: it DID (tools/provider_error_tally.py + tests/test_provider_error_tally.py on disk; LEDGER row 2026-09-26T18:44:00Z "B2-98-provider-error-visibility landed"; receipt watch/inbox/burn_wave_20260926/B2_98_error_visibility_20260926.md; first baseline reads 1785 driver-visible failures, 1780 statusCode 429 [1302], 1741 absorbed by the main-session retry path). Per the brief's two arms, the armed branch applies: the VALIDATION ARM appended to the B2-97 card (append-only, at the file tail) now requires every width-15 fire to harvest the session's provider_errors.json tally, voids clean-read claims without it (fire records provisional only, extends no rung), and lets a tally-present zero-absorbed-1302 read claim the rung WITHOUT the provisional flag. The falsifier as written is closed on the card: a width-15 receipt with a clean ceiling read and no counter in the harvest now self-identifies as void.

## Evidence file:line quotes

- watch/inbox/burn_wave_20260926/B2_97_width15_probe_20260926.md:49-53 (pre-edit): BLIND SPOT "the main-session retry path (maxAttempts 11...) absorbs 1302/429 without a lane-visible trace ... until B2-98's provider-error counter lands. A clean width-15 read under this blind spot extends the ladder only provisionally."
- memory/burns/LEDGER.jsonl row 2026-09-26T18:44:00Z slug b2-98-provider-error-visibility: "tools/provider_error_tally.py plus tests/test_provider_error_tally.py (3 pins) ... first baseline on sess_fd5ec147 reads 1785 driver-visible failures today, 1780 statusCode 429 with the [1302] marker, 1741 absorbed by t[he retry path]".
- File bytes: tools/provider_error_tally.py (12,740 bytes) and tests/test_provider_error_tally.py (6,247 bytes) exist; B2-98 receipt on disk.
- Appended card tail (this lane): "VALIDATION ARM (appended 2026-09-26, B2-436)" naming the harvest requirement, the void rule, and the full-read rule; the card's earlier canonical check (tools/operator_go.py width-15) untouched.

## Work done

1. Located the B2-98 landing by LEDGER and file bytes (the QUEUE row for B2-98 had been erased by the concurrent board restore sweeping this lane's rows; the durable records are the citation).
2. Appended the validation arm to the B2-97 card at the tail, append-only, no earlier byte touched; the arm names the exact harvest artifact (provider_errors.json tally over the firing session) and both read classes (void-provisional vs full clean).
3. Registered the receipt in index_events.jsonl; LEDGER row; QUEUE row flip.

## Falsifier

Dies if: (a) a fired width-15 receipt claims a clean ceiling read with no provider-error counter tally in its harvest and is not marked provisional/void by its own text; (b) the arm's claim about the counter's shape breaks (tools/provider_error_tally.py stops emitting a session tally file) without the arm being amended; (c) the appended arm bytes are altered or removed (the card is append-only; amendments append, never rewrite).

## Bibliography closed

Read whole: watch/inbox/burn_wave_20260926/B2_97_width15_probe_20260926.md (fire preconditions, blind spot, canonical check), memory/burns/LEDGER.jsonl B2-98 rows, watch/inbox/burn_wave_20260926/B2_25_envelope_remeasure_20260926.md falsifier 1 lines. Bytes: counter files ls-verified; card tail re-read post-append. Nothing synthesized.
