---
name: secret-scan-credential-exposure-20260926
description: B2-73 secret scan 9/26 — filed artifacts clean, but 19 corpus oral-history files carry a harvested .env dump with 18 real-shaped credentials pasted into remote grok/codex seats; ROTATION OWED operator-gated
metadata:
  type: project
  originSessionId: sess_fd5ec147-a47d-41ee-91f4-afd899b524ca
---

B2-73 flash-lane lane (9/26, local-only scan: 64,220 files seen, 38,240 text,
1.34GB, 31 gitleaks-pattern rules + 4.3-bit entropy, no network no model calls)
found the filed surface CLEAN but the corpus oral-history estate LEAKING: 19
files carry a harvested dump of the repo root .env pasted into remote grok/codex
seats (grok session 01a04e25 family, 9 codex rollouts, 2026-08-30 to 09-02), 18
distinct real-shaped credentials (OpenRouter x2, Groq x2, DeepSeek x2, xAI x2,
Anthropic x2, Vast.ai, OpenAI project, ZAI x6), plausibly still live since root
.env holds matching key names.

**Why:** this is the fleet's own no-fabrication/honesty law applied against
itself — the seat that pasted the .env into remote seats was doing "context
preparation" and leaked the whole credential set into an estate that later got
filed as canon. Redact-on-harvest is now a queued law (B2-350).

**How to apply:** ROTATION IS OWED and operator-gated — masked heads only in any
filed byte (the lane held this: no full secret value in any landing). Rule set +
solo-operator rotation policy at watch/inbox/SECRET_SCAN_RULESET_ROTATION_20260926.md;
scanner + census scripts in watch/inbox/burn_wave_20260926/B2_73_*. Scheduled
scan + redact-on-harvest self-fed B2-349/350/351. Instrument defects caught
in-lane: capture-group shift mislabeled rules after PRIVATE-KEY; census `_2?`
pattern silently dropped primary-key lines. Related: [[essentials-pack-disaster-recovery]].
