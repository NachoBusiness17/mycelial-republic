# hermes docs b2 wing 10 (docs/streaming-tts.md)

via seat-b1 beat ext-0e3164e209 folded=True

Report on watch\hermes_wings\b1_docs\b2doc_10.md

1. What it does
This document specifies streaming text-to-speech: it defines a four-stage pipeline where an LLM's text deltas are accumulated by SentenceChunker, converted per-sentence to PCM by a StreamingTTSProvider, and played to sounddevice.OutputStream or a gateway adapter's write_streaming_tts seam. It also sets provider selection rules (pinned or "auto" priority walk), a capability/credential matrix, extension steps, and gateway fallback rules.

2. Design patterns named in the file
- Registry pattern: @register("yourname") decorator makes providers discoverable via tools/tts_streaming.py.
- Template Method via ABC: StreamingTTSProvider enforces the stream() contract; the dispatcher supplies sentence buffering, stop events, and sink.
- Strategy/priority chain: "auto" walks elevenlabs -> gemini -> openai -> xai, taking the first whose credentials resolve.

3. Risks visible in this file only
- Single point of failure: resolve_provider_secret() is the sole credential path for every provider; if it misresolves, all streaming auth fails (file also notes an env fallback chain, which mitigates).
- Hidden shared state: none named explicitly, but the dispatcher and gateway consumer both manage the sentence buffer and stop events off-file.
- Duplicate scheduler: none described; only single-path playback, with double playback suppressed per-turn.
