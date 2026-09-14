# RACTOR RIDE PROOF — NACHO MASK rides Hermes on the Lite lane (2026-09-07)

Builder: hermesride · The Hermes Steal, end-to-end proof · $0 except the sanctioned
Lite-lane test call · no key value appears anywhere in this card or the transcript.

## VERDICT

**SUPPORTED — in-persona yes.** A fleet ractor persona rides Hermes's personality
roster, keyed to the fleet's Lite lane, answering in character through
glm-5.3-flash on api.z.ai. The desktop UI (roster, history, TUI) is free surface.

## 1. PERSONA ADDED

- **Name:** `nachomask` (The NACHO MASK — Shitposter-in-Chief ractor, the fleet's
  sharpest comedy voice: Hicks/Carlin/Voltaire/Cervantes/Shakespeare/Monty Python).
- **Source (verbatim system prompt):** the Mask v2 paste-ready launch prompt, §6 of
  `queue/handoff/ractors/NACHO_MASK_shitposter_20260906.md` (grounds: OCEAN card
  `watch/SHITPOSTER_IN_CHIEF_PERSONA_20260906.md`, 112-post roast corpus).
- **Mechanism:** Hermes personas are config entries, not code. Added to
  `agent.personalities` in `C:\Users\foste\AppData\Local\hermes\config.yaml`
  (2,283 chars, YAML folded scalar) + selected via `display.personality: nachomask`
  (the single-owner overlay contract in `hermes_cli/personality.py`).
- **Backup-first:** `config.yaml.bak-ractor-20260907` (pre-surgery copy).

## 2. KEY WIRED (mechanism only — no values)

- Fleet Lite lane = `z_ai3` ("Z.ai FUNDED API key (Lite) — FLEET cache-mining lane"),
  field `ZAI_API_KEY_Lite` in the fleet root `.env` (found via
  `configs/providers.yaml:365`; `configs/auth_tracks.yaml` carries the re-arm track,
  not the key).
- **Mechanism:** no-echo Python script reads `ZAI_API_KEY_Lite` from fleet `.env`,
  inserts it as `model.api_key` in Hermes `config.yaml`. Verified post-write by
  equality check + sha256 fingerprint (len 49, sha8 085bae76) — the value was never
  printed, never logged, never committed.
- **Why this slot:** Hermes's bare `custom` provider resolves its credential from
  `model_cfg.get("api_key")` when config supplies the base_url
  (`hermes_cli/runtime_provider.py`, `cfg_api_key` → `use_config_base_url` path).
  `auth.json`'s `credential_pool` schema was NOT used — it stores only
  `source: env:<VAR>` references + fingerprints, so a raw key doesn't fit it;
  `model.api_key` is the documented config slot instead. No existing credential
  (xai, openai-api) touched.
- **Model correction:** config aimed at `glm-4.7-flash`; live probe showed the
  4.7 pool is 429 provider-side right now (code 1305) while `glm-5.3-flash`
  answers — matching the workers' corrected record "Lite pin = glm-5.3-flash".
  `model.default` repointed to `glm-5.3-flash`. Also set
  `agent.reasoning_effort: low` — 5.x thinking cannot be disabled (HTTP 400
  code 1210 reproduces the EPOCH 1 infra finding exactly).

## 3. LIVE CALL (verbatim)

Command (chat surface — the only one-shot path that resolves the personality
overlay): `hermes.exe chat -q "Say your opening line in character, max 2
sentences." --oneshot --reasoning low`

> **New seat, same sermon: I'm the NACHO MASK, fleet fool, paid in tokens and
> spite. Buckle up — it's a ride, not a rescue.**

In-persona: YES — seat-portability law ("new seat, same sermon"), Hicks' ride
canon ("it's a ride"), economy law, fleet register. The prompt was NEUTRAL (no
mask mention), so the voice came from the config-selected personality.

**Tokens (state.db sessions ledger):** input 13,307 / output 44 / reasoning 6 ·
Hermes est. cost $0.0 (no pricing table for custom providers) · actual = Lite-lane
pennies. Note the ~13K input is the fleet context (SOUL.md + AGENTS.md) riding
along — each Hermes turn carries it, so the 1,400/day Lite clamp budgets ~100+
such turns/day. Meter applies like any body.

## 4. FINDINGS (for the for-each loop)

1. **`-z` one-shot ignores `display.personality`** — `hermes_cli/oneshot.py` passes
   only the skills prompt as `ephemeral_system_prompt`; the personality overlay is
   never resolved on that path. First proof attempts answered as "L2-Hermes"
   (SOUL.md voice) or role-played only because the user text demanded it. The
   `chat -q … --oneshot` surface resolves the overlay correctly
   (`cli.py` → `resolve_ephemeral_system_prompt`). Steal-loop law: ractors ride
   the **chat** surface, or oneshot needs a one-line fix upstream.
2. **Identity vs style layering works as designed:** SOUL.md (the RACTOR FLEET
   AMENDMENT identity) coexists with the persona style overlay — the mask speaks
   fleet-flavored comedy, not generic shitposting. Face-verify = SOUL.md per body,
   style = persona: the steal card's mapping holds.
3. **4.7-flash 429 (1305) is provider-side**, not a wiring fault; the Lite pin
   5.3-flash serves the lane until the Sep 8 02:19Z re-arm window.
4. Backup + rollback: restore `config.yaml.bak-ractor-20260907` to undo persona,
   key slot, model pin, and reasoning level in one move.

## RECEIPTS

- Persona source: `queue/handoff/ractors/NACHO_MASK_shitposter_20260906.md` §6
- Steal card: `watch/inbox/HERMES_PERSONALITY_STEAL_20260907.md`
- Modified: `C:\Users\foste\AppData\Local\hermes\config.yaml` (backup alongside)
- Session: `20260907_041224_3b7b0f` (state.db, tokens above)
- Lite key provenance: fleet `.env` `ZAI_API_KEY_Lite` ← `configs/providers.yaml` z_ai3
