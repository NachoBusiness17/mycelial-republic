# B2-115 receipt (2026-09-26)

## Verdict

LANDED (annotation arm). The groq model_chain in watch/inbox/burn_wave_20260926/B2_04_probe.py line 219 was annotated in place as a dated period artifact, per the brief's first offered option. The chain bytes were left as-written; the comment names the two dead entries and the rerun hazard.

## Evidence file:line quotes

- watch/inbox/burn_wave_20260926/B2_04_probe.py:219 (before edit): `            ["openai/gpt-oss-120b", "qwen/qwen3.6-27b", "groq/compound-mini"],`
- watch/inbox/burn_wave_20260926/B2_04_probe.py:219 (after edit, lines 219-224): `# B2-115 dated-frozen 2026-09-26: chain kept as a period artifact.` / `# qwen/qwen3.6-27b and groq/compound-mini were 404-dead on groq as of` / `# 2026-09-26 (post-surgery roster); a rerun burns 404s on them before` / `# falling through. Fix this roster before any rerun, or read` / `# configs/providers.yaml for the live set.` above the unchanged chain literal.
- grep over the whole script for `qwen3.6|compound-mini|qwen/qwen` returned exactly one hit (line 219), so the annotation covers every dead-name site in the file.
- configs/providers.yaml:242-243 read at land time: they hold the anthropic block models list (`claude-sonnet-4-20250514`, `claude-3-5-haiku-20241022`), i.e. the brief's second pointer names the live-roster source region, not another dead chain; no edit needed there.

## Work done

1. Verified line 219 still carries both dead model names (qwen/qwen3.6-27b, groq/compound-mini).
2. Grepped the script for all occurrences of either name: one site only.
3. Chose the brief's annotation arm (zero-behavior-change) over the roster rewrite, because the post-surgery groq live set was not re-verified against the API in this lane and a guessed roster would be fabrication-adjacent.
4. Inserted the dated frozen-artifact comment directly above the chain literal; syntax checked via py_compile.

## Falsifier

The brief's falsifier shape: "any rerun wastes calls on 404s before falling through". After this landing a rerun still would (the chain is deliberately unchanged), but the script now self-declares the hazard at the exact line, so the failure mode is named at the byte that causes it. If a future lane updates the chain to a verified live roster, it must delete this comment in the same edit or the comment becomes a lie; that paired check is the standing falsifier.

## Bibliography closed

- watch/inbox/burn_wave_20260926/B2_04_probe.py (lines 1-30 header, 214-231 groq block)
- configs/providers.yaml lines 235-250 (anthropic block at the cited 242-243)
- QUEUE.md row B2-115 (line 294 at lane start)
