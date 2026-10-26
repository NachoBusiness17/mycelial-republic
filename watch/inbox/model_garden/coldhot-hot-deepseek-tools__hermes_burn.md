# coldhot-hot-deepseek-tools__hermes_burn (deepseek-chat @ deepseek, turn 1, channel: content)

DEFECT 1: EVIDENCE-PREFLIGHT head probe checks `text[:400].strip() not in body` but the system prompt is prepended ahead of the evidence block only via `_system_for` which returns face_for(model)+laws; on turn 2 the rebuilt `messages` drops the system prompt and contract entirely, so probe for evidence material still present in turn-2 body holds only because evidence rides the original user msg - but a revision whose evidence rendered into `contract` (not evidence[]) passes exactly as the DUEL2/T1W2 disease did | EVIDENCE: tools/hermes_burn.py:262-266 | FIX: require every evidence path also appear in `meta.get("contract")` render, or resolve material via evidence[] only and reject contract-embedded pseudo-evidence.

DEFECT 2: `_assert_public_endpoint` resolves once per call but urllib.request follows redirects by default; a 30x from the allowlisted host to an internal URL bypasses the IP fence entirely | EVIDENCE: tools/hermes_burn.py:100-107 and tools/hermes_burn.py:126-133 | FIX: install an HTTPRedirectHandler that raises on any redirect, or pass a custom opener with redirects disabled.

DEFECT 3: `_bank` writes usage rows to a shared jsonl and `_landed_skip` reads `out_path.exists()` but turn-1 write uses `out_path.write_text` non-atomically; a crash mid-write leaves a partial deliverable that `_landed_skip` then treats as landed and refuses every re-fire forever | EVIDENCE: tools/hermes_burn.py:319-323 and tools/hermes_burn.py:154-172 | FIX: write to `out_path.with_suffix('.md.tmp')` then `os.replace`, and gate `_landed_skip` on a non-empty trailing marker or size floor.

DEAD-CODE: `USAGE` module constant is shadowed nowhere but `USAGE.parent.mkdir` in `_bank` is the only writer; the `guard_terminal` call passes `_bank` as a callback but no other caller exists | EVIDENCE: tools/hermes_burn.py:186-189

ONE-SITTING FIX: disable redirects on the endpoint call | EVIDENCE: tools/hermes_burn.py:126-133
