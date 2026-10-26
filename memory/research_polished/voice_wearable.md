# voice_wearable — polished synthesis

Packs merged (3, effectively 2 + 1 duplicate): 20260808T_vscode-voice-communication-steal · steal_voice_earbud_stt_20260811 (.answer.local + .answer.remote). Register: digest_rp_07/15.

## Essence
Voice quality is a capture-and-device problem before a model problem: one on-device STT engine with surface-adapted cleanup plus a mic-device selector beats any model work — both steals (VS Code 1.132 dictation invariants; earbud BT-profile fix) have landed in the Mag voice stack, with thin spots at queued turns, language surfacing, and onboarding.

## Merged findings (receipts)
1. **VS Code 1.132 dictation invariants, verdict STEAL_NOW** (benefit 8 · adapt_cost 4 · ignore_risk 6 · adopt_risk 2): on-device STT (multilingual Nemotron 3.5, audio never leaves the machine); one surface-agnostic engine with per-surface cleanup — "git commit dash m hello world" → `git commit -m "Hello World"`; layered instruction files (~/.copilot/dictation.md + workspace dictation.md); voice-aware agent tailors terse spoken replies; warm-capture pre-roll; queued concurrent turns. Sources credited: code.visualstudio.com/updates/v1_132, PRs #327899/#328205/#328225/#328217.
2. **Earbud STT fails on the Bluetooth SCO hands-free profile (~8kHz mono), not the model.** When the earbud mic activates, Windows drops A2DP stereo for SCO; fix = let the user route STT to a clean mic while audio keeps playing on the earbuds: `enumerateDevices()` dropdown persisted in localStorage + `deviceId: {exact}` constraint + `sampleRate: 16000, channelCount: 1`. The local faster-whisper pipeline (VAD on, beam 5) was already fine — the gap was input-device selection.
3. **Both steals verified landed** (register gates): `mag/voice_dictate.py` exists with the credited invariants (SURFACES = chat/terminal/command, layered ~/.mag/dictation.md + .mag/dictation.md); I1 spoken-turn marker in mag/voice_turn.py:321; I3 warm-capture pre-roll in dashboard/static/cast-voice.html:215; mic selector (`selectedMicId()`, `enumerateDevices()`, `deviceId:{exact}`) at cast-voice.html:392, 529-537; mag/voice_stt.py with faster-whisper + VAD.
4. **Pipeline hygiene:** the .remote earbud pack is content-identical to .local (only the "filed" timestamp differs, 12:50 vs 12:58Z) — the steal pipeline double-filed the same pack under local and remote; dedup candidate.

## Verified vs owed
- **Verified:** voice_dictate.py with per-surface cleanup + layered instruction files; voice:true turn marker (voice_turn.py:321); warm pre-roll (cast-voice.html:215); mic device selector (cast-voice.html:392, 529-537); faster-whisper + VAD STT path.
- **Owed:** I4 queued concurrent voice turns (no-drop under rapid fire) not spot-verified; I5 language picker / I6 onboarding (mic waveform, device picker, offline model fallback) not spot-verified; the remote duplicate pack not yet deduped; optional "test mic" A/B (2s record + transcribe) never built.

## Three next actions
1. Spot-verify I4: fire rapid concurrent voice turns and confirm voice_scratch/voice_turn queue commits instead of overwriting; fix if they drop.
2. Close I5/I6: expose the whisper `language` picker and a 2-second test-mic A/B (earbud vs laptop mic) in cast-voice.html.
3. Dedup the earbud pack: keep one copy, note the local+remote double-file in the register.
