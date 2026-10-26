# B2-134 Key inventory truth sweep (SW-07, 2026-09-26)

## Verdict

LANDED. Every keys.json and spend_overlay status now reconciles against providers.yaml dormant flags and the B2-04 live verdicts; five lies named and fixed in bytes. Two structural findings registered: (1) silence-equals-active in mag/key_law.py (missing status defaults to "active", which is how dormant lanes read active), now closed by explicit statuses on the dormant entries; (2) an env-name split on the cerebras lane, the fleet key is CEREBAS_API_KEY (no R, .env:98-99, keys.json, spend_overlay, free_tier.py:61, subscriptions.py:131, research_fanout.py:130-132) while providers.yaml:656 declares primary api_key_env CEREBRAS_API_KEY, a name that matches no .env var (the :659 fallback list is what actually resolves).

## Evidence file:line quotes

- The brief's lie, quoted: configs/keys.json:70-75 pre-sweep `"cerebras_2": { "env": "CEREBAS_API_KEY2", "provider": "cerebras", "role": "fast_bulk", "status": "active" }` against configs/providers.yaml:639+654 `name: Cerebras (card-gated 30-day trial, dormant pending operator GO)` / `dormant: true   # card-gated trial; operator GO flips this + re-adds to prefer_order`, and B2-04 live bytes watch/inbox/PROVIDER_HEALTH_20260926.md:22 `| cerebras | api.cerebras.ai/v1 | ... | NO | /models 200 (2 models ...) but chat 402 Payment Required x3, empty body = zero usable credit | 0 |`.
- configs/spend_overlay.yaml:75-78 pre-sweep: `- key: CEREBAS_API_KEY / provider: cerebras / balance_usd: null / as_of: null` -- a spend-tracking row for a lane with no spendable credit.
- The other named lies: keys.json:85 pre-sweep `"status": "verify-auth"` on together while B2-04:18 reads `| together | api.together.xyz/v1 | deepseek-ai/DeepSeek-V4-Flash-0731 | YES 3/3 | ... | 540 |`; keys.json nvidia_build/nvidia_build_2 and mistral_1/mistral_2 carried no status at all (mag/key_law.py:71 `e.get("status", "active")` makes silence read active) while B2-04:23 reads `chat 410 Gone x3; listed model 404 ... zero callable functions post-purge | 0 |` for nvidia and B2-04:25 reads `chat 429 x3 with x-ratelimit-limit-req-minute: 0, remaining: 0` for mistral.
- Env-name split bytes: .env:97-99 `# ---  Cerebas  ---` / `CEREBAS_API_KEY=<present>` / `CEREBAS_API_KEY2=<present>`; configs/providers.yaml:656 `api_key_env: CEREBRAS_API_KEY`; :659 `api_key_envs: [CEREBRAS_API_KEY, CEREBAS_API_KEY]`; mag/free_tier.py:61 `"keys": ["CEREBAS_API_KEY"]`.

## Work done

- configs/keys.json: cerebras_2 "active" replaced with "dormant-no-credit (...)" naming the B2-04 402x3 verdict and the providers.yaml dormant flag; cerebras_1 gained the same explicit status (it previously lied by silence).
- configs/keys.json: together "verify-auth" cleared to "verified-live (...)" on the B2-04 YES 3/3 measurement.
- configs/keys.json: nvidia_build and nvidia_build_2 gained "dormant-roster-purged (...)" statuses; mistral_1 and mistral_2 gained "dormant-limit-0 (...)" statuses.
- configs/spend_overlay.yaml: the CEREBAS_API_KEY row gained status + note fields naming the no-credit truth and the env-name split; balance left null because no balance exists to track.
- Both files re-parsed after edit: keys.json 32 entries, spend_overlay.yaml yaml.safe_load clean.

## Falsifier

The brief's falsifier is the lie table itself. Reopen conditions: any keys.json entry with status active (explicit or by silence) whose providers.yaml block carries dormant: true; any status contradicted by a newer PROVIDER_HEALTH row; or the cerebras env-name split unresolved (providers.yaml primary api_key_env still CEREBRAS_API_KEY while .env holds only CEREBAS_API_KEY). Structural falsifier left on file for a later lane: mag/key_law.py:71 still defaults missing status to "active", so any FUTURE key added without a status to a dormant lane re-mints lie class (1).

## Bibliography closed

Read: configs/keys.json (full), configs/spend_overlay.yaml (lines 60-99 + parse), configs/providers.yaml (saelis/mistral/nvidia/cerebras blocks, dormant grep), watch/inbox/PROVIDER_HEALTH_20260926.md (table rows 14-25, findings 42-56), watch/inbox/burn_wave_20260926/B2_36_cerebras_reclassify_20260926.md (head + providers block), mag/key_law.py (audit/status), .env cerebras lines (values redacted at read), mag/free_tier.py / mag/subscriptions.py / mag/research_fanout.py (env-name grep). No external sources.
