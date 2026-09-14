# Pass 2 — Probe Scheduler (distance 512) · pure-prompt recall

- **Score: 1.0 (exact)** — verbatim quote, confidence 1.0, no tools (`toolMetas: []`).
- **Quoted sentinel:** `SENTINEL-OCTAGON: the violet cargo manifest was sealed under brass in dock eleven.`
- **Harness:** pure_prompt_attachment_v2 — full 246,672-byte doc embedded as immutable payload; ctx 58,028 tok; needle byte-offset 242,242; no tool round-trips.
- **Verdict:** pass-1 failure signature (harness_leak_read_tool…) resolved — recall was attention/generation-based this run.
- **Anomalies:** (1) `needle_to_query_tokens` fixed 16384→512 on the existing pass-2 row (prior continuation mis-filled); (2) fresh long-context 58K prompt conflicts with ZAI cached-prefix Flash rule — one-off task-mandated, battery cost ~1.25 cr (well under 400 cr cap).
