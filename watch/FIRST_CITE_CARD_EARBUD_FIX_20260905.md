# FIRST CITE-AT-BIRTH CARD — the earbud fix, ghost gold wired live (2026-09-05)

**Operator:** "the time is now" — so the new consumption regime demonstrated
itself the same turn it was born: ghost-era gold #1 verified, wired, and this
card is the first to obey the cite law.

## What landed

`dashboard/static/cast-voice.html` (STT mic routing, 4 edits, JS compile-check
PASS at 40,407 chars):
- `Mic (STT input)` selector next to STT mode — `enumerateDevices()` populated,
  persisted in localStorage (`magVoiceMicDevice`), devicechange-aware.
- `startWhisperRec()` now requests `sampleRate: 16000` + `deviceId: {exact}`
  from the selector — faster-whisper's 16k-mono target straight from capture.
- echoCancellation/noiseSuppression/autoGainControl untouched; whisper stays
  the default STT mode. No backend change (recipe's own verdict).

## The re-test (falsifier act #1)

Ghost-excavation claim (SUPPORTED pre-fix): "no deviceId constraint in
cast-voice.html; the earbud fix was written 2026-08-11 and never wired."
Re-verified by grep + code read, then CLOSED BY WIRING. The claim is now
DISPROVED AS STANDING — the oldest cheap win on the board is live. The
operator's earbud mic vs laptop mic choice survives reloads.

## Regime notes (the first cycle, receipted)

- This card carries `Cites:` — the first of the cite-at-birth era.
- Time from gold-identification to wire: one turn. The 4-agent excavation
  found it at ~20:30Z; the word came; it is wired by ~01:45Z.

Cites: STEAL_VOICE_EARBUD_STT_20260811, GHOST_ERA_EXCAVATION_20260905, ZERO_BACKREF_TRIAGE_20260905
Decision: none (built + wired in-turn, 2026-09-05)

**Score:** 19/25 BUILD (small, but it closes a 25-day-old loop and proves the
whole consumption machine end-to-end on its first day).

*Filed by the zcode seat. Operator test: open cast-voice, pick the earbud mic,
talk — whisper eats 16k mono from the device you chose.*
