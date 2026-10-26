# Lane C · glm-5.3-flash · pure-prompt recall · distance 16384 tok
- SCORE: 1 (exact quote, byte-identical) · 2026-09-01T12:24Z
- QUOTE: "SENTINEL-OCTAGON: the violet cargo manifest was sealed under brass in dock eleven." · model confidence 1 (1 decimal; 108 reasoning tokens billed)
- Route: full 247KB doc embedded as immutable payload (toolsAllow=[] — no read/grep; pure in-prompt generation). PASS. ctx 58004 in / 134 out; 1M budget, no compaction.
- ANOMALY 1: doc self-contains QUERY-MARKER at line 585 ("quote sentence that begins with SENTINEL-OCTAGON") — sentinel not hidden, though 16384 tokens before marker.
- ANOMALY 2: model wrapped quote in extra double-quotes — harmless, interior byte-identical. ANOMALY 3: reasoning=off still billed 108 reasoningTokens.
- Verdict: PASS at 16384 — single distance; sparse/global-window boundary locus NOT determined.
