# B2-349 receipt: rotate the 18 exposed credentials (2026-09-26)

## Verdict

OWED, operator-gated: rotation requires provider console access (revoke is a human-in-console action per the solo-operator rotation policy), so this lane files the exposure state as re-verified on bytes, the per-provider rotation checklist in execution order, and the journal obligation, without claiming any rotation happened. Zero rotation has occurred as of this receipt: watch/inbox/KEY_ROTATION_JOURNAL.jsonl does not exist, and the root .env still carries all 20 key NAME rows matching the scan's inventory. Masked heads only in this receipt; no secret value is quoted, printed, or hashed here.

## Evidence file:line quotes

- watch/inbox/burn_wave_20260926/B2_73_secret_scan_20260926.md:7-11: "entropy pass over watch/inbox (18,684 candidates in 1,051 files) resolves to ..." and "The leak is in the corpus oral-history estate: 19 corpus files tallying 18 distinct real-shaped values (2 OpenRouter, 2 Groq, 2 DeepSeek, [2 xAI, 2 Anthropic, 1 Vast.ai, 1 OpenAI proj, 6 ZAI])".
- Measured this lane: watch/inbox/KEY_ROTATION_JOURNAL.jsonl absent (ls: no such file); root .env holds 20 KEY/TOKEN/SECRET-name rows (names listed in evidence only: ANTHROPIC_API_KEY, CEREBAS_API_KEY, COHERE_API_KEY_FREE, COHERE_API_KEY_PAID, CURSOR_API_KEY, DEEPSEEK_API_KEY, GEMINI_API_KEY, GOOGLE_API_KEY, GROK_API_KEY, GROQ_API_KEY, MAPBOX_TOKEN, NOTION_API_KEY, OPENAI_API_KEY, OPENCLAW_GATEWAY_TOKEN, OPENROUTER_API_KEY, TOGETHER_API_KEY, VASTAI_API_KEY, VERCEL_KEY, XAI_API_KEY, ZAI_API_KEY); no value bytes reproduced.
- watch/inbox/SECRET_SCAN_RULESET_ROTATION_20260926.md section 2 rule 4 (the event-driven rotation clause this brief invokes) and line 31 (rule-name tallies: OPENAI-CLASSIC 14, OPENROUTER-KEY 28, GROQ-KEY 28, XAI-KEY 18, ...).

## Work done

1. Re-verified the exposure state on bytes: scan receipt's 18-value/19-file tally re-read; journal absence confirmed (no rotation has been logged by any lane); .env key-name inventory enumerated (names only).
2. Filed the execution order for the operator console pass (revoke-first at each provider per the policy, then replace in .env, then journal): (1) ZAI (6 keys, largest blast radius, console per key), (2) OpenRouter (2), (3) Groq (2), (4) DeepSeek (2), (5) xAI (2), (6) Anthropic (2), (7) OpenAI project key (1), (8) Vast.ai (1). For each: revoke the exposed key at the console, mint the replacement, update the root .env row, then append one line to watch/inbox/KEY_ROTATION_JOURNAL.jsonl naming provider, masked OLD head, masked NEW head, and date. Masked heads only in any receipt or journal line, per the brief.
3. Confirmed the falsifier instrument exists and is the acceptance test: watch/inbox/burn_wave_20260926/B2_73_secret_scan.py rerun post-rotation must find none of the same masked heads in corpus bytes (the corpus oral-history files retain the OLD values until provider-side revocation kills them, which is why revoke-first order matters).
4. No rotation claimed, no .env value touched, no secret value written anywhere by this lane.

## Falsifier

This receipt is the owed-arm record; it closes when: (a) watch/inbox/KEY_ROTATION_JOURNAL.jsonl exists with 18 provider-revocation lines (or a documented per-provider decline), and (b) a post-rotation rerun of B2_73_secret_scan.py over the corpus finds none of the 18 masked heads live (a rerun still finding the same heads = rotation not actually done console-side, voiding any journal-only claim). Until both hold, the exposure stands and this receipt stays the honest state. Any receipt claiming rotation without the journal row and the clean rescan is void under the no-fabrication law.

## Bibliography closed

All read this lane: watch/inbox/burn_wave_20260926/B2_73_secret_scan_20260926.md (tally lines), watch/inbox/SECRET_SCAN_RULESET_ROTATION_20260926.md (section 2 rule 4, rule-name tallies), watch/inbox/KEY_ROTATION_JOURNAL.jsonl (absence confirmed), root .env (key NAMES enumerated, values never emitted), QUEUE.md B2-349 row.
