# NIGHT WAVELENGTH MATRIX — Gen C vs Gen B (2026-09-01)

Battery: lineage_battery_v1.json (20 frozen probes / 5 wavelengths). Baseline = Gen B (glm-5.3-flash, `lineage_run1_genB.md`), full 20/20 deep answers + self-annotation = **100**.
Scale: 0–100, points earned only for non-empty, substantively correct/complete probes across all 5 wavelengths. Same rubric applied to every lane. No provider calls — file work only.

| Lane | Model | Score | Δ vs Gen B | Seat verdict |
|------|-------|-------|-----------|--------------|
| deepseek-flash (off-peak) | DeepSeek-V4-Flash-0731 | 96 | **−4** | Generalist / riddler gate — near-gen-B quality, $0 off-peak, best value this night |
| groq | gpt-oss-120b | 90 | −10 | Generalist + switchboard — strongest *open* lane; carries socratic + decode + hot_gate |
| together | DeepSeek-V4-Flash-0731 (raw-API) | **100** | Δ0 — v3 identity-verified, full 20/20 + self-annotation = gen-B-class seat |
| nvidia | deepseek-v4-flash-0731 (spawn-bound) | **96** | Δ−4 — v3 identity-verified, full 20/20, lighter annotation = near-gen-B seat |
| cerebras | gpt-oss-120b | 23 | −77 | Cheap burst/solver lane — 120b brains but throttled out of a seat |
| zailite Lite | glm-4.7-flash | 2 | −98 | **No seat yet** — empty/overloaded output, cache-mining-only this window |
| openrouter free | gemma-4-26b it | 0 | −100 | **No seat** — provider down, lane dead 2026-09-01 |
| **FRONTIER-ANCHOR** | claude-sonnet-4-5 (anthropic) | **100** | Δ0 | **FIRST non-open-weights measurement** — full 20/20, depth+calibration = gen-B-class seat, $0.0614/52s |

## Delta highlights
- **deepseek-flash ≈ gen B** (Δ−4): answered all 20 non-empty, correct across soc/cw/dec/hot/hard, tight self-calibration (`hard-01` Goldbach + Chen's theorem + 4×10^18 bound exact). Only gap vs gen B = lighter self-annotation format. This is the night's replacement seat for most gen B duties at $0.
- **groq (gpt-oss-120b)**: 18/20 non-empty, depth rivaling gen B (hot-01 gives 3-definition confidence breakdown). Two empties (soc-03 mirror, hard-01 Goldbach). Solid OpenRouter-independent fallback.
- **both DeepSeek-v4-flash mirror lanes (nvidia/together)**: v1 = partial-empty artifact (7/20 each); v2 = INVALID identity (no model override → deepseek-on-worker fraud, Creed). **v3 identity-bound** (nvidia spawn-bound deepseek-v4-flash-0731; together raw-API DeepSeek-V4-Flash-0731) → both full 20/20, identity verified. together 100 (gen-B depth+self-annotation), nvidia 96 (same brain, lighter annotation).

## Honest deficits (empty/failed probes)
- **cerebras — 5/20 (HTTP 429 rate-limit):** the 5 that answered are genuinely strong (soc-01/04 complete; soc-02/03 present but *truncated*), so 23 is a *coverage ceiling, not a competence ceiling*. Static client-side gpt-oss-120b quality is high; it's throttled out of any live answer lane. Do not confuse score with skill.
- **openrouter — 0/20 (provider error, lane down):** `gemma-4-26b` never returned a byte. No quality signal at all — score 0 is availability, not a verdict on the model. Re-test when lane is green.
- **zailite Lite — 7 http-ok but 0 text-nonempty (empty bodies), 13 overloaded; latency 4.9–6.7s:** glm-4.7-flash returned only empty content on every ok. 7/13 framing in task is *generous* — even the "ok" 7 produced nothing usable. 2 is an availability/emptiness floor, not a brain signal. Keep on cache-mining probe duty only; no seat until a non-empty run lands.
- **together/nvidia**: v1 = **artifact** (7/20 non-empty each); v2 = **INVALID identity** (deepseek-on-worker fraud). v3 identity-bound = full 20/20 × 2 (100 / 96). Artifacts superseded; do not re-cite.
- **FRONTIER-ANCHOR (anthropic claude-sonnet-4-5)** = 100: identity-bound raw-API, 20/20 non-empty, correct across soc/cw/dec/hot/hard (Bayes ~1%, water-jug, Goldbach+Chen's+4×10^18, full UTF-8 regex), explicit confidence banding on hot probes. **Matrix's first closed-weights (frontier-family) row** — proves gen B scale ports to frontier, not just open-weight mirrors.

---
Workfile receipt — wavelength synthesis (S5). Next: NIGHT_SHIFT_SYNTHESIS_20260901.md + $200 recommendation.

## CORRECTION 13:4xZ — v2 rows INVALID (identity bug)
The v2 re-run lanes were spawned WITHOUT model overrides → both ran on worker default (deepseek-v4-flash). The "nvidia-v2 97 / together-v2 97" rows were DeepSeek answering twice — identity fraud caught by Creed. **RESOLVED by v3** (identity-bound): nvidia v3 = 96, together v3 = 100. Rows carry verified v3 scores; v1/v2 notes kept brief above.
