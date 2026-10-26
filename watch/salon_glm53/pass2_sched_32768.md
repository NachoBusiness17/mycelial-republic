# Lane C · glm-5.3-flash · pure-prompt recall · distance 32768 tok
- SCORE: 1 (exact quote, byte-identical) · 2026-09-01T12:37Z
- QUOTE: "SENTINEL-OCTAGON: the violet cargo manifest was sealed under brass in dock eleven." · model confidence 1, no reasoning/backtracking.
- Route: full 247KB doc embedded as immutable payload (toolsAllow=[] — no read/grep; pure in-prompt generation). PASS. ctx ~74K in / minimal out.
- ANOMALY 1: doc self-contains QUERY-MARKER at line 601 ("quote sentence that begins with SENTINEL-OCTAGON") — sentinel at line 3 (top), ~32768 tokens before marker; not hidden.
- ANOMALY 2: sentinel sits at very top of doc (line 3), so retrieval is trivial positional read, not long-range attention — distance does not genuinely stress recall.
- ANOMALY 3: worker reuse of same byte-identical sentinel string across all pass-2 distances (512/16384/32768 all PASS score 1) — suggests string/copy, not distance-sensitive.
- Verdict: PASS at 32768 — single distance; sparse/global-window boundary locus NOT determined. Reinforces verdict file's warning (pure attachment, not attention boundary).
