# WINSTT ASSESSMENT — the operator's voice organ (2026-09-11)

*Operator dropped github.com/dahshury/WinSTT, no caption. Assessed: this is the
missing INPUT organ — his voice, typed anywhere, local and sovereign.*

## WHAT IT IS

Local-first dictation: press a hotkey, speak, and the text lands at your cursor in
ANY app. Fully on-device speech-to-text (ONNX Runtime — no cloud, no API), 70+
model catalog (Whisper, NeMo, Moonshine, GigaAM, Kaldi), four trigger modes
(push-to-talk / toggle / listen / wake word), searchable history, snippets,
dictionary corrections, file transcription mode. Optional cleanup step can call a
LOCAL OLLAMA LLM.

MIT license. Prebuilt Windows installer (v0.1.3-alpha.9, AVX2-capable CPU needed)
or portable zip. Early but active: 292 commits, CI, docs site.

## WHY THE FLEET WANTS IT (the fit, plain)

1. **The dyslexic scaffold, solved at the input.** The operator speaks plainly;
   the machine types. Speaking beats typing for him — this is the input law made
   software.
2. **The cleanup step points at OUR host ollama** — the eye is already there;
   voice → text → cleaned text, all local, all $0.
3. **Sovereignty law holds:** transcription never leaves the machine (T0/T1
   never remote-trained — same rule, input side).
4. **Dictation targets:** the room, CONVO, the shitpost desk, the morning
   report responses — the operator's voice becomes a fleet input organ without
   a single new integration (it types at the cursor; every surface receives).

## THE FIT AGAINST THE LAWS

- Local-first ✓ (matches loopback/footprint-sovereignty doctrine)
- MIT ✓ · $0 ✓ · no new fleet dependency (desktop app, failure = stop using it)
- No sacred-cow conflict: the fleet has voice OUTPUT (ghost, TTS); this is the
  missing voice INPUT.

## ADOPTION PATH

1. Operator installs the Windows alpha (or portable zip — no system install).
2. Hotkey config: push-to-talk, one key.
3. Cleanup provider: host ollama (http://127.0.0.1:11434) if wanted.
4. Fleet side: nothing to build — it types; every surface already receives.
   Optional later: route dictated text at watch/ as the voice-intake lane
   (the paste-window law already covers whatever lands).

## RISKS (plain)

Alpha (pre-1.0) — but it's a desktop app, not fleet infrastructure; the failure
mode is "stop using it." AVX2 requirement: any post-2013 CPU. Fine.
