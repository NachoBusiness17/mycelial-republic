# B2-189 parse provider retirement bodies (2026-09-26)

## Verdict

LANDED. scripts/build_lane_game.py now parses the in-band successor out of
404 bodies: on any HTTP 404 whose body matches "Use it now: <URL>", the lane
files a flip-card row {ts, dead_model, successor, successor_url, source:
"build_lane_404_body"} to watch/inbox/burn_lane_flip_cards.jsonl (append-only,
deduped per (dead_model, successor) in-process AND against existing file
bytes, never raises into the lane). The next window death files itself
instead of waiting for a human lane, which is exactly what happened with the
union-alpha death (B2-55 had to hand-parse it).

## Evidence file:line quotes

- The in-band carrier, watch/inbox/union_fullsend_20260917/build_lane/
  proposals.jsonl:100 (per the brief): "Use it now:
  https://openrouter.ai/unbiased/pareto" inside the union-alpha 404 body;
  B2_55_buildlane_flip_20260926.md:5 records the manual flip that had to
  follow ("stealth/union-alpha is provider-dead (its 404 body names the
  successor). Primary flipped to unbiased/pareto").
- Post-edit scripts/build_lane_game.py: module-level `_FLIP_CARDS` +
  `_USE_IT_NOW_RE = re.compile(r"Use it now:\s*(https?://[^\s\"'<>\\]+)",
  re.I)`; `_file_retirement_flip(dead_model, body_text)` with docstring
  naming cause and law; `_call` HTTPError branch now reads the FULL body,
  truncates to 200 chars only for the record's detail, and parses the full
  body before any later consumer truncates it.
- Handler proof (this lane, both body forms):
  - JSON body `{"error": {"message": "This model was Unbiased's Pareto. Use
    it now: https://openrouter.ai/unbiased/pareto", "code": 404}}` yields
    {"dead_model": "stealth/union-alpha", "successor": "unbiased/pareto",
    "successor_url": "https://openrouter.ai/unbiased/pareto", ...};
  - raw-text body with trailing period yields the same successor;
  - a third identical call returns None (in-process dedupe);
  - a no-match body ("plain 404 not found") returns None.
- First draft bug, stated because it shaped the final bytes: the original
  regex anchored the URL to end-of-line and returned null on the JSON form
  (the real carrier shape); the character-class form above was the fix.
- Test rows written during the proof were removed; the flip-card file stands
  empty, wired for real lane 404s only. ast.parse of the edited module: ok.
  No existing test file targets this module (tests/test_build_lane_game.py
  absent; pytest collected none).

## Work done

1. Read `_call` and the B2-55 receipt; confirmed no flip-card surface
   existed anywhere in watch/inbox/.
2. Added `_file_retirement_flip` + regex + `_FLIP_CARDS` path; wired it into
   the 404 arm of `_call` with full-body parse before detail truncation.
3. Proved the handler on the exact historical body shape (JSON and raw),
   including dedupe and no-match arms.
4. Cleaned the test rows out of watch/inbox/burn_lane_flip_cards.jsonl so
   only genuine lane 404s populate it; validated module parse.
5. Filed this receipt; LEDGER row; QUEUE pointer; INDEX registration.

## Falsifier

This landing is inverted if any of the following holds: (a) a real 404 with
a "Use it now:" body lands after this date and watch/inbox/
burn_lane_flip_cards.jsonl gains no row (the handler is unreachable from the
live path, e.g. an exception path bypasses it, or a later edit removed the
arm); (b) the flip-card file holds a row for a model that is not actually
4xx-dead (the regex matched a body that was not a retirement, e.g. a
marketing message); (c) the handler throws into the lane on an unwritable
inbox (the never-raise contract broke and a build run died on card filing).

## Bibliography closed

watch/inbox/union_fullsend_20260917/build_lane/proposals.jsonl:100 (the
historical body, cited from the brief and cross-read against the B2-55
receipt's quotes); watch/inbox/burn_wave_20260926/B2_55_buildlane_flip_20260926.md
(read in full); scripts/build_lane_game.py `_call` + census sections read
before edit. No network calls in this lane.
