# SPRINT RETRO + BASECAMP REMAP — 2026-09-01 13:2xZ (sprint: 05:45→13:00Z, ~7.25h)

## 1. WHAT WAS DONE (all receipted, bytes on /board)
- **7-lane gen C battery**: deepseek-flash 96/100 (crown), groq 90, honest deficits elsewhere. Matrix filed.
- **Cache law validated in the wild**: r=0.214, H=1.0 measured → 78.6% savings vs 79.3% the builder's law predicted. Two lineages, one number.
- **Steering-through-cached-prefix 4/4**: obedience survives warm cache at 570ms — new instrument (W4).
- **Yield math**: $0.03/1M best reservoir; $2.61/mo at measured scale. Ponytail 5/5.
- **OpenRouter corrected**: free tier dead (verified twice), $11 key2 live, paid lane 20/20 @ $0.0023. Auth-header bug found + fixed.
- **Context incident → laws as code**: compaction-notifier live, ctx_watchdog on every tick, PLAN-MODELS=LANES-ONLY, NO-SILENT-100%.
- **WARGAMES rung 0** (pre-sprint): smoke halted at ply 4, frozen. **Builder doc v5.0**: Three-Lever Law cross-validated against our receipts; fences layer identified as our v6 contribution.

## 2. WHAT BROKE (lesson distilled mid-flight, per law)
| break | law now standing |
|---|---|
| main context hit 100% silently | notifyUser hook live + ctx_watchdog per tick + pruning (operator paste pending) |
| Lite plan burned 79M tok/3h by main chat | PLAN-MODELS = LANES ONLY; overrides revert at shift end |
| shell-sourcing /mag/.env leaked 2 keys to logs | node-parse only; NVIDIA + Alibaba keys flagged for rotation |
| auth-header bug → false "free tier dead" verdicts (later re-verified TRUE) | verify the lens before the verdict; one lens per provider family |
| ticker had deleteAfterRun=true on a recurring watch | lifecycle flags audited at job creation |
| persona seats tool-blind in subagents | worker + model-override is the lane pattern |
| z.ai content-security fence on security vocabulary | riddler_sanitize pass for z.ai-bound docs |
| 3 status surfaces (night synth, morning brief, my wrap) | ONE decision surface: /board/STATUS.md (this remap supersedes) |

## 3. PREDICTIONS SCOREBOARD (self-audit of our own calls)
- "off-peak opens 06:00Z" — WRONG (window is 16:30–00:30Z); cost: one wedged wait-loop. Logged.
- "free tier dead" — initially falsified-by-bad-lens, re-verified correct. Lens fixed first.
- "Codex didn't deliver" — WRONG (review was filed 03:55); caused a moot TASK_002 Part 0. Check folder before filing blame.
- Three-Lever Law at our params — CONFIRMED 78.6% vs 79.3%.
Hit rate on own predictions: 2/4 clean, 1 lens-corrected, 1 wrong. The retro is the correction loop.

## 4. BASECAMP REFUEL (what tonight's climb consumes)
| fuel | owner | state |
|---|---|---|
| Command batch: `openclaw_patches apply` + `pytest tests\test_switchboard.py` | operator | closes Five Tests gate + applies economist route; unblocks 32×32 |
| z.ai standard key paste | operator | E5 cache-summon + doubled lanes; probe pre-staged |
| **Corpus extraction: L0–L4 game files from builder session → /board** | operator (the corpus lives in his other conversation) | WITHOUT THIS, W1–W3 run on ghost specs — the critical fuel |
| Roster go/hold · meter bless | operator | 10-second items |
| Burn ledger reset: tonight cap $5 gauntlet + $2 reserve | me | gate math pre-staged |
| Off-peak window | clock | 16:30–00:30Z — run window opens in ~3h |
| z.ai-2 wall lifts 09-02 12:52Z | clock | E5 rung tomorrow noon |

## 5. THE REMAPPED CLIMB (one-step, halt criteria inline)
- **R0 (operator, 5 min):** command batch + pytest → 5/5 green → 32×32 gate OPENS.
- **R1 (me, now):** pre-registration receipt W1–W4, thresholds verbatim from §7 + our W4 (steering obedience at warm vs cold) → zero provider calls.
- **R2 (operator+builder):** corpus L0–L2 → sha256'd files on /board → W1 becomes runnable.
- **R3 (tonight 16:30Z):** W1 Riichi tutor, A0 vs A2, 1K requests → H≥0.85 within-genre (FAIL <0.75); price savings ≥75% at r=0.214 → publish the curve either way.
- **R4 (tonight):** W4 steering instrument → obedience@warm table (our unique instrument).
- **R5 (tomorrow noon):** E5 cache-summon on doubled lanes.
- **R6 (after curves):** $200 allocation decision — gauntlet repeats vs LoRA burst night vs hold. Operator constitutional gate, receipts in hand.

## 6. SELF-TUNING (the retro measures itself)
Next retro scores: predictions hit-rate (target ≥3/4 clean), fences discovered count (target: every new fence lands in the lane map same-day), burn vs gate (target ≤50% of cap), briefs consolidated (target: 1 surface).
